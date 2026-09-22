import 'package:get/get.dart';
import '../../core/network/api_client.dart';
import '../../core/storage/secure_storage_service.dart';
import '../../features/authentication/controllers/auth_controller.dart';
import '../../features/chat/controllers/chat_controller.dart';

class InitialBinding extends Bindings {
  @override
  void dependencies() {
    Get.put<SecureStorageService>(SecureStorageService(), permanent: true);
    Get.put<ApiClient>(ApiClient(Get.find<SecureStorageService>()), permanent: true);
    Get.put<AuthController>(AuthController(), permanent: true);
    Get.lazyPut<ChatController>(() => ChatController(), fenix: true);
  }
}
