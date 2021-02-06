Django adminministration
========================



Основной модуль для работы приложения администрирования

Обрабатывает модели из model.py
   
Необходимые пакеты::

	from django.contrib import admin # для работы с моделями
	
	django.contrib import messages # для обработки вывода сообщений

	from abc import ABC # для обработчика события фильтрации
	
	from . import models # все модели из проекта

Возможности `ModelAdmin`_

.. _ModelAdmin: https://docs.djangoproject.com/en/3.0/ref/contrib/admin/

Класс управления моделью "Человек" - PersonAdmin::

	class PersonAdmin(admin.ModelAdmin, RemoveAdminDefaultMessageMixin):
	
	# Список отображаемых полей
	
    list_display = [models.Person.i_name,'phone','group_name','telegram_id',
	
	'vk_url','birth_date','check_in','arrive_status','room','team',]
    
	exclude = ['status'] # Поля запрещенные к редактированию
	
	# Список фильтров, доступных пользователю
	
    list_filter = [('group_name', custom_titled_filter('Номер группы')),
	
                   ('arrive_status', custom_titled_filter('Статус прибытия')),
				   
                   ('room', custom_titled_filter('Номер комнаты')),
				   
                   ('team', custom_titled_filter('Команда'))]
	
	# Поля по которым организован поиск
				   				   
    search_fields = [field.name for field in models.Person._meta.fields] 

Методы класса PersonAdmin::
	
	def get_readonly_fields(self, request, obj=None): # Задаём полю "статус" режим "только чтение"
        
	if obj:  # when editing an object
        
		return ['status']

    return self.readonly_fields

	# Метод для сохранения модели с
	
	# проверкой на заполненность комнаты (по количеству мест в комнате)
		
	# И вывод сообщения об ошибке
	
	def save_model(self, request, obj, form, change): 
	
	  tmp = models.Participant.objects.filter(room=obj.room)

        rooms = models.Room.objects.filter(r_id=obj.room.r_id)

        if tmp.exists():

            for room in rooms:

                if len(tmp) < room.bed_num:

                    super().save_model(request, obj, form, change)

                else:

                    messages.error(request, 'В комнате заняты все места')

        else:

            super().save_model(request, obj, form, change)


    class Meta:

        model = models.Participant

	# Регистрация модели в django-admin
	 
	admin.site.register(models.Participant, PersonAdmin)