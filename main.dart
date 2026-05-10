import 'package:flutter/material.dart';
import 'package:wfp_market_watch/screens/splash_screen.dart';
import 'package:wfp_market_watch/theme/app_theme.dart';

void main() {
  runApp(const MarketWatchApp());
}

class MarketWatchApp extends StatelessWidget {
  const MarketWatchApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'WFP Market Watch',
      theme: AppTheme.lightTheme,
      home: const SplashScreen(),
    );
  }
}
