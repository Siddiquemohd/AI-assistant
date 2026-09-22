import 'package:get/get.dart';
import '../../../core/network/api_client.dart';

class SettingsController extends GetxController {
  final ApiClient _apiClient = Get.find<ApiClient>();

  final RxString theme = 'System'.obs;
  final RxBool voiceEnabled = true.obs;
  final RxBool proactiveAssistance = false.obs;
  final RxString quietHoursStart = '22:00'.obs;
  final RxString quietHoursEnd = '07:00'.obs;
  final RxString assistantPersonality = 'Helpful, accurate personal AI assistant'.obs;

  final RxBool isLoading = false.obs;
  final RxBool isExporting = false.obs;
  final RxBool isDeletingAccount = false.obs;

  @override
  void onInit() {
    super.onInit();
    fetchPreferences();
  }

  Future<void> fetchPreferences() async {
    isLoading.value = true;
    try {
      final response = await _apiClient.dio.get('/settings/preferences');
      if (response.statusCode == 200 && response.data != null) {
        final data = response.data as Map<String, dynamic>;
        theme.value = data['theme'] ?? 'System';
        voiceEnabled.value = data['voice_enabled'] ?? true;
        proactiveAssistance.value = data['proactive_assistance'] ?? false;
        quietHoursStart.value = data['quiet_hours_start'] ?? '22:00';
        quietHoursEnd.value = data['quiet_hours_end'] ?? '07:00';
        assistantPersonality.value = data['assistant_personality'] ?? 'Helpful, accurate personal AI assistant';
      }
    } catch (e) {
      Get.snackbar('Error', 'Failed to load user settings: $e', snackPosition: SnackPosition.BOTTOM);
    } finally {
      isLoading.value = false;
    }
  }

  Future<void> savePreferences({
    String? newTheme,
    bool? newVoiceEnabled,
    bool? newProactiveAssistance,
    String? newQuietHoursStart,
    String? newQuietHoursEnd,
    String? newPersonality,
  }) async {
    isLoading.value = true;
    try {
      final body = {
        if (newTheme != null) 'theme': newTheme,
        if (newVoiceEnabled != null) 'voice_enabled': newVoiceEnabled,
        if (newProactiveAssistance != null) 'proactive_assistance': newProactiveAssistance,
        if (newQuietHoursStart != null) 'quiet_hours_start': newQuietHoursStart,
        if (newQuietHoursEnd != null) 'quiet_hours_end': newQuietHoursEnd,
        if (newPersonality != null) 'assistant_personality': newPersonality,
      };

      final response = await _apiClient.dio.patch('/settings/preferences', data: body);
      if (response.statusCode == 200 && response.data != null) {
        final data = response.data as Map<String, dynamic>;
        theme.value = data['theme'] ?? theme.value;
        voiceEnabled.value = data['voice_enabled'] ?? voiceEnabled.value;
        proactiveAssistance.value = data['proactive_assistance'] ?? proactiveAssistance.value;
        quietHoursStart.value = data['quiet_hours_start'] ?? quietHoursStart.value;
        quietHoursEnd.value = data['quiet_hours_end'] ?? quietHoursEnd.value;
        assistantPersonality.value = data['assistant_personality'] ?? assistantPersonality.value;

        Get.snackbar('Success', 'Preferences updated successfully', snackPosition: SnackPosition.BOTTOM);
      }
    } catch (e) {
      Get.snackbar('Error', 'Failed to update preferences: $e', snackPosition: SnackPosition.BOTTOM);
    } finally {
      isLoading.value = false;
    }
  }

  Future<void> exportUserData() async {
    isExporting.value = true;
    try {
      final response = await _apiClient.dio.post('/settings/export');
      if (response.statusCode == 200) {
        Get.defaultDialog(
          title: 'Data Export Ready',
          middleText: 'Your ISAI user data export (JSON format) has been prepared successfully.',
          textConfirm: 'OK',
          onConfirm: () => Get.back(),
        );
      }
    } catch (e) {
      Get.snackbar('Export Failed', 'Unable to export user data: $e', snackPosition: SnackPosition.BOTTOM);
    } finally {
      isExporting.value = false;
    }
  }

  Future<void> requestAccountDeletion() async {
    isDeletingAccount.value = true;
    try {
      final response = await _apiClient.dio.delete('/settings/account');
      if (response.statusCode == 200) {
        Get.defaultDialog(
          title: 'Account Deletion Requested',
          middleText: 'Your account and personal data have been scheduled for deletion with a 14-day grace period.',
          textConfirm: 'Log Out Now',
          onConfirm: () {
            Get.back();
            Get.offAllNamed('/login');
          },
        );
      }
    } catch (e) {
      Get.snackbar('Deletion Failed', 'Unable to request account deletion: $e', snackPosition: SnackPosition.BOTTOM);
    } finally {
      isDeletingAccount.value = false;
    }
  }
}
