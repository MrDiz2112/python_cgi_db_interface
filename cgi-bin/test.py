import re

def table_insert_form(headers_list):
    content = """
    <form action='../cgi-bin/table_insert_form.py' method='post'>
        {0}
        <input type='submit' value='Добавить'>
    </form>"""

    field_tmp = """
    <div>
        <label for='{0}'>{0}</label><input type='text' name='{0}' id='{0} {1}'>
    </div>"""

    field_list_html = ''

    re_match = r"nextval\('.*'::regclass\)"

    for item in headers_list:
        res = re.search(re_match, item[1])

        if bool(res):
            field_list_html += field_tmp.format(item[0], 'value="DEFAULT" readonly')
        else:
            field_list_html += field_tmp.format(item[0], '') + '\n'

    content = content.format(field_list_html)

    return content

list = [('idproduct', "nextval('products_idproduct_seq'::regclass)"),
 ('idtype', None),
 ('model', None),
 ('cost', '0'),
 ('idprovider', None)]


print(table_insert_form(list))
