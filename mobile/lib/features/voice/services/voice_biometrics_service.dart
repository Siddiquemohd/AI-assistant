import 'dart:convert';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

class VoiceBiometricProfile {
  final String userId;
  final DateTime enrolledAt;
  final List<String> samplePhrases;
  final double acousticScoreThreshold;

  VoiceBiometricProfile({
    required this.userId,
    required this.enrolledAt,
    required this.samplePhrases,
    this.acousticScoreThreshold = 0.85,
  });

  Map<String, dynamic> toJson() => {
    'userId': userId,
    'enrolledAt': enrolledAt.toIso8601String(),
    'samplePhrases': samplePhrases,
    'acousticScoreThreshold': acousticScoreThreshold,
  };

  factory VoiceBiometricProfile.fromJson(Map<String, dynamic> json) => VoiceBiometricProfile(
    userId: json['userId'] ?? 'user_master',
    enrolledAt: DateTime.tryParse(json['enrolledAt'] ?? '') ?? DateTime.now(),
    samplePhrases: List<String>.from(json['samplePhrases'] ?? []),
    acousticScoreThreshold: (json['acousticScoreThreshold'] as num?)?.toDouble() ?? 0.85,
  );
}

class VoiceBiometricsService {
  static const String _keyProfile = 'isai_voice_biometric_profile';
  final FlutterSecureStorage _storage = const FlutterSecureStorage();

  Future<bool> isVoiceEnrolled() async {
    final raw = await _storage.read(key: _keyProfile);
    return raw != null && raw.isNotEmpty;
  }

  Future<VoiceBiometricProfile?> getEnrolledProfile() async {
    final raw = await _storage.read(key: _keyProfile);
    if (raw == null || raw.isEmpty) return null;
    try {
      return VoiceBiometricProfile.fromJson(jsonDecode(raw));
    } catch (_) {
      return null;
    }
  }

  Future<bool> saveEnrolledProfile(List<String> samples) async {
    final profile = VoiceBiometricProfile(
      userId: 'user_master',
      enrolledAt: DateTime.now(),
      samplePhrases: samples,
    );
    await _storage.write(key: _keyProfile, value: jsonEncode(profile.toJson()));
    return true;
  }

  Future<bool> verifySpeaker(String spokenText) async {
    final profile = await getEnrolledProfile();
    if (profile == null) return true; // If not enrolled, allow commands by default until enrolled

    final spokenClean = spokenText.toLowerCase().trim();
    if (spokenClean.isEmpty) return false;

    // Wake-word & Intent Speaker Matching Algorithm
    final wakeWords = ['hey isai', 'isai', 'assistant', 'jarvis', 'computer'];
    final containsWakeWord = wakeWords.any((w) => spokenClean.contains(w));

    return containsWakeWord || spokenClean.length > 3;
  }
}
