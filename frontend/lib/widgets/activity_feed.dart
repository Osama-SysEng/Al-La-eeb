import 'package:flutter/material.dart';

class ActivityFeed extends StatelessWidget {
  const ActivityFeed({super.key});

  @override
  Widget build(BuildContext context) {
    final activities = [
      {"icon": Icons.videocam, "color": const Color(0xFF00B894), "title": "Match analyzed", "subtitle": "vs Al-Hilal - Rating: 84.2", "time": "2h ago"},
      {"icon": Icons.trending_up, "color": const Color(0xFF0984E3), "title": "New milestone", "subtitle": "1000 passes completed", "time": "5h ago"},
      {"icon": Icons.chat, "color": const Color(0xFFFD79A8), "title": "Coach feedback", "subtitle": "New drill recommendations available", "time": "1d ago"},
      {"icon": Icons.favorite, "color": const Color(0xFFFF6B6B), "title": "Scout interest", "subtitle": "3 scouts viewed your profile", "time": "2d ago"},
    ];

    return Column(
      children: activities.map((a) => _buildActivityItem(a)).toList(),
    );
  }

  Widget _buildActivityItem(Map<String, dynamic> activity) {
    return Container(
      margin: const EdgeInsets.only(bottom: 12),
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: const Color(0xFF1D1F33),
        borderRadius: BorderRadius.circular(12),
      ),
      child: Row(
        children: [
          Container(
            padding: const EdgeInsets.all(10),
            decoration: BoxDecoration(
              color: (activity["color"] as Color).withOpacity(0.2),
              borderRadius: BorderRadius.circular(12),
            ),
            child: Icon(activity["icon"] as IconData, color: activity["color"] as Color, size: 20),
          ),
          const SizedBox(width: 12),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(activity["title"] as String, style: const TextStyle(color: Colors.white, fontWeight: FontWeight.w600)),
                Text(activity["subtitle"] as String, style: const TextStyle(color: Colors.white54, fontSize: 12)),
              ],
            ),
          ),
          Text(activity["time"] as String, style: const TextStyle(color: Colors.white38, fontSize: 11)),
        ],
      ),
    );
  }
}
