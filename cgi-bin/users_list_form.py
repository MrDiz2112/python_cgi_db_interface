#!/home/mrdiz/anaconda3/bin/python

import sys
sys.path.append("/home/mrdiz/SQL/Lab5(2)")

import cgi
from utils.site_manager import Manager
import utils.site_template as template

form = cgi.FieldStorage()

selected_user = form.getfirst('users_list')

Manager.cookie["user_grants"] = selected_user
print(Manager.cookie)

template.redirect('users_list_tables.py')
