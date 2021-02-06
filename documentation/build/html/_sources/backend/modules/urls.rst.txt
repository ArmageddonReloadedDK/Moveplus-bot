Django urls
===========



Подключаемые пакеты::
	
	from django.conf.urls import url, include
	
	from . import views

Название приложения::

	app_name = 'EventsP'

Список url адресов для всех представлений из views.py

	urlpatterns = [
		url(r'^$', views.MainView.as_view(), name='Homepage'),	 # Главная страница
		
		
		url(r'^register$', views.RegisterFormView.as_view()),	 # Регистрация
		
		url(r'^login$', views.LoginFormView.as_view()),		 	 # Авторизация
		
		url(r'^logout$', views.LogoutView.as_view()),		 	 # Выход из системы
		
		url(r'^json-upload$', views.JSONPartView),			 	 # JSON данные об участнике
		
		url(r'^json-upload-room$', views.JSONRoomView),			 # JSON данные о комнате
		
		url(r'^json-upload-team$', views.JSONTeamView), 	  	 # JSON данные о команде

		url(r'^json-upload-timetable$', views.JSONTimetableView),# JSON данные о расписании


