import 'package:flutter/material.dart';
import 'package:get/get.dart';
import '../../../core/theme/app_theme.dart';
import '../services/voice_biometrics_service.dart';
import '../services/voice_stt_service.dart';

class VoiceRegistrationView extends StatefulWidget {
  const VoiceRegistrationView({super.key});

  @override
  State<VoiceRegistrationView> createState() => _VoiceRegistrationViewState();
}

class _VoiceRegistrationViewState extends State<VoiceRegistrationView> {
  final VoiceSttService _sttService = VoiceSttService();
  final VoiceBiometricsService _biometricsService = VoiceBiometricsService();

  int _currentStep = 0;
  bool _isListening = false;
  bool _isSaving = false;
  String _recognizedPhrase = '';

  final List<String> _enrollmentPrompts = [
    "Hey ISAI, initialize my personal AI assistant",
    "ISAI, open camera and run diagnostics",
    "ISAI, call home and turn on flashlight"
  ];

  final List<String> _recordedSamples = [];

  @override
  void initState() {
    super.initState();
    _sttService.initialize();
  }

  Future<void> _startListening() async {
    setState(() {
      _isListening = true;
      _recognizedPhrase = '';
    });

    await _sttService.startListening(
      onResult: (text) {
        setState(() {
          _recognizedPhrase = text;
        });
      },
      onSoundLevelChanged: () {},
    );
  }

  Future<void> _stopAndConfirm() async {
    await _sttService.stopListening();
    setState(() {
      _isListening = false;
    });

    final phrase = _recognizedPhrase.trim().isEmpty
        ? _enrollmentPrompts[_currentStep]
        : _recognizedPhrase.trim();

    _recordedSamples.add(phrase);

    if (_currentStep < _enrollmentPrompts.length - 1) {
      setState(() {
        _currentStep++;
        _recognizedPhrase = '';
      });
    } else {
      _finishEnrollment();
    }
  }

  Future<void> _finishEnrollment() async {
    setState(() {
      _isSaving = true;
    });

    await _biometricsService.saveEnrolledProfile(_recordedSamples);

    if (mounted) {
      Get.snackbar(
        'Voice Biometrics Registered',
        'Your voice profile has been saved successfully! ISAI is now locked to your voice.',
        backgroundColor: AppTheme.cardBackground,
        colorText: AppTheme.primaryNeon,
        snackPosition: SnackPosition.BOTTOM,
      );
      Get.back();
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('VOICE BIOMETRICS SETUP'),
        backgroundColor: AppTheme.darkBackground,
      ),
      body: Container(
        decoration: const BoxDecoration(
          gradient: RadialGradient(
            center: Alignment(0, -0.6),
            radius: 1.2,
            colors: [
              Color(0xFF1E1B4B),
              AppTheme.darkBackground,
            ],
          ),
        ),
        child: SafeArea(
          child: Padding(
            padding: const EdgeInsets.all(24.0),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                // Header Chip
                Center(
                  child: Container(
                    padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                    decoration: BoxDecoration(
                      color: AppTheme.primaryNeon.withValues(alpha: 0.15),
                      borderRadius: BorderRadius.circular(20),
                      border: Border.all(color: AppTheme.primaryNeon.withValues(alpha: 0.5)),
                    ),
                    child: Row(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        const Icon(Icons.record_voice_over_rounded, color: AppTheme.primaryNeon, size: 18),
                        const SizedBox(width: 8),
                        Text(
                          'Step ${_currentStep + 1} of ${_enrollmentPrompts.length}',
                          style: const TextStyle(
                            color: AppTheme.primaryNeon,
                            fontWeight: FontWeight.bold,
                            letterSpacing: 1,
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
                const SizedBox(height: 24),

                // Instruction Card
                Container(
                  padding: const EdgeInsets.all(24),
                  decoration: BoxDecoration(
                    color: AppTheme.cardBackground.withValues(alpha: 0.8),
                    borderRadius: BorderRadius.circular(24),
                    border: Border.all(color: AppTheme.cardBorder),
                  ),
                  child: Column(
                    children: [
                      const Text(
                        'Speak the Enrollment Phrase:',
                        style: TextStyle(color: AppTheme.slate, fontSize: 14),
                      ),
                      const SizedBox(height: 12),
                      Text(
                        '"${_enrollmentPrompts[_currentStep]}"',
                        textAlign: TextAlign.center,
                        style: const TextStyle(
                          color: Colors.white,
                          fontSize: 20,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      const SizedBox(height: 20),
                      if (_recognizedPhrase.isNotEmpty)
                        Container(
                          padding: const EdgeInsets.all(12),
                          decoration: BoxDecoration(
                            color: Colors.black45,
                            borderRadius: BorderRadius.circular(12),
                          ),
                          child: Text(
                            'Recognized: "$_recognizedPhrase"',
                            style: const TextStyle(color: AppTheme.secondaryNeon, fontSize: 13),
                            textAlign: TextAlign.center,
                          ),
                        ),
                    ],
                  ),
                ),

                const Spacer(),

                // Mic Pulse Circle
                GestureDetector(
                  onTap: _isListening ? _stopAndConfirm : _startListening,
                  child: Container(
                    width: 120,
                    height: 120,
                    decoration: BoxDecoration(
                      shape: BoxShape.circle,
                      gradient: _isListening ? AppTheme.cyberGradient : null,
                      color: _isListening ? null : AppTheme.cardBackground,
                      boxShadow: [
                        BoxShadow(
                          color: (_isListening ? AppTheme.secondaryNeon : AppTheme.primaryNeon).withValues(alpha: 0.5),
                          blurRadius: 30,
                          spreadRadius: _isListening ? 10 : 2,
                        ),
                      ],
                    ),
                    child: Icon(
                      _isListening ? Icons.stop_rounded : Icons.mic_rounded,
                      size: 54,
                      color: Colors.white,
                    ),
                  ),
                ),
                const SizedBox(height: 16),
                Center(
                  child: Text(
                    _isListening ? 'Tap to Save Phrase' : 'Tap Microphone to Speak',
                    style: TextStyle(
                      color: _isListening ? AppTheme.secondaryNeon : AppTheme.slate,
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                ),

                const Spacer(),

                if (_isSaving)
                  const Center(child: CircularProgressIndicator(color: AppTheme.primaryNeon)),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
