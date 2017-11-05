#!/home/mrdiz/anaconda3/bin/python

import sys
sys.path.append("/home/mrdiz/SQL/Lab5(2)")

import cgi

from utils.site_manager import Manager
import utils.site_template as template

form = cgi.FieldStorage()
selected_table = form.getfirst('table_list')

Manager.cookie["table"] = selected_table
print(Manager.cookie)

template.redirect('table.py')