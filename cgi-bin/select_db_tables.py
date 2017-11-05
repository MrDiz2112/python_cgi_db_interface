#!/home/mrdiz/anaconda3/bin/python

import sys
sys.path.append("/home/mrdiz/SQL/Lab5(2)")

from utils.site_manager import Manager
import utils.site_template as template

selected_db = Manager.cookie["database"].value

tables_list = Manager.sql_db_tables_list(selected_db)

options = template.build_option_list(tables_list, one_column=True)

is_su = Manager.sql_is_user_su()
su_links = template.su_postgres_links(is_su)

content = """
<h2>Список таблиц базы данных {1}</h2>
{2}
<p>Доступны только те таблицы, на которые пользователь имеет <br>
привилегию <strong>SELECT</strong>.</p>
<p>Выберете таблицу</p>

<form action='select_db_tables_form.py' method='post'>
    <div>
        <select name='table_list' id='table_list' size='5'>
            {0}
        </select>
    </div>
    
    <input type='submit' value='Выбрать'>
</form>

<br>
<a href='select_db.py'>Назад</a>
""".format(options, selected_db, su_links)

template.build_with_content(content)
