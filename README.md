![example workflow](https://github.com/cnlis/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)

# Продуктовый помощник (Foodgram)

Docker-контейнеризация c web-сервером Nginx, базой данных Postgres и фронтендом 
на React первой версии API пока еще неизвестной социальной сети для любителей 
вкусной еды **Продуктовый помощник**.
Предоставляет доступ к данным моделей Ingredient, Unit, Tag, Recipe, User, 
IngredientAmount всем пользователям на чтение, аутентифицированным 
по токену пользователям - все перечисленные модели и Subscribe, Follow, 
ShoppingCart на запись и изменение только своих данных 
(кроме моделей Ingredient, Unit, Tag). 
Администраторы имеют все права на чтение и запись, в том числе 
через админ-панель (/admin).

The project has full English internationalization. To enable it change option
LANGUAGE_CODE to 'en' in file backend/foodgram/settings.py.

### Ссылка на приложение **Продуктовый помощник**, запущенное на сервере:
### http://cnlis.ddns.net/

### Полная документация к API в формате ReDoc: 
### http://cnlis.ddns.net/api/docs/

### Технологии вебсайта:
- Python 3.10
- Django 4.0.3
- djangorestframework 3.13.1
- Node.js 13.12
- React 11.1

### Технологии сервера:
- Docker 20.10.13
- docker-compose 1.29.2
- Nginx 1.21.6
- Postgres 13.0

### Как запустить проект:

- Клонировать репозиторий и перейти в него в командной строке:

```console
git clone https://github.com/cnlis/foodgram-project-react.git
```

```console
cd foodgram-project-react/infra
```

- Создать в папке файл .env:
```console
nano .env
```
- Заполнить файл следующими данными:
```
DJANGO_SECRET_KEY=''  # секретный ключ Django
DJANGO_ALLOWED_HOSTS='["localhost"]'  # список хостов в формате JSON
DB_ENGINE=django.db.backends.postgresql # используемая СУБД
DB_NAME=postgres  # название базы данных
POSTGRES_USER=  # имя пользователя БД
POSTGRES_PASSWORD=  # пароль БД
DB_HOST=db  # название сервиса (контейнера)
DB_PORT=5432  # используемый порт БД
```

- Для работы файлов документации скопируйте папку **data/** в корневую папку 
пользователя. 

- Запустить docker-compose:

```console
docker-compose up --build -d
```

- Выполнить миграции базы данных, создать суперпользователя, собрать статику:

```console
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --no-input
```

- Загрузить исходные данные в базу (ингредиенты и единицы измерения):

```console
docker-compose exec web python manage.py loaddata fixtures.json
```
