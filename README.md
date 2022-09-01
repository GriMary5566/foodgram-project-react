# Проект Foodgram
[workflow](https://github.com/GriMary5566/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)

[сайт проекта](http://51.250.100.222/)


## Социальная сеть любителей кулинарии «Продуктовый помощник»

На этом сервисе пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

## requirements

- asgiref==3.2.10
- django==2.2.16
- django-filter==21.1
- djangorestframework==3.12.4
- djangorestframework-simplejwt==4.8.0
- djoser==2.1.0
- drf-extra-fields==3.4.0
- drf-yasg==1.20.0
- gunicorn==20.0.4
- psycopg2-binary==2.8.6
- PyJWT==2.4.0
- Pillow==9.2.0
- python-dotenv==0.20.0
- pytz==2022.1
- sqlparse==0.4.2
- requests==2.26.0

## Основные ресурсы api:

- AUTH - Регистрация пользователей и выдача токенов
- USERS - Пользователи
- TAGS - Теги
- RECIPES - Рецепты
- INGREDIENTS - Ингредиенты

Более подробно см в /api/docs/


## Подготовка и запуск проекта:

### Склонировать репозиторий на локальную машину:

```
git clone https://github.com/GriMary5566/foodgram-project-react

```

### Для работы с удаленным сервером:

- Выполните вход на свой удаленный сервер

- Установите на сервер docker и docker-compose:

- Локально отредактируйте файл infra/nginx.conf и в строке server_name впишите свой IP

- Скопируйте файлы docker-compose.yml и nginx.conf из директории infra на сервер

- Cоздайте .env файл и впишите:

```
B_ENGINE=<django.db.backends.postgresql>
DB_NAME=<имя базы данных postgres>
DB_USER=<пользователь бд>
DB_PASSWORD=<пароль>
DB_HOST=<db>
DB_PORT=<5432>
SECRET_KEY=<секретный ключ проекта django>

```

- Для работы с Workflow добавьте в Secrets GitHub переменные окружения для работы:

```
DB_ENGINE=<django.db.backends.postgresql>
DB_NAME=<имя базы данных postgres>
DB_USER=<пользователь бд>
DB_PASSWORD=<пароль>
DB_HOST=<db>
DB_PORT=<5432>

DOCKER_PASSWORD=<пароль от DockerHub>
DOCKER_USERNAME=<имя пользователя>

SECRET_KEY=<секретный ключ проекта django>

USER=<username для подключения к серверу>
HOST=<IP сервера>
PASSPHRASE=<пароль для сервера, если он установлен>
SSH_KEY=<ваш SSH ключ (для получения команда: cat ~/.ssh/id_rsa)>

TELEGRAM_TO=<ID чата, в который придет сообщение>
TELEGRAM_TOKEN=<токен вашего бота>

```

-   На сервере соберите docker-compose:
    

```
sudo docker-compose up -d --build

```

-   После успешной сборки на сервере выполните команды (только после первого деплоя):
    
    -   Соберите статические файлы:
    
    ```
    sudo docker-compose exec backend python manage.py collectstatic --noinput
    
    ```
    
    -   Примените миграции:
    
    ```
    sudo docker-compose exec backend python manage.py migrate
    
    ```
         
       
    -   Создать суперпользователя Django:
    
    ```
    sudo docker-compose exec backend python manage.py createsuperuser
    
    ```
    
    -   Проект будет доступен по вашему IP



## Авторы проекта:

- Команда Яндекс.Практикума - фронтед, бэкенд(методическое руководство)
- Григорьева Мария - бэкенд