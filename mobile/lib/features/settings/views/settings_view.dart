import 'package:flutter/material.dart';
import 'package:get/get.dart';
import '../../../core/theme/app_theme.dart';
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
      backgroundColor: AppTheme.darkBackground,
      appBar: AppBar(
        title: const Text('ISAI — Settings & Diagnostics'),
      ),
      body: Obx(() {
        if (_controller.isLoading.value) {
          return const Center(child: CircularProgressIndicator(color: AppTheme.primaryNeon));
        }

        _personalityController.text = _controller.assistantPersonality.value;
        _quietStartController.text = _controller.quietHoursStart.value;
        _quietEndController.text = _controller.quietHoursEnd.value;

        return ListView(
          padding: const EdgeInsets.all(16.0),
          children: [
            // Engine Diagnostics Card
            Container(
              padding: const EdgeInsets.all(16.0),
              decoration: BoxDecoration(
                color: AppTheme.cardBackground,
                borderRadius: BorderRadius.circular(16),
                border: Border.all(color: AppTheme.primaryNeon.withValues(alpha: 0.5)),
                boxShadow: [
                  BoxShadow(
                    color: AppTheme.primaryNeon.withValues(alpha: 0.15),
                    blurRadius: 16,
                  ),
                ],
              ),
              child: const Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      Icon(Icons.memory_rounded, color: AppTheme.primaryNeon),
                      SizedBox(width: 8),
                      Text(
                        'AI ENGINE STATUS',
                        style: TextStyle(fontWeight: FontWeight.bold, fontSize: 14, color: AppTheme.primaryNeon, letterSpacing: 1),
                      ),
                    ],
                  ),
                  SizedBox(height: 8),
                  Text('• Model: ISAI 25-Engine Uncensored Suite', style: TextStyle(color: Colors.white, fontSize: 12)),
                  Text('• Deployment: Render Cloud Web Service (24/7)', style: TextStyle(color: Colors.white, fontSize: 12)),
                  Text('• Refusal Filters: Disabled (0% Content Refusal)', style: TextStyle(color: Colors.white, fontSize: 12)),
                  Text('• Database: Supabase PostgreSQL (SSL Active)', style: TextStyle(color: Colors.white, fontSize: 12)),
                ],
              ),
            ),
            const SizedBox(height: 24),

            const Text(
              'App Preferences',
              style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: AppTheme.primaryNeon),
            ),
            const SizedBox(height: 12),

            // Theme Setting
            Container(
              decoration: BoxDecoration(
                color: AppTheme.cardBackground,
                borderRadius: BorderRadius.circular(16),
                border: Border.all(color: AppTheme.cardBorder),
              ),
              child: ListTile(
                title: const Text('Theme Mode', style: TextStyle(color: Colors.white)),
                trailing: DropdownButton<String>(
                  value: _controller.theme.value,
                  dropdownColor: AppTheme.cardBackground,
                  style: const TextStyle(color: AppTheme.primaryNeon, fontWeight: FontWeight.bold),
                  items: const [
                    DropdownMenuItem(value: 'System', child: Text('System')),
                    DropdownMenuItem(value: 'Light', child: Text('Light')),
                    DropdownMenuItem(value: 'Dark', child: Text('Dark (Cyberpunk)')),
                  ],
                  onChanged: (val) {
                    if (val != null) {
                      _controller.savePreferences(newTheme: val);
                    }
                  },
                ),
              ),
            ),
            const SizedBox(height: 12),

            // Voice AI Toggle
            Container(
              decoration: BoxDecoration(
                color: AppTheme.cardBackground,
                borderRadius: BorderRadius.circular(16),
                border: Border.all(color: AppTheme.cardBorder),
              ),
              child: SwitchListTile(
                title: const Text('Enable Voice AI Mode', style: TextStyle(color: Colors.white)),
                subtitle: const Text('Allow speech synthesis & recognition (10 Neural Voices)', style: TextStyle(color: AppTheme.slate, fontSize: 11)),
                value: _controller.voiceEnabled.value,
                activeColor: AppTheme.primaryNeon,
                onChanged: (val) {
                  _controller.savePreferences(newVoiceEnabled: val);
                },
              ),
            ),
            const SizedBox(height: 12),

            // Proactive Assistance Toggle
            Container(
              decoration: BoxDecoration(
                color: AppTheme.cardBackground,
                borderRadius: BorderRadius.circular(16),
                border: Border.all(color: AppTheme.cardBorder),
              ),
              child: SwitchListTile(
                title: const Text('Proactive Assistance', style: TextStyle(color: Colors.white)),
                subtitle: const Text('Allow ISAI to remind you of upcoming tasks', style: TextStyle(color: AppTheme.slate, fontSize: 11)),
                value: _controller.proactiveAssistance.value,
                activeColor: AppTheme.primaryNeon,
                onChanged: (val) {
                  _controller.savePreferences(newProactiveAssistance: val);
                },
              ),
            ),
            const SizedBox(height: 24),

            const Text(
              'Quiet Hours & Directives',
              style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: AppTheme.primaryNeon),
            ),
            const SizedBox(height: 12),

            Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _quietStartController,
                    style: const TextStyle(color: Colors.white),
                    decoration: const InputDecoration(
                      labelText: 'Quiet Start',
                      hintText: '22:00',
                    ),
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: TextField(
                    controller: _quietEndController,
                    style: const TextStyle(color: Colors.white),
                    decoration: const InputDecoration(
                      labelText: 'Quiet End',
                      hintText: '07:00',
                    ),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 12),

            TextField(
              controller: _personalityController,
              style: const TextStyle(color: Colors.white),
              decoration: const InputDecoration(
                labelText: 'Assistant System Directive',
                hintText: 'e.g. Uncensored, expert developer, concise and direct',
              ),
              maxLines: 2,
            ),
            const SizedBox(height: 16),

            ElevatedButton.icon(
              onPressed: () {
                _controller.savePreferences(
                  newQuietHoursStart: _quietStartController.text,
                  newQuietHoursEnd: _quietEndController.text,
                  newPersonality: _personalityController.text,
                );
              },
              icon: const Icon(Icons.save_rounded, color: Colors.black),
              label: const Text('Save Directives', style: TextStyle(color: Colors.black, fontWeight: FontWeight.bold)),
            ),

            const SizedBox(height: 24),

            const Text(
              'Privacy & Data Controls',
              style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: AppTheme.primaryNeon),
            ),
            const SizedBox(height: 12),

            // Data Export Button
            Container(
              decoration: BoxDecoration(
                color: AppTheme.cardBackground,
                borderRadius: BorderRadius.circular(16),
                border: Border.all(color: AppTheme.cardBorder),
              ),
              child: ListTile(
                leading: const Icon(Icons.download_rounded, color: AppTheme.accentEmerald),
                title: const Text('Export My Data', style: TextStyle(color: Colors.white)),
                subtitle: const Text('Download JSON copy of all conversations & tasks', style: TextStyle(color: AppTheme.slate, fontSize: 11)),
                trailing: _controller.isExporting.value
                    ? const SizedBox(width: 20, height: 20, child: CircularProgressIndicator(strokeWidth: 2, color: AppTheme.primaryNeon))
                    : const Icon(Icons.chevron_right_rounded, color: AppTheme.slate),
                onTap: _controller.isExporting.value ? null : () => _controller.exportUserData(),
              ),
            ),

            const SizedBox(height: 12),

            // Account Deletion Button
            Container(
              decoration: BoxDecoration(
                color: AppTheme.cardBackground,
                borderRadius: BorderRadius.circular(16),
                border: Border.all(color: Colors.redAccent.withValues(alpha: 0.4)),
              ),
              child: ListTile(
                leading: const Icon(Icons.delete_forever_rounded, color: Colors.redAccent),
                title: const Text('Request Account Deletion', style: TextStyle(color: Colors.redAccent, fontWeight: FontWeight.bold)),
                subtitle: const Text('Permanently remove account and associated data', style: TextStyle(color: AppTheme.slate, fontSize: 11)),
                onTap: () {
                  Get.defaultDialog(
                    title: 'Confirm Account Deletion',
                    titleStyle: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold),
                    middleText: 'Are you sure you want to request account deletion? All your data will be permanently purged after 14 days.',
                    middleTextStyle: const TextStyle(color: AppTheme.slate),
                    backgroundColor: AppTheme.cardBackground,
                    textConfirm: 'Delete My Account',
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
            ),
          ],
        );
      }),
    );
  }
}
