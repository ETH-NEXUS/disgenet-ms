from django.core.management.base import BaseCommand
import sqlite3
import requests
import os.path
import os
import gzip
import shutil
import base64

url_db = 'https://www.disgenet.org/static/disgenet_ap1/files/sqlite_downloads/current/disgenet_2020.db.gz'
# password = "PiPaPo_2016"
# email = "anastasia.escher@gmail.com"
url = 'https://www.disgenet.org/login/'

gz_filename = 'disgenet_2020.db.gz'
db_filename = 'disgenet_2020.db'

def get_creds():
    base64_message = open('.disgenet_creds', 'r').read()
    base64_bytes = base64_message.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    message = message_bytes.decode('ascii')
    return message.split(':')


def download_db():
    if os.path.exists('disgenet_2020.db'):
        print('DB already exists')
        return False
    email = get_creds()[0]
    password = get_creds()[1]
    with requests.session() as session:
        session.get(url)  # sets cookie
        if 'csrftoken' in session.cookies:
            csrftoken = session.cookies['csrftoken']
        else:
            csrftoken = session.cookies['csrf']
        login_data = dict(username=email, password=password,
                          csrfmiddlewaretoken=csrftoken, next='/')
        response = session.post(url, data=login_data,
                                headers=dict(Referer=url))
        if response.status_code != 200:
            print('Login failed')
        elif response.status_code == 200:
            print('Logged in')
            r = session.get(url_db, stream=True)
            with open(gz_filename, 'wb') as f:
                for chunk in r.raw.stream(1024, decode_content=False):
                    if chunk:
                        f.write(chunk)
            with gzip.open(gz_filename, 'rb') as f_in:
                with open(db_filename, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            os.remove(gz_filename)
        print('New DB is downloaded')
        return True


def update_db(db_filename):
    connection = sqlite3.connect(db_filename)
    cursor = connection.cursor()
    cursor.execute('''UPDATE variantDiseaseNetwork
                    SET year = null
                    WHERE year = 'NA';''')
    connection.commit()
    connection.close()
    print('DB is updated')


class Command(BaseCommand):
    help = 'run in order to get the db from the disgenet website'

    def handle(self, *args, **kwargs):
        if download_db():
            update_db(db_filename)
