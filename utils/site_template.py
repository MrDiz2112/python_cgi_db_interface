#!/home/mrdiz/anaconda3/bin/python

import sys
sys.path.append("/home/mrdiz/SQL/Lab5(2)")

import re


def build_with_content(content=''):

    print("Content-type: text/html")
    print()

    print("""
    <!DOCTYPE html>
    <html lang="ru">
    
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta http-equiv="X-UA-Compatible" content="ie=edge">
        <link rel='stylesheet' href='../css/stylesheet.css'>
        
        <title>Database Interface</title>
    </head>
    
    <body>
        {0}
    </body>
    </html>""".format(content))


def build_option_list(list, one_column=False):
    option_temp = '<option value="{0}">{1}</option>'  # шаблон для пунктов select
    option_list_html = ""

    if not one_column:
        for item in list:
            option_list_html += option_temp.format(item[0], item[1]) + '\n'
    else:
        for item in list:
            option_list_html += option_temp.format(item[0], item[0]) + '\n'

    return option_list_html


def su_postgres_links(is_su):
    if is_su:
        content = """
        <p><a href='../cgi-bin/users_list.py'>Список привилегий пользователей</a></p>"""
    else:
        content = ''

    return content


def user_table_grants(grant_list):
    checkbox_tmp = "<div><input type='checkbox' name='{0}' id='{0}' {1}><label for='{0}'>{0}</label></div>\n\n"

    content = ""

    for i, item in enumerate(grant_list):
        if i == 0:
            if item:
                content += checkbox_tmp.format('SELECT', ' checked')
            else:
                content += checkbox_tmp.format('SELECT', '')
        elif i == 1:
            if item:
                content += checkbox_tmp.format('INSERT', ' checked')
            else:
                content += checkbox_tmp.format('INSERT', '')
        elif i == 2:
            if item:
                content += checkbox_tmp.format('UPDATE', ' checked')
            else:
                content += checkbox_tmp.format('UPDATE', '')
        elif i == 3:
            if item:
                content += checkbox_tmp.format('DELETE', ' checked')
            else:
                content += checkbox_tmp.format('DELETE', '')

    return content


def table_alter_buttons(grant_list):
    btn_tmp = "<form class='alter_btn' action='{0}'><input type='submit' value='{1}'{2}></form>"

    content = ""

    for i, item in enumerate(grant_list):
        if i == 0:
            if item:
                content += btn_tmp.format('../cgi-bin/table_insert.py', 'Вставить', '')
            else:
                content += btn_tmp.format('../cgi-bin/table_insert.py', 'Вставить', 'disabled')
        elif i == 1:
            if item:
                content += btn_tmp.format('../cgi-bin/table_update.py', 'Обновить', '')
            else:
                content += btn_tmp.format('../cgi-bin/table_update.py', 'Обновить', 'disabled')
        elif i == 2:
            if item:
                content += btn_tmp.format('../cgi-bin/table_delete.py', 'Удалить', '')
            else:
                content += btn_tmp.format('../cgi-bin/table_delete.py', 'Удалить', 'disabled')

    content += "<br class='alter_btn'>"

    return content


def table_insert_form(headers_list):
    content = """
    <form action='../cgi-bin/table_insert_form.py' method='post'>
        {0}
        <br><br>
        <input type='submit' value='Добавить'>
    </form>"""
    
    field_tmp = """
    <div>
        <input type='text' name='{0}' id='{0}' {1}><label for='{0}'> {0}</label>
    </div>"""

    field_list_html = ''

    re_match = r"nextval\('.*'::regclass\)"

    for item in headers_list:
        res = re.search(re_match, str(item[1]))

        if res:
            field_list_html += field_tmp.format(item[0], 'value="DEFAULT" readonly')
        else:
            field_list_html += field_tmp.format(item[0], '') + '\n'

    content = content.format(field_list_html)

    return content


def table_update_form(headers_list, values_list, pk_column):

    header_value_list = list(zip(headers_list, values_list))

    content = """
        <form action='../cgi-bin/table_update_row_form.py' method='post'>
            {0}
            <br><br>
            <input type='submit' value='Изменить'>
        </form>"""

    field_tmp = """
        <div>
            <input type='text' name='{0}' id='{0}' {1}><label for='{0}'> {0}</label>
        </div>"""

    field_list_html = ''

    for item in header_value_list:
        if item[0] == pk_column:
            field_list_html += field_tmp.format(item[0], 'value="{0}" readonly'.format(item[1]))
        else:
            field_list_html += field_tmp.format(item[0], 'value="{0}"'.format(item[1]))

    content = content.format(field_list_html)

    return content


def reformat_list(list):
    new_list = []

    for item in list:
        row_list = []
        full_name = ""

        for i, row in enumerate(item):
            if i == 0:
                row_list.append(str(row))
            else:
                full_name += " " + str(row)

        row_list.append(full_name)
        new_list.append(row_list)

    return new_list


def form_table(list, headers):
    content = ""

    # Шаблон таблицы
    table_temp = """
            <table>
                {0}
                {1}
            </table>"""

    # Шаблон одной строки таблицы
    row_temp = """
                <tr>
                    {0}
                </tr>"""

    header_temp = "<th>{0}</th>"
    cell_temp = "<td>{0}</td>"

    headers_list_html = ""
    row_list_html = ""

    # Форматировать заголовки
    headers_list = ""

    for item in headers:
        for cell_item in item:
            cell = header_temp.format(cell_item)

            headers_list += cell + '\n'

    row_item = row_temp.format(headers_list)
    headers_list_html += row_item + "\n"

    # Для каждой строки из БД сделать html строку
    for item in list:
        headers_list = ""
        for cell_item in item:
            cell = cell_temp.format(cell_item)

            headers_list += cell + '\n'

        row_item = row_temp.format(headers_list)
        row_list_html += row_item + "\n"

    # Сформировать таблицу
    table_item = table_temp.format(headers_list_html, row_list_html)

    # Добавить таблицу к содержимому
    content += table_item + "\n"

    return content


def redirect(path):
    print("""
    <!DOCTYPE html>
<html lang="ru">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">


    <script type="text/javascript">
        window.location.href = "{0}"
    </script>

    <title>Admin panel</title>
</head>

<body>
    If you are not redirected automatically, follow this <a href='{0}'>link.</a>.
</body>

</html>
    """.format(path))