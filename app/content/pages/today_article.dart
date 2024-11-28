import 'package:flutter/material.dart';
import 'package:hive/hive.dart';
import 'package:hive_flutter/hive_flutter.dart';
import 'package:dio/dio.dart';

class TodayArticlePage extends StatefulWidget {
  const TodayArticlePage({super.key});

  @override
  State<TodayArticlePage> createState() => _TodayArticlePageState();
}

class _TodayArticlePageState extends State<TodayArticlePage> {
  final dio = Dio();
  Response? response;
  late Box themesBox;

  @override
  void initState() {
    super.initState();
    getHttp();
    openBox();
  }

  Future<void> openBox() async {
    themesBox = await Hive.openBox('themesBox');
    setState(() {}); // Обновляем интерфейс, когда бокс открыт
  }

  // Асинхронный запрос с использованием Dio
  Future<void> getHttp() async {
    try {
      Response res = await dio.get('ip:8000/article');
      setState(() {
        response = res; // Обновляем состояние после получения данных
      });
    } catch (e) {
      print('Ошибка запроса: $e');
    }
  }

  @override
  Widget build(BuildContext context) {
    var storedValue = themesBox.get('selectedThemes', defaultValue: 'Нет значения');

    return Scaffold(
      backgroundColor: Colors.white,
      body: SafeArea(
        child: response == null ? (
          Center(child: CircularProgressIndicator(

      ))
      ) : Container(
            margin: const EdgeInsets.all(20.0),
            child: Column(
            mainAxisAlignment: MainAxisAlignment.start,
            children: [
              const Text(
                'Ваша сегодняшняя статья:',
                style: TextStyle(
                  color: Color(0xFF023047),
                  fontSize: 38,
                  fontWeight: FontWeight.bold,
                ),
              ),
              Container(
                  decoration: BoxDecoration(
                    borderRadius: BorderRadius.circular(30),
                    border: Border.all(width: 0, color: Colors.black12),
                    color: Color(0xFF023047),
                  ),
                padding: const EdgeInsets.all(20.0),
                margin: EdgeInsets.only(top:30),
                  width: double.infinity,
                  height: 300,
                  alignment: Alignment.center,
                  child: Text(
                      '${response?.data[0]['name'].toString()}',
                    textAlign: TextAlign.center,
                    style: TextStyle(
                      color: Colors.white,
                      fontSize: 30,
                      fontWeight: FontWeight.bold,
                    ),
                  )
              ),
              Container(
                  margin: EdgeInsets.only(top:30),
                  width: double.infinity,
                  height: 100,
                  child: Text(
                      ' ',
                      textDirection: TextDirection.ltr
                  )
            )
          ],
      )
          )
        ),
    );
  }
}