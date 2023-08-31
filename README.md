# Диплом "Продуктовый помощник"
[![Python](https://img.shields.io/badge/python-version?style=plastic&logo=python&labelColor=grey)](https://www.python.org/) [![Django](https://img.shields.io/badge/django-version?style=plastic&logo=django&labelColor=grey)](https://www.djangoproject.com/) [![Django Rest Framework](https://img.shields.io/badge/django_rest_framework-version?style=plastic)](https://www.django-rest-framework.org/) [![Nginx](https://img.shields.io/badge/Nginx-version?style=plastic&logo=Nginx&labelColor=grey)](https://nginx.org/) [![Docker](https://img.shields.io/badge/Docker-version?style=plastic&logo=docker&labelColor=grey)](https://www.docker.com/) [![Postgresql](https://img.shields.io/badge/Postgresql-version?style=plastic&logo=postgresql&labelColor=grey)](https://www.postgresql.org/) [![Gunicorn](https://img.shields.io/badge/Gunicorn-version?style=plastic&logo=Gunicorn&labelColor=grey)](https://gunicorn.org/)
### Домен
##### [![Foodgram](https://relax-foodgram.freedynamicdns.org/favicon.png)](http://relax-foodgram.freedynamicdns.org)
### Технологии
- Python 3.9.10
- Django 3.2.3
- Django rest framework 3.12.4
- Gunicorn 20.1.0
- Djoser 2.1.0
- Psycopg2 binary 2.9.3

### Описание
Сайт по созданию рецептов для приготовления блюд и подписки на авторов
### Возможности
**Для неавторизаванного пользователя**:
- Просмотр страицы рецептов и отдельного рецепта
- Регистрация в приложении

**Для авторизованного пользователя**:
- Вход в систему под своим логином и паролем
- Выход из системы
- Просмотр страицы рецептов и отдельного рецепта
- Создание, редактирование и удаление собственных рецептов
- Просмотр страниц пользователей и подписки/отписка на них
- Фильтрация рецептов по тегам
- Работа с персональным списком покупок: 
добавление и удаление любых рецептов, выгрузка файла с количеством 
необходимых ингредиентов для рецептов из списка покупок
- Работа с персональным списком избранного: 
добавление в него рецептов или удаление их, просмотр своей страницы избранных рецептов

**Для админа**:
- Все права авторизованного пользователя
- Изменение пароля любого пользователя
- Создание, блокировка и удаление аккаунтов пользователей
- Редактирование и удаление любых рецептов
- Добавление, удаление и редактирование ингредиентов
- Добавление, удаление и редактирование тегов


### Docker-контейнеры
- foodgram_frontend
- foodgram_backend
- nginx 1.19.3
- postgres 13.10


### Деплой
Запуск приложения docker.
Создание образов:
```sh
foodgram-project-react$ cd backend
docker build -t имя-пользователя-dockerhub/foodgram_backend .
cd frontend
docker build -t имя-пользователя-dockerhub/foodgram_frontend .
```
Загрузка образов на docker hub:
```
docker push имя-пользователя-dockerhub/foodgram_backend
docker push имя-пользователя-dockerhub/foodgram_frontend
```
На виртуальной машине создать папку **foodgram**.
В эту папку перенести файлы docker-compose.yml, .env, ngingx.conf
Запустить Docker Compose в режиме демона:
```
sudo docker compose -f docker-compose.production.yml up -d 
```
Выполнить миграции, создать суперпользователя, собрать статику, импортировать бд ингредиентов:
```
sudo docker compose -f docker-compose.yml exec backend python manage.py migrate
sudo docker compose -f docker-compose.yml exec backend python manage.py createsuperuser
sudo docker compose -f docker-compose.yml backend python manage.py collectstatic --no-input
sudo docker compose -f docker-compose.yml backend python manage.py import_db
```
### Доступ к админке:
email: petro@mail.ru
password: Infinity2023

### Автор Проекта
Дмитрий Абдурахимов