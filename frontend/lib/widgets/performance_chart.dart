import 'package:flutter/material.dart';
import 'package:fl_chart/fl_chart.dart';

class PerformanceChart extends StatelessWidget {
  const PerformanceChart({super.key});

  @override
  Widget build(BuildContext context) {
    return Container(
      height: 200,
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: const Color(0xFF1D1F33),
        borderRadius: BorderRadius.circular(16),
      ),
      child: LineChart(
        LineChartData(
          gridData: FlGridData(show: true, drawVerticalLine: false, horizontalInterval: 10, getDrawingHorizontalLine: (value) {
            return FlLine(color: Colors.white10, strokeWidth: 1);
          }),
          titlesData: FlTitlesData(
            leftTitles: AxisTitles(sideTitles: SideTitles(showTitles: true, interval: 20, getTitlesWidget: (value, meta) {
              return Text(value.toInt().toString(), style: const TextStyle(color: Colors.white38, fontSize: 10));
            })),
            bottomTitles: AxisTitles(sideTitles: SideTitles(showTitles: true, getTitlesWidget: (value, meta) {
              const labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'];
              if (value.toInt() < labels.length) {
                return Text(labels[value.toInt()], style: const TextStyle(color: Colors.white38, fontSize: 10));
              }
              return const Text('');
            })),
            rightTitles: AxisTitles(sideTitles: SideTitles(showTitles: false)),
            topTitles: AxisTitles(sideTitles: SideTitles(showTitles: false)),
          ),
          borderData: FlBorderData(show: false),
          minX: 0,
          maxX: 5,
          minY: 60,
          maxY: 100,
          lineBarsData: [
            LineChartBarData(
              spots: const [
                FlSpot(0, 72),
                FlSpot(1, 74),
                FlSpot(2, 73),
                FlSpot(3, 76),
                FlSpot(4, 78),
                FlSpot(5, 78.5),
              ],
              isCurved: true,
              color: const Color(0xFF00B894),
              barWidth: 3,
              isStrokeCapRound: true,
              dotData: FlDotData(show: true, getDotPainter: (spot, percent, bar, index) {
                return FlDotCirclePainter(radius: 4, color: const Color(0xFF00B894), strokeWidth: 2, strokeColor: Colors.white);
              }),
              belowBarData: BarAreaData(
                show: true,
                color: const Color(0xFF00B894).withOpacity(0.1),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
