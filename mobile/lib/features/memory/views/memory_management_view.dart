import 'package:flutter/material.dart';
import 'package:get/get.dart';
import '../../../core/theme/app_theme.dart';
import '../controllers/memory_controller.dart';

class MemoryManagementView extends StatelessWidget {
  MemoryManagementView({super.key});

  final MemoryController _controller = Get.put(MemoryController());

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppTheme.darkBackground,
      appBar: AppBar(
        title: const Text('ISAI — Memory Bank & Knowledge Triples'),
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
        backgroundColor: AppTheme.primaryNeon,
        foregroundColor: Colors.black,
        icon: const Icon(Icons.psychology_rounded),
        label: const Text('Add Memory', style: TextStyle(fontWeight: FontWeight.bold)),
      ),
      body: Column(
        children: [
          Padding(
            padding: const EdgeInsets.all(16.0),
            child: TextField(
              style: const TextStyle(color: Colors.white),
              decoration: const InputDecoration(
                hintText: 'Search personal memories...',
                prefixIcon: Icon(Icons.search, color: AppTheme.primaryNeon),
              ),
              onChanged: (val) => _controller.searchQuery.value = val,
            ),
          ),
          Expanded(
            child: Obx(() {
              if (_controller.isLoading.value) {
                return const Center(child: CircularProgressIndicator(color: AppTheme.primaryNeon));
              }
              final list = _controller.filteredMemories;
              if (list.isEmpty) {
                return Center(
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      const Icon(Icons.psychology_outlined, size: 64, color: AppTheme.slate),
                      const SizedBox(height: 16),
                      const Text(
                        'No long-term memories stored yet.',
                        style: TextStyle(color: AppTheme.slate, fontSize: 16),
                      ),
                      const SizedBox(height: 6),
                      const Text(
                        'Store personal context, preferences, or facts!',
                        style: TextStyle(color: AppTheme.slate, fontSize: 12),
                      ),
                    ],
                  ),
                );
              }
              return ListView.builder(
                padding: const EdgeInsets.all(16.0),
                itemCount: list.length,
                itemBuilder: (context, index) {
                  final mem = list[index];
                  return Container(
                    margin: const EdgeInsets.only(bottom: 12.0),
                    decoration: BoxDecoration(
                      color: AppTheme.cardBackground,
                      borderRadius: BorderRadius.circular(16),
                      border: Border.all(color: AppTheme.cardBorder),
                    ),
                    child: ListTile(
                      title: Text(
                        mem.content,
                        style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold),
                      ),
                      subtitle: Padding(
                        padding: const EdgeInsets.only(top: 6.0),
                        child: Row(
                          children: [
                            Chip(
                              label: Text(mem.category, style: const TextStyle(fontSize: 10, color: Colors.white)),
                              backgroundColor: AppTheme.inputBackground,
                              side: const BorderSide(color: AppTheme.cardBorder),
                              padding: EdgeInsets.zero,
                              visualDensity: VisualDensity.compact,
                            ),
                            const SizedBox(width: 8),
                            Chip(
                              label: Text(mem.sensitivityLevel, style: TextStyle(fontSize: 10, color: mem.sensitivityLevel == 'Confidential' ? Colors.redAccent : AppTheme.primaryNeon)),
                              backgroundColor: AppTheme.inputBackground,
                              side: BorderSide(color: mem.sensitivityLevel == 'Confidential' ? Colors.redAccent : AppTheme.cardBorder),
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
                            activeColor: AppTheme.primaryNeon,
                            onChanged: (val) => _controller.toggleMemoryEnabled(mem, val),
                          ),
                          IconButton(
                            icon: const Icon(Icons.delete_outline, color: Colors.redAccent, size: 20),
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
        backgroundColor: AppTheme.cardBackground,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
        title: const Text('Add Approved Memory', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            TextField(
              controller: contentCtrl,
              style: const TextStyle(color: Colors.white),
              decoration: const InputDecoration(
                labelText: 'Memory Content',
                hintText: 'e.g. User prefers Python and Dark Mode',
              ),
              maxLines: 3,
            ),
            const SizedBox(height: 16),
            DropdownButtonFormField<String>(
              value: category,
              dropdownColor: AppTheme.cardBackground,
              style: const TextStyle(color: Colors.white),
              decoration: const InputDecoration(labelText: 'Category'),
              items: ['Preference', 'Fact', 'Work', 'Personal']
                  .map((c) => DropdownMenuItem(value: c, child: Text(c)))
                  .toList(),
              onChanged: (val) => category = val!,
            ),
            const SizedBox(height: 16),
            DropdownButtonFormField<String>(
              value: sensitivity,
              dropdownColor: AppTheme.cardBackground,
              style: const TextStyle(color: Colors.white),
              decoration: const InputDecoration(labelText: 'Sensitivity Level'),
              items: ['Normal', 'Private', 'Confidential']
                  .map((s) => DropdownMenuItem(value: s, child: Text(s)))
                  .toList(),
              onChanged: (val) => sensitivity = val!,
            ),
          ],
        ),
        actions: [
          TextButton(onPressed: () => Get.back(), child: const Text('Cancel', style: TextStyle(color: AppTheme.slate))),
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
        backgroundColor: AppTheme.cardBackground,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
        title: const Text('Clear All Memories?', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
        content: const Text(
          'Are you sure you want to delete all stored memories? This operation cannot be undone.',
          style: TextStyle(color: AppTheme.slate),
        ),
        actions: [
          TextButton(onPressed: () => Get.back(), child: const Text('Cancel', style: TextStyle(color: AppTheme.slate))),
          ElevatedButton(
            style: ElevatedButton.styleFrom(backgroundColor: Colors.redAccent, foregroundColor: Colors.white),
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
