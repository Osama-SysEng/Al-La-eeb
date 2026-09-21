import 'package:flutter/material.dart';

class CoachChatScreen extends StatefulWidget {
  const CoachChatScreen({super.key});

  @override
  State<CoachChatScreen> createState() => _CoachChatScreenState();
}

class _CoachChatScreenState extends State<CoachChatScreen> {
  final _controller = TextEditingController();
  final List<Map<String, dynamic>> _messages = [
    {
      "isUser": false,
      "text": "مرحباً! أنا مدربك الافتراضي. كيف يمكنني مساعدتك في تحسين أدائك اليوم؟",
      "time": "14:30"
    },
    {
      "isUser": true,
      "text": "How can I improve my shooting power?",
      "time": "14:31"
    },
    {
      "isUser": false,
      "text": "To improve your shooting power, focus on:

1. Hip rotation through the shot
2. Plant foot positioning (shoulder-width)
3. Follow-through towards target
4. Core strength training

Try drill DR-001 3x per week. Your current shot power is 87 km/h - target is 95+ km/h for professional level.",
      "time": "14:31"
    },
  ];

  void _sendMessage() {
    if (_controller.text.isEmpty) return;
    setState(() {
      _messages.add({"isUser": true, "text": _controller.text, "time": "14:32"});
      _messages.add({
        "isUser": false,
        "text": "That's a great question! Based on your recent match analysis, I recommend focusing on that specific area. Check your weekly plan for the relevant drills.",
        "time": "14:32"
      });
    });
    _controller.clear();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Row(
          children: [
            CircleAvatar(
              backgroundColor: Color(0xFF00B894),
              child: Icon(Icons.sports, color: Colors.white),
            ),
            SizedBox(width: 12),
            Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text("AI Coach", style: TextStyle(fontSize: 16)),
                Text("Online", style: TextStyle(fontSize: 12, color: Color(0xFF00B894))),
              ],
            ),
          ],
        ),
      ),
      body: Column(
        children: [
          Expanded(
            child: ListView.builder(
              padding: const EdgeInsets.all(16),
              itemCount: _messages.length,
              itemBuilder: (context, index) {
                final msg = _messages[index];
                return Align(
                  alignment: msg["isUser"] ? Alignment.centerRight : Alignment.centerLeft,
                  child: Container(
                    margin: const EdgeInsets.only(bottom: 12),
                    padding: const EdgeInsets.all(12),
                    constraints: BoxConstraints(maxWidth: MediaQuery.of(context).size.width * 0.75),
                    decoration: BoxDecoration(
                      color: msg["isUser"] ? const Color(0xFF00B894) : const Color(0xFF1D1F33),
                      borderRadius: BorderRadius.circular(16),
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(msg["text"], style: const TextStyle(color: Colors.white)),
                        const SizedBox(height: 4),
                        Text(msg["time"], style: const TextStyle(color: Colors.white38, fontSize: 10)),
                      ],
                    ),
                  ),
                );
              },
            ),
          ),
          Container(
            padding: const EdgeInsets.all(12),
            color: const Color(0xFF1D1F33),
            child: Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _controller,
                    style: const TextStyle(color: Colors.white),
                    decoration: InputDecoration(
                      hintText: "Ask your coach...",
                      hintStyle: const TextStyle(color: Colors.white38),
                      filled: true,
                      fillColor: const Color(0xFF0A0E21),
                      border: OutlineInputBorder(borderRadius: BorderRadius.circular(24), borderSide: BorderSide.none),
                      contentPadding: const EdgeInsets.symmetric(horizontal: 20, vertical: 14),
                    ),
                  ),
                ),
                const SizedBox(width: 8),
                CircleAvatar(
                  backgroundColor: const Color(0xFF00B894),
                  child: IconButton(
                    icon: const Icon(Icons.send, color: Colors.white, size: 20),
                    onPressed: _sendMessage,
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
