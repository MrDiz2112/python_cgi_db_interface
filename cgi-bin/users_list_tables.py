#!/home/mrdiz/anaconda3/bin/python

import sys
sys.path.append("/home/mrdiz/SQL/Lab5(2)")

from utils.site_manager import Manager
import utils.site_template as template

selected_db = Manager.cookie["database"].value
selected_user = Manager.cookie["user_grants"].value

tables_list = Manager.sql_db_tables_list(selected_db)

options = template.build_option_list(tables_list, one_column=True)

content = """
<h2>Список таблиц базы данных {1}</h2>
<p>Выберете таблицу, чтобы редактировать привилегии <br>
пользователя <strong>{2}</strong>.</p>

<form action='users_list_tables_form.py' method='post'>
    <div>
        <select name='table_list' id='table_list' size='5'>
            {0}
        </select>
    </div>

    <input type='submit' value='Выбрать'>
</form>

<br>
<a href='users_list.py'>Назад</a>
""".format(options, selected_db, selected_user)

template.build_with_content(content)
