import 'package:flutter/material.dart';
import 'package:app/pages/choose_theme.dart';
import 'package:app/pages/today_article.dart';
import 'package:app/pages/splash.dart';
import 'package:hive_flutter/hive_flutter.dart';


void main() async {

  WidgetsFlutterBinding.ensureInitialized();
  await Hive.initFlutter();
  var themesBox = await Hive.openBox('themesBox');

  runApp(MaterialApp(
    initialRoute: '/',
    routes: {
      '/': (context) => const SplashPage(),
      '/todayArticle': (context) => const TodayArticlePage(),
      '/chooseThemePage': (context) => const ChooseThemePage(),
    },
  ));
}