import 'package:dio/dio.dart';
import 'package:get/get.dart';
import '../../../core/network/api_client.dart';
import '../../../core/storage/secure_storage_service.dart';

class AuthController extends GetxController {
  final ApiClient _apiClient = Get.find<ApiClient>();
  final SecureStorageService _storageService = Get.find<SecureStorageService>();

  final RxBool isLoading = false.obs;
  final RxBool isAuthenticated = false.obs;
  final RxString userEmail = ''.obs;
  final RxString userDisplayName = ''.obs;
  final RxString errorMessage = ''.obs;

  @override
  void onInit() {
    super.onInit();
    checkAuthState();
  }

  Future<void> checkAuthState() async {
    final token = await _storageService.getAccessToken();
    if (token != null && token.isNotEmpty) {
      isAuthenticated.value = true;
      userEmail.value = await _storageService.getUserEmail() ?? '';
      userDisplayName.value = await _storageService.getDisplayName() ?? '';
    } else {
      isAuthenticated.value = false;
    }
  }

  Future<bool> login(String email, String password) async {
    isLoading.value = true;
    errorMessage.value = '';
    final cleanEmail = email.trim().toLowerCase();
    final cleanPassword = password.trim();
    try {
      final response = await _apiClient.dio.post(
        '/auth/login',
        data: {'email': cleanEmail, 'password': cleanPassword},
      );

      final data = response.data;
      final accessToken = (data['access_token'] ?? data['accessToken']) as String;
      final refreshToken = (data['refresh_token'] ?? data['refreshToken']) as String;
      final user = data['user'];
      final userEmailStr = user['email'] as String;
      final userDisplayNameStr = (user['display_name'] ?? user['displayName'] ?? '') as String;

      await _storageService.saveTokens(
        accessToken: accessToken,
        refreshToken: refreshToken,
      );
      await _storageService.saveUserInfo(
        email: userEmailStr,
        displayName: userDisplayNameStr,
      );

      userEmail.value = userEmailStr;
      userDisplayName.value = userDisplayNameStr;
      isAuthenticated.value = true;

      Get.offAllNamed('/chat');
      return true;
    } on DioException catch (e) {
      if (e.type == DioExceptionType.connectionTimeout || 
          e.type == DioExceptionType.receiveTimeout || 
          e.type == DioExceptionType.sendTimeout || 
          e.type == DioExceptionType.connectionError) {
        errorMessage.value = 'Server is starting up. Please wait a few seconds and try again.';
      } else {
        final detail = e.response?.data['detail'] ?? e.response?.data['message'];
        errorMessage.value = detail != null ? detail.toString() : 'Login failed. Please check credentials.';
      }
      return false;
    } catch (e) {
      errorMessage.value = 'An unexpected error occurred: $e';
      return false;
    } finally {
      isLoading.value = false;
    }
  }

  Future<bool> register(String email, String password, String displayName) async {
    isLoading.value = true;
    errorMessage.value = '';
    final cleanEmail = email.trim().toLowerCase();
    final cleanPassword = password.trim();
    final cleanName = displayName.trim();
    try {
      final response = await _apiClient.dio.post(
        '/auth/register',
        data: {
          'email': cleanEmail,
          'password': cleanPassword,
          'display_name': cleanName.isEmpty ? cleanEmail.split('@')[0] : cleanName,
        },
      );

      final data = response.data;
      final accessToken = (data['access_token'] ?? data['accessToken']) as String;
      final refreshToken = (data['refresh_token'] ?? data['refreshToken']) as String;
      final user = data['user'];
      final userEmailStr = user['email'] as String;
      final userDisplayNameStr = (user['display_name'] ?? user['displayName'] ?? '') as String;

      await _storageService.saveTokens(
        accessToken: accessToken,
        refreshToken: refreshToken,
      );
      await _storageService.saveUserInfo(
        email: userEmailStr,
        displayName: userDisplayNameStr,
      );

      userEmail.value = userEmailStr;
      userDisplayName.value = userDisplayNameStr;
      isAuthenticated.value = true;

      Get.offAllNamed('/chat');
      return true;
    } on DioException catch (e) {
      if (e.type == DioExceptionType.connectionTimeout || 
          e.type == DioExceptionType.receiveTimeout || 
          e.type == DioExceptionType.sendTimeout || 
          e.type == DioExceptionType.connectionError) {
        errorMessage.value = 'Server is starting up. Please wait a few seconds and try again.';
      } else {
        final detail = e.response?.data['detail'] ?? e.response?.data['message'];
        errorMessage.value = detail != null ? detail.toString() : 'Registration failed.';
      }
      return false;
    } catch (e) {
      errorMessage.value = 'An unexpected error occurred: $e';
      return false;
    } finally {
      isLoading.value = false;
    }
  }

  Future<void> logout() async {
    await _storageService.clearAll();
    isAuthenticated.value = false;
    userEmail.value = '';
    userDisplayName.value = '';
    Get.offAllNamed('/login');
  }
}
