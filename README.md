# Мобильное приложение Articles Today
[![.github/workflows/main.yml](https://github.com/Cuudemi/Articles_Today/actions/workflows/main.yml/badge.svg)](https://github.com/Cuudemi/Articles_Today/actions/workflows/main.yml)

## Основная идея приложения

Пользователь выбирает интересную ему предметную область из определенного перечня, и затем приложение отправляет ему одну или несколько статей в день с выбранной тематикой.

## Расмотренные аналоги

Для оценки востребованности разрабатываемого приложения и выявления требуемых функций был проведен анализ существующих программных решений в данной области. Рассмотрим два приложения, BigMag и Surfingbird, с целью выявления их особенностей и возможных недостатков.

1. *BigMag* – приложение предоставляет пользователю выбор лучших материалов по различным разделам, из которых можно выбрать наиболее интересные. К сожалению, ознакомиться с данным приложением не удалось из-за трудностей с запуском.

3. *Surfingbird* – при первом запуске приложения нужно выбрать несколько тематик, а дальше остаётся только листать ленту и читать приглянувшиеся статьи. С этим приложением ознакомиться также не удалось из-за ошибки, которая делает регистрацию невозможной.

Оба рассмотренных приложения, BigMag и Surgingburd, столкнулись с техническими проблемами, препятствующими ознакомлению с их функционалом. Эти трудности подчеркивают важность разработки стабильного и доступного приложения

## Реализация приложения
### Используемые технологии
#### Серверная часть
* PostgreSQL 
* FastAPI 0.109.2
* Request 2.32.3
* BeautifulSoup 4.12.3
* Fake-useragent
* Pydantic 2.6.1
* SQLAlchemy 2.0.36
#### Мобильное приложение
* Flutter
* Hive ^2.2.3
* Dio ^5.7.0

### Хранение и управление данными
Для эффективного управления данными используются следующие таблицы:
#### Таблица со статьями
Таблица со статьями заполняется с использованием парсера и содержит сами статьи.

| Column      | Type         | Description                |
|-------------|--------------|----------------------------|
| id          | Integer      | Primary Key                |
| name        | String       |                            |
| id_source   | Integer      | Foreign Key (source.id)    |
| content     | String       |                            |
| url         | String       |                            |
| theme_name  | String       |    |

**Relationships:**
- `source`: relationship with `Source` (back_populates="articles")

---

### Таблица с источниками
В таблице с источниками хранится информация о различных источниках, включая тематику и ссылки. 
| Column   | Type    | Description           |
|----------|---------|-----------------------|
| id       | Integer | Primary Key           |
| name     | String  |                       |
| theme    | String  |                       |
| url      | String  |                       |

**Relationships:**
- `articles`: relationship with `Article` (back_populates="source")

## Проектирование приложения
### Проектирование пользовательского интерфейса приложения
Прототип разработан с помощью сервиса Figma.

<table>
  <tr>
    <td align="center" width="230">
      <img src="https://github.com/user-attachments/assets/75e80f5f-f471-4e3d-9b58-343244a582a1" alt="Стартовая страница">
    </td>
    <td align="center" width="230">
      <img src="https://github.com/user-attachments/assets/f66536e2-562a-4b07-b738-292b0f18c7e0" alt="Выбор тематики">
    </td>
    <td align="center" width="230">
      <img src="https://github.com/user-attachments/assets/f9379e33-2ae5-4e87-9ec5-74a8fcdabb97" alt="Сегодняшняя статья">
    </td>
  </tr>
  <tr>
    <td align="center" width="230">Стартовая страница</td>
    <td align="center" width="230">Выбор тематики</td>
    <td align="center" width="230">Сегодняшняя статья</td>
  </tr>
</table>
<table>
  <tr>
    <td align="center" width="230">
      <img src="https://github.com/user-attachments/assets/f55bcbe5-80ff-41c0-85d6-78e3a1c25572" alt="Настройки">
    </td>
    <td align="center" width="230">
      <img src="https://github.com/user-attachments/assets/dd2adc4d-d058-4337-90ca-653c01165a75" alt="Архив">
    </td>
    <td width="230"></td>
  </tr>
    <tr>
    <td align="center" width="230">Настройки</td>
    <td align="center" width="230">Архив</td>
      <td align="center" width="230"></td>
  </tr>
</table>

### Проектирование архитектуры приложения 

![architecture](https://github.com/user-attachments/assets/599c199f-2b1e-4679-8c0f-fde62521c124)
