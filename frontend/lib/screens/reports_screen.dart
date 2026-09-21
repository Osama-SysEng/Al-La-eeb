import 'package:flutter/material.dart';
import '../widgets/metric_card.dart';

class ReportsScreen extends StatelessWidget {
  const ReportsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Performance Reports")),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          _buildReportCard(
            "Match vs Al-Hilal",
            "2024-07-28",
            84.2,
            ["Excellent passing", "Great vision", "Needs more shots"],
          ),
          _buildReportCard(
            "Match vs Al-Nassr",
            "2024-07-21",
            81.5,
            ["Strong defensive work", "Good positioning", "Improve aerial duels"],
          ),
          _buildReportCard(
            "Training Session",
            "2024-07-18",
            79.8,
            ["High intensity", "Good technique", "Focus on finishing"],
          ),
        ],
      ),
    );
  }

  Widget _buildReportCard(String title, String date, double rating, List<String> notes) {
    return Card(
      color: const Color(0xFF1D1F33),
      margin: const EdgeInsets.only(bottom: 12),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(title, style: const TextStyle(color: Colors.white, fontSize: 18, fontWeight: FontWeight.bold)),
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                  decoration: BoxDecoration(
                    color: rating >= 80 ? const Color(0xFF00B894) : const Color(0xFF0984E3),
                    borderRadius: BorderRadius.circular(20),
                  ),
                  child: Text(rating.toString(), style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
                ),
              ],
            ),
            const SizedBox(height: 4),
            Text(date, style: const TextStyle(color: Colors.white38)),
            const SizedBox(height: 12),
            ...notes.map((note) => Padding(
              padding: const EdgeInsets.only(bottom: 4),
              child: Row(
                children: [
                  const Icon(Icons.check_circle, size: 16, color: Color(0xFF00B894)),
                  const SizedBox(width: 8),
                  Expanded(child: Text(note, style: const TextStyle(color: Colors.white70))),
                ],
              ),
            )),
            const SizedBox(height: 12),
            ElevatedButton(
              onPressed: () {},
              style: ElevatedButton.styleFrom(backgroundColor: const Color(0xFF1D1F33), side: const BorderSide(color: Color(0xFF00B894))),
              child: const Text("View Full Report"),
            ),
          ],
        ),
      ),
    );
  }
}
