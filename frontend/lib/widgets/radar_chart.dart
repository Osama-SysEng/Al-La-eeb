import 'package:flutter/material.dart';
import 'dart:math';

class RadarChartWidget extends StatelessWidget {
  const RadarChartWidget({super.key});

  @override
  Widget build(BuildContext context) {
    return Container(
      height: 250,
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: const Color(0xFF1D1F33),
        borderRadius: BorderRadius.circular(16),
      ),
      child: CustomPaint(
        size: const Size(double.infinity, 200),
        painter: RadarChartPainter(),
      ),
    );
  }
}

class RadarChartPainter extends CustomPainter {
  @override
  void paint(Canvas canvas, Size size) {
    final center = Offset(size.width / 2, size.height / 2);
    final radius = min(size.width, size.height) / 2 - 30;
    final labels = ["Speed", "Passing", "Shooting", "Defense", "Physical", "Tactical"];
    final values = [0.85, 0.91, 0.76, 0.78, 0.79, 0.82];

    final gridPaint = Paint()
      ..color = Colors.white12
      ..style = PaintingStyle.stroke
      ..strokeWidth = 1;

    for (int i = 1; i <= 5; i++) {
      final r = radius * i / 5;
      final path = Path();
      for (int j = 0; j < 6; j++) {
        final angle = (2 * pi * j / 6) - pi / 2;
        final x = center.dx + r * cos(angle);
        final y = center.dy + r * sin(angle);
        if (j == 0) path.moveTo(x, y);
        else path.lineTo(x, y);
      }
      path.close();
      canvas.drawPath(path, gridPaint);
    }

    final axisPaint = Paint()
      ..color = Colors.white24
      ..strokeWidth = 1;

    for (int i = 0; i < 6; i++) {
      final angle = (2 * pi * i / 6) - pi / 2;
      final x = center.dx + radius * cos(angle);
      final y = center.dy + radius * sin(angle);
      canvas.drawLine(center, Offset(x, y), axisPaint);
      final labelX = center.dx + (radius + 20) * cos(angle);
      final labelY = center.dy + (radius + 20) * sin(angle);
      final textPainter = TextPainter(
        text: TextSpan(text: labels[i], style: const TextStyle(color: Colors.white70, fontSize: 10)),
        textDirection: TextDirection.ltr,
        textAlign: TextAlign.center,
      );
      textPainter.layout();
      textPainter.paint(canvas, Offset(labelX - textPainter.width / 2, labelY - textPainter.height / 2));
    }

    final dataPaint = Paint()
      ..color = const Color(0xFF00B894).withOpacity(0.3)
      ..style = PaintingStyle.fill;

    final dataPath = Path();
    for (int i = 0; i < 6; i++) {
      final angle = (2 * pi * i / 6) - pi / 2;
      final r = radius * values[i];
      final x = center.dx + r * cos(angle);
      final y = center.dy + r * sin(angle);
      if (i == 0) dataPath.moveTo(x, y);
      else dataPath.lineTo(x, y);
      canvas.drawCircle(Offset(x, y), 4, Paint()..color = const Color(0xFF00B894));
    }
    dataPath.close();
    canvas.drawPath(dataPath, dataPaint);

    final borderPaint = Paint()
      ..color = const Color(0xFF00B894)
      ..style = PaintingStyle.stroke
      ..strokeWidth = 2;
    canvas.drawPath(dataPath, borderPaint);
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => false;
}
