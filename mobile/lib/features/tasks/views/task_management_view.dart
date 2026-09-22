import 'package:flutter/material.dart';
import 'package:get/get.dart';
import '../controllers/task_controller.dart';

class TaskManagementView extends StatelessWidget {
  TaskManagementView({super.key});

  final TaskController _controller = Get.put(TaskController());

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('ISAI — Tasks & Agent'),
        actions: [
          IconButton(
            icon: const Icon(Icons.smart_toy_outlined, color: Colors.blueAccent),
            tooltip: 'Run Agent Command',
            onPressed: () => _showAgentCommandDialog(context),
          ),
        ],
      ),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: () => _showAddTaskDialog(context),
        icon: const Icon(Icons.add_task),
        label: const Text('New Task'),
      ),
      body: Obx(() {
        if (_controller.isLoading.value) {
          return const Center(child: CircularProgressIndicator());
        }
        if (_controller.tasks.isEmpty) {
          return const Center(
            child: Text('No tasks found. Create one or run an Agent command!'),
          );
        }
        return ListView.builder(
          padding: const EdgeInsets.all(16.0),
          itemCount: _controller.tasks.length,
          itemBuilder: (context, index) {
            final task = _controller.tasks[index];
            final isCompleted = task.status == 'Completed';

            return Card(
              margin: const EdgeInsets.only(bottom: 12.0),
              child: ListTile(
                leading: Checkbox(
                  value: isCompleted,
                  onChanged: (val) => _controller.toggleTaskCompleted(task),
                ),
                title: Text(
                  task.title,
                  style: TextStyle(
                    decoration: isCompleted ? TextDecoration.lineThrough : TextDecoration.none,
                    color: isCompleted ? Colors.grey : Colors.white,
                  ),
                ),
                subtitle: Text(
                  task.description.isNotEmpty ? task.description : 'Priority: ${task.priority}',
                  style: const TextStyle(fontSize: 12, color: Colors.grey),
                ),
                trailing: Row(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Chip(
                      label: Text(task.priority, style: const TextStyle(fontSize: 10)),
                      backgroundColor: task.priority == 'High' || task.priority == 'Urgent'
                          ? Colors.red.shade900
                          : Colors.blueGrey.shade800,
                      padding: EdgeInsets.zero,
                      visualDensity: VisualDensity.compact,
                    ),
                    IconButton(
                      icon: const Icon(Icons.delete_outline, color: Colors.redAccent),
                      onPressed: () => _controller.deleteTask(task),
                    ),
                  ],
                ),
              ),
            );
          },
        );
      }),
    );
  }

  void _showAddTaskDialog(BuildContext context) {
    final titleCtrl = TextEditingController();
    final descCtrl = TextEditingController();
    String priority = 'Medium';

    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        title: const Text('Create New Task'),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            TextField(
              controller: titleCtrl,
              decoration: const InputDecoration(labelText: 'Title', border: OutlineInputBorder()),
            ),
            const SizedBox(height: 16),
            TextField(
              controller: descCtrl,
              decoration: const InputDecoration(labelText: 'Description', border: OutlineInputBorder()),
            ),
            const SizedBox(height: 16),
            DropdownButtonFormField<String>(
              value: priority,
              decoration: const InputDecoration(labelText: 'Priority', border: OutlineInputBorder()),
              items: ['Low', 'Medium', 'High', 'Urgent']
                  .map((p) => DropdownMenuItem(value: p, child: Text(p)))
                  .toList(),
              onChanged: (val) => priority = val!,
            ),
          ],
        ),
        actions: [
          TextButton(onPressed: () => Get.back(), child: const Text('Cancel')),
          ElevatedButton(
            onPressed: () async {
              if (titleCtrl.text.trim().isNotEmpty) {
                final ok = await _controller.createTask(titleCtrl.text, descCtrl.text, priority);
                if (ok) Get.back();
              }
            },
            child: const Text('Save'),
          ),
        ],
      ),
    );
  }

  void _showAgentCommandDialog(BuildContext context) {
    final intentCtrl = TextEditingController();

    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        title: const Text('Submit Agent Intent'),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Text(
              'Enter a natural language command for the Personal Agent.',
              style: TextStyle(fontSize: 12, color: Colors.grey),
            ),
            const SizedBox(height: 12),
            TextField(
              controller: intentCtrl,
              decoration: const InputDecoration(
                hintText: 'e.g. Create a task to review PR',
                border: OutlineInputBorder(),
              ),
            ),
          ],
        ),
        actions: [
          TextButton(onPressed: () => Get.back(), child: const Text('Cancel')),
          ElevatedButton(
            onPressed: () async {
              final text = intentCtrl.text.trim();
              if (text.isNotEmpty) {
                Get.back();
                final result = await _controller.submitAgentRun(text);
                if (result != null && result['status'] == 'AwaitingConfirmation' && context.mounted) {
                  _showConfirmationModal(context, result['id'], result['confirmation_token_digest'], text);
                }
              }
            },
            child: const Text('Execute Agent'),
          ),
        ],
      ),
    );
  }

  void _showConfirmationModal(BuildContext context, String runId, String digest, String intent) {
    showDialog(
      context: context,
      barrierDismissible: false,
      builder: (ctx) => AlertDialog(
        title: const Row(
          children: [
            Icon(Icons.warning_amber_rounded, color: Colors.amber),
            SizedBox(width: 8),
            Text('Action Confirmation Required'),
          ],
        ),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'The Personal Agent requests permission to perform a high-risk action:',
              style: TextStyle(fontSize: 13),
            ),
            const SizedBox(height: 12),
            Card(
              color: Colors.amber.shade900.withValues(alpha: 0.3),
              child: Padding(
                padding: const EdgeInsets.all(12.0),
                child: Text('Command: "$intent"', style: const TextStyle(fontWeight: FontWeight.bold)),
              ),
            ),
            const SizedBox(height: 12),
            Text('Digest: ${digest.substring(0, 16)}...', style: const TextStyle(fontSize: 10, color: Colors.grey)),
          ],
        ),
        actions: [
          TextButton(onPressed: () => Get.back(), child: const Text('Reject')),
          ElevatedButton(
            style: ElevatedButton.styleFrom(backgroundColor: Colors.amber.shade700),
            onPressed: () async {
              Get.back();
              await _controller.confirmAgentRun(runId, digest);
            },
            child: const Text('Authorize & Execute'),
          ),
        ],
      ),
    );
  }
}
