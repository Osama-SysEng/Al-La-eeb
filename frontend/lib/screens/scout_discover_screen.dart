import 'package:flutter/material.dart';

class ScoutDiscoverScreen extends StatelessWidget {
  const ScoutDiscoverScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Discover Talent"),
        actions: [
          IconButton(icon: const Icon(Icons.filter_list), onPressed: () {}),
        ],
      ),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          _buildPlayerCard("Omar Al-Farsi", 17, "CM", 81.2, "UAE", "Al-Ain FC", 0.92),
          _buildPlayerCard("Khalid Al-Mansouri", 16, "ST", 76.8, "Saudi Arabia", "Al-Hilal Youth", 0.87),
          _buildPlayerCard("Youssef Benali", 18, "RW", 79.3, "Morocco", "Wydad AC", 0.84),
          _buildPlayerCard("Ahmed Hassan", 17, "CB", 74.5, "Egypt", "Zamalek SC", 0.81),
        ],
      ),
    );
  }

  Widget _buildPlayerCard(String name, int age, String position, double rating, String country, String club, double similarity) {
    return Card(
      color: const Color(0xFF1D1F33),
      margin: const EdgeInsets.only(bottom: 12),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Row(
          children: [
            CircleAvatar(
              radius: 30,
              backgroundColor: const Color(0xFF00B894),
              child: Text(position, style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
            ),
            const SizedBox(width: 16),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(name, style: const TextStyle(color: Colors.white, fontSize: 18, fontWeight: FontWeight.bold)),
                  const SizedBox(height: 4),
                  Text("$age years • $country • $club", style: const TextStyle(color: Colors.white70)),
                  const SizedBox(height: 8),
                  Row(
                    children: [
                      Container(
                        padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                        decoration: BoxDecoration(color: const Color(0xFF00B894), borderRadius: BorderRadius.circular(8)),
                        child: Text("$rating", style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
                      ),
                      const SizedBox(width: 8),
                      Container(
                        padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                        decoration: BoxDecoration(color: const Color(0xFF0984E3), borderRadius: BorderRadius.circular(8)),
                        child: Text("${(similarity * 100).toInt()}% match", style: const TextStyle(color: Colors.white, fontSize: 12)),
                      ),
                    ],
                  ),
                ],
              ),
            ),
            IconButton(
              icon: const Icon(Icons.favorite_border, color: Colors.white70),
              onPressed: () {},
            ),
          ],
        ),
      ),
    );
  }
}
