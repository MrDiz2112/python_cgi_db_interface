#!/home/mrdiz/anaconda3/bin/python

import sys
sys.path.append("/home/mrdiz/SQL/Lab5(2)")

import utils.site_template as template
from utils.site_manager import Manager

users_list = Manager.sql_select('usename', 'pg_user')

options_list = template.build_option_list(users_list, True)

content = """
<h2>Список пользователей</h2>
<p>Выбирите пользователя, чтобы настроить его права</p>

<form action='users_list_form.py' method='post'>
    <div>
        <select name='users_list' id='users_list' size='5'>
            {0}
        </select>
    </div>
    
    <input type='submit' value='Выбрать'>
</form>

<br>
<a href='select_db_tables.py'>Назад</a>""".format(options_list)

template.build_with_content(content)
