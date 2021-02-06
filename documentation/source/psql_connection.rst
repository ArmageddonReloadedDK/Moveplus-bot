Connection to databases
========================

Postgresql
----------

To connect to Postgresql database in python need to use psycopg2 module::
  
  import psycopg2
  
Second step - creating connection::

   connection = psycopg2.connect(database="Events",
                              user="postgres",
                              password="123",
                              host="localhost",
                              port="5432")
							 
Where:

  1) 'database' - database name

  2) 'user'  - database user username
  
  3) 'password' - user password

  4) 'host' - database ip adress (on local machine ip is 'localhost' or '127.0.0.1' )

  5) 'port' - port, which your Postgresql uses ('5432' by default) 
  

Then creating cursor::

      cursor = connection.cursor() 
	
It uses to send queries to database::
 
    cursor.execute(querry)
	
    connection.commit() # ONLY in case of inserting/updating data in database
    #without this comand no changes will be saved

To get rows from cursor use method fetchall::

  rows=cursor.fetchall()
  

Vedis
-----

To use database import module::

  from vedis import Vedis 

You can work with Vedis like typical list::

    with Vedis(name) as db:
	   db[index]=value
	   
When first value insertes in database python creates special file. His name will be the string,wich you send as input parameter at first commad. In other cases python will use already created file.

.. note:: all returned values from Vedis database have string type

.. warning:: Vedis database file name must be in format 'some_name.db'
