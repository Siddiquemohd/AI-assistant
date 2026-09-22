import 'package:speech_to_text/speech_to_text.dart';

class VoiceSttService {
  final SpeechToText _speechToText = SpeechToText();
  bool _isAvailable = false;

  bool get isAvailable => _isAvailable;
  bool get isListening => _speechToText.isListening;

  Future<bool> initialize() async {
    _isAvailable = await _speechToText.initialize(
      onError: (errorNotification) {},
      onStatus: (status) {},
    );
    return _isAvailable;
  }

  Future<void> startListening({
    required Function(String recognizedWords) onResult,
    required Function() onSoundLevelChanged,
  }) async {
    if (!_isAvailable) {
      final initSuccess = await initialize();
      if (!initSuccess) return;
    }

    await _speechToText.listen(
      onResult: (result) {
        onResult(result.recognizedWords);
      },
      listenOptions: SpeechListenOptions(
        listenMode: ListenMode.dictation,
        cancelOnError: true,
        partialResults: true,
      ),
    );
  }

  Future<void> stopListening() async {
    if (_speechToText.isListening) {
      await _speechToText.stop();
    }
  }

  Future<void> cancelListening() async {
    if (_speechToText.isListening) {
      await _speechToText.cancel();
    }
  }
}
