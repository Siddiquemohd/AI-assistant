import 'package:flutter/material.dart';
import 'package:get/get.dart';
import '../../../core/theme/app_theme.dart';
import '../controllers/voice_controller.dart';

class VoiceAssistantView extends StatelessWidget {
  VoiceAssistantView({super.key});

  final VoiceController _voiceController = Get.put(VoiceController());

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppTheme.darkBackground,
      appBar: AppBar(
        title: const Text('ISAI — Voice Assistant'),
        centerTitle: true,
        backgroundColor: Colors.transparent,
      ),
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(24.0),
          child: Column(
            children: [
              const SizedBox(height: 16),
              // Voice Status Header Pill
              Obx(() {
                final state = _voiceController.state.value;
                return Container(
                  padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 10),
                  decoration: BoxDecoration(
                    color: AppTheme.cardBackground,
                    borderRadius: BorderRadius.circular(20),
                    border: Border.all(color: _getCircleColor(state).withValues(alpha: 0.6)),
                    boxShadow: [
                      BoxShadow(
                        color: _getCircleColor(state).withValues(alpha: 0.3),
                        blurRadius: 16,
                      ),
                    ],
                  ),
                  child: Text(
                    _getStateText(state),
                    style: TextStyle(
                      color: _getCircleColor(state),
                      fontWeight: FontWeight.bold,
                      fontSize: 15,
                    ),
                    textAlign: TextAlign.center,
                  ),
                );
              }),
              const SizedBox(height: 32),

              // Glowing Pulsing Orb Visualizer
              Expanded(
                child: Center(
                  child: Obx(() {
                    final state = _voiceController.state.value;
                    final isActive = state == VoiceState.listening || state == VoiceState.speaking;
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
                        width: isActive ? 180 : 140,
                        height: isActive ? 180 : 140,
                        decoration: BoxDecoration(
                          shape: BoxShape.circle,
                          gradient: LinearGradient(
                            colors: [
                              _getCircleColor(state),
                              _getCircleColor(state).withValues(alpha: 0.6),
                            ],
                            begin: Alignment.topLeft,
                            end: Alignment.bottomRight,
                          ),
                          boxShadow: [
                            BoxShadow(
                              color: _getCircleColor(state).withValues(alpha: 0.6),
                              blurRadius: isActive ? 40 : 20,
                              spreadRadius: isActive ? 10 : 4,
                            ),
                          ],
                        ),
                        child: Icon(
                          _getIcon(state),
                          size: isActive ? 72 : 56,
                          color: Colors.black,
                        ),
                      ),
                    );
                  }),
                ),
              ),

              // 10 Neural Voices Selector Title
              const Align(
                alignment: Alignment.centerLeft,
                child: Text(
                  'NEURAL VOICE ENGINE (10 FEMALE VOICES)',
                  style: TextStyle(
                    fontSize: 11,
                    fontWeight: FontWeight.bold,
                    letterSpacing: 1.2,
                    color: AppTheme.primaryNeon,
                  ),
                ),
              ),
              const SizedBox(height: 8),
              SizedBox(
                height: 40,
                child: ListView(
                  scrollDirection: Axis.horizontal,
                  children: [
                    _buildVoiceChip('Aria (Default)'),
                    _buildVoiceChip('Jenny'),
                    _buildVoiceChip('Ava'),
                    _buildVoiceChip('Emma'),
                    _buildVoiceChip('Sonia'),
                    _buildVoiceChip('Clara'),
                    _buildVoiceChip('Natasha'),
                    _buildVoiceChip('Neerja'),
                    _buildVoiceChip('Elvira'),
                    _buildVoiceChip('Denise'),
                  ],
                ),
              ),
              const SizedBox(height: 20),

              // Recognized Speech Output Card
              Obx(() {
                if (_voiceController.recognizedText.value.isNotEmpty) {
                  return Container(
                    width: double.infinity,
                    padding: const EdgeInsets.all(16.0),
                    decoration: BoxDecoration(
                      color: AppTheme.cardBackground,
                      borderRadius: BorderRadius.circular(16),
                      border: Border.all(color: AppTheme.cardBorder),
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const Text(
                          'Transcribed Speech:',
                          style: TextStyle(color: AppTheme.slate, fontSize: 11, fontWeight: FontWeight.bold),
                        ),
                        const SizedBox(height: 4),
                        Text(
                          _voiceController.recognizedText.value,
                          style: const TextStyle(fontSize: 15, color: Colors.white),
                        ),
                      ],
                    ),
                  );
                }
                return const SizedBox.shrink();
              }),
              const SizedBox(height: 16),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                children: [
                  ElevatedButton.icon(
                    onPressed: () => Get.back(),
                    icon: const Icon(Icons.chat_bubble_outline, color: Colors.black),
                    label: const Text('Text Mode', style: TextStyle(color: Colors.black)),
                  ),
                  OutlinedButton.icon(
                    onPressed: () => _voiceController.cancelVoiceInteraction(),
                    icon: const Icon(Icons.close, color: Colors.redAccent),
                    label: const Text('Cancel', style: TextStyle(color: Colors.redAccent)),
                    style: OutlinedButton.styleFrom(
                      side: const BorderSide(color: Colors.redAccent),
                    ),
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildVoiceChip(String name) {
    final isSelected = name.contains('Aria');
    return Container(
      margin: const EdgeInsets.only(right: 8),
      child: Chip(
        label: Text(
          name,
          style: TextStyle(
            color: isSelected ? Colors.black : Colors.white,
            fontSize: 12,
            fontWeight: isSelected ? FontWeight.bold : FontWeight.normal,
          ),
        ),
        backgroundColor: isSelected ? AppTheme.primaryNeon : AppTheme.cardBackground,
        side: BorderSide(color: isSelected ? AppTheme.primaryNeon : AppTheme.cardBorder),
      ),
    );
  }

  String _getStateText(VoiceState state) {
    switch (state) {
      case VoiceState.idle:
        return 'Tap orb to speak to ISAI';
      case VoiceState.requestingPermission:
        return 'Requesting microphone...';
      case VoiceState.listening:
        return 'Listening... Tap when finished';
      case VoiceState.processingSpeech:
        return 'Transcribing audio...';
      case VoiceState.sendingToAssistant:
        return 'ISAI is processing...';
      case VoiceState.speaking:
        return 'ISAI is speaking...';
      case VoiceState.paused:
        return 'Voice Paused';
      case VoiceState.cancelling:
        return 'Cancelling...';
      case VoiceState.failed:
        return 'Voice Interaction Error';
    }
  }

  Color _getCircleColor(VoiceState state) {
    switch (state) {
      case VoiceState.listening:
        return AppTheme.accentPink;
      case VoiceState.speaking:
        return AppTheme.accentEmerald;
      case VoiceState.sendingToAssistant:
      case VoiceState.processingSpeech:
        return AppTheme.secondaryNeon;
      case VoiceState.failed:
        return Colors.redAccent;
      default:
        return AppTheme.primaryNeon;
    }
  }

  IconData _getIcon(VoiceState state) {
    switch (state) {
      case VoiceState.listening:
        return Icons.mic;
      case VoiceState.speaking:
        return Icons.graphic_eq_rounded;
      case VoiceState.sendingToAssistant:
      case VoiceState.processingSpeech:
        return Icons.hourglass_top_rounded;
      default:
        return Icons.mic_none_rounded;
    }
  }
}
