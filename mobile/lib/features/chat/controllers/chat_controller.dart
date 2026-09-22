import 'dart:convert';
import 'package:dio/dio.dart';
import 'package:get/get.dart';
import '../../../core/network/api_client.dart';

class ChatMessageModel {
  final String id;
  final String role;
  String content;
  final DateTime createdAt;
  bool isStreaming;
  String status;

  ChatMessageModel({
    required this.id,
    required this.role,
    required this.content,
    required this.createdAt,
    this.isStreaming = false,
    this.status = 'Completed',
  });

  factory ChatMessageModel.fromJson(Map<String, dynamic> json) {
    return ChatMessageModel(
      id: json['id'] as String,
      role: json['role'] as String,
      content: json['content'] as String,
      createdAt: DateTime.parse(json['createdAt'] as String),
      status: json['status'] as String? ?? 'Completed',
    );
  }
}

class ConversationModel {
  final String id;
  final String title;
  final DateTime updatedAt;

  ConversationModel({
    required this.id,
    required this.title,
    required this.updatedAt,
  });

  factory ConversationModel.fromJson(Map<String, dynamic> json) {
    return ConversationModel(
      id: json['id'] as String,
      title: json['title'] as String,
      updatedAt: DateTime.parse(json['updatedAt'] as String),
    );
  }
}

class ChatController extends GetxController {
  final ApiClient _apiClient = Get.find<ApiClient>();

  final RxList<ConversationModel> conversations = <ConversationModel>[].obs;
  final RxList<ChatMessageModel> messages = <ChatMessageModel>[].obs;
  final Rxn<ConversationModel> currentConversation = Rxn<ConversationModel>();

  final RxBool isLoadingConversations = false.obs;
  final RxBool isLoadingMessages = false.obs;
  final RxBool isStreaming = false.obs;
  final RxString errorMessage = ''.obs;

  CancelToken? _cancelToken;

  @override
  void onInit() {
    super.onInit();
    fetchConversations();
  }

  Future<void> fetchConversations() async {
    isLoadingConversations.value = true;
    try {
      final response = await _apiClient.dio.get('/conversations');
      final list = (response.data as List)
          .map((item) => ConversationModel.fromJson(item))
          .toList();
      conversations.value = list;

      if (conversations.isNotEmpty && currentConversation.value == null) {
        selectConversation(conversations.first);
      }
    } catch (e) {
      errorMessage.value = 'Failed to load conversations.';
    } finally {
      isLoadingConversations.value = false;
    }
  }

  Future<void> createNewConversation() async {
    try {
      final response = await _apiClient.dio.post(
        '/conversations',
        data: {'title': 'New Conversation'},
      );
      final newConv = ConversationModel.fromJson(response.data);
      conversations.insert(0, newConv);
      selectConversation(newConv);
    } catch (e) {
      errorMessage.value = 'Failed to create conversation.';
    }
  }

  Future<void> selectConversation(ConversationModel conv) async {
    currentConversation.value = conv;
    messages.clear();
    isLoadingMessages.value = true;
    try {
      final response = await _apiClient.dio.get('/conversations/${conv.id}/messages');
      final list = (response.data as List)
          .map((item) => ChatMessageModel.fromJson(item))
          .toList();
      messages.value = list;
    } catch (e) {
      errorMessage.value = 'Failed to load messages.';
    } finally {
      isLoadingMessages.value = false;
    }
  }

  Future<void> sendStreamMessage(String text) async {
    if (text.trim().isEmpty) return;

    if (currentConversation.value == null) {
      await createNewConversation();
    }

    final convId = currentConversation.value!.id;
    isStreaming.value = true;
    _cancelToken = CancelToken();

    final userMsg = ChatMessageModel(
      id: DateTime.now().toString(),
      role: 'user',
      content: text.trim(),
      createdAt: DateTime.now(),
    );
    messages.add(userMsg);

    final placeholderId = 'temp_${DateTime.now().millisecondsSinceEpoch}';
    final assistantMsg = ChatMessageModel(
      id: placeholderId,
      role: 'assistant',
      content: '',
      createdAt: DateTime.now(),
      isStreaming: true,
      status: 'Processing',
    );
    messages.add(assistantMsg);

    try {
      final response = await _apiClient.dio.post<ResponseBody>(
        '/conversations/$convId/messages/stream',
        data: {'content': text.trim()},
        options: Options(
          responseType: ResponseType.stream,
          headers: {'Accept': 'text/event-stream'},
        ),
        cancelToken: _cancelToken,
      );

      final stream = response.data?.stream;
      if (stream == null) return;

      String eventType = '';
      final lineStream = stream.cast<List<int>>().transform(utf8.decoder).transform(const LineSplitter());

      await for (final line in lineStream) {
        if (line.startsWith('event:')) {
          eventType = line.substring(6).trim();
        } else if (line.startsWith('data:')) {
          final dataString = line.substring(5).trim();
          if (dataString.isEmpty) continue;

          final json = jsonDecode(dataString);

          if (eventType == 'message.started') {
            // Started
          } else if (eventType == 'message.delta') {
            final chunk = json['chunk'] as String? ?? '';
            assistantMsg.content += chunk;
            messages.refresh();
          } else if (eventType == 'message.completed') {
            assistantMsg.isStreaming = false;
            assistantMsg.status = 'Completed';
            messages.refresh();
            fetchConversations();
          } else if (eventType == 'message.cancelled') {
            assistantMsg.isStreaming = false;
            assistantMsg.status = 'Interrupted';
            messages.refresh();
          }
        }
      }
    } on DioException catch (e) {
      if (CancelToken.isCancel(e)) {
        assistantMsg.isStreaming = false;
        assistantMsg.status = 'Cancelled';
      } else {
        assistantMsg.isStreaming = false;
        assistantMsg.status = 'Failed';
        errorMessage.value = 'Network or server error occurred.';
      }
      messages.refresh();
    } finally {
      assistantMsg.isStreaming = false;
      isStreaming.value = false;
      _cancelToken = null;
    }
  }

  void cancelStreaming() {
    _cancelToken?.cancel('User requested cancellation.');
    isStreaming.value = false;
  }

  Future<void> retryMessage(ChatMessageModel msg) async {
    if (msg.role == 'user') {
      await sendStreamMessage(msg.content);
    }
  }
}
