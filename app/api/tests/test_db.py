"""
Testing if db is downloaded and correctly populated.
"""

import sqlite3
from contextlib import closing
from os.path import exists
from django.test import TestCase

DB_FILE = '/data/disgenet.db'


class DBtest(TestCase):
    """Test models"""

    def test_create_db_successful(self):
        """Testing if creating the db is successful"""

        self.assertTrue(exists(DB_FILE))

    def test_db_populated_successful(self):
        """Testing populating the db is successful"""
        if exists(DB_FILE):
            with sqlite3.connect(DB_FILE) as connection:
                with closing(connection.cursor()) as cursor:
                    pass
                    cursor.execute("select count(*) from pragma_table_info('diseaseAttributes')")
                    number = int(cursor.fetchone()[0])
                    self.assertEqual(number, 6)

