#!/home/mrdiz/anaconda3/bin/python

import sys
sys.path.append("/home/mrdiz/SQL/Lab5(2)")

import cgi
import html
from utils.site_manager import Manager

form = cgi.FieldStorage()
user_login = form.getfirst("login", "")
user_pas = form.getfirst("pas", "")

user_login = html.escape(user_login)
user_pas = html.escape(user_pas)

Manager.sql_login(user_login, user_pas)
