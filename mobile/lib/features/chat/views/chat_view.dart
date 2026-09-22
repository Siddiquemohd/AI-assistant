import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_markdown/flutter_markdown.dart';
import 'package:get/get.dart';
import '../../authentication/controllers/auth_controller.dart';
import '../controllers/chat_controller.dart';

class ChatView extends StatelessWidget {
  ChatView({super.key});

  final ChatController _chatController = Get.find<ChatController>();
  final AuthController _authController = Get.find<AuthController>();
  final TextEditingController _messageController = TextEditingController();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Obx(() => Text(
              _chatController.currentConversation.value?.title ?? 'ISAI Assistant',
            )),
        actions: [
          IconButton(
            icon: const Icon(Icons.mic_rounded, color: Colors.blueAccent),
            tooltip: 'Voice Assistant',
            onPressed: () => Get.toNamed('/voice'),
          ),
          IconButton(
            icon: const Icon(Icons.add_comment_outlined),
            tooltip: 'New Conversation',
            onPressed: () => _chatController.createNewConversation(),
          ),
          IconButton(
            icon: const Icon(Icons.logout),
            tooltip: 'Sign Out',
            onPressed: () => _authController.logout(),
          ),
        ],
      ),
      drawer: Drawer(
        child: Column(
          children: [
            UserAccountsDrawerHeader(
              accountName: Obx(() => Text(_authController.userDisplayName.value)),
              accountEmail: Obx(() => Text(_authController.userEmail.value)),
              currentAccountPicture: const CircleAvatar(
                backgroundColor: Colors.white,
                child: Icon(Icons.smart_toy_rounded, size: 36, color: Colors.blueAccent),
              ),
            ),
            ListTile(
              leading: const Icon(Icons.mic),
              title: const Text('Voice Mode'),
              onTap: () {
                Get.back();
                Get.toNamed('/voice');
              },
            ),
            ListTile(
              leading: const Icon(Icons.psychology_outlined),
              title: const Text('Memory Bank'),
              onTap: () {
                Get.back();
                Get.toNamed('/memory');
              },
            ),
            ListTile(
              leading: const Icon(Icons.check_circle_outline),
              title: const Text('Tasks & Agent'),
              onTap: () {
                Get.back();
                Get.toNamed('/tasks');
              },
            ),
            ListTile(
              leading: const Icon(Icons.settings_outlined),
              title: const Text('Settings & Privacy'),
              onTap: () {
                Get.back();
                Get.toNamed('/settings');
              },
            ),
            ListTile(
              leading: const Icon(Icons.add),
              title: const Text('New Conversation'),
              onTap: () {
                Get.back();
                _chatController.createNewConversation();
              },
            ),
            const Divider(),
            Expanded(
              child: Obx(() {
                if (_chatController.isLoadingConversations.value) {
                  return const Center(child: CircularProgressIndicator());
                }
                return ListView.builder(
                  itemCount: _chatController.conversations.length,
                  itemBuilder: (context, index) {
                    final conv = _chatController.conversations[index];
                    final isSelected = _chatController.currentConversation.value?.id == conv.id;
                    return ListTile(
                      leading: const Icon(Icons.chat_bubble_outline),
                      title: Text(conv.title, maxLines: 1, overflow: TextOverflow.ellipsis),
                      selected: isSelected,
                      onTap: () {
                        Get.back();
                        _chatController.selectConversation(conv);
                      },
                    );
                  },
                );
              }),
            ),
          ],
        ),
      ),
      body: Column(
        children: [
          Expanded(
            child: Obx(() {
              if (_chatController.isLoadingMessages.value) {
                return const Center(child: CircularProgressIndicator());
              }
              if (_chatController.messages.isEmpty) {
                return const Center(
                  child: Text('Start a conversation with ISAI!'),
                );
              }
              return ListView.builder(
                padding: const EdgeInsets.all(16.0),
                itemCount: _chatController.messages.length,
                itemBuilder: (context, index) {
                  final msg = _chatController.messages[index];
                  final isUser = msg.role == 'user';
                  return Align(
                    alignment: isUser ? Alignment.centerRight : Alignment.centerLeft,
                    child: Container(
                      margin: const EdgeInsets.symmetric(vertical: 4.0),
                      padding: const EdgeInsets.all(12.0),
                      constraints: BoxConstraints(
                        maxWidth: MediaQuery.of(context).size.width * 0.8,
                      ),
                      decoration: BoxDecoration(
                        color: isUser ? Colors.blue[700] : Colors.grey[850],
                        borderRadius: BorderRadius.circular(12.0),
                      ),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          MarkdownBody(
                            data: msg.content.isEmpty && msg.isStreaming ? '...' : msg.content,
                            styleSheet: MarkdownStyleSheet(
                              p: const TextStyle(color: Colors.white),
                              code: const TextStyle(
                                backgroundColor: Colors.black45,
                                fontFamily: 'monospace',
                                color: Colors.lightGreenAccent,
                              ),
                            ),
                          ),
                          const SizedBox(height: 4),
                          Row(
                            mainAxisSize: MainAxisSize.min,
                            children: [
                              IconButton(
                                icon: const Icon(Icons.copy_rounded, size: 16, color: Colors.white70),
                                tooltip: 'Copy to Clipboard',
                                onPressed: () {
                                  Clipboard.setData(ClipboardData(text: msg.content));
                                  Get.snackbar('Copied', 'Message copied to clipboard',
                                      snackPosition: SnackPosition.BOTTOM,
                                      duration: const Duration(seconds: 2));
                                },
                              ),
                              if (isUser)
                                IconButton(
                                  icon: const Icon(Icons.refresh_rounded, size: 16, color: Colors.white70),
                                  tooltip: 'Retry',
                                  onPressed: () => _chatController.retryMessage(msg),
                                ),
                            ],
                          )
                        ],
                      ),
                    ),
                  );
                },
              );
            }),
          ),
          Obx(() {
            if (_chatController.isStreaming.value) {
              return Padding(
                padding: const EdgeInsets.symmetric(horizontal: 16.0, vertical: 8.0),
                child: Row(
                  children: [
                    const Expanded(child: LinearProgressIndicator()),
                    const SizedBox(width: 12),
                    ElevatedButton.icon(
                      onPressed: () => _chatController.cancelStreaming(),
                      icon: const Icon(Icons.stop_rounded, size: 18),
                      label: const Text('Cancel'),
                      style: ElevatedButton.styleFrom(backgroundColor: Colors.redAccent),
                    ),
                  ],
                ),
              );
            }
            return const SizedBox.shrink();
          }),
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 8.0, vertical: 8.0),
            color: Theme.of(context).cardColor,
            child: Row(
              children: [
                IconButton(
                  icon: const Icon(Icons.mic_none_rounded, color: Colors.blueAccent),
                  tooltip: 'Voice Input',
                  onPressed: () => Get.toNamed('/voice'),
                ),
                Expanded(
                  child: TextField(
                    controller: _messageController,
                    decoration: const InputDecoration(
                      hintText: 'Type your message...',
                      border: InputBorder.none,
                      contentPadding: EdgeInsets.symmetric(horizontal: 16.0),
                    ),
                    onSubmitted: (val) {
                      _chatController.sendStreamMessage(val);
                      _messageController.clear();
                    },
                  ),
                ),
                Obx(() => IconButton(
                      icon: const Icon(Icons.send_rounded, color: Colors.blueAccent),
                      onPressed: _chatController.isStreaming.value
                          ? null
                          : () {
                              _chatController.sendStreamMessage(_messageController.text);
                              _messageController.clear();
                            },
                    )),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
