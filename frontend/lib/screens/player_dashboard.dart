import 'package:flutter/material.dart';
import '../widgets/metric_card.dart';
import '../widgets/performance_chart.dart';
import '../widgets/radar_chart.dart';
import '../widgets/activity_feed.dart';

class PlayerDashboard extends StatefulWidget {
  const PlayerDashboard({super.key});

  @override
  State<PlayerDashboard> createState() => _PlayerDashboardState();
}

class _PlayerDashboardState extends State<PlayerDashboard> {
  int _selectedIndex = 0;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Dashboard"),
        leading: IconButton(
          icon: const Icon(Icons.notifications_outlined),
          onPressed: () => Navigator.pushNamed(context, '/notifications'),
        ),
        actions: [
          GestureDetector(
            onTap: () => Navigator.pushNamed(context, '/profile'),
            child: const Padding(
              padding: EdgeInsets.all(8.0),
              child: CircleAvatar(
                radius: 18,
                backgroundColor: Color(0xFF00B894),
                child: Icon(Icons.person, size: 20, color: Colors.white),
              ),
            ),
          ),
          const SizedBox(width: 8),
        ],
      ),
      body: RefreshIndicator(
        onRefresh: () async => await Future.delayed(const Duration(seconds: 2)),
        color: const Color(0xFF00B894),
        child: SingleChildScrollView(
          physics: const AlwaysScrollableScrollPhysics(),
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Welcome Card
              Container(
                width: double.infinity,
                padding: const EdgeInsets.all(20),
                decoration: BoxDecoration(
                  gradient: const LinearGradient(
                    colors: [Color(0xFF00B894), Color(0xFF00CEC9)],
                    begin: Alignment.topLeft,
                    end: Alignment.bottomRight,
                  ),
                  borderRadius: BorderRadius.circular(20),
                  boxShadow: [
                    BoxShadow(
                      color: const Color(0xFF00B894).withOpacity(0.3),
                      blurRadius: 20,
                      offset: const Offset(0, 10),
                    ),
                  ],
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text("Welcome back, Ahmed!", style: TextStyle(color: Colors.white70, fontSize: 14)),
                    const SizedBox(height: 12),
                    Row(
                      children: [
                        const Expanded(
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text("78.5", style: TextStyle(color: Colors.white, fontSize: 48, fontWeight: FontWeight.bold)),
                              Text("Overall Rating", style: TextStyle(color: Colors.white70, fontSize: 14)),
                            ],
                          ),
                        ),
                        Container(
                          padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                          decoration: BoxDecoration(
                            color: Colors.white.withOpacity(0.2),
                            borderRadius: BorderRadius.circular(20),
                          ),
                          child: const Row(
                            children: [
                              Icon(Icons.trending_up, color: Colors.white, size: 16),
                              SizedBox(width: 4),
                              Text("+2.3%", style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
                            ],
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 8),
                    Text("82nd percentile vs 10,000+ professionals", style: TextStyle(color: Colors.white.withOpacity(0.9))),
                  ],
                ),
              ),
              const SizedBox(height: 24),

              // Quick Stats Row
              Row(
                children: [
                  Expanded(child: _buildQuickStat("Matches", "24", Icons.sports_soccer)),
                  const SizedBox(width: 12),
                  Expanded(child: _buildQuickStat("Hours", "36h", Icons.timer)),
                  const SizedBox(width: 12),
                  Expanded(child: _buildQuickStat("Rank", "#142", Icons.emoji_events)),
                ],
              ),
              const SizedBox(height: 24),

              // Metrics Grid
              const Text("Key Metrics", style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
              const SizedBox(height: 12),
              GridView.count(
                shrinkWrap: true,
                physics: const NeverScrollableScrollPhysics(),
                crossAxisCount: 2,
                crossAxisSpacing: 12,
                mainAxisSpacing: 12,
                childAspectRatio: 1.3,
                children: const [
                  MetricCard(title: "Max Speed", value: "32.4", unit: "km/h", icon: Icons.speed, color: Color(0xFF00B894), trend: "+1.2"),
                  MetricCard(title: "Pass Accuracy", value: "87%", unit: "", icon: Icons.sports_soccer, color: Color(0xFF0984E3), trend: "+3.5"),
                  MetricCard(title: "Distance", value: "11.2", unit: "km", icon: Icons.directions_run, color: Color(0xFFE17055), trend: "+0.8"),
                  MetricCard(title: "Sprints", value: "16", unit: "", icon: Icons.bolt, color: Color(0xFFFD79A8), trend: "+2"),
                ],
              ),
              const SizedBox(height: 24),

              // Performance Chart
              const Text("Performance Trend", style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
              const SizedBox(height: 12),
              const PerformanceChart(),
              const SizedBox(height: 24),

              // Radar Chart
              const Text("Skill Breakdown", style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
              const SizedBox(height: 12),
              const RadarChartWidget(),
              const SizedBox(height: 24),

              // Activity Feed
              const Text("Recent Activity", style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
              const SizedBox(height: 12),
              const ActivityFeed(),
              const SizedBox(height: 24),

              // Action Buttons
              Row(
                children: [
                  Expanded(
                    child: ElevatedButton.icon(
                      onPressed: () => Navigator.pushNamed(context, '/upload'),
                      icon: const Icon(Icons.cloud_upload),
                      label: const Text("Upload Video"),
                    ),
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    child: ElevatedButton.icon(
                      onPressed: () => Navigator.pushNamed(context, '/coach'),
                      icon: const Icon(Icons.chat_bubble_outline),
                      label: const Text("AI Coach"),
                      style: ElevatedButton.styleFrom(backgroundColor: const Color(0xFF0984E3)),
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 24),
            ],
          ),
        ),
      ),
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: _selectedIndex,
        onTap: (index) {
          setState(() => _selectedIndex = index);
          if (index == 1) Navigator.pushNamed(context, '/reports');
          if (index == 2) Navigator.pushNamed(context, '/coach');
          if (index == 3) Navigator.pushNamed(context, '/discover');
          if (index == 4) Navigator.pushNamed(context, '/leaderboard');
        },
        items: const [
          BottomNavigationBarItem(icon: Icon(Icons.dashboard_outlined), activeIcon: Icon(Icons.dashboard), label: 'Home'),
          BottomNavigationBarItem(icon: Icon(Icons.assessment_outlined), activeIcon: Icon(Icons.assessment), label: 'Reports'),
          BottomNavigationBarItem(icon: Icon(Icons.chat_bubble_outline), activeIcon: Icon(Icons.chat_bubble), label: 'Coach'),
          BottomNavigationBarItem(icon: Icon(Icons.search_outlined), activeIcon: Icon(Icons.search), label: 'Discover'),
          BottomNavigationBarItem(icon: Icon(Icons.leaderboard_outlined), activeIcon: Icon(Icons.leaderboard), label: 'Top'),
        ],
      ),
    );
  }

  Widget _buildQuickStat(String label, String value, IconData icon) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: const Color(0xFF1D1F33),
        borderRadius: BorderRadius.circular(16),
      ),
      child: Column(
        children: [
          Icon(icon, color: const Color(0xFF00B894), size: 24),
          const SizedBox(height: 8),
          Text(value, style: const TextStyle(color: Colors.white, fontSize: 20, fontWeight: FontWeight.bold)),
          Text(label, style: const TextStyle(color: Colors.white54, fontSize: 12)),
        ],
      ),
    );
  }
}
