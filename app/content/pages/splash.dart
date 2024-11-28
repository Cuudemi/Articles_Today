import 'dart:async';
import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:hive/hive.dart';

class SplashPage extends StatefulWidget {
  const SplashPage({super.key});

  @override
  State<SplashPage> createState() => _SplashPageState();
}

class _SplashPageState extends State<SplashPage> {
  late Box themesBox;
  @override
  void initState() {
    super.initState();

    themesBox = Hive.box('themesBox');
    final List<String> selectedThemes =
        List.from(themesBox.get('selectedThemes', defaultValue: []));

    final String nextPage = selectedThemes.isEmpty ? '/chooseThemePage' : '/chooseThemePage';

    Timer(const Duration(seconds: 3), () {
      Navigator.pushNamedAndRemoveUntil(
          context, nextPage, (route) => false);
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      body: Center(
        child: Container(
          width: 300.0,
          height: 300.0,
          decoration: const BoxDecoration(
            shape: BoxShape.circle,
            color: Color(0xFF219ebc),
          ),
          child: Center(
            child: Text(
              'Articles Today',
              style: TextStyle(
                fontFamily: GoogleFonts.inriaSans().fontFamily,
                fontSize: 70.0,
                fontWeight: FontWeight.bold,
                color: Colors.white,
              ),
              textAlign: TextAlign.center,
            ),
          ),
        ),
      ),
    );
  }
}
