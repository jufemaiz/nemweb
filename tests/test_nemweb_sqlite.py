""" check that we download data the same as a saved pkl """

import datetime
import os
import pkg_resources
import pytest
import sqlite3
from sqlite3 import Error

from nemweb import CONFIG
from nemweb import nemweb_sqlite
from nemweb.nemweb_current import CurrentFileHandler, DATASETS

class TestNemwebSqlite(object):
    def setup_method(self, test_method):
        # configure self.attribute
        # Setup the database
        try:
            # Create database
            setupconn = sqlite3.connect(self.db_path())
            print('SQLite3 version: ', sqlite3.version)
        except Error as e:
            print(e)
        finally:
            setupconn.close()

    def teardown_method(self, test_method):
        # tear down self.attribute
        if os.path.exists(self.db_path()):
            os.remove(self.db_path())
            print('Removed previous test database at', self.db_path())
        else:
            print('No database to delete at', self.db_path())

    @staticmethod
    def db_path():
        return os.path.abspath(os.path.join(CONFIG.get('local_settings', 'sqlite_dir'),
                                            'test.db'))

    # Let's go testing!
    def test_db_path(self):
        path = nemweb_sqlite.db_path('bob.db')
        expected_path = os.path.join(CONFIG.get('local_settings', 'sqlite_dir'),
                                            'bob.db')

        assert path == expected_path

    def test_start_from(self):
        assert True == True

    def test_insert(self):
        handler = CurrentFileHandler()

        #test latest previous trading_interval
        local_datetime = datetime.datetime.now()
        start_datetime = local_datetime - datetime.timedelta(0,3600)

        handler.update_data(
            DATASETS['dispatch_scada'],
            print_progress=True,
            db_name='test.db',
            start_date = start_datetime.strftime('%Y%m%d')
        )
        assert True != True

    def test_table_latest_record(self):
        assert True == True

    # def test_nemweb(self):
    #     db_path = self.db_path()
    #
    #     handler = CurrentFileHandler()
    #
    #     handler.update_data(
    #         DATASETS['trading_is'],
    #         start_date='20190101',
    #         end_date='20190102',
    #         print_progress=True,
    #         db_name='test.db'
    #     )
    #
    #     conn = sqlite3.connect(db_path)
    #     cur = conn.cursor()
    #
    #     test_data = cur.execute('SELECT RRP FROM TRADING_PRICE').fetchall()
    #
    #     test_data_check = pkg_resources.resource_filename(
    #         'tests', '2018_09_21.pkl'
    #     )
    #
    #     test_data_check = load_pickle(test_data_check)
    #
    #     assert test_data == test_data_check
