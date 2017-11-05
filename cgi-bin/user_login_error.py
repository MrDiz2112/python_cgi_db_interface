#!/home/mrdiz/anaconda3/bin/python

import sys
sys.path.append("/home/mrdiz/SQL/Lab5(2)")

import utils.site_template as template

content = """
<h2>Ошибка входа</h2>
<p>Попробуйте <a href='index.py'>снова</a>.</p>"""

template.build_with_content(content)
