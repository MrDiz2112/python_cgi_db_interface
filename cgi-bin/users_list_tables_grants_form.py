#!/home/mrdiz/anaconda3/bin/python

import sys
sys.path.append("/home/mrdiz/SQL/Lab5(2)")

import cgi
from utils.site_manager import Manager
import utils.site_template as template

form = cgi.FieldStorage()

is_select = form.getfirst('SELECT')
is_insert = form.getfirst('INSERT')
is_update = form.getfirst('UPDATE')
is_delete = form.getfirst('DELETE')

grants_list = (is_select, is_insert, is_update, is_delete)

Manager.sql_set_grants(grants_list)

template.redirect('users_list_tables_grants.py')
