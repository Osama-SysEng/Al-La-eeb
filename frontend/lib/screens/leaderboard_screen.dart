import 'package:flutter/material.dart';

class LeaderboardScreen extends StatelessWidget {
  const LeaderboardScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final players = [
      {"rank": 1, "name": "Omar Al-Farsi", "country": "UAE", "score": 89.5, "club": "Al-Ain", "trend": "up"},
      {"rank": 2, "name": "Khalid Al-Mansouri", "country": "KSA", "score": 88.1, "club": "Al-Hilal", "trend": "up"},
      {"rank": 3, "name": "Youssef Benali", "country": "MAR", "score": 87.2, "club": "Wydad", "trend": "same"},
      {"rank": 4, "name": "Ahmed Hassan", "country": "EGY", "score": 85.3, "club": "Zamalek", "trend": "down"},
      {"rank": 5, "name": "Faisal Al-Rashid", "country": "QAT", "score": 84.9, "club": "Al-Sadd", "trend": "up"},
    ];

    return Scaffold(
      appBar: AppBar(title: const Text("Leaderboard")),
      body: ListView.builder(
        padding: const EdgeInsets.all(16),
        itemCount: players.length,
        itemBuilder: (context, index) {
          final p = players[index];
          final isTop3 = (p["rank"] as int) <= 3;
          return Container(
            margin: const EdgeInsets.only(bottom: 12),
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(
              color: const Color(0xFF1D1F33),
              borderRadius: BorderRadius.circular(16),
              border: isTop3 ? Border.all(color: const Color(0xFF00B894), width: 2) : null,
            ),
            child: Row(
              children: [
                Container(
                  width: 40,
                  height: 40,
                  decoration: BoxDecoration(
                    color: isTop3 ? const Color(0xFF00B894) : const Color(0xFF2D2F45),
                    borderRadius: BorderRadius.circular(12),
                  ),
                  child: Center(
                    child: Text(
                      "${p["rank"]}",
                      style: TextStyle(
                        color: isTop3 ? Colors.white : Colors.white70,
                        fontWeight: FontWeight.bold,
                        fontSize: 18,
                      ),
                    ),
                  ),
                ),
                const SizedBox(width: 16),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(p["name"] as String, style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
                      Text("${p["country"]} - ${p["club"]}", style: const TextStyle(color: Colors.white54, fontSize: 12)),
                    ],
                  ),
                ),
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                  decoration: BoxDecoration(
                    color: const Color(0xFF00B894).withOpacity(0.2),
                    borderRadius: BorderRadius.circular(20),
                  ),
                  child: Text("${p["score"]}", style: const TextStyle(color: Color(0xFF00B894), fontWeight: FontWeight.bold)),
                ),
              ],
            ),
          );
        },
      ),
    );
  }
}
