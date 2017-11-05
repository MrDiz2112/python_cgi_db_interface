#!/home/mrdiz/anaconda3/bin/python

import sys
sys.path.append("/home/mrdiz/SQL/Lab5(2)")

import cgi
import html

from utils.site_manager import Manager
import utils.site_template as template

selected_table = Manager.cookie["table"].value

headers_list = Manager.sql_select('column_name, data_type', 'information_schema.columns',
                                  "(table_schema='public') AND (table_name='{0}')".format(selected_table))

headers_value_type_list = []

form = cgi.FieldStorage()

for item in headers_list:
    value = form.getfirst(item[0])
    type = item[1]
    value = html.escape(value)
    header = item[0]

    list_item = (header, value, type)

    headers_value_type_list.append(list_item)

Manager.sql_update(selected_table, headers_value_type_list)

template.redirect('table_update.py')
