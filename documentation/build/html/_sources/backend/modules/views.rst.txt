Django views
============



Модуль отвечающий за формирование http ответа. 

Документация по 'представлениям'_

.. _представлениям: https://docs.djangoproject.com/en/3.0/topics/http/views/

Самое важное: djnago предоставляет программисту две возможности формировать представления. Как функции представлений и как Class-Based представления, то есть представления в основе которых лежат классы django

Пакеты, которые я использовал::
		
	#Для отправки на веб страницу готовых форм
	
	from django.views.generic.edit import FormView

	from django.views.generic import TemplateView

	# для формирования ответов перенаправлений

	from django.http import HttpResponseRedirect
	
	# Базовый класс представления
	
	from django.views.generic.base import View
	
	from django.contrib.auth import logout
	
	# Форма для регистрации новых пользователей
	
	from .forms import UserCreateForm
	
	# Все модели для формирования объектов наших классов-моделей и построения запросов к базе данных

	from . import models

	# Пакет для авторизации пользователей форма авторизации
	
	from django.contrib.auth.forms import AuthenticationForm

	from django.contrib.auth import login
		
	# для формирования ответа в формате json 

	from django.http import JsonResponse

	from django.http import HttpResponse
	
	# Классы сериализаторы

	from .serializers import ParticipantSerializer, RoomSerializer, TeamSerializer, TimetableSerializer

	import json
	
Основные представления
-----------------------

Class-Based представление для отображения главной страницы::
	
	class MainView(TemplateView):
    
		# Html шаблон
		
		template_name = 'ajax.html'
    
		participant_form = PartForm
		
Class-Based представление для отображения страницы регистрации::

	class RegisterFormView(FormView):
		
		form_class = UserCreateForm
		
		success_url = "/events/login"
		
		template_name = "register.html"


    def form_valid(self, form):
        
		form.save()
       
	   return super(RegisterFormView, self).form_valid(form)


    def form_invalid(self, form):
       
	   return super(RegisterFormView, self).form_invalid(form)

Class-Based представление для отображения страницы авторизации::

	class LoginFormView(FormView):
		
		form_class = AuthenticationForm
		
		template_name = "login.html"

    success_url = "/events/"

    def form_valid(self, form):
       
	   # Получаем объект пользователя на основе введённых в форму данных.
       
	   self.user = form.get_user()
       
	   # Выполняем аутентификацию пользователя.
        
		login(self.request, self.user)
       
	   return super(LoginFormView, self).form_valid(form)

Class-Based представление для возможности пользователя выйти из системы::

	class LogoutView(View):
    
	def get(self, request):
     
		logout(request)
    
		return HttpResponseRedirect("/events/")

Возвращающие JSON представления
-----------------------

Функция представления данных об участнике/участниках::

	def JSONPartView(request):
	
		if request.method == 'GET': # При методе запроса GET вернём данные
	
			if request.user.is_authenticated:
			
				# переменная с текстом запроса к базе данных 
			
				query = "SELECT *
			
				FROM\
			
				ev_people as p, \
			
				ev_Part as part \
			
				LEFT OUTER JOIN ev_rooms as r\
				
				ON part.room_id = r.r_id\
				
				LEFT OUTER JOIN ev_teams as t\
				
                ON part.team_id = t.t_id\
				
				WHERE\
			
				part.person_ptr_id = p.p_id;"
			
				participants = models.Person.objects.raw(query)
			
				serializer = ParticipantSerializer(participants, many=True)
			
				return JsonResponse(serializer.data, safe=False)
			
		elif request.method == 'POST': # При методе запроса POST добавим данные в таблицу
	
			if request.is_ajax(): # Проверка, что это именно ajax запрос
		
				# Получаем данные из запроса и формируем объект нужного класса-модели
				
				data = json.loads(request.body) 
			
				person = models.Participant.objects.get(p_id=data['p_id'])
			
				person.first_name = data['first_name']
			
				person.middle_name = data['middle_name']
			
				person.family_name = data['family_name']
			
				person.phone = data['phone']
			
				person.group_name = data['group_name']
			
				person.vk_url = data['vk_url']
			
				person.birth_date = data['birth_date'].split('T')[0]
						
				person.arrive_status = data['arrive_status']
				
			# Проверка на пустую строку нужна потому, что при создании объекта связанных моделей, например Участник-комната
			
			# Подразумевает, что атрибут room(комната) у участника будет являться текстовым указателем на определенный объект класса комната
			
			# Поэтому при попытке добавить пустое значение, мы будем получать ошибку, т.к. строка вернувшаяся с сервера не является указателем
				
            if data['room'] != '':
                
				room = models.Room.objects.get(r_id=data['room'])
                
				person.room = room
			
            if data['team'] != '':
			
                team = models.Team.objects.get(t_id=data['team'])
				
                person.team = team
				
            person.save() # сохраняем в базу данных новый или измененный объект класса участник
			
            return HttpResponse(status=201) 
			
        else:
					
            return HttpResponse(status=400) # Если форма некорректна - пользователь получит ошибку с кодом 400

Функция представления данных о комнате/комнатах::

	def JSONRoomView(request):
		
		if request.method == 'GET':
		
		if request.user.is_authenticated:

				query = 'SELECT r_id, room_num, bed_num\

                     FROM ev_rooms\

                            LEFT OUTER JOIN (\

                                SELECT room_id, count(*) as c\

                                FROM ev_part\

                                WHERE room_id IS NOT NULL\

                                GROUP BY room_id) A ON ev_rooms.r_id = A.room_id\

                     WHERE bed_num > COALESCE(A.c, 0);'

            rooms = models.Room.objects.raw(query)

            serializer = RoomSerializer(rooms, many=True)

            return JsonResponse(serializer.data, safe=False)

Функция представления данных об команде/командах::

	def JSONTeamView(request):

		if request.method == 'GET':

			if request.user.is_authenticated:

				rooms = models.Team.objects.all()

				serializer = TeamSerializer(rooms, many=True)

				return JsonResponse(serializer.data, safe=False)

Функция представления данных о расписании::

	def JSONTimetableView(request):

		if request.method == "GET":

			if request.user.is_authenticated:

				query = "SELECT ev_timetable.event_start_time,\

				ev_timetable.event_end_time,\

				ev_timetable.id,\

				Ev_People.first_name,\

				Ev_People.middle_name,\

				Ev_People.family_name,\

				ev_posts.post_name,\

				Ev_Posts.post_id,\

				Ev_Places.place_id,\

				Ev_Places.place_name,\

				Ev_Events.ev_id,\

				Ev_Events.ev_name,\

				Ev_Teams.team_name,\

				Ev_Teams.t_id\

				FROM ev_timetable\

					LEFT JOIN ev_person_posts as pp ON ev_timetable.id_person_post = pp.id\

					LEFT JOIN ev_org ON pp.org_id = Ev_Org.org_id\

					LEFT JOIN ev_posts ON pp.id_post = Ev_Posts.post_id\

					LEFT JOIN ev_people ON Ev_Org.person_ptr_id = Ev_People.p_id\

					LEFT OUTER JOIN ev_places ON ev_timetable.id_place = Ev_Places.place_id\

					LEFT OUTER JOIN ev_teams ON ev_timetable.id_team = ev_teams.t_id\

					LEFT JOIN ev_events ON ev_timetable.id_event = Ev_Events.ev_id;"

				timetable = models.Timetable.objects.raw(query)

				serializer = TimetableSerializer(timetable, many=True)

				return JsonResponse(serializer.data, safe=False)



