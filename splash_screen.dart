import 'package:flutter/material.dart';
import 'package:animate_do/animate_do.dart';
import 'package:flutter_spinkit/flutter_spinkit.dart';
import 'package:wfp_market_watch/services/api_service.dart';
import 'package:wfp_market_watch/theme/app_theme.dart';
import 'package:wfp_market_watch/screens/insights_screen.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  String? selectedCity;
  String? selectedCommodity;
  List<String> cities = [];
  List<String> commodities = [];
  bool isLoading = true;
  bool isPredicting = false;
  double? predictedPrice;

  @override
  void initState() {
    super.initState();
    _fetchMetadata();
  }

  Future<void> _fetchMetadata() async {
    try {
      final data = await ApiService.getMetadata();
      setState(() {
        cities = List<String>.from(data['cities']);
        commodities = List<String>.from(data['commodities']);
        isLoading = false;
      });
    } catch (e) {
      setState(() {
        isLoading = false;
      });
    }
  }

  Future<void> _predict() async {
    if (selectedCity == null || selectedCommodity == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Please select both City and Commodity!'), backgroundColor: Colors.orange),
      );
      return;
    }
    setState(() {
      isPredicting = true;
      predictedPrice = null;
    });

    try {
      final data = await ApiService.getPrediction(selectedCity!, selectedCommodity!);
      setState(() {
        predictedPrice = data['predicted_price'];
        isPredicting = false;
      });
    } catch (e) {
      setState(() {
        isPredicting = false;
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Error: $e'), backgroundColor: Colors.redAccent),
        );
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Price Predictor'),
        actions: [
          IconButton(
            icon: const Icon(Icons.info_outline),
            onPressed: () => Navigator.push(
              context, 
              MaterialPageRoute(builder: (context) => const InsightsScreen())
            ),
          )
        ],
      ),
      body: isLoading
          ? const Center(child: SpinKitPulse(color: AppTheme.primaryMint, size: 50.0))
          : Padding(
              padding: const EdgeInsets.all(20.0),
              child: SingleChildScrollView(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    FadeInLeft(
                      child: const Text(
                        'Select Details',
                        style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold),
                      ),
                    ),
                    const SizedBox(height: 20),
                    _buildDropdown(
                      label: 'Select City',
                      value: selectedCity,
                      items: cities,
                      onChanged: (val) => setState(() => selectedCity = val),
                    ),
                    const SizedBox(height: 15),
                    _buildDropdown(
                      label: 'Select Commodity',
                      value: selectedCommodity,
                      items: commodities,
                      onChanged: (val) => setState(() => selectedCommodity = val),
                    ),
                    const SizedBox(height: 30),
                    Center(
                      child: ZoomIn(
                        child: ElevatedButton(
                          onPressed: _predict,
                          style: ElevatedButton.styleFrom(
                            minimumSize: const Size(250, 60),
                          ),
                          child: const Text('Predict Price 🚀', style: TextStyle(fontSize: 18)),
                        ),
                      ),
                    ),
                    const SizedBox(height: 40),
                    if (isPredicting)
                      const Center(child: SpinKitThreeBounce(color: AppTheme.primaryMint, size: 30)),
                    if (predictedPrice != null)
                      FadeInUp(
                        child: _buildResultCard(),
                      ),
                  ],
                ),
              ),
            ),
    );
  }

  Widget _buildDropdown({required String label, required String? value, required List<String> items, required Function(String?) onChanged}) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 15, vertical: 5),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(15),
        boxShadow: [BoxShadow(color: Colors.black.withOpacity(0.05), blurRadius: 10)],
      ),
      child: DropdownButtonHideUnderline(
        child: DropdownButton<String>(
          hint: Text(label),
          value: value,
          isExpanded: true,
          items: items.map((e) => DropdownMenuItem(value: e, child: Text(e))).toList(),
          onChanged: onChanged,
        ),
      ),
    );
  }

  Widget _buildResultCard() {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(25),
      decoration: BoxDecoration(
        color: AppTheme.primaryMint.withOpacity(0.2),
        borderRadius: BorderRadius.circular(30),
        border: Border.all(color: AppTheme.primaryMint, width: 2),
      ),
      child: Column(
        children: [
          const Text('Predicted Price', style: TextStyle(fontSize: 18, color: Colors.black54)),
          const SizedBox(height: 10),
          Text(
            'PKR ${predictedPrice!.toStringAsFixed(2)}',
            style: const TextStyle(fontSize: 40, fontWeight: FontWeight.bold, color: AppTheme.textDark),
          ),
          const SizedBox(height: 10),
          const Text('Aligned with SDG 2: Zero Hunger', style: TextStyle(fontStyle: FontStyle.italic, color: Colors.black45)),
        ],
      ),
    );
  }
}
