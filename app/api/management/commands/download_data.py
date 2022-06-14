from wsgiref import headers
from django.core.management.base import BaseCommand
import sqlite3
import requests
from os.path import exists, basename
from os import environ, remove
import gzip
import shutil
from urllib.request import urlretrieve, build_opener, install_opener
from urllib.parse import urlparse
from friendlylog import colored_logger as log
from tqdm import tqdm
from contextlib import closing

DB_FILE = '/data/disgenet.db'


class TqdmUpTo(tqdm):
    def update_to(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)


def get_creds():
    with open('/var/run/secrets/disgenet_creds', 'r') as creds:
        return f"Basic {creds.read().encode('utf-8')}"


def download_db():
    url = environ.get(
        'DISGENET_DB_URL', 'https://www.disgenet.org/static/disgenet_ap1/files/sqlite_downloads/current/disgenet_2020.db.gz')
    gz_file = basename(urlparse(url).path)
    try:
        opener = build_opener()
        opener.addheaders = [('User-Authorization', get_creds())]
        install_opener(opener)
        with TqdmUpTo(unit='B', unit_scale=True, unit_divisor=1024, miniters=1, desc=gz_file) as t:
            urlretrieve(url,
                        filename=gz_file,
                        reporthook=t.update_to)
        with gzip.open(gz_file, 'rb') as gzf:
            with open(DB_FILE, 'wb') as dbf:
                shutil.copyfileobj(gzf, dbf)
        remove(gz_file)
    except Exception as ex:
        log.error(ex)


def update_db():
    with sqlite3.connect(DB_FILE) as connection:
        with closing(connection.cursor()) as cursor:
            cursor.execute('''UPDATE variantDiseaseNetwork
                    SET year = null
                    WHERE year = 'NA';''')
            connection.commit()


class Command(BaseCommand):
    help = 'run in order to get the db from the disgenet website'

    def handle(self, *args, **kwargs):
        if not exists(DB_FILE):
            download_db()
            update_db()
