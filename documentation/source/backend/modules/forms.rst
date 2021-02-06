Django Forms
============



=======Модуль для формирования готовых форм вывода или редактирования для html шаблонов

Подключенные пакеты::

	from django.contrib.auth.models import User # Класс пользователя предоставляемый фреймворком django
	
	from django.contrib.auth.forms import UserCreationForm # Форма для  класса пользователя предоставляемый фреймворком django
	
	from django import forms

Форма регистрации нового пользователя::

	class UserCreateForm(UserCreationForm):

		class Meta:
			model = User
			fields = ("username", "password1", "password2")
