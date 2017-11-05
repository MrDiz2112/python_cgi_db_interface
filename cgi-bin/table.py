#!/home/mrdiz/anaconda3/bin/python

import sys
sys.path.append("/home/mrdiz/SQL/Lab5(2)")

from utils.site_manager import Manager
import utils.site_template as template

selected_table = Manager.cookie["table"].value

headers_list = Manager.sql_select('column_name', 'information_schema.columns',
                                  "(table_schema='public') AND (table_name='{0}')".format(selected_table))

data_list = Manager.sql_select('*', selected_table)

content_table = template.form_table(data_list, headers_list)

grant_list = Manager.sql_table_grant()
alter_buttons = template.table_alter_buttons(grant_list)

content = """
<h2>Список данных в таблице {0}</h2>
<a href='select_db_tables.py'>Назад</a>
<br><br>
{2}
<br>

{1}""".format(selected_table, content_table, alter_buttons)

template.build_with_content(content)
