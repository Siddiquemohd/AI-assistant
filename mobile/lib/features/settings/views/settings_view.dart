import 'package:flutter/material.dart';
import 'package:get/get.dart';
import '../controllers/settings_controller.dart';

class SettingsView extends StatelessWidget {
  SettingsView({super.key});

  final SettingsController _controller = Get.put(SettingsController());
  final TextEditingController _personalityController = TextEditingController();
  final TextEditingController _quietStartController = TextEditingController();
  final TextEditingController _quietEndController = TextEditingController();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Settings & Privacy'),
      ),
      body: Obx(() {
        if (_controller.isLoading.value) {
          return const Center(child: CircularProgressIndicator());
        }

        _personalityController.text = _controller.assistantPersonality.value;
        _quietStartController.text = _controller.quietHoursStart.value;
        _quietEndController.text = _controller.quietHoursEnd.value;

        return ListView(
          padding: const EdgeInsets.all(16.0),
          children: [
            const Text(
              'App Preferences',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.blueAccent),
            ),
            const SizedBox(height: 12),

            // Theme Setting
            ListTile(
              title: const Text('Theme'),
              trailing: DropdownButton<String>(
                value: _controller.theme.value,
                items: const [
                  DropdownMenuItem(value: 'System', child: Text('System')),
                  DropdownMenuItem(value: 'Light', child: Text('Light')),
                  DropdownMenuItem(value: 'Dark', child: Text('Dark')),
                ],
                onChanged: (val) {
                  if (val != null) {
                    _controller.savePreferences(newTheme: val);
                  }
                },
              ),
            ),

            // Voice AI Toggle
            SwitchListTile(
              title: const Text('Enable Voice AI Mode'),
              subtitle: const Text('Allow local speech synthesis & recognition'),
              value: _controller.voiceEnabled.value,
              onChanged: (val) {
                _controller.savePreferences(newVoiceEnabled: val);
              },
            ),

            // Proactive Assistance Toggle
            SwitchListTile(
              title: const Text('Proactive Assistance'),
              subtitle: const Text('Allow ISAI to remind you of upcoming tasks'),
              value: _controller.proactiveAssistance.value,
              onChanged: (val) {
                _controller.savePreferences(newProactiveAssistance: val);
              },
            ),
            const Divider(),

            const SizedBox(height: 8),
            const Text(
              'Quiet Hours & Personality',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.blueAccent),
            ),
            const SizedBox(height: 12),

            Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _quietStartController,
                    decoration: const InputDecoration(
                      labelText: 'Quiet Hours Start',
                      hintText: '22:00',
                      border: OutlineInputBorder(),
                    ),
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: TextField(
                    controller: _quietEndController,
                    decoration: const InputDecoration(
                      labelText: 'Quiet Hours End',
                      hintText: '07:00',
                      border: OutlineInputBorder(),
                    ),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 12),

            TextField(
              controller: _personalityController,
              decoration: const InputDecoration(
                labelText: 'Assistant Personality Directive',
                hintText: 'e.g. Concise, professional, and friendly',
                border: OutlineInputBorder(),
              ),
              maxLines: 2,
            ),
            const SizedBox(height: 12),

            ElevatedButton.icon(
              onPressed: () {
                _controller.savePreferences(
                  newQuietHoursStart: _quietStartController.text,
                  newQuietHoursEnd: _quietEndController.text,
                  newPersonality: _personalityController.text,
                );
              },
              icon: const Icon(Icons.save_rounded),
              label: const Text('Save Custom Directives'),
            ),

            const Divider(height: 32),

            const Text(
              'Privacy & Data Ownership',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.blueAccent),
            ),
            const SizedBox(height: 12),

            // Data Export Button
            ListTile(
              leading: const Icon(Icons.download_rounded, color: Colors.greenAccent),
              title: const Text('Export My Data'),
              subtitle: const Text('Download a JSON copy of all your conversations, memories & tasks'),
              trailing: _controller.isExporting.value
                  ? const SizedBox(width: 24, height: 24, child: CircularProgressIndicator(strokeWidth: 2))
                  : const Icon(Icons.chevron_right_rounded),
              onTap: _controller.isExporting.value ? null : () => _controller.exportUserData(),
            ),

            const SizedBox(height: 8),

            // Account Deletion Button
            ListTile(
              leading: const Icon(Icons.delete_forever_rounded, color: Colors.redAccent),
              title: const Text('Request Account Deletion', style: TextStyle(color: Colors.redAccent)),
              subtitle: const Text('Permanently remove your account and all associated data'),
              onTap: () {
                Get.defaultDialog(
                  title: 'Confirm Account Deletion',
                  middleText: 'Are you sure you want to request account deletion? All your data will be queued for soft deletion and permanently purged after 14 days.',
                  textConfirm: 'Yes, Delete My Account',
                  textCancel: 'Cancel',
                  confirmTextColor: Colors.white,
                  buttonColor: Colors.redAccent,
                  onConfirm: () {
                    Get.back();
                    _controller.requestAccountDeletion();
                  },
                );
              },
            ),
          ],
        );
      }),
    );
  }
}
