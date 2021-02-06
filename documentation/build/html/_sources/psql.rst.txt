
DDL queries
~~~~~~~~~~~

To create databse use those queries:

Ev_people

Code::
 
 CREATE TABLE Ev_People
 (
    p_id serial PRIMARY key,
    first_name varchar(20) not null,
    family_name varchar(20) not null,
    middle_name varchar(20) not null,
    birth_date DATE NOT NULL,
    phone varchar(15) not null unique,
    group_name varchar(10) NOT NULL ,
    telegram_username varchar(50) not null unique,
    vk_url varchar(50) not null,
    chat_id NUMERIC(11),
    status NUMERIC(1) not null default(0) -- 1 - орг, 2 - участник, 0 - человек без роли
	    CONSTRAINT status_values_check CHECK (status=0 OR status=1 OR status=2)
 );


	team_name varchar(40)
 );

Ev_Part

Code::

 CREATE TABLE Ev_Part
 (
    part_id SERIAL PRIMARY KEY,
    person_id integer REFERENCES Ev_People(p_id),
    check_in timestamp,
    arrive_status NUMERIC(1) default(0) NOT NULL --0 - не прибыл, 1 - прибыл, 2 - выехал
	    CONSTRAINT status_values_check CHECK (arrive_status=0 OR arrive_status=1 OR arrive_status=2),
    room_id integer REFERENCES Ev_Rooms(r_id),
    team_id integer references Ev_Teams(t_id)
 );
 
Ev_Org

Code::

 create table Ev_Org
 (
	org_id serial primary key,
	person_id integer REFERENCES Ev_People(p_id),
	web_login varchar(20),
	web_password varchar(20)
 );


Ev_Rooms

Code::

 create table Ev_Rooms
 (
	r_id serial primary key,
	room_num numeric(5) not null,
	room_floor numeric(3),
	room_building varchar(5),
	bed_num numeric(2) not null,
	CHECK (bed_num >= 0),
	bed_num_empty numeric(2) not null
	    constraint empty_bed_check CHECK (bed_num_empty <= bed_num),
	CHECK (bed_num_empty >= 0),
	features varchar(40000)
 );

Ev_Teams

Code::

 create table Ev_Teams
 (
	t_id serial primary key,
	team_name varchar(40)
 );


Ev_Posts

Code::

 create table Ev_Posts
 (
	post_id serial primary key,
	post_name varchar(40) UNIQUE
 );

Ev_Places

Code::

 create table Ev_Places
 (
	place_id serial primary key,
	place_name varchar(100) not null,
    features varchar(40000)
 );

Ev_Requisite

Code::

 create table Ev_Requisite
 (
	req_id serial primary key,
	req_name varchar(20) not null,
	req_amount numeric(5) not null,
	req_description varchar(40000),
	req_owner serial REFERENCES Ev_People(p_id)
	--req_status boolean default false --false - не занят, true - занят
 );

Ev_Events

Code::

 create table Ev_Events
 (
	ev_id serial primary key,
	ev_name varchar(40) not null ,
	event_features varchar(40000)
 );

Ev_person_posts

Code::

 create table Ev_person_posts
 (
	id serial PRIMARY KEY,
	person INTEGER REFERENCES Ev_Org(org_id) ON DELETE CASCADE,
	post INTEGER REFERENCES Ev_Posts(post_id) ON DELETE CASCADE
 );

Ev_Busyness

Code::

 create table Ev_Busyness
 (
	id serial PRIMARY KEY,
	id_person_post INTEGER REFERENCES Ev_person_posts(id) ON DELETE CASCADE,
	id_event INTEGER REFERENCES Ev_Events(ev_id) ON DELETE CASCADE,
	id_team INTEGER REFERENCES Ev_Teams(t_id) ON DELETE CASCADE,
	place_id INTEGER REFERENCES Ev_Places(place_id) ON DELETE CASCADE,
	event_start_time timestamp,
	event_end_time timestamp
 );


Trigger participant_status_check

Code::

 CREATE FUNCTION pr_part_status_check()
 RETURNS trigger as $$
 DECLARE err INTEGER;
    BEGIN
        select count() INTO err FROM Ev_People
            where (status in (1, 2))AND
                  NEW.person_id = p_id;
        if err = 1 then
            RAISE EXCEPTION'Уже существует такой участник или организатор';
        END IF;
        RETURN NEW;
    END;
    $$language plpgsql;

 CREATE TRIGGER tr_part_status_check
    BEFORE INSERT
    ON Ev_Part
    FOR EACH ROW
    EXECUTE PROCEDURE  pr_part_status_check();


Trigger organizator_status_check

Code:: 

 CREATE FUNCTION pr_org_status_check()
 RETURNS trigger as $$
 DECLARE err INTEGER;
    BEGIN
        select count() INTO err FROM Ev_People
            where (status = 1 OR status = 2) AND
                  NEW.person_id = p_id;
        if err = 1 then
            RAISE EXCEPTION'Уже существует такой участник или организатор';
        END IF;
        RETURN NEW;
    END;
    $$language plpgsql;

 CREATE TRIGGER tr_org_status_check
    BEFORE INSERT
    ON Ev_Org
    FOR EACH ROW
    EXECUTE PROCEDURE  pr_org_status_check();
	
ER-Diagram
~~~~~~~~~~

`Link`_

Screenshot

.. image:: /image/er.jpg

.. _Link: https://miro.com/app/board/o9J_kvBZHR0=/

