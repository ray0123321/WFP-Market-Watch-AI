import 'package:flutter/material.dart';
import 'package:animate_do/animate_do.dart';
import 'package:wfp_market_watch/screens/home_screen.dart';
import 'package:wfp_market_watch/theme/app_theme.dart';

class SplashScreen extends StatelessWidget {
  const SplashScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        width: double.infinity,
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
            colors: [AppTheme.secondaryCream, AppTheme.primaryMint],
          ),
        ),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            FadeInDown(
              duration: const Duration(seconds: 1),
              child: const Icon(
                Icons.waves_rounded,
                size: 100,
                color: AppTheme.textDark,
              ),
            ),
            const SizedBox(height: 20),
            FadeIn(
              delay: const Duration(milliseconds: 500),
              child: Text(
                'WFP Market Watch',
                style: Theme.of(context).textTheme.displaySmall?.copyWith(
                  fontWeight: FontWeight.bold,
                  letterSpacing: 1.2,
                ),
              ),
            ),
            FadeInUp(
              delay: const Duration(milliseconds: 800),
              child: const Text(
                'AI Price Prediction for Pakistan',
                style: TextStyle(fontSize: 16, color: Colors.black54),
              ),
            ),
            const SizedBox(height: 50),
            ElasticIn(
              delay: const Duration(milliseconds: 1500),
              child: ElevatedButton(
                onPressed: () {
                  Navigator.pushReplacement(
                    context,
                    MaterialPageRoute(builder: (context) => const HomeScreen()),
                  );
                },
                child: const Text('Get Started ✨'),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
