import 'package:get/get.dart';
import '../../../core/network/api_client.dart';

class TaskModel {
  final String id;
  final String title;
  final String description;
  String status;
  final String priority;
  final DateTime? dueAt;
  final DateTime? completedAt;

  TaskModel({
    required this.id,
    required this.title,
    required this.description,
    required this.status,
    required this.priority,
    this.dueAt,
    this.completedAt,
  });

  factory TaskModel.fromJson(Map<String, dynamic> json) {
    return TaskModel(
      id: json['id'] as String,
      title: json['title'] as String,
      description: json['description'] as String? ?? '',
      status: json['status'] as String? ?? 'Pending',
      priority: json['priority'] as String? ?? 'Medium',
      dueAt: json['due_at'] != null ? DateTime.parse(json['due_at'] as String) : null,
      completedAt: json['completed_at'] != null ? DateTime.parse(json['completed_at'] as String) : null,
    );
  }
}

class TaskController extends GetxController {
  final ApiClient _apiClient = Get.find<ApiClient>();

  final RxList<TaskModel> tasks = <TaskModel>[].obs;
  final RxBool isLoading = false.obs;
  final RxString errorMessage = ''.obs;

  @override
  void onInit() {
    super.onInit();
    fetchTasks();
  }

  Future<void> fetchTasks() async {
    isLoading.value = true;
    try {
      final response = await _apiClient.dio.get('/tasks');
      final list = (response.data as List)
          .map((item) => TaskModel.fromJson(item))
          .toList();
      tasks.value = list;
    } catch (e) {
      errorMessage.value = 'Failed to load tasks.';
    } finally {
      isLoading.value = false;
    }
  }

  Future<bool> createTask(String title, String description, String priority) async {
    if (title.trim().isEmpty) return false;
    try {
      final response = await _apiClient.dio.post(
        '/tasks',
        data: {
          'title': title.trim(),
          'description': description.trim(),
          'priority': priority,
        },
      );
      final newTask = TaskModel.fromJson(response.data);
      tasks.insert(0, newTask);
      return true;
    } catch (e) {
      Get.snackbar('Error', 'Failed to create task');
      return false;
    }
  }

  Future<void> toggleTaskCompleted(TaskModel task) async {
    final newStatus = task.status == 'Completed' ? 'Pending' : 'Completed';
    task.status = newStatus;
    tasks.refresh();

    try {
      await _apiClient.dio.patch(
        '/tasks/${task.id}',
        data: {'status': newStatus},
      );
    } catch (e) {
      task.status = newStatus == 'Completed' ? 'Pending' : 'Completed';
      tasks.refresh();
    }
  }

  Future<void> deleteTask(TaskModel task) async {
    tasks.removeWhere((t) => t.id == task.id);
    try {
      await _apiClient.dio.delete('/tasks/${task.id}');
    } catch (e) {
      tasks.add(task);
      Get.snackbar('Error', 'Failed to delete task');
    }
  }

  Future<Map<String, dynamic>?> submitAgentRun(String intent) async {
    try {
      final response = await _apiClient.dio.post(
        '/agent/runs',
        data: {'intent': intent},
      );
      fetchTasks();
      return response.data as Map<String, dynamic>;
    } catch (e) {
      Get.snackbar('Error', 'Failed to submit agent run');
      return null;
    }
  }

  Future<bool> confirmAgentRun(String runId, String digest) async {
    try {
      await _apiClient.dio.post(
        '/agent/runs/$runId/confirm',
        data: {'confirmation_token_digest': digest},
      );
      fetchTasks();
      Get.snackbar('Authorized', 'Agent action authorized and completed.');
      return true;
    } catch (e) {
      Get.snackbar('Error', 'Authorization failed or stale confirmation token');
      return false;
    }
  }
}
