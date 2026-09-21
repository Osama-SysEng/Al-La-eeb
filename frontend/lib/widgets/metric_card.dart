import 'package:flutter/material.dart';

class MetricCard extends StatelessWidget {
  final String title;
  final String value;
  final String unit;
  final IconData icon;
  final Color color;
  final String? trend;

  const MetricCard({super.key, required this.title, required this.value, required this.unit, required this.icon, required this.color, this.trend});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: const Color(0xFF1D1F33),
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: color.withOpacity(0.3), width: 1),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(children: [Icon(icon, color: color, size: 20), const SizedBox(width: 8), Expanded(child: Text(title, style: const TextStyle(color: Colors.white70, fontSize: 12)))]),
          const Spacer(),
          Row(crossAxisAlignment: CrossAxisAlignment.end, children: [Text(value, style: TextStyle(color: color, fontSize: 28, fontWeight: FontWeight.bold)), const SizedBox(width: 4), Text(unit, style: const TextStyle(color: Colors.white38, fontSize: 12))]),
          if (trend != null)
            Padding(padding: const EdgeInsets.only(top: 4), child: Row(children: [const Icon(Icons.trending_up, color: Color(0xFF00B894), size: 14), const SizedBox(width: 4), Text(trend!, style: const TextStyle(color: Color(0xFF00B894), fontSize: 12))])),
        ],
      ),
    );
  }
}
