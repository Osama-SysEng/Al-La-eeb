import 'package:flutter/material.dart';

class NotificationsScreen extends StatelessWidget {
  const NotificationsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final notifications = [
      {"title": "Match Analysis Complete", "message": "Your match vs Al-Hilal has been analyzed. Rating: 84.2", "time": "2h ago", "read": false, "icon": Icons.analytics, "color": const Color(0xFF00B894)},
      {"title": "New Scout Interest", "message": "A scout from Manchester City viewed your profile", "time": "5h ago", "read": false, "icon": Icons.visibility, "color": const Color(0xFF0984E3)},
      {"title": "Weekly Plan Updated", "message": "Your AI coach has updated your training plan", "time": "1d ago", "read": true, "icon": Icons.fitness_center, "color": const Color(0xFFFD79A8)},
    ];

    return Scaffold(
      appBar: AppBar(
        title: const Text("Notifications"),
        actions: [
          TextButton(onPressed: () {}, child: const Text("Mark All Read", style: TextStyle(color: Color(0xFF00B894)))),
        ],
      ),
      body: ListView.builder(
        padding: const EdgeInsets.all(16),
        itemCount: notifications.length,
        itemBuilder: (context, index) {
          final n = notifications[index];
          return Container(
            margin: const EdgeInsets.only(bottom: 12),
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(
              color: const Color(0xFF1D1F33),
              borderRadius: BorderRadius.circular(16),
              border: !(n["read"] as bool) ? Border.all(color: const Color(0xFF00B894), width: 1) : null,
            ),
            child: Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Container(
                  padding: const EdgeInsets.all(10),
                  decoration: BoxDecoration(color: (n["color"] as Color).withOpacity(0.2), borderRadius: BorderRadius.circular(12)),
                  child: Icon(n["icon"] as IconData, color: n["color"] as Color, size: 20),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        children: [
                          Expanded(child: Text(n["title"] as String, style: const TextStyle(color: Colors.white, fontWeight: FontWeight.w600))),
                          if (!(n["read"] as bool))
                            Container(width: 8, height: 8, decoration: const BoxDecoration(color: Color(0xFF00B894), shape: BoxShape.circle)),
                        ],
                      ),
                      const SizedBox(height: 4),
                      Text(n["message"] as String, style: const TextStyle(color: Colors.white70, fontSize: 13)),
                      const SizedBox(height: 8),
                      Text(n["time"] as String, style: const TextStyle(color: Colors.white38, fontSize: 11)),
                    ],
                  ),
                ),
              ],
            ),
          );
        },
      ),
    );
  }
}
