# Проект Async API

[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![PostgreSQL](https://img.shields.io/badge/-ElasticSearch-464646?style=flat-square&logo=ElasticSearch)](https://www.elastic.co/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![Nginx](https://img.shields.io/badge/-FastApi-464646?style=flat-square&logo=FastApi)](https://fastapi.tiangolo.com/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)

## Системные требования
______

- [Python 3](https://www.python.org/)
- [Django 3.2](https://www.djangoproject.com/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Elasticsearch](https://www.elastic.co/)
- [NGINX](https://www.nginx.com/)
- [Gunicorn](https://gunicorn.org/)
- [Docker](https://www.docker.com/)
- [PostgrSQL](https://www.postgresql.org/)

## Для запуска проекта необходимо:
- Из корня проекта выполните команду `cp .env.sample .env`
- Добавьте в .env настройки базы данных
```
DB_NAME=movies_database
DB_USER=app
DB_PASSWORD=123qwe
DB_HOST=db
DB_PORT=5432
```
- Собираем проект `docker-compose build`
- Для запуска используйте команду `docker-compose up`

## Накатывание фикстур по умолчанию:
- Необходимо попасть в контейнер `docker exec -it movies_web sh`
- Выполнить команду `python manage.py loaddata fixtures/db.json`
