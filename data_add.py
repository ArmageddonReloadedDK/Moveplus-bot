import pandas as pd
from base import base_psql
import psycopg2
import numpy as np

connection = psycopg2.connect(database="Events",
                                   user="postgres",
                                   password="postgres",
                                   host="localhost",
                                   port="5432")
cursor = connection.cursor()



file=pd.read_csv('data.csv', names = ['id', 'family', 'name', 'second_name', 'room', 'group', 'phone', 'vk'])
file=pd.DataFrame(file)
arr=np.array(file)
N=309
for i in range(0,N) :
    print( arr[i])

    cursor.execute(
        ''' insert into public.ev_people (
        p_id,first_name,
        middle_name, family_name,
        group_name, phone,
        telegram_username,   birth_date,
        status, vk_url,
        chat_id)
         values(
         '%s','%s',
         '%s','%s',
         '%s','%s',
         '%s','%s' ,
         '%s','%s',
         '%s')''' %
        (int(arr[i][0]), # айди
         str(arr[i][2]), # имя
         str(arr[i][3]), # отчество
         str(arr[i][1]), # фамилия
         str(arr[i][5]), # группа
         str(arr[i][6]), # телефон
         'None',
         '12.12.1234',
         '2',
         str(arr[i][7]), # вк
         '0'))
connection.commit()
"""    cursor.execute(
        ''' insert into public.ev_people (
        p_id,first_name,
        middle_name, family_name,
        group_name, phone,
        telegram_username,   birth_date,
        status, vk_url,
        chat_id)
         values(
         '%s','%s',
         '%s','%s',
          %s,'%s',
         '%s','%s' ,
         '%s','%s',
         '%s')''' %
        (str(file['id'][i]),
         str(file['name'][i]),
         str(file['second_name'][i]),
         str(file['family'][i]),
         file['group'][i],
         file['phone'][i],
         'None',
         '12.12.1234',
         2,
         str(file['vk'][i]),
         0))"""
