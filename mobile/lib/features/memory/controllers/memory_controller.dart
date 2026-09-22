import 'package:dio/dio.dart';
import 'package:get/get.dart';
import '../../../core/network/api_client.dart';

class MemoryModel {
  final String id;
  final String content;
  final String category;
  final String sensitivityLevel;
  bool isEnabled;
  final DateTime createdAt;

  MemoryModel({
    required this.id,
    required this.content,
    required this.category,
    required this.sensitivityLevel,
    required this.isEnabled,
    required this.createdAt,
  });

  factory MemoryModel.fromJson(Map<String, dynamic> json) {
    return MemoryModel(
      id: json['id'] as String,
      content: json['content'] as String,
      category: json['category'] as String? ?? 'General',
      sensitivityLevel: json['sensitivity_level'] as String? ?? 'Normal',
      isEnabled: json['is_enabled'] as bool? ?? true,
      createdAt: DateTime.parse(json['created_at'] as String),
    );
  }
}

class MemoryController extends GetxController {
  final ApiClient _apiClient = Get.find<ApiClient>();

  final RxList<MemoryModel> memories = <MemoryModel>[].obs;
  final RxBool isLoading = false.obs;
  final RxString errorMessage = ''.obs;
  final RxString searchQuery = ''.obs;

  @override
  void onInit() {
    super.onInit();
    fetchMemories();
  }

  List<MemoryModel> get filteredMemories {
    if (searchQuery.value.trim().isEmpty) return memories;
    final q = searchQuery.value.toLowerCase();
    return memories.where((m) => m.content.toLowerCase().contains(q) || m.category.toLowerCase().contains(q)).toList();
  }

  Future<void> fetchMemories() async {
    isLoading.value = true;
    errorMessage.value = '';
    try {
      final response = await _apiClient.dio.get('/memories');
      final list = (response.data as List)
          .map((item) => MemoryModel.fromJson(item))
          .toList();
      memories.value = list;
    } on DioException catch (e) {
      errorMessage.value = e.response?.data['detail'] ?? 'Failed to fetch memories.';
    } finally {
      isLoading.value = false;
    }
  }

  Future<bool> createMemory(String content, String category, String sensitivityLevel) async {
    if (content.trim().isEmpty) return false;
    try {
      final response = await _apiClient.dio.post(
        '/memories',
        data: {
          'content': content.trim(),
          'category': category,
          'sensitivity_level': sensitivityLevel,
          'is_enabled': true,
        },
      );
      final newMem = MemoryModel.fromJson(response.data);
      memories.insert(0, newMem);
      return true;
    } catch (e) {
      errorMessage.value = 'Failed to create memory.';
      return false;
    }
  }

  Future<void> toggleMemoryEnabled(MemoryModel memory, bool enabled) async {
    final oldState = memory.isEnabled;
    memory.isEnabled = enabled;
    memories.refresh();
    try {
      await _apiClient.dio.patch(
        '/memories/${memory.id}',
        data: {'is_enabled': enabled},
      );
    } catch (e) {
      memory.isEnabled = oldState;
      memories.refresh();
      Get.snackbar('Error', 'Failed to update memory setting');
    }
  }

  Future<void> deleteMemory(MemoryModel memory) async {
    memories.removeWhere((m) => m.id == memory.id);
    try {
      await _apiClient.dio.delete('/memories/${memory.id}');
    } catch (e) {
      memories.add(memory);
      Get.snackbar('Error', 'Failed to delete memory');
    }
  }

  Future<void> clearAllMemories() async {
    try {
      await _apiClient.dio.post('/memories/clear');
      memories.clear();
      Get.snackbar('Cleared', 'All durable memories cleared');
    } catch (e) {
      Get.snackbar('Error', 'Failed to clear memories');
    }
  }
}
