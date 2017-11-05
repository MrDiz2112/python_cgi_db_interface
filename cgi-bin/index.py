#!/home/mrdiz/anaconda3/bin/python

import sys
sys.path.append("/home/mrdiz/SQL/Lab5(2)")

import utils.site_template as template
from utils.site_manager import Manager

Manager.cookie["user"] = None
Manager.cookie["password"] = None

print(Manager.cookie)

content = """
<h2>Подключение к базе данных</h2>
<p>Введите логин и пароль</p>

<form action='user_login_form.py' method='post'>
    <div>
        <label for='login'>Логин:</label>
        <br>
        <input type='text' name='login' id='login'>
    </div>
    
    <div>
        <label for='pas'>Пароль:</label>
        <br>
        <input type='password' name='pas' id='pas'>
    </div>
    
    <input type='submit' value='Подключится'>
</form>"""

template.build_with_content(content)
