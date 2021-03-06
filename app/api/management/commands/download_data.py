import gzip
import shutil
import sqlite3
from contextlib import closing
from os import environ, remove
from os.path import exists, basename, join
from sys import exit
from urllib.parse import urlparse
from urllib.request import urlretrieve, build_opener, install_opener

from django.core.management.base import BaseCommand
from friendlylog import colored_logger as log
from tqdm import tqdm

DB_FILE = '/data/disgenet.db'
UMLS_FILE = '/data/disease_attr.tsv'


class TqdmUpTo(tqdm):
    def update_to(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)


def get_creds():
    with open('/var/run/secrets/disgenet_creds', 'r') as creds:
        return f"Basic {creds.read().encode('utf-8')}"


def download_from_disgenet(url, target, overwrite=False):
    if overwrite or not exists(target):
        gz_file = join('/tmp', basename(urlparse(url).path))
        try:
            if not exists(gz_file):
                opener = build_opener()
                opener.addheaders = [('User-Authorization', get_creds())]
                install_opener(opener)
                log.info(f"Downloading {target} from {url}...")
                with TqdmUpTo(unit='B', unit_scale=True, unit_divisor=1024, miniters=1, desc=gz_file) as t:
                    urlretrieve(url,
                                filename=gz_file,
                                reporthook=t.update_to)
            log.info(f"Gunzip {gz_file} to {target}...")
            with gzip.open(gz_file, 'rb') as gzf:
                with open(target, 'wb+') as dbf:
                    shutil.copyfileobj(gzf, dbf)
            remove(gz_file)
            log.info(f"DONE downloading {target}.")
            # We return true if we downloaded something
            return True
        except Exception as ex:
            log.error(ex)
    # If the file is not downloaded
    return False


def update_db(db_file):
    log.info(f"Updating db ({db_file})...")

    try:
        with sqlite3.connect(db_file) as connection:
            with closing(connection.cursor()) as cursor:
                # We want to have null instead of NA in the year field
                cursor.execute('''
                    UPDATE variantDiseaseNetwork
                    SET year = null
                    WHERE year = 'NA'
                    ''')
                # Because the pattern of a combined foreign key looks different in django
                # we adjust disease2class and variantGene accordingly
                cursor.execute('''
                    create table disease2class_copy (
                    id integer primary key autoincrement, 
                    diseaseNID int,
                    diseaseClassNID int,
                    FOREIGN KEY (diseaseNID) REFERENCES diseaseAttributes(diseaseNID),
                    FOREIGN KEY (diseaseClassNID) REFERENCES diseaseClass(diseaseClassNID))
                    ''')
                cursor.execute('''
                    insert into disease2class_copy (diseaseNID, diseaseClassNID) 
                    select diseaseNID, diseaseClassNID from disease2class
                    ''')
                cursor.execute('drop table disease2class')
                cursor.execute('''
                    alter table disease2class_copy rename to disease2class
                    ''')
                cursor.execute('''
                    create table variantGene_copy (
                    id integer primary key autoincrement, 
                    geneNID int,
                    variantNID int,
                    FOREIGN KEY (geneNID) REFERENCES geneAttributes(geneNID),
                    FOREIGN KEY (variantNID) REFERENCES variantAttributes(variantNID))
                    ''')
                cursor.execute('''
                    insert into variantGene_copy (geneNID, variantNID) 
                    select geneNID, variantNID from variantGene
                    ''')
                cursor.execute('drop table variantGene')
                cursor.execute('''
                    alter table variantGene_copy rename to variantGene
                    ''')
                connection.commit()
        log.info(f"DONE updating db ({db_file}).")
    except Exception as ex:
        log.error(f"Error during db update: {ex}")


def create_umls_table(umls_file):
    log.info(f"Create new table from umls ({umls_file})...")
    try:
        with open(umls_file, 'r') as f:
            new_data = [tuple(map(lambda x: x.strip(), line.split('\t')))
                        for line in f.readlines()[1:]]
        with sqlite3.connect(DB_FILE) as connection:
            with closing(connection.cursor()) as cursor:
                cursor.execute('''CREATE TABLE umls (
                        diseaseId text, 
                        name text,	
                        type text,
                        diseaseClassMSH text, 
                        diseaseClassNameMSH text, 
                        hpoClassId text,	
                        hpoClassName text,
                        doClassId text, 
                        doClassName text, 
                        umlsSemanticTypeId text, 
                        umlsSemanticTypeName text
                    )
                    ''')
                cursor.executemany(
                    'INSERT INTO umls VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', new_data)
                log.info(f"DONE creating umls table.")
                log.info(f"Updating table diseaseAttributes.")

                cursor.execute('''CREATE TABLE diseaseAttributes_copy1 AS
                SELECT  umls.umlsSemanticTypeId,
                umls.umlsSemanticTypeName,
                diseaseAttributes.diseaseId,
                diseaseAttributes.diseaseNID,
                diseaseAttributes.diseaseName,
                diseaseAttributes.type FROM diseaseAttributes
                LEFT JOIN umls
                ON diseaseAttributes.diseaseId = umls.diseaseId ''')

                cursor.execute('''CREATE TABLE diseaseAttributes_copy2 (
                umlsSemanticTypeId text,
                umlsSemanticTypeName text,
                diseaseId text,
                diseaseNID integer,
                diseaseName text,
                type text
                    )''')
                cursor.execute('''insert into diseaseAttributes_copy2 (diseaseId, diseaseNID, diseaseName, type, umlsSemanticTypeId, umlsSemanticTypeName )
                                                select diseaseId, diseaseNID, diseaseName, type, umlsSemanticTypeId, umlsSemanticTypeName from diseaseAttributes_copy1''')


                cursor.execute('''drop table diseaseAttributes''')
                cursor.execute('''drop table diseaseAttributes_copy1''')
                cursor.execute('''alter table diseaseAttributes_copy2 rename to diseaseAttributes''')

                connection.commit()

    except Exception as ex:
        log.error(f"Error during table umls creation: {ex}")


class Command(BaseCommand):
    help = 'run in order to get the db from the disgenet website'

    def handle(self, *args, **kwargs):
        try:
            if download_from_disgenet(environ.get(
                    'DISGENET_DB_URL',
                    'https://www.disgenet.org/static/disgenet_ap1/files/sqlite_downloads/current/disgenet_2020.db.gz'),
                    DB_FILE):
                update_db(DB_FILE)
            if download_from_disgenet(environ.get(
                    'DISGENET_UMLS_URL',
                    'https://www.disgenet.org/static/disgenet_ap1/files/downloads/disease_mappings_to_attributes.tsv.gz'),
                    UMLS_FILE):
                create_umls_table(UMLS_FILE)
        except Exception as ex:
            log.error("Error during database preparation: {ex}")
            exit(1)
        exit(0)
