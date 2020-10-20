import pandas as pd
from base import base_psql
import psycopg2
import re
import numpy as np

connection = psycopg2.connect(database="Events",
                              user="postgres",
                              password="postgres",
                              host="localhost",
                              port="5432")
cursor = connection.cursor()

file = pd.ExcelFile('rooms.xlsx')
data = file.parse('sheet')  # num and people
data_new = {'num': [], 'family': [], 'name': [], 'second_name': [],'count':[]}
df = pd.DataFrame(data_new)
n = len(data)
for i in range(n):

    x = str(data['num'][i])
    x = re.sub(r'\([^()]*\)', '', x)
    fios = str(data['people'][i])
    fios = fios.split('\n')

    for k in range(len(fios)):

        fio_elem = fios[k].split(' ')
        try:
            fio_elem.remove('')
        except Exception:
            pass
        fios[k] = fio_elem
    for r, fio in enumerate(fios):
        print(fio)
        print(len(fio))
        if len(fio) == 3:
            df = df.append({'num': x, 'family': fio[0], 'name': fio[1], 'second_name': fio[2],'count': len(fio)},
                           ignore_index=True)
        else:
            df = df.append({'num': x, 'family': fio[0], 'name': fio[1], 'second_name':'nan','count': len(fio)},
                           ignore_index=True)

N = len(df)
for i in range(N):
  if df['count'][i]==3:
        cursor.execute(
            ''' insert into participants (part_id, room) 
                select p.p_id,'%s' 
                from ev_people p 
                where (select similarity(p.family_name,'%s'))>0.1 and
                       (select similarity(p.first_name,'%s'))>0.1 and 
                       (select similarity(p.middle_name,'%s'))>0.1 and     not exists(select e.*
                                                                                  from ev_people e,participants p2
                                                                                  where p2.part_id=e.p_id and 
                                                                                  p.family_name=e.family_name and 
                                                                                  p.first_name=e.first_name and 
                                                                                  p.middle_name=e.middle_name)
                                 '''
            % (
                str(df['num'][i]),
                str(df['family'][i]),
                str(df['name'][i]),
                str(df['second_name'][i])))
        connection.commit()
  else:
      cursor.execute(
          ''' insert into participants (part_id, room) 
              select p.p_id,'%s' 
              from ev_people p 
              where (select similarity(p.family_name,'%s'))>0.1 and
                     (select similarity(p.first_name,'%s'))>0.1 and  not exists(select e.*
                                                                                  from ev_people e,participants p2
                                                                                  where p2.part_id=e.p_id and 
                                                                                  p.family_name=e.family_name and 
                                                                                  p.first_name=e.first_name 
                                                                                  )
          '''
          % (
              str(df['num'][i]),
              str(df['family'][i]),
              str(df['name'][i])))
      connection.commit()




"""
for i in range(N):
  if df['count'][i]==3:
        cursor.execute(
            ''' insert into participants (part_id, room) 
                select p.p_id,'%s' 
                from ev_people p 
                where (select similarity(p.family_name,'%s'))>0.2 and
                       (select similarity(p.first_name,'%s'))>0.2 and 
                       (select similarity(p.middle_name,'%s'))>0.2 
            '''
            % (
                str(df['num'][i]),
                str(df['family'][i]),
                str(df['name'][i]),
                str(df['second_name'][i])))
        connection.commit()
  else:
      cursor.execute(
          ''' insert into participants (part_id, room) 
              select p.p_id,'%s' 
              from ev_people p 
              where (select similarity(p.family_name,'%s'))>0.2 and
                     (select similarity(p.first_name,'%s'))>0.2 
          '''
          % (
              str(df['num'][i]),
              str(df['family'][i]),
              str(df['name'][i])))
      connection.commit()

"""
