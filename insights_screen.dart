import 'package:flutter/material.dart';
import 'package:animate_do/animate_do.dart';
import 'package:wfp_market_watch/theme/app_theme.dart';

class InsightsScreen extends StatelessWidget {
  const InsightsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Market Insights')),
      body: SingleChildScrollView(
        child: Padding(
          padding: const EdgeInsets.all(20.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // 1. Quick Stats Row
              FadeInDown(
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    _buildStatBadge('95% Accuracy', Colors.green.shade100, Icons.verified),
                    _buildStatBadge('6 Cities', Colors.blue.shade100, Icons.location_city),
                    _buildStatBadge('XGBoost', Colors.purple.shade100, Icons.bolt),
                  ],
                ),
              ),
              const SizedBox(height: 30),
              
              // 2. Main Mission Card
              FadeInLeft(
                child: Container(
                  width: double.infinity,
                  padding: const EdgeInsets.all(25),
                  decoration: BoxDecoration(
                    gradient: LinearGradient(
                      colors: [AppTheme.primaryMint, Colors.teal.shade100],
                    ),
                    borderRadius: BorderRadius.circular(30),
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Icon(Icons.auto_awesome, color: Colors.white, size: 30),
                      const SizedBox(height: 15),
                      const Text(
                        'Our Mission',
                        style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold, color: Colors.white),
                      ),
                      const SizedBox(height: 10),
                      Text(
                        'Building an AI-driven Pakistan where food affordability is monitored in real-time to prevent hunger and support local communities.',
                        style: TextStyle(fontSize: 16, color: Colors.white.withOpacity(0.9)),
                      ),
                    ],
                  ),
                ),
              ),
              const SizedBox(height: 30),
              
              // 3. Technical Cards
              const Text('Project Highlights', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
              const SizedBox(height: 15),
              FadeInUp(
                delay: const Duration(milliseconds: 300),
                child: _buildInsightCard(
                  title: 'SDG 2: Zero Hunger',
                  desc: 'Aligned with UN goals to improve food security across Pakistan.',
                  icon: Icons.favorite,
                  color: Colors.pink.shade50,
                ),
              ),
              const SizedBox(height: 15),
              FadeInUp(
                delay: const Duration(milliseconds: 500),
                child: _buildInsightCard(
                  title: 'Data Science',
                  desc: 'Utilizing WFP datasets with advanced feature engineering.',
                  icon: Icons.science,
                  color: Colors.blue.shade50,
                ),
              ),
              const SizedBox(height: 15),
              FadeInUp(
                delay: const Duration(milliseconds: 700),
                child: _buildInsightCard(
                  title: 'Mobile Innovation',
                  desc: 'A cross-platform Flutter interface connected to a FastAPI backend.',
                  icon: Icons.phonelink_setup,
                  color: Colors.orange.shade50,
                ),
              ),
              
              const SizedBox(height: 40),
              // Footer
              Center(
                child: Column(
                  children: [
                    const Text('Kinnaird College for Women | 2026', style: TextStyle(fontSize: 12, color: Colors.grey)),
                  ],
                ),
              ),
              const SizedBox(height: 20),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildStatBadge(String text, Color color, IconData icon) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
      decoration: BoxDecoration(
        color: color,
        borderRadius: BorderRadius.circular(15),
      ),
      child: Row(
        children: [
          Icon(icon, size: 16, color: Colors.black87),
          const SizedBox(width: 5),
          Text(text, style: const TextStyle(fontSize: 12, fontWeight: FontWeight.bold)),
        ],
      ),
    );
  }

  Widget _buildInsightCard({required String title, required String desc, required IconData icon, required Color color}) {
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: color,
        borderRadius: BorderRadius.circular(20),
        boxShadow: [BoxShadow(color: Colors.black.withOpacity(0.02), blurRadius: 10)],
      ),
      child: Row(
        children: [
          Icon(icon, size: 35, color: AppTheme.textDark),
          const SizedBox(width: 20),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(title, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 17)),
                const SizedBox(height: 4),
                Text(desc, style: const TextStyle(fontSize: 13, color: Colors.black54)),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
