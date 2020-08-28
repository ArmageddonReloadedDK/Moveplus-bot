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
3) Создайту базу данных, выполнив транзакцию в файле db_creation_tr

4) установите python версии 2.7 и выше либо установите [anaconda](https://www.anaconda.com/products/individual), нажав при установке Add to global PATH, 
 и создайте глобальное окружение 
    ```shell script
    conda create -n env_name python=3.6
    ```
5) установите необходимые модули для python
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
