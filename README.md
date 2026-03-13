# 🚀 production_BOT | Портфолио-проект

> Современный асинхронный Telegram-бот, построенный на базе **aiogram 3**, **PostgreSQL**, **Redis** и **APScheduler**.  
> Проект демонстрирует модульную архитектуру, работу с состояниями (FSM), фоновые задачи с учётом таймзон и интеграцию с базой данных через SQLAlchemy.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![aiogram](https://img.shields.io/badge/aiogram-3.x-2CA5E0?style=for-the-badge)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?style=for-the-badge&logo=postgresql)
![Redis](https://img.shields.io/badge/Redis-7-red?style=for-the-badge&logo=redis)
![APScheduler](https://img.shields.io/badge/APScheduler-enabled-success?style=for-the-badge)
![Docker](https://img.shields.io/badge/Docker-ready-2496ED?style=for-the-badge&logo=docker)

---

## ✨ О проекте

Данный репозиторий создан как **наглядный пример** разработки Telegram-ботов production-уровня. 
Архитектура проекта позволяет легко масштабировать функционал, добавлять новые модули, миграции и бизнес-логику без переписывания ядра.

### Основные блоки:
- 👤 **Пользовательский сценарий (User flow)**
- 🛠️ **Панель администратора (Admin flow)**
- 🧠 **Многошаговые формы (FSM)**
- 🗄️ **Асинхронная работа с БД (SQLAlchemy)**
- 🔴 **Хранение состояний в кэше (Redis)**
- ⏰ **Фоновые задачи и рассылки (APScheduler)**
- 📊 **Сбор статистики и экспорт данных**

---

## 🧩 Ключевые возможности

### 👥 Для пользователей
- Продуманное главное меню (Reply-клавиатуры)
- Оформление заявки через пошаговую форму (FSM)
- Валидация вводимых данных на каждом этапе
- Возможность просматривать историю своих заявок
- Получение уведомлений об изменении статуса заявки

### 🔐 Для администратора
- Изолированная админ-панель (доступ по `ADMIN_ID`)
- Просмотр новых заявок
- Принятие и отклонение заявок (Inline-кнопки + Callback-хендлеры)
- Просмотр агрегированной статистики из БД
- Экспорт данных в формате `.xlsx` (Excel)

### ⏳ Планировщик (Background Jobs)
- Интеграция `APScheduler`
- Поддержка отложенных и периодических задач
- **Учёт часовых поясов (Timezone-aware scheduling)**
- Подготовленная база для: утренних пушей, еженедельных отчётов, напоминаний

---

## 🛠 Технологический стек

| Технология | Назначение |
|------------|------------|
| **Python 3.10+** | Основной язык разработки |
| **aiogram 3.x** | Асинхронный фреймворк для Telegram API |
| **SQLAlchemy Async** | ORM для работы с базой данных |
| **PostgreSQL 15** | Основная реляционная СУБД |
| **Redis 7** | In-memory хранилище для состояний FSM |
| **APScheduler** | Планировщик фоновых задач |
| **openpyxl** | Генерация Excel-отчётов |
| **Docker & Compose** | Контейнеризация и быстрый развёртывание |

---

## 📁 Структура проекта

```text
telegram-bot-demo/
├── bot.py                  # Точка входа, запуск polling и инициализация
├── config.py               # Загрузка переменных окружения
├── requirements.txt        # Зависимости проекта
├── Dockerfile              # Инструкция для сборки образа бота
├── docker-compose.yml      # Поднятие связки Bot + PostgreSQL + Redis
├── .env.example            # Пример файла конфигурации
├── README.md               # Документация проекта
│
├── handlers/               # Обработчики сообщений и коллбеков
│   ├── __init__.py
│   ├── user.py             # Клиентская часть и FSM
│   └── admin.py            # Админ-панель и модерация
│
├── keyboards/              # Клавиатуры (Reply & Inline)
│   ├── __init__.py
│   └── kb.py               # Константы кнопок и генераторы клавиатур
│
├── database/               # Работа с базой данных
│   ├── __init__.py
│   ├── db.py               # CRUD-операции и подключение
│   └── models.py           # Декларативные модели SQLAlchemy
│
├── services/               # Вспомогательные сервисы
│   ├── __init__.py
│   └── scheduler.py        # Настройка и задачи APScheduler
│
└── utils/                  # Утилиты
    ├── __init__.py
    └── export.py           # Логика выгрузки в Excel
```

---

## 📸 Скриншоты работы

*(Нажмите на изображение, чтобы увеличить)*

| 1️⃣ Главное меню | 2️⃣ Пошаговая форма (FSM) | 3️⃣ Отмена действия (Cancel) |
|:---:|:---:|:---:|
| ![Start menu](screenshots/01_start_menu.png) | ![FSM request flow](screenshots/02_fsm_request_flow.png) | ![FSM cancel](screenshots/03_fsm_cancel_keyboard.png) |

| 4️⃣ История заявок | 5️⃣ Админ-панель | 6️⃣ Статистика (Аналитика БД) |
|:---:|:---:|:---:|
| ![User requests](screenshots/04_user_requests_list.png) | ![Admin panel](screenshots/05_admin_panel.png) | ![Statistics](screenshots/06_admin_statistics.png) |

| 7️⃣ Модерация заявок | 8️⃣ Сообщение от планировщика | 9️⃣ Логи запуска |
|:---:|:---:|:---:|
| ![New requests](screenshots/07_admin_new_requests.png) | ![Scheduler message](screenshots/08_scheduler_message.png) | ![Startup logs](screenshots/09_bot_startup_logs.png) |

| 🔟 Выгрузка в Excel | 1️⃣1️⃣ Обновление статуса |
|:---:|:---:|
| ![Excel export](screenshots/10_export_excel.png) | ![Status update](screenshots/11_request_status_update.png) |

---

## ⚙️ Переменные окружения (.env)

Для локального запуска необходимо создать файл `.env` в корне проекта (см. шаблон `.env.example`):

```env
BOT_TOKEN=ваш_токен_от_BotFather
ADMIN_ID=ваш_telegram_id
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/bot_demo
REDIS_URL=redis://localhost:6379/0
```

---

## 🚀 Быстрый старт

### 🐳 Запуск через Docker (Рекомендуется)

Самый быстрый способ развернуть весь стек: Бота, PostgreSQL и Redis.

```bash
# 1. Склонировать репозиторий
git clone https://github.com/YYaroslavSSolovev/telegram-bot-demo.git
cd telegram-bot-demo

# 2. Настроить конфигурацию
cp .env.example .env
# Отредактируйте .env, добавив BOT_TOKEN и ADMIN_ID

# 3. Запустить контейнеры
docker compose up -d --build

# 4. Проверить логи запуска
docker compose logs -f bot
```

### 💻 Локальный запуск (Без Docker)

```bash
# 1. Создать и активировать виртуальное окружение
python -m venv .venv
source .venv/bin/activate  # Для Linux/macOS
# .venv\Scripts\activate   # Для Windows

# 2. Установить зависимости
pip install -r requirements.txt

# 3. Убедиться, что локально запущены PostgreSQL и Redis, настроить .env

# 4. Запустить бота
python bot.py
```

---

## 🎯 Архитектурные решения

- **Изоляция слоёв**: Обработчики сообщений (`handlers/`) не содержат прямых SQL-запросов, вся логика вынесена в `database/db.py`.
- **FSM in Redis**: Состояния пользователей при заполнении форм не сбрасываются при перезапуске бота, так как хранятся в Redis.
- **Async First**: Весь код, включая запросы к БД (`asyncpg`) и планировщик задач, полностью асинхронен и не блокирует Event Loop.

---

## 👨‍💻 Автор

**Ярослав Соловьев (Yaroslav Solovev)**  
`Python Developer` | `Telegram Bots` | `aiogram 3` | `Backend Automation`

🔗 **GitHub:** [@YYaroslavSSolovev](https://github.com/YYaroslavSSolovev)  
📫 **Telegram:** *@Yaroslav_GIT*

---

## 📄 Лицензия

Этот проект распространяется под лицензией **MIT License**. Вы можете свободно использовать этот код в образовательных и коммерческих целях. См. файл `LICENSE` для получения дополнительной информации.
