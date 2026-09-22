import 'package:flutter_secure_storage/flutter_secure_storage.dart';

class SecureStorageService {
  final FlutterSecureStorage _storage = const FlutterSecureStorage();

  static const String keyAccessToken = 'access_token';
  static const String keyRefreshToken = 'refresh_token';
  static const String keyUserEmail = 'user_email';
  static const String keyDisplayName = 'display_name';

  Future<void> saveTokens({required String accessToken, required String refreshToken}) async {
    await _storage.write(key: keyAccessToken, value: accessToken);
    await _storage.write(key: keyRefreshToken, value: refreshToken);
  }

  Future<String?> getAccessToken() async {
    return await _storage.read(key: keyAccessToken);
  }

  Future<String?> getRefreshToken() async {
    return await _storage.read(key: keyRefreshToken);
  }

  Future<void> saveUserInfo({required String email, required String displayName}) async {
    await _storage.write(key: keyUserEmail, value: email);
    await _storage.write(key: keyDisplayName, value: displayName);
  }

  Future<String?> getUserEmail() async {
    return await _storage.read(key: keyUserEmail);
  }

  Future<String?> getDisplayName() async {
    return await _storage.read(key: keyDisplayName);
  }

  Future<void> clearAll() async {
    await _storage.deleteAll();
  }
}
