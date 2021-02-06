Django models
=============



Модуль отвечающий за связь между сущностями в базе данных(таблицами) и веб-приложением

Интерпретирует данные базы данных как объекты классов.

Необходимые пакеты::

	 # Содержит базовый класс для наследования каждой модели

	from django.db import models
	
Документация о `моделях`_

.. _моделях: https://docs.djangoproject.com/en/3.0/topics/db/models/

Класс модели "Человек" - Person::

	class Person(models.Model):
    
	# Словарь для поля с выпадающим списком
    
	choice_status_list = (
    
		(0, 'Без статуса'),

        (1, 'Организатор'),

        (2, 'Участник'),
    
	)
    
	# id человека
    
	p_id = models.AutoField(primary_key=True)
    
	# Поле имени
    
	# max_length - максимальная длинна записи
    
	# verbose_name - отображаемое имя
    
	# unique - атрибут для каждой записи уникален
    
	# blank - возможность атрибута иметь неопределенное значение
    
	# null -  возможность записать в базу данных неопределенное значение
    
	# choices - выпадающий список
    
	middle_name = models.CharField(max_length=20, verbose_name='Фамилия')
    
	first_name = models.CharField(max_length=20, verbose_name='Имя')
    
	family_name = models.CharField(max_length=20, verbose_name='Отчество')
    
	phone = models.CharField(unique=True, max_length=15, verbose_name='Телефон')
    
	group_name = models.CharField(max_length=10, blank=True, null=True, verbose_name='Номер группы')
    
	telegram_id = models.CharField(unique=True, max_length=50, verbose_name='Телеграм id')
    
	vk_url = models.CharField(max_length=50, verbose_name='VK')
    
	status = models.SmallIntegerField(default=0, verbose_name='Статус', choices=choice_status_list)

    # Вложенный класс определяет связь между моделью и сущностью внутри базы данных
    
	class Meta:
    
		managed = True  # изменения модели влекут за собой изменения сущности в базе данных

        db_table = 'ev_people'  # связанная таблица


    # Специальный метод для отображения ФИО целиком

    def i_name(self):

        return self.middle_name + ' ' + self.first_name + ' ' + self.family_name

    
    # Краткое название метода

    i_name.short_description = 'ФИО'

В некоторых  классах моделей введены дполнительные проверки на значения вводимые в базу данных.