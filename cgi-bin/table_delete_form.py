#!/home/mrdiz/anaconda3/bin/python

import sys
sys.path.append("/home/mrdiz/SQL/Lab5(2)")

import re
import cgi

from utils.site_manager import Manager
import utils.site_template as template

form = cgi.FieldStorage()

selected_table = Manager.cookie["table"].value
selected_row = form.getfirst('row_delete')

headers_list = Manager.sql_select('column_name, column_default', 'information_schema.columns',
                                  "(table_schema='public') AND (table_name='{0}')".format(selected_table))

re_match = r"nextval\('.*'::regclass\)"
pk_column = ''

for item in headers_list:
    res = re.search(re_match, str(item[1]))

    if res:
        pk_column = item[0]
        break

Manager.sql_delete(selected_table, pk_column, selected_row)

template.redirect('table_delete.py')
