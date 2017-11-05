#!/home/mrdiz/anaconda3/bin/python

import sys
sys.path.append("/home/mrdiz/SQL/Lab5(2)")

import re
import cgi

from utils.site_manager import Manager
import utils.site_template as template

form = cgi.FieldStorage()

selected_table = Manager.cookie["table"].value
selected_row = form.getfirst('row_update')

headers_list = Manager.sql_select('column_name, column_default', 'information_schema.columns',
                                  "(table_schema='public') AND (table_name='{0}')".format(selected_table))

re_match = r"nextval\('.*'::regclass\)"
pk_column = ''

for item in headers_list:
    res = re.search(re_match, str(item[1]))

    if res:
        pk_column = item[0]
        break

Manager.cookie["pk_column"] = pk_column
Manager.cookie["selected_row"] = selected_row
print(Manager.cookie)

headers_list_new = []

for item in headers_list:
    headers_list_new.append(item[0])

data_list = Manager.sql_select('*',
                               selected_table,
                               "{0} = {1}".format(pk_column, selected_row))

form_list = template.table_update_form(headers_list_new, data_list[0], pk_column)

content = """
<h2>Изменение данных в строке с PK {0}</h2>
<p><a href='table_update.py'>Назад</a></p>
<p>Измените данные в строке</p>
{1}""".format(selected_row, form_list)

template.build_with_content(content)
