import 'dart:math';
import 'package:hive/hive.dart';
import 'package:hive_flutter/hive_flutter.dart';
import 'package:flutter/material.dart';

class ChooseThemePage extends StatefulWidget {
  const ChooseThemePage({super.key});

  @override
  State<ChooseThemePage> createState() => _ChooseThemePageState();
}

class _ChooseThemePageState extends State<ChooseThemePage> {
  /// Изменение яркости цвета
  Color increaseColorLightness(Color color, double increment) {
    var hslColor = HSLColor.fromColor(color);
    var newValue = min(max(hslColor.lightness + increment, 0.0), 1.0);
    return hslColor.withLightness(newValue).toColor();
  }

  final List<Map<String, dynamic>> themes = [
    {
      'name': 'Разработка',
      'source': 'Habr',
      'defaultColor': const Color(0xFFFFB703),
    },
    {
      'name': 'Научпоп',
      'source': 'Habr',
      'defaultColor': const Color(0xFFFB8500),
    },
    {
      'name': 'Дизайн',
      'source': 'Habr',
      'defaultColor': const Color(0xFF219EBC),
    },
    {
      'name': 'Менеджмент',
      'source': 'Habr',
      'defaultColor': const Color(0xFF8ECAE6),
    },
    {
      'name': 'Забота о себе',
      'source': 'Журнал Кинжал',
      'defaultColor': const Color(0xFF3ED9B1),
    },
  ];

  late Box themesBox;
  late List<String> selectedThemes;

  @override
  /// Рассчитывает цвета при инициализации страницы
  void initState() {
    super.initState();

    themesBox = Hive.box('themesBox');
    selectedThemes =
        List.from(themesBox.get('selectedThemes', defaultValue: []));

    // Установка currentColor в зависимости от наличия тем в selectedThemes
    for (var theme in themes) {
      theme['touchColor'] = increaseColorLightness(theme['defaultColor'], 0.2);
      theme['currentColor'] = selectedThemes.contains(theme['name'])
          ? theme['touchColor']
          : theme['defaultColor'];
    }
  }

  /// обработчик нажатия на кнопку
  void _toggleTheme(String themeName) {
    setState(() {
      var theme = themes.firstWhere((t) => t['name'] == themeName);
      if (theme['currentColor'] == theme['defaultColor']) {
        theme['currentColor'] = theme['touchColor'];
        selectedThemes.add(themeName);
      } else {
        theme['currentColor'] = theme['defaultColor'];
        selectedThemes.remove(themeName);
      }
    });
  }

  /// Создание кнопок с цветами
  Widget buildTopicButton(Map<String, dynamic> theme) {
    bool isSelected = selectedThemes.contains(theme['name']);
    return GestureDetector(
      onTap: () => _toggleTheme(theme['name']),
      child: Container(
        decoration: BoxDecoration(
          gradient: isSelected
              ? LinearGradient(
              colors: [
                theme['defaultColor'], theme['touchColor']
              ],
              begin: Alignment.centerLeft,
              end: Alignment.centerRight,
          ) : null,
          color: isSelected ? null : theme['defaultColor'],
          borderRadius: BorderRadius.circular(20),
          border: Border.all(width: 0, color: Colors.black12),
        ),
          padding: const EdgeInsets.all(20.0),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Row(
            children: [
              Text(
                  theme['name'],
                  style: const TextStyle(
                    fontSize: 26,
                    fontWeight: FontWeight.bold,
                    color: Colors.white,
                  )
              ),
              const SizedBox(width: 8.0),
              Text(
                  theme['source'],
                  style: const TextStyle(
                      fontSize: 15,
                      height: 1.7,
                      fontWeight: FontWeight.bold,
                      color: Colors.white
                  )
              ),
            ],
          ),
          if (isSelected)
            const Icon(
              Icons.check,
              color: Colors.white,
              size: 30,
            ),
        ],
      )
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        backgroundColor: Colors.white,
        body: SafeArea(
            child: Container(
                margin: const EdgeInsets.all(20.0),
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                  children: [
                    const Text(
                      'Выберите темы, которые вас интересуют:',
                      style: TextStyle(
                        color: Color(0xFF023047),
                        fontSize: 38,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    ...themes.map(buildTopicButton).toList(),

                    /// Кнопка для подтверждения перехода
                    OutlinedButton(
                        onPressed: () {
                          themesBox.put('selectedThemes', selectedThemes);
                          Navigator.pushNamedAndRemoveUntil(
                              context, '/todayArticle', (route) => false);
                        },
                        style: TextButton.styleFrom(
                          foregroundColor: const Color(0xFF023047),
                          backgroundColor: Colors.white,
                          padding: const EdgeInsets.all(20.0),
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(20.0),
                          ),
                          side:
                              const BorderSide(width: 3.0, color: Colors.black),
                        ),
                        child: const Align(
                            alignment: Alignment.center,
                            child: Text("Подтвердить темы и продолжить",
                                style: TextStyle(
                                  fontSize: 18,
                                  fontWeight: FontWeight.bold,
                                ))))
                  ],
                )
            )
        )
    );
  }
}
