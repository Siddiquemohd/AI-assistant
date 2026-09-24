import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_markdown/flutter_markdown.dart';
import 'package:get/get.dart';
import '../../../core/theme/app_theme.dart';
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
      backgroundColor: AppTheme.darkBackground,
      appBar: AppBar(
        backgroundColor: const Color(0xFF0F172A),
        elevation: 0,
        title: Column(
          children: [
            Obx(() => Text(
                  _chatController.currentConversation.value?.title ?? 'ISAI Super-AI',
                  style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16),
                )),
            const SizedBox(height: 2),
            Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                Container(
                  width: 8,
                  height: 8,
                  decoration: const BoxDecoration(
                    color: AppTheme.accentEmerald,
                    shape: BoxShape.circle,
                  ),
                ),
                const SizedBox(width: 6),
                const Text(
                  '25 ENGINES ONLINE • 100% UNCENSORED',
                  style: TextStyle(
                    fontSize: 10,
                    fontWeight: FontWeight.w600,
                    color: AppTheme.accentEmerald,
                    letterSpacing: 0.8,
                  ),
                ),
              ],
            ),
          ],
        ),
        actions: [
          IconButton(
            icon: Container(
              padding: const EdgeInsets.all(6),
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                color: AppTheme.primaryNeon.withValues(alpha: 0.15),
              ),
              child: const Icon(Icons.mic_rounded, color: AppTheme.primaryNeon, size: 20),
            ),
            tooltip: 'Voice Assistant',
            onPressed: () => Get.toNamed('/voice'),
          ),
          IconButton(
            icon: const Icon(Icons.add_comment_outlined, color: Colors.white70),
            tooltip: 'New Chat',
            onPressed: () => _chatController.createNewConversation(),
          ),
        ],
      ),
      drawer: _buildFuturisticDrawer(context),
      body: Column(
        children: [
          Expanded(
            child: Obx(() {
              if (_chatController.isLoadingMessages.value) {
                return const Center(
                  child: CircularProgressIndicator(color: AppTheme.primaryNeon),
                );
              }
              if (_chatController.messages.isEmpty) {
                return _buildEmptyStateHero(context);
              }
              return ListView.builder(
                padding: const EdgeInsets.symmetric(horizontal: 16.0, vertical: 12.0),
                itemCount: _chatController.messages.length,
                itemBuilder: (context, index) {
                  final msg = _chatController.messages[index];
                  final isUser = msg.role == 'user';
                  return _buildMessageBubble(context, msg, isUser);
                },
              );
            }),
          ),
          Obx(() {
            if (_chatController.isStreaming.value) {
              return Container(
                padding: const EdgeInsets.symmetric(horizontal: 16.0, vertical: 6.0),
                color: AppTheme.cardBackground,
                child: Row(
                  children: [
                    const Expanded(
                      child: LinearProgressIndicator(
                        backgroundColor: Color(0xFF1E293B),
                        color: AppTheme.primaryNeon,
                      ),
                    ),
                    const SizedBox(width: 12),
                    TextButton.icon(
                      onPressed: () => _chatController.cancelStreaming(),
                      icon: const Icon(Icons.stop_circle_outlined, size: 16, color: Colors.redAccent),
                      label: const Text('Stop', style: TextStyle(color: Colors.redAccent, fontSize: 12)),
                    ),
                  ],
                ),
              );
            }
            return const SizedBox.shrink();
          }),
          _buildInputDock(context),
        ],
      ),
    );
  }

  Widget _buildEmptyStateHero(BuildContext context) {
    final quickPrompts = [
      {'title': '🎨 Uncensored Image Gen', 'prompt': 'Generate uncensored cyberpunk artwork of a futuristic metropolis'},
      {'title': '🎙️ 10 Female Neural Voices', 'prompt': 'Speak to me in Aria female neural voice'},
      {'title': '🛠️ Code Debugger & Refactor', 'prompt': 'Debug code def process(data): eval(data)'},
      {'title': '📈 Market & Crypto Analytics', 'prompt': 'Analyze BTC cryptocurrency market metrics'},
      {'title': '🎯 Autonomous Agent Planner', 'prompt': 'Plan goal Build a 25 engine personal AI model'},
      {'title': '🧮 Symbolic Math Solver', 'prompt': 'Solve derivative of x^3 * sin(x)'},
    ];

    return SingleChildScrollView(
      padding: const EdgeInsets.all(24.0),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          const SizedBox(height: 20),
          Container(
            width: 80,
            height: 80,
            decoration: BoxDecoration(
              shape: BoxShape.circle,
              gradient: AppTheme.primaryGradient,
              boxShadow: [
                BoxShadow(
                  color: AppTheme.primaryNeon.withValues(alpha: 0.5),
                  blurRadius: 24,
                  spreadRadius: 4,
                ),
              ],
            ),
            child: const Icon(Icons.smart_toy_rounded, size: 48, color: Colors.black),
          ),
          const SizedBox(height: 16),
          const Text(
            'Welcome to ISAI AI',
            style: TextStyle(
              fontSize: 22,
              fontWeight: FontWeight.bold,
              color: Colors.white,
            ),
          ),
          const SizedBox(height: 6),
          const Text(
            'Your 25-Engine Uncensored Multimodal AI Assistant',
            style: TextStyle(fontSize: 13, color: AppTheme.slate),
          ),
          const SizedBox(height: 32),
          const Align(
            alignment: Alignment.centerLeft,
            child: Text(
              'QUICK SUGGESTIONS',
              style: TextStyle(
                fontSize: 11,
                fontWeight: FontWeight.bold,
                letterSpacing: 1.2,
                color: AppTheme.primaryNeon,
              ),
            ),
          ),
          const SizedBox(height: 12),
          GridView.builder(
            shrinkWrap: true,
            physics: const NeverScrollableScrollPhysics(),
            gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
              crossAxisCount: 2,
              childAspectRatio: 2.2,
              crossAxisSpacing: 12,
              mainAxisSpacing: 12,
            ),
            itemCount: quickPrompts.length,
            itemBuilder: (context, index) {
              final item = quickPrompts[index];
              return InkWell(
                onTap: () {
                  _messageController.text = item['prompt']!;
                  _chatController.sendStreamMessage(item['prompt']!);
                  _messageController.clear();
                },
                borderRadius: BorderRadius.circular(16),
                child: Container(
                  padding: const EdgeInsets.all(12),
                  decoration: BoxDecoration(
                    color: AppTheme.cardBackground,
                    borderRadius: BorderRadius.circular(16),
                    border: Border.all(color: AppTheme.cardBorder),
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Text(
                        item['title']!,
                        style: const TextStyle(
                          fontSize: 12,
                          fontWeight: FontWeight.bold,
                          color: Colors.white,
                        ),
                        maxLines: 1,
                        overflow: TextOverflow.ellipsis,
                      ),
                      const SizedBox(height: 4),
                      Text(
                        item['prompt']!,
                        style: const TextStyle(fontSize: 10, color: AppTheme.slate),
                        maxLines: 2,
                        overflow: TextOverflow.ellipsis,
                      ),
                    ],
                  ),
                ),
              );
            },
          ),
        ],
      ),
    );
  }

  Widget _buildMessageBubble(BuildContext context, dynamic msg, bool isUser) {
    return Align(
      alignment: isUser ? Alignment.centerRight : Alignment.centerLeft,
      child: Container(
        margin: const EdgeInsets.symmetric(vertical: 6.0),
        constraints: BoxConstraints(
          maxWidth: MediaQuery.of(context).size.width * 0.85,
        ),
        decoration: BoxDecoration(
          gradient: isUser ? AppTheme.purpleGradient : null,
          color: isUser ? null : AppTheme.cardBackground,
          borderRadius: BorderRadius.only(
            topLeft: const Radius.circular(20),
            topRight: const Radius.circular(20),
            bottomLeft: Radius.circular(isUser ? 20 : 4),
            bottomRight: Radius.circular(isUser ? 4 : 20),
          ),
          border: isUser ? null : Border.all(color: AppTheme.cardBorder),
          boxShadow: [
            BoxShadow(
              color: Colors.black.withValues(alpha: 0.25),
              blurRadius: 10,
              offset: const Offset(0, 4),
            ),
          ],
        ),
        padding: const EdgeInsets.all(14.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                Icon(
                  isUser ? Icons.person_rounded : Icons.smart_toy_rounded,
                  size: 14,
                  color: isUser ? Colors.white70 : AppTheme.primaryNeon,
                ),
                const SizedBox(width: 6),
                Text(
                  isUser ? 'You' : 'ISAI Assistant',
                  style: TextStyle(
                    fontSize: 11,
                    fontWeight: FontWeight.bold,
                    color: isUser ? Colors.white70 : AppTheme.primaryNeon,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 8),
            MarkdownBody(
              data: msg.content.isEmpty && msg.isStreaming ? '...' : msg.content,
              styleSheet: MarkdownStyleSheet(
                p: const TextStyle(color: Colors.white, fontSize: 14, height: 1.4),
                code: const TextStyle(
                  backgroundColor: Color(0xFF0F172A),
                  fontFamily: 'monospace',
                  color: Color(0xFF4ADE80),
                  fontSize: 12,
                ),
                codeblockPadding: const EdgeInsets.all(12),
                codeblockDecoration: BoxDecoration(
                  color: const Color(0xFF0F172A),
                  borderRadius: BorderRadius.circular(12),
                  border: Border.all(color: const Color(0xFF1E293B)),
                ),
              ),
            ),
            const SizedBox(height: 8),
            Row(
              mainAxisAlignment: MainAxisAlignment.end,
              mainAxisSize: MainAxisSize.min,
              children: [
                InkWell(
                  onTap: () {
                    Clipboard.setData(ClipboardData(text: msg.content));
                    Get.snackbar(
                      'Copied',
                      'Text copied to clipboard',
                      snackPosition: SnackPosition.BOTTOM,
                      backgroundColor: AppTheme.cardBackground,
                      colorText: Colors.white,
                      duration: const Duration(seconds: 2),
                    );
                  },
                  child: const Padding(
                    padding: EdgeInsets.all(4.0),
                    child: Icon(Icons.copy_rounded, size: 14, color: AppTheme.slate),
                  ),
                ),
                if (isUser)
                  InkWell(
                    onTap: () => _chatController.retryMessage(msg),
                    child: const Padding(
                      padding: EdgeInsets.all(4.0),
                      child: Icon(Icons.refresh_rounded, size: 14, color: AppTheme.slate),
                    ),
                  ),
              ],
            )
          ],
        ),
      ),
    );
  }

  Widget _buildInputDock(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 12.0, vertical: 10.0),
      decoration: const BoxDecoration(
        color: Color(0xFF0F172A),
        border: Border(top: BorderSide(color: AppTheme.cardBorder)),
      ),
      child: SafeArea(
        child: Row(
          children: [
            IconButton(
              icon: const Icon(Icons.mic_none_rounded, color: AppTheme.primaryNeon),
              tooltip: 'Voice Input',
              onPressed: () => Get.toNamed('/voice'),
            ),
            Expanded(
              child: Container(
                decoration: BoxDecoration(
                  color: AppTheme.inputBackground,
                  borderRadius: BorderRadius.circular(24),
                  border: Border.all(color: AppTheme.cardBorder),
                ),
                child: TextField(
                  controller: _messageController,
                  style: const TextStyle(color: Colors.white, fontSize: 14),
                  decoration: const InputDecoration(
                    hintText: 'Ask ISAI anything...',
                    border: InputBorder.none,
                    enabledBorder: InputBorder.none,
                    focusedBorder: InputBorder.none,
                    contentPadding: EdgeInsets.symmetric(horizontal: 16.0, vertical: 12.0),
                  ),
                  onSubmitted: (val) {
                    if (val.trim().isNotEmpty) {
                      _chatController.sendStreamMessage(val.trim());
                      _messageController.clear();
                    }
                  },
                ),
              ),
            ),
            const SizedBox(width: 8),
            Obx(() => Container(
                  decoration: const BoxDecoration(
                    gradient: AppTheme.primaryGradient,
                    shape: BoxShape.circle,
                  ),
                  child: IconButton(
                    icon: const Icon(Icons.send_rounded, color: Colors.black, size: 20),
                    onPressed: _chatController.isStreaming.value
                        ? null
                        : () {
                            final text = _messageController.text.trim();
                            if (text.isNotEmpty) {
                              _chatController.sendStreamMessage(text);
                              _messageController.clear();
                            }
                          },
                  ),
                )),
          ],
        ),
      ),
    );
  }

  Widget _buildFuturisticDrawer(BuildContext context) {
    return Drawer(
      backgroundColor: const Color(0xFF0F172A),
      child: Column(
        children: [
          UserAccountsDrawerHeader(
            decoration: const BoxDecoration(
              gradient: LinearGradient(
                colors: [Color(0xFF1E1B4B), Color(0xFF0F172A)],
              ),
            ),
            accountName: Obx(() => Text(
                  _authController.userDisplayName.value,
                  style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16),
                )),
            accountEmail: Obx(() => Text(
                  _authController.userEmail.value,
                  style: const TextStyle(color: AppTheme.slate, fontSize: 12),
                )),
            currentAccountPicture: Container(
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                gradient: AppTheme.primaryGradient,
                boxShadow: [
                  BoxShadow(
                    color: AppTheme.primaryNeon.withValues(alpha: 0.4),
                    blurRadius: 12,
                  )
                ],
              ),
              child: const Icon(Icons.smart_toy_rounded, size: 36, color: Colors.black),
            ),
          ),
          ListTile(
            leading: const Icon(Icons.mic_rounded, color: AppTheme.primaryNeon),
            title: const Text('Voice Mode (10 Voices)', style: TextStyle(color: Colors.white)),
            onTap: () {
              Get.back();
              Get.toNamed('/voice');
            },
          ),
          ListTile(
            leading: const Icon(Icons.psychology_outlined, color: AppTheme.secondaryNeon),
            title: const Text('Memory Bank & Triples', style: TextStyle(color: Colors.white)),
            onTap: () {
              Get.back();
              Get.toNamed('/memory');
            },
          ),
          ListTile(
            leading: const Icon(Icons.task_alt_rounded, color: AppTheme.accentEmerald),
            title: const Text('Tasks & Autonomous Agent', style: TextStyle(color: Colors.white)),
            onTap: () {
              Get.back();
              Get.toNamed('/tasks');
            },
          ),
          ListTile(
            leading: const Icon(Icons.settings_outlined, color: AppTheme.slate),
            title: const Text('Settings & 25-Engine Info', style: TextStyle(color: Colors.white)),
            onTap: () {
              Get.back();
              Get.toNamed('/settings');
            },
          ),
          const Divider(color: AppTheme.cardBorder),
          ListTile(
            leading: const Icon(Icons.add_circle_outline, color: AppTheme.primaryNeon),
            title: const Text('New Conversation', style: TextStyle(color: AppTheme.primaryNeon, fontWeight: FontWeight.bold)),
            onTap: () {
              Get.back();
              _chatController.createNewConversation();
            },
          ),
          const Divider(color: AppTheme.cardBorder),
          Expanded(
            child: Obx(() {
              if (_chatController.isLoadingConversations.value) {
                return const Center(child: CircularProgressIndicator(color: AppTheme.primaryNeon));
              }
              return ListView.builder(
                itemCount: _chatController.conversations.length,
                itemBuilder: (context, index) {
                  final conv = _chatController.conversations[index];
                  final isSelected = _chatController.currentConversation.value?.id == conv.id;
                  return ListTile(
                    leading: Icon(
                      Icons.chat_bubble_outline_rounded,
                      color: isSelected ? AppTheme.primaryNeon : AppTheme.slate,
                      size: 18,
                    ),
                    title: Text(
                      conv.title,
                      maxLines: 1,
                      overflow: TextOverflow.ellipsis,
                      style: TextStyle(
                        color: isSelected ? Colors.white : AppTheme.slate,
                        fontWeight: isSelected ? FontWeight.bold : FontWeight.normal,
                      ),
                    ),
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
          ListTile(
            leading: const Icon(Icons.logout_rounded, color: Colors.redAccent),
            title: const Text('Sign Out', style: TextStyle(color: Colors.redAccent)),
            onTap: () => _authController.logout(),
          ),
        ],
      ),
    );
  }
}
