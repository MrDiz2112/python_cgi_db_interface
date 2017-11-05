import sys
sys.path.append("/home/mrdiz/SQL/Lab5(2)")

import os
import psycopg2
import http.cookies
import utils.site_template as template

class Manager:

    connect_args_tmp = "dbname='{0}' user='{1}' host='localhost' password='{2}'"
    cookie = http.cookies.SimpleCookie(os.environ.get("HTTP_COOKIE"))

    @staticmethod
    def sql_login(user, password):
        connect_args = Manager.connect_args_tmp.format('postgres', user, password)
        cookie = Manager.cookie

        try:
            connect = psycopg2.connect(connect_args)
            cookie["user"] = user
            cookie["password"] = password
            connect.close()
            print(cookie)
            template.redirect('../cgi-bin/select_db.py')
        except:
            template.redirect('../cgi-bin/user_login_error.py')


    @staticmethod
    def sql_db_list():
        cookie = Manager.cookie
        connect_args = Manager.connect_args_tmp.format('postgres',
                                                       cookie["user"].value,
                                                       cookie["password"].value)

        db_list = []

        with psycopg2.connect(connect_args) as connect:
            with connect.cursor() as cursor:
                sql_command = "SELECT datname FROM pg_database WHERE datistemplate = false;"
                cursor.execute(sql_command)

                db_list = cursor.fetchall()
                connect.commit()


        return db_list


    @staticmethod
    def sql_db_tables_list(db):
        cookie = Manager.cookie
        connect_args = Manager.connect_args_tmp.format(db,
                                                       cookie["user"].value,
                                                       cookie["password"].value)

        tables_list = []

        with psycopg2.connect(connect_args) as connect:
            with connect.cursor() as cursor:
                sql_command = """SELECT table_name 
                FROM information_schema.tables  
                WHERE (table_schema='public');"""

                cursor.execute(sql_command)
                tables_list = cursor.fetchall()

                for item in tables_list.copy():
                    sql_command = """SELECT has_table_privilege('{0}', 'select')""".format(item[0])
                    cursor.execute(sql_command)

                    hasGrant = cursor.fetchall()
                    hasGrant = hasGrant[0][0]

                    if not hasGrant:
                        tables_list.remove(item)


                connect.commit()

        return tables_list


    @staticmethod
    def sql_is_user_su():
        cookie = Manager.cookie
        connect_args = Manager.connect_args_tmp.format(cookie["database"].value,
                                                       cookie["user"].value,
                                                       cookie["password"].value)

        sql_command = "SELECT usesuper FROM pg_user WHERE usename = current_user;"

        is_su = []

        with psycopg2.connect(connect_args) as connect:
            with connect.cursor() as cursor:
                cursor.execute(sql_command)

                is_su = cursor.fetchall()
                is_su = is_su[0][0]

                connect.commit()

        return is_su


    @staticmethod
    def sql_create_db(db_name):
        cookie = Manager.cookie
        connect_args = Manager.connect_args_tmp.format(cookie["database"].value,
                                                       cookie["user"].value,
                                                       cookie["password"].value)

        sql_command = "CREATE DATABASE {0};".format(db_name)

        with psycopg2.connect(connect_args) as connect:
            with connect.cursor() as cursor:
                cursor.execute(sql_command)
                connect.commit()


    @staticmethod
    def sql_user_table_grants(user, table):
        cookie = Manager.cookie
        connect_args = Manager.connect_args_tmp.format(cookie["database"].value,
                                                       cookie["user"].value,
                                                       cookie["password"].value)

        grant_list = []

        with psycopg2.connect(connect_args) as connect:
            with connect.cursor() as cursor:
                sql_command = """SELECT has_table_privilege('{0}', '{1}', 'select') AS has_select,
                        has_table_privilege('{0}', '{1}', 'insert') AS has_insert,
                        has_table_privilege('{0}', '{1}', 'update') AS has_update,
                        has_table_privilege('{0}', '{1}', 'delete') AS has_delete;
                        """.format(user, table)

                cursor.execute(sql_command)
                grant_list = cursor.fetchall()

                grant_list = grant_list[0]

                connect.commit()

        return grant_list


    @staticmethod
    def sql_table_grant():
        cookie = Manager.cookie
        connect_args = Manager.connect_args_tmp.format(cookie["database"].value,
                                                       cookie["user"].value,
                                                       cookie["password"].value)

        grant_list = []

        with psycopg2.connect(connect_args) as connect:
            with connect.cursor() as cursor:
                sql_command = """SELECT has_table_privilege('{0}', '{1}', 'insert') AS has_insert,
                has_table_privilege('{0}', '{1}', 'update') AS has_update,
                has_table_privilege('{0}', '{1}', 'delete') AS has_delete;
                """.format(cookie["user"].value, cookie["table"].value)

                cursor.execute(sql_command)
                grant_list = cursor.fetchall()

                grant_list = grant_list[0]

                connect.commit()

        return grant_list


    @staticmethod
    def sql_set_grants(grants_list):
        cookie = Manager.cookie
        connect_args = Manager.connect_args_tmp.format(cookie["database"].value,
                                                       cookie["user"].value,
                                                       cookie["password"].value)

        selected_user = cookie["user_grants"].value
        selected_table = cookie["table_grants"].value

        sql_grant_cmd = "GRANT {0} ON TABLE {1} TO {2};"
        sql_revoke_cmd = "REVOKE {0} ON TABLE {1} FROM {2};"
        sql_command = ''

        with psycopg2.connect(connect_args) as connect:
            with connect.cursor() as cursor:
                for i, item in enumerate(grants_list):
                    if i == 0:
                        if item:
                            sql_command = sql_grant_cmd.format('SELECT', selected_table, selected_user)
                        else:
                            sql_command = sql_revoke_cmd.format('SELECT', selected_table, selected_user)
                    elif i == 1:
                        if item:
                            sql_command = sql_grant_cmd.format('INSERT', selected_table, selected_user)
                        else:
                            sql_command = sql_revoke_cmd.format('INSERT', selected_table, selected_user)
                    elif i == 2:
                        if item:
                            sql_command = sql_grant_cmd.format('UPDATE', selected_table, selected_user)
                        else:
                            sql_command = sql_revoke_cmd.format('UPDATE', selected_table, selected_user)
                    elif i == 3:
                        if item:
                            sql_command = sql_grant_cmd.format('DELETE', selected_table, selected_user)
                        else:
                            sql_command = sql_revoke_cmd.format('DELETE', selected_table, selected_user)

                    cursor.execute(sql_command)
                    connect.commit()



    @staticmethod
    def sql_select(columns, tables, where_stmt=None):
        cookie = Manager.cookie
        connect_args = Manager.connect_args_tmp.format(cookie["database"].value,
                                                       cookie["user"].value,
                                                       cookie["password"].value)

        data_list = []

        with psycopg2.connect(connect_args) as connect:
            with connect.cursor() as cursor:

                if not where_stmt:
                    sql_command = "SELECT {0} FROM {1};".format(columns, tables)
                else:
                    sql_command = "SELECT {0} FROM {1} WHERE {2};".format(columns,
                                                                          tables,
                                                                          where_stmt)

                cursor.execute(sql_command)
                data_list = cursor.fetchall()

                connect.commit()

        return data_list


    @staticmethod
    def sql_insert(table, values):
        cookie = Manager.cookie
        connect_args = Manager.connect_args_tmp.format(cookie["database"].value,
                                                       cookie["user"].value,
                                                       cookie["password"].value)

        sql_command = "INSERT INTO {0} VALUES ({1});"
        values_str = ""

        for i, item in enumerate(values):
            item_str = ''

            if item[1] == 'character varying':
                item_str += "'" + item[0] + "'"
            else:
                item_str += item[0]

            if i < len(values)-1:
                values_str += item_str + ", "
            else:
                values_str += item_str

        sql_command = sql_command.format(table, values_str)

        with psycopg2.connect(connect_args) as connect:
            with connect.cursor() as cursor:
                cursor.execute(sql_command)
                connect.commit()


    @staticmethod
    def sql_update(table, header_value_type_list):
        cookie = Manager.cookie
        connect_args = Manager.connect_args_tmp.format(cookie["database"].value,
                                                       cookie["user"].value,
                                                       cookie["password"].value)

        sql_command = "UPDATE {0} SET {1} WHERE {2};"
        set_params = ""

        for i, item in enumerate(header_value_type_list):
            item_str = ''

            if item[2] == 'character varying':
                item_str += item[0] + "='" + item[1] + "'"
            else:
                item_str += item[0] + '=' + item[1]

            if i < len(header_value_type_list)-1:
                set_params += item_str + ", "
            else:
                set_params += item_str

        column = Manager.cookie["pk_column"].value
        row = Manager.cookie["selected_row"].value
        where_stmt = "{0} = {1}".format(column, row)

        sql_command = sql_command.format(table, set_params, where_stmt)

        with psycopg2.connect(connect_args) as connect:
            with connect.cursor() as cursor:

                cursor.execute(sql_command)
                connect.commit()


    @staticmethod
    def sql_delete(table, pk_column, row):
        cookie = Manager.cookie
        connect_args = Manager.connect_args_tmp.format(cookie["database"].value,
                                                       cookie["user"].value,
                                                       cookie["password"].value)

        sql_command = "DELETE FROM {0} WHERE {1};"
        where_stmt = "{0} = {1}".format(pk_column, row)

        sql_command = sql_command.format(table, where_stmt)

        with psycopg2.connect(connect_args) as connect:
            with connect.cursor() as cursor:
                cursor.execute(sql_command)
                connect.commit()
