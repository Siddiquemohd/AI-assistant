// ignore_for_file: constant_identifier_names

import 'package:get/get.dart';
import '../../features/authentication/views/login_view.dart';
import '../../features/authentication/views/register_view.dart';
import '../../features/chat/views/chat_view.dart';
import '../../features/voice/views/voice_assistant_view.dart';
import '../../features/memory/views/memory_management_view.dart';
import '../../features/tasks/views/task_management_view.dart';
import '../../features/settings/views/settings_view.dart';
import 'app_routes.dart';

class AppPages {
  static const INITIAL = Routes.LOGIN;

  static final routes = [
    GetPage(
      name: Routes.LOGIN,
      page: () => LoginView(),
    ),
    GetPage(
      name: Routes.REGISTER,
      page: () => RegisterView(),
    ),
    GetPage(
      name: Routes.CHAT,
      page: () => ChatView(),
    ),
    GetPage(
      name: Routes.VOICE,
      page: () => VoiceAssistantView(),
    ),
    GetPage(
      name: Routes.MEMORY,
      page: () => MemoryManagementView(),
    ),
    GetPage(
      name: Routes.TASKS,
      page: () => TaskManagementView(),
    ),
    GetPage(
      name: Routes.SETTINGS,
      page: () => SettingsView(),
    ),
  ];
}

