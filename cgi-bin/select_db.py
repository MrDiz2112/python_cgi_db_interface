#!/home/mrdiz/anaconda3/bin/python

import sys
sys.path.append("/home/mrdiz/SQL/Lab5(2)")

import utils.site_template as template
from utils.site_manager import Manager

options = template.build_option_list(Manager.sql_db_list(), True)

content = """
<h2>Подключение к базе данных</h2>
<p>Выберете базу данных</p>

<form action='select_db_form.py' method='post'>
    <div>
        <select name='db_list' id='db_list' size='5'>
            {0}
        </select>
    </div>
    
    <input type='submit' value='Выбрать'>
</form>

<br>
<a href='index.py'>Назад</a>
""".format(options)

template.build_with_content(content)
