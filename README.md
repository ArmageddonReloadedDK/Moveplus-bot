# Move_plus telegram-bot

Это бот для помощи при организациии мероприятий на платформе Move_pus.

Установка
=========

Для начала работы нужно создать базу данных.

1) Установите PostgreSQL

2) создайте базу данных и пользователя
   ```shell script
   create user with encrypted password "password"
   create database database_name
   ```
    
3) установите python версии 2.7 либо установите [anaconda](https://www.anaconda.com/products/individual)
 и создайте глобальное окружение 
    ```shell script
    conda create -n env_name python=3.6
    ```
4) установите необходимые модули для python
    ```shell script
    activate env_name #если используете окружение анаконды
    pip install pyTelegramBotAPI
    pip install cython vedis
    pip install psycopg2
    pip install pillow
    ```

В данном проекте задействована библиотека  [Vedis](https://vedis-python.readthedocs.io/en/latest/), которая является продолжением базы данных вида ключ-значение Redis 

Благодарности
-------------

Отдельная благодарность Л.Авагян, Л.Миракян за помощь во время дебага бота.