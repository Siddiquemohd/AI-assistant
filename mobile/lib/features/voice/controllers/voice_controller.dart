import 'package:get/get.dart';
import '../../chat/controllers/chat_controller.dart';
import '../services/voice_stt_service.dart';
import '../services/voice_tts_service.dart';

enum VoiceState {
  idle,
  requestingPermission,
  listening,
  processingSpeech,
  sendingToAssistant,
  speaking,
  paused,
  cancelling,
  failed,
}

class VoiceController extends GetxController {
  final VoiceSttService _sttService = VoiceSttService();
  final VoiceTtsService _ttsService = VoiceTtsService();
  final ChatController _chatController = Get.find<ChatController>();

  final Rx<VoiceState> state = VoiceState.idle.obs;
  final RxString recognizedText = ''.obs;
  final RxString assistantResponseText = ''.obs;
  final RxString errorMessage = ''.obs;

  @override
  void onInit() {
    super.onInit();
    _initServices();
  }

  Future<void> _initServices() async {
    await _sttService.initialize();
    await _ttsService.initialize();
  }

  Future<void> startVoiceInteraction() async {
    errorMessage.value = '';
    recognizedText.value = '';
    assistantResponseText.value = '';

    state.value = VoiceState.requestingPermission;
    final isAvailable = await _sttService.initialize();

    if (!isAvailable) {
      state.value = VoiceState.failed;
      errorMessage.value = 'Microphone permission or speech recognition service unavailable.';
      return;
    }

    state.value = VoiceState.listening;

    await _sttService.startListening(
      onResult: (text) {
        recognizedText.value = text;
      },
      onSoundLevelChanged: () {},
    );
  }

  Future<void> stopListeningAndProcess() async {
    if (state.value != VoiceState.listening) return;

    state.value = VoiceState.processingSpeech;
    await _sttService.stopListening();

    final textToSend = recognizedText.value.trim();
    if (textToSend.isEmpty) {
      state.value = VoiceState.idle;
      return;
    }

    state.value = VoiceState.sendingToAssistant;
    await _chatController.sendStreamMessage(textToSend);

    final assistantMessages = _chatController.messages.where((m) => m.role == 'assistant').toList();
    final lastAssistantMsg = assistantMessages.isNotEmpty ? assistantMessages.last : null;

    if (lastAssistantMsg != null && lastAssistantMsg.content.isNotEmpty) {
      assistantResponseText.value = lastAssistantMsg.content;
      state.value = VoiceState.speaking;

      await _ttsService.speak(
        lastAssistantMsg.content,
        onComplete: () {
          state.value = VoiceState.idle;
        },
      );
    } else {
      state.value = VoiceState.idle;
    }
  }

  Future<void> cancelVoiceInteraction() async {
    state.value = VoiceState.cancelling;
    await _sttService.cancelListening();
    await _ttsService.stop();
    state.value = VoiceState.idle;
  }

  Future<void> stopSpeaking() async {
    await _ttsService.stop();
    state.value = VoiceState.idle;
  }

  @override
  void onClose() {
    _sttService.cancelListening();
    _ttsService.stop();
    super.onClose();
  }
}
