# Flask Project: Управление пользователями и Docker-развертывание

Проект представляет собой веб-приложение на Flask с системой аутентификации пользователей, миграциями базы данных и полным циклом Docker-развертывания.

![Структура проекта](project_structure.png) <!-- Замените на путь к вашему первому изображению -->
![Интерфейс приложения](app_interface.png) <!-- Замените на путь к вашему второму изображению -->

## Основные возможности

- **Аутентификация пользователей**
  - Регистрация новых учетных записей
  - Авторизация через Flask-Login
  - Управление сессиями пользователей
  - Flash-сообщения для обратной связи

- **Работа с базой данных**
  - Миграции через Flask-Migrate (Alembic)
  - Связи между таблицами (SQLAlchemy)
  - Фильтрация данных через выпадающие списки

- **Фронтенд оптимизация**
  - Сборка и минификация CSS/JS через Flask-Assets
  - Управление статическими ресурсами

- **Деплой и инфраструктура**
  - Docker-контейнеризация приложения
  - Развертывание через Docker Compose
  - Готовая production-сборка

## Технологический стек

**Бэкенд**
- Python 3.10+
- Flask 2.3+
- Flask-Login
- Flask-Migrate
- Flask-Assets
- SQLAlchemy
- PostgreSQL

**Фронтенд**
- Bootstrap 5
- Jinja2
- Webassets (для минификации)

**Инфраструктура**
- Docker 20.10+
- Docker Compose 2.0+
- Nginx (реверс-прокси)
- Gunicorn (production WSGI-сервер)

## Структура проекта

```bash
├── app/
│   ├── __init__.py
│   ├── auth/              # Модуль аутентификации
│   ├── models/            # Модели базы данных
│   ├── templates/         # Jinja2 шаблоны
│   ├── static/            # Статические файлы
│   │   ├── src/           # Исходные CSS/JS
│   │   ├── dist/          # Минифицированные ресурсы
│   ├── views/             # Бизнес-логика
│   ├── assets.py          # Конфигурация Flask-Assets
│   └── extensions.py      # Инициализация расширений
├── migrations/            # Скрипты миграций
├── docker/
│   ├── nginx/
│   │   └── nginx.conf     # Конфиг Nginx
│   └── app/
│       └── entrypoint.sh  # Скрипт запуска
├── .env                   # Переменные окружения
├── docker-compose.yml     # Конфиг Docker Compose
├── Dockerfile             # Докеризация приложения
├── requirements.txt       # Зависимости Python
└── README.md              # Документация
```

## Установка и запуск

### Локальная разработка

1. Клонировать репозиторий:
```bash
git clone https://github.com/yourusername/flask-docker-project.git
cd flask-docker-project
```

2. Создать виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Установить зависимости:
```bash
pip install -r requirements.txt
```

4. Настроить переменные окружения (создать файл `.env`):
```env
FLASK_APP=app
FLASK_ENV=development
SECRET_KEY=your_secret_key
DATABASE_URL=postgresql://user:password@localhost/dbname
```

5. Запустить приложение:
```bash
flask run
```

### Запуск через Docker

1. Собрать и запустить контейнеры:
```bash
docker-compose up --build
```

2. Приложение будет доступно по адресу:  
`http://localhost:8080`

3. Остановить контейнеры:
```bash
docker-compose down
```

## Миграции базы данных

Создать новую миграцию:
```bash
flask db migrate -m "Описание изменений"
```

Применить миграции:
```bash
flask db upgrade
```

В Docker-среде:
```bash
docker-compose exec web flask db upgrade
```

## Конфигурация Docker Compose

```yaml
version: '3.8'

services:
  web:
    build: .
    command: gunicorn --bind 0.0.0.0:5000 app:create_app()
    volumes:
      - .:/app
    environment:
      - DATABASE_URL=postgresql://db_user:db_password@db:5432/app_db
    depends_on:
      - db
    ports:
      - "5000:5000"

  db:
    image: postgres:13-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    environment:
      - POSTGRES_USER=db_user
      - POSTGRES_PASSWORD=db_password
      - POSTGRES_DB=app_db

  nginx:
    image: nginx:1.21-alpine
    ports:
      - "8080:80"
    volumes:
      - ./docker/nginx/nginx.conf:/etc/nginx/conf.d/default.conf
    depends_on:
      - web

volumes:
  postgres_data:
```

## Защищенные маршруты

Пример ограничения доступа:
```python
from flask_login import login_required, current_user

@app.route('/dashboard')
@login_required
def dashboard():
    if not current_user.is_admin:
        abort(403)  # Запрет доступа для не-админов
    return render_template('dashboard.html')
```

## Минификация ресурсов

Пример конфигурации Flask-Assets (`app/assets.py`):
```python
from flask_assets import Bundle, Environment

assets = Environment()

css = Bundle(
    'src/css/*.css',
    filters='cssmin',
    output='dist/css/main.min.css'
)

js = Bundle(
    'src/js/*.js',
    filters='jsmin',
    output='dist/js/main.min.js'
)

assets.register('css_all', css)
assets.register('js_all', js)
```

## Развертывание в production

1. Собрать production-образ:
```bash
docker build -t myflaskapp:prod .
```

2. Запустить через Docker Compose:
```bash
docker-compose -f docker-compose.prod.yml up -d
```

Рекомендуемые настройки для production:
- Использовать WSGI-сервер (Gunicorn)
- Настроить Nginx как reverse proxy
- Использовать production-ready базу данных
- Регулярное резервное копирование данных
- Мониторинг и логирование

## Лицензия

Этот проект распространяется под лицензией MIT. Полный текст лицензии доступен в файле [LICENSE](LICENSE).
