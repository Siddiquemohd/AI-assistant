import 'package:flutter/material.dart';
import 'package:get/get.dart';
import '../controllers/voice_controller.dart';

class VoiceAssistantView extends StatelessWidget {
  VoiceAssistantView({super.key});

  final VoiceController _voiceController = Get.put(VoiceController());

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('ISAI — Voice Assistant'),
        centerTitle: true,
      ),
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(24.0),
          child: Column(
            children: [
              const SizedBox(height: 32),
              Obx(() {
                final state = _voiceController.state.value;
                return Text(
                  _getStateText(state),
                  style: Theme.of(context).textTheme.headlineSmall?.copyWith(
                        color: Colors.blueAccent,
                        fontWeight: FontWeight.bold,
                      ),
                  textAlign: TextAlign.center,
                );
              }),
              const SizedBox(height: 48),
              Expanded(
                child: Center(
                  child: Obx(() {
                    final state = _voiceController.state.value;
                    return GestureDetector(
                      onTap: () {
                        if (state == VoiceState.listening) {
                          _voiceController.stopListeningAndProcess();
                        } else if (state == VoiceState.speaking) {
                          _voiceController.stopSpeaking();
                        } else {
                          _voiceController.startVoiceInteraction();
                        }
                      },
                      child: AnimatedContainer(
                        duration: const Duration(milliseconds: 300),
                        width: state == VoiceState.listening || state == VoiceState.speaking ? 160 : 120,
                        height: state == VoiceState.listening || state == VoiceState.speaking ? 160 : 120,
                        decoration: BoxDecoration(
                          shape: BoxShape.circle,
                          color: _getCircleColor(state),
                          boxShadow: [
                            BoxShadow(
                              color: _getCircleColor(state).withValues(alpha: 0.5),
                              blurRadius: 24,
                              spreadRadius: 8,
                            ),
                          ],
                        ),
                        child: Icon(
                          _getIcon(state),
                          size: 64,
                          color: Colors.white,
                        ),
                      ),
                    );
                  }),
                ),
              ),
              Obx(() {
                if (_voiceController.recognizedText.value.isNotEmpty) {
                  return Card(
                    color: Colors.grey[900],
                    child: Padding(
                      padding: const EdgeInsets.all(16.0),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          const Text(
                            'You said:',
                            style: TextStyle(color: Colors.grey, fontSize: 12),
                          ),
                          const SizedBox(height: 4),
                          Text(
                            _voiceController.recognizedText.value,
                            style: const TextStyle(fontSize: 16, color: Colors.white),
                          ),
                        ],
                      ),
                    ),
                  );
                }
                return const SizedBox.shrink();
              }),
              const SizedBox(height: 16),
              Obx(() {
                if (_voiceController.errorMessage.value.isNotEmpty) {
                  return Text(
                    _voiceController.errorMessage.value,
                    style: const TextStyle(color: Colors.red),
                    textAlign: TextAlign.center,
                  );
                }
                return const SizedBox.shrink();
              }),
              const SizedBox(height: 24),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                children: [
                  ElevatedButton.icon(
                    onPressed: () => Get.back(),
                    icon: const Icon(Icons.chat_bubble_outline),
                    label: const Text('Text Mode'),
                  ),
                  OutlinedButton.icon(
                    onPressed: () => _voiceController.cancelVoiceInteraction(),
                    icon: const Icon(Icons.close),
                    label: const Text('Cancel'),
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }

  String _getStateText(VoiceState state) {
    switch (state) {
      case VoiceState.idle:
        return 'Tap microphone to speak';
      case VoiceState.requestingPermission:
        return 'Requesting microphone permission...';
      case VoiceState.listening:
        return 'Listening... Tap to finish';
      case VoiceState.processingSpeech:
        return 'Processing speech...';
      case VoiceState.sendingToAssistant:
        return 'ISAI is thinking...';
      case VoiceState.speaking:
        return 'ISAI is speaking...';
      case VoiceState.paused:
        return 'Paused';
      case VoiceState.cancelling:
        return 'Cancelling...';
      case VoiceState.failed:
        return 'Voice Interaction Error';
    }
  }

  Color _getCircleColor(VoiceState state) {
    switch (state) {
      case VoiceState.listening:
        return Colors.redAccent;
      case VoiceState.speaking:
        return Colors.greenAccent.shade700;
      case VoiceState.sendingToAssistant:
      case VoiceState.processingSpeech:
        return Colors.amber.shade700;
      case VoiceState.failed:
        return Colors.grey;
      default:
        return Colors.blueAccent;
    }
  }

  IconData _getIcon(VoiceState state) {
    switch (state) {
      case VoiceState.listening:
        return Icons.mic;
      case VoiceState.speaking:
        return Icons.volume_up_rounded;
      case VoiceState.sendingToAssistant:
      case VoiceState.processingSpeech:
        return Icons.hourglass_top_rounded;
      default:
        return Icons.mic_none_rounded;
    }
  }
}
