#!/home/mrdiz/anaconda3/bin/python

import sys
sys.path.append("/home/mrdiz/SQL/Lab5(2)")

import cgi
from utils.site_manager import Manager
import utils.site_template as template

form = cgi.FieldStorage()
selected_db = form.getfirst('db_list')

Manager.cookie["database"] = selected_db
print(Manager.cookie)

template.redirect('select_db_tables.py')
