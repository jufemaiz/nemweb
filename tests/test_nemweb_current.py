""" check that we download data the same as a saved pkl """

import datetime
import os
import pytest
import sqlite3

from nemweb import CONFIG
from nemweb.nemweb_current import CurrentFileHandler, CurrentDataset, DATASETS, update_datasets

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

    # Let's get testing
    def test_update_datasets_fail_with_invalid(self):
        try:
            update_datasets(['this_does_not_exist'])
        except KeyError:
            return

    def test_update_datasets(self):
        update_datasets(['dispatch_scada'])
        return

    def test_current_file_handler_get_link_200(self):
        handler = CurrentFileHandler()

        return

    def test_current_file_handler_get_link_timeout(self):

        return

    def test_current_file_handler_(self):
        return

    @pytest.mark.parametrize(
        'dt, start, finish, result',
        [(
            datetime.datetime.strptime('2010-01-01', '%Y-%m-%d'),
            datetime.datetime.strptime('2010-01-01', '%Y-%m-%d'),
            datetime.datetime.strptime('2010-02-01', '%Y-%m-%d'),
            True
        ),(
            datetime.datetime.strptime('2010-02-01', '%Y-%m-%d'),
            datetime.datetime.strptime('2010-01-01', '%Y-%m-%d'),
            datetime.datetime.strptime('2010-03-01', '%Y-%m-%d'),
            True
        ),(
            datetime.datetime.strptime('2010-01-01', '%Y-%m-%d'),
            datetime.datetime.strptime('2010-02-01', '%Y-%m-%d'),
            datetime.datetime.strptime('2010-03-01', '%Y-%m-%d'),
            False
        ),(
            datetime.datetime.strptime('2010-02-01', '%Y-%m-%d'),
            datetime.datetime.strptime('2010-01-01', '%Y-%m-%d'),
            datetime.datetime.strptime('2010-02-01', '%Y-%m-%d'),
            False
        ),(
            datetime.datetime.strptime('2010-03-01', '%Y-%m-%d'),
            datetime.datetime.strptime('2010-01-01', '%Y-%m-%d'),
            datetime.datetime.strptime('2010-02-01', '%Y-%m-%d'),
            False
        )]
    )
    def test_current_file_handler_valid_datetime(self, dt, start, finish, result):
        handler = CurrentFileHandler()

        assert handler.valid_datetime(dt, start, finish) == result
