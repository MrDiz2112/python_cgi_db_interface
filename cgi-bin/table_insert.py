#!/home/mrdiz/anaconda3/bin/python

import sys
sys.path.append("/home/mrdiz/SQL/Lab5(2)")

from utils.site_manager import Manager
import utils.site_template as template

selected_table = Manager.cookie["table"].value

headers_list = Manager.sql_select('column_name, column_default', 'information_schema.columns',
                                  "(table_schema='public') AND (table_name='{0}')".format(selected_table))


form_list = template.table_insert_form(headers_list)

content = """
<h2>Добавление данных в таблицу {0}</h2>
<p><a href='table.py'>Назад</a></p>
<p>Заполните поля, чтобы добавить строку</p>
{1}""".format(selected_table, form_list)

template.build_with_content(content)
