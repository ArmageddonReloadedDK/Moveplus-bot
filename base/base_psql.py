import psycopg2

from .base_vedis import base_vedis_class

vedis=base_vedis_class



class base_psql_class:
    def __init__(self):
        self.connection = psycopg2.connect(database="Events",
                                           user="postgres",
                                           password="postgres",
                                           host="localhost",
                                           port="5432")
        self.cursor = self.connection.cursor()

    def get_db_connection(self):
        return self.connection

    def in_base(self, msg):
        self.cursor.execute(
            '''select p.p_id from public.ev_people p where p.chat_id='%s' ''' % (msg.chat.id))
        rows_info = self.cursor.fetchall()
        if len(rows_info) > 0:
            return True
        else:
            return False

    def inform_state(self, msg):
        self.cursor.execute(
            '''select p.chat_id from ev_people p, spec s where p.p_id=s.spec_id and s.inform=TRUE and p.chat_id='%s' ''' % (
                msg.chat.id))
        rows_info = self.cursor.fetchall()
        if len(rows_info) > 0:
            return True
        else:
            return False

    def work_type(self, msg, x):
        self.cursor.execute(
            '''select p.p_id from ev_people p where p.chat_id='%s' and p.status='%s' ''' % (msg.chat.id, x))
        rows_info = self.cursor.fetchall()
        if len(rows_info) > 0:
            return True
        else:
            return False

    def reg_type(self, msg):
        self.cursor.execute(
            '''select o.regist from ev_people p,organizators o where p.chat_id='%s' and o.org_id=p.p_id and p.status='%s' ''' % (
                msg.chat.id, 1))
        rows = self.cursor.fetchall()
        return rows[0][0]

    def insert_new(self, msg):
        self.cursor.execute(
            ''' insert into public.ev_people (first_name, middle_name, family_name, group_name, phone, telegram_username,   birth_date, status, vk_url, chat_id)
             values('%s','%s','%s','%s',%s,'%s','%s',default ,'%s','%s')''' % (
               vedis.get_var(msg.chat.id, 'Name'),vedis.get_var(msg.chat.id, 'Middle'),
               vedis.get_var(msg.chat.id, 'Family'),vedis.get_var(msg.chat.id, 'Group'),
               vedis.get_var(msg.chat.id, 'Phone'),vedis.get_var(msg.chat.id, 'Username'),
               vedis.get_var(msg.chat.id, 'Date'),vedis.get_var(msg.chat.id, 'VK'),
               vedis.get_var(msg.chat.id, 'Chatid')))
        self.connection.commit()
    def registraion_change(self, status, chat_id):
        self.cursor.execute(
            ''' update organizators set regist='%s' 
                where org_id=(select p.p_id 
                              from ev_people p 
                              where p.chat_id='%s') ''' % (
                status,
                chat_id))
        self.connection.commit()

    def check_out_change(self, status, chat_id):
        self.cursor.execute(
            ''' update organizators set check_out='%s' 
                where org_id=(select p.p_id 
                              from ev_people p 
                              where p.chat_id='%s') ''' % (
                status,
                chat_id))
        self.connection.commit()
