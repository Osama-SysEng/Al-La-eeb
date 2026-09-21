import 'package:flutter/material.dart';

class ProfileScreen extends StatelessWidget {
  const ProfileScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("My Profile")),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            const CircleAvatar(radius: 50, backgroundColor: Color(0xFF00B894), child: Icon(Icons.person, size: 50, color: Colors.white)),
            const SizedBox(height: 16),
            const Text("Ahmed Al-Rashid", style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold, color: Colors.white)),
            const Text("Midfielder - Al-Ahli FC", style: TextStyle(color: Colors.white70)),
            const SizedBox(height: 24),
            _buildStatRow("Age", "17 years"),
            _buildStatRow("Height", "182 cm"),
            _buildStatRow("Weight", "78 kg"),
            _buildStatRow("Dominant Foot", "Right"),
            _buildStatRow("Jersey Number", "#10"),
            _buildStatRow("Nationality", "UAE"),
            const SizedBox(height: 24),
            const Text("Achievements", style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.white)),
            const SizedBox(height: 12),
            _buildAchievement("U-17 National Champion 2024", Icons.emoji_events, const Color(0xFFFFD700)),
            _buildAchievement("Best Midfielder - Youth League", Icons.star, const Color(0xFF00B894)),
            const SizedBox(height: 24),
            ElevatedButton.icon(
              onPressed: () {},
              icon: const Icon(Icons.edit),
              label: const Text("Edit Profile"),
              style: ElevatedButton.styleFrom(minimumSize: const Size(double.infinity, 50)),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildStatRow(String label, String value) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text(label, style: const TextStyle(color: Colors.white70)),
          Text(value, style: const TextStyle(color: Colors.white, fontWeight: FontWeight.w600)),
        ],
      ),
    );
  }

  Widget _buildAchievement(String title, IconData icon, Color color) {
    return Container(
      margin: const EdgeInsets.only(bottom: 8),
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(color: const Color(0xFF1D1F33), borderRadius: BorderRadius.circular(12)),
      child: Row(
        children: [
          Icon(icon, color: color),
          const SizedBox(width: 12),
          Expanded(child: Text(title, style: const TextStyle(color: Colors.white))),
        ],
      ),
    );
  }
}
