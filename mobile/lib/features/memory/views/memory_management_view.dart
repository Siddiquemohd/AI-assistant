import 'package:flutter/material.dart';
import 'package:get/get.dart';
import '../controllers/memory_controller.dart';

class MemoryManagementView extends StatelessWidget {
  MemoryManagementView({super.key});

  final MemoryController _controller = Get.put(MemoryController());

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('ISAI — Memory Bank'),
        actions: [
          IconButton(
            icon: const Icon(Icons.delete_sweep_outlined, color: Colors.redAccent),
            tooltip: 'Clear All Memories',
            onPressed: () => _showClearAllDialog(context),
          ),
        ],
      ),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: () => _showAddMemoryDialog(context),
        icon: const Icon(Icons.add),
        label: const Text('Add Memory'),
      ),
      body: Column(
        children: [
          Padding(
            padding: const EdgeInsets.all(16.0),
            child: TextField(
              decoration: const InputDecoration(
                hintText: 'Search memories...',
                prefixIcon: Icon(Icons.search),
                border: OutlineInputBorder(),
              ),
              onChanged: (val) => _controller.searchQuery.value = val,
            ),
          ),
          Expanded(
            child: Obx(() {
              if (_controller.isLoading.value) {
                return const Center(child: CircularProgressIndicator());
              }
              final list = _controller.filteredMemories;
              if (list.isEmpty) {
                return const Center(
                  child: Text('No approved memories found.'),
                );
              }
              return ListView.builder(
                padding: const EdgeInsets.all(16.0),
                itemCount: list.length,
                itemBuilder: (context, index) {
                  final mem = list[index];
                  return Card(
                    margin: const EdgeInsets.only(bottom: 12.0),
                    child: ListTile(
                      title: Text(mem.content),
                      subtitle: Padding(
                        padding: const EdgeInsets.only(top: 4.0),
                        child: Row(
                          children: [
                            Chip(
                              label: Text(mem.category, style: const TextStyle(fontSize: 10)),
                              padding: EdgeInsets.zero,
                              visualDensity: VisualDensity.compact,
                            ),
                            const SizedBox(width: 8),
                            Chip(
                              label: Text(mem.sensitivityLevel, style: const TextStyle(fontSize: 10)),
                              backgroundColor: mem.sensitivityLevel == 'Confidential' ? Colors.red.shade900 : Colors.blueGrey.shade800,
                              padding: EdgeInsets.zero,
                              visualDensity: VisualDensity.compact,
                            ),
                          ],
                        ),
                      ),
                      trailing: Row(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          Switch(
                            value: mem.isEnabled,
                            onChanged: (val) => _controller.toggleMemoryEnabled(mem, val),
                          ),
                          IconButton(
                            icon: const Icon(Icons.delete_outline, color: Colors.redAccent),
                            onPressed: () => _controller.deleteMemory(mem),
                          ),
                        ],
                      ),
                    ),
                  );
                },
              );
            }),
          ),
        ],
      ),
    );
  }

  void _showAddMemoryDialog(BuildContext context) {
    final contentCtrl = TextEditingController();
    String category = 'Preference';
    String sensitivity = 'Normal';

    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        title: const Text('Add User-Approved Memory'),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            TextField(
              controller: contentCtrl,
              decoration: const InputDecoration(
                labelText: 'Memory Content',
                hintText: 'e.g. User prefers concise code snippets',
                border: OutlineInputBorder(),
              ),
              maxLines: 3,
            ),
            const SizedBox(height: 16),
            DropdownButtonFormField<String>(
              value: category,
              decoration: const InputDecoration(labelText: 'Category', border: OutlineInputBorder()),
              items: ['Preference', 'Fact', 'Work', 'Personal']
                  .map((c) => DropdownMenuItem(value: c, child: Text(c)))
                  .toList(),
              onChanged: (val) => category = val!,
            ),
            const SizedBox(height: 16),
            DropdownButtonFormField<String>(
              value: sensitivity,
              decoration: const InputDecoration(labelText: 'Sensitivity Level', border: OutlineInputBorder()),
              items: ['Normal', 'Private', 'Confidential']
                  .map((s) => DropdownMenuItem(value: s, child: Text(s)))
                  .toList(),
              onChanged: (val) => sensitivity = val!,
            ),
          ],
        ),
        actions: [
          TextButton(onPressed: () => Get.back(), child: const Text('Cancel')),
          ElevatedButton(
            onPressed: () async {
              if (contentCtrl.text.trim().isNotEmpty) {
                final success = await _controller.createMemory(
                  contentCtrl.text,
                  category,
                  sensitivity,
                );
                if (success) Get.back();
              }
            },
            child: const Text('Save Memory'),
          ),
        ],
      ),
    );
  }

  void _showClearAllDialog(BuildContext context) {
    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        title: const Text('Clear All Memories?'),
        content: const Text(
          'Are you sure you want to delete all user-approved durable memories? This operation cannot be undone.',
        ),
        actions: [
          TextButton(onPressed: () => Get.back(), child: const Text('Cancel')),
          ElevatedButton(
            style: ElevatedButton.styleFrom(backgroundColor: Colors.red),
            onPressed: () {
              Get.back();
              _controller.clearAllMemories();
            },
            child: const Text('Clear All'),
          ),
        ],
      ),
    );
  }
}
