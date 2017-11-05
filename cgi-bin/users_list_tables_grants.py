#!/home/mrdiz/anaconda3/bin/python

import sys
sys.path.append("/home/mrdiz/SQL/Lab5(2)")

from utils.site_manager import Manager
import utils.site_template as template

selected_table = Manager.cookie["table_grants"].value
selected_user = Manager.cookie["user_grants"].value

grants_list = Manager.sql_user_table_grants(selected_user, selected_table)

grants_list_form = template.user_table_grants(grants_list)

content = """
<h2>Список привилегий пользователя {0} в таблице {1}</h2>
<a href='users_list_tables.py'>Назад</a>
<p>Назначьте привелегии</p>

<form action='users_list_tables_grants_form.py'>
    {2}
    <input type='submit' value='Назначить'>
</form>""".format(selected_user, selected_table, grants_list_form)

template.build_with_content(content)
