# yandex-rest-task
### Второе вступительное задание (REST API)
***
#### Общая информация

#### Внешние зависимости: 
```python
asgiref==3.3.1
Django==3.1.7
django-filter==2.4.0
djangorestframework==3.12.2
Markdown==3.3.4
mysqlclient==2.0.3
pytz==2021.1
sqlparse==0.4.1
```
#### Развертывание:
1. Скачать репозиторий и перенести файлы на свою машину (или сервер);
2. Установить Python версии, не ниже 3.8  
``$ sudo apt-get install python3``
3. Создать виртуальное окружение (удалив старое)  
``$ rm -rf venv``  
``$ python3 -m venv venv`` 
4. Подключить виртуальное оокружение
``$ source venv/bin/activate``   
5. Установить внешние зависимости в виртуальное окружение  
``$ pip3 install -r requirements.txt``
6. Установить MySQL (версии 8) на сервер  
``$ sudo apt install mysql-server mysql-client``
7. Произвести первоначальную настройку БД  
``$ sudo mysql_secure_installation``  
8. Создать базу данных и специального пользователя для rest  
```mysql
CREATE DATABASE <database>; # <имя_базы>
CREATE USER 'username'@'localhost' IDENTIFIED BY 'password';
GRANT USAGE ON *.* TO 'username'@'localhost';
GRANT ALL PRIVILEGES ON <database>.* TO 'username'@'localhost';
```
9. В `rest/rest/settings.py` сконфигурировать настройки БД
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '127.0.0.1',
        'NAME': "<database>",
        'USER': 'username',
        'PASSWORD': 'password',
    },
}
```
10. Провести миграции в БД  
``$ python3 manage.py migrate``
11. Запустить решение  
``$ python3 manage.py runserver 0.0.0.0:80``
>Для запуска тестов используйте    
``$ python3 manage.py test``





