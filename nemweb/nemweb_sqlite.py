""" Module for interfacing with sqlite3 database
"""
import sqlite3
import os
import datetime
from nemweb import CONFIG

def create_tables(db_name='nemweb_live.db'):
    """ Creates all the tables we need!

    Args:
        db_name (str, optional): the name of the database to create tables in

    Returns:
        None
    """
    return
    with sqlite3.connect(db_path(db_name)) as conn:
        create_table(conn, sql_create_projects_table)
        conn.commit()
def insert(dataframe, table_name, db_name='nemweb_live.db'):
    """ Inserts dataframe into a table (table name) in an sqlite3 database
    (db_name).

    Database directory needs to be specfied in `config.ini` file.

    Args:
        dataframe (:obj:`pandas.DataFrame`): a DataFrame of data
        table_name (str): the name of the table to use.
        db_name (str, optional): the name of the database to use. Defaults to
            'nemweb_live.db'.

    Returns:
        None
    """
    with sqlite3.connect(db_path(db_name)) as conn:
        dataframe.to_sql(table_name, con=conn, if_exists='append', index=None)
        conn.commit()

def table_latest_record(table_name, db_name="nemweb_live.db", timestamp_col="SETTLEMENTDATE"):
    """ Returns the lastest timestamp from a table in an sqlite3 database as a
    datetime object.

    Timestamp fields in nemweb files usually named "SETTLEMENTDATE", but
    sometimes INTERVAL_DATETIME is used.

    Args:
        table_name (str): the name of the table to use.
        db_name (str, optional): the name of the database to use. Defaults to
            'nemweb_live.db'.
        timestamp_col (str, optional): the column to use for the timestamp.
            Defaults to 'SETTLEMENTDATE'

    Returns:
        :obj:`datetime`
    """
    with sqlite3.connect(db_path(db_name)) as conn:
        result = conn.execute(
            "SELECT MAX({0}) FROM {1}".format(timestamp_col, table_name)
        )
        date_str = result.fetchall()[0][0]
    return datetime.datetime.strptime(date_str, '%Y/%m/%d %H:%M:%S')

def start_from(
        table_name,
        db_name="nemweb_live.db",
        timestamp_col="SETTLEMENTDATE",
        start_date=None
    ):
    """ Tries determining latest date from table in database. On fail prompts
    user to input date.

    Args:
        table_name (str): the name of the table to use.
        db_name (str, optional): the name of the database to use. Defaults to
            'nemweb_live.db'.
        timestamp_col (str, optional): the column to use for the timestamp.
            Defaults to 'SETTLEMENTDATE'

    Returns:
        :obj:`datetime`

    Raises:
        :obj:`sqlite3.OperationalError`: if there's an sqlite3 error
    """
    try:
        date = table_latest_record(table_name,
                                   db_name=db_name,
                                   timestamp_col=timestamp_col)
    except sqlite3.OperationalError as error:
        print('Error:', error)
        # msg = error.args[0].split(":")
        # if msg[0] == 'no such table':
        #     date_str = input("{0} doesn't exist. Enter start date [YYYYMMDD]: ".format(msg[1]))
        #     date = datetime.datetime.strptime(date_str, "%Y%m%d")
        date = datetime.datetime.strptime(start_date, "%Y%m%d")

    return date

def db_path(db_name):
    """ Tries determining latest date from table in database. On fail prompts
    user to input date.

    Args:
        db_name (str): the name of the database to use.

    Returns:
        :obj:`os.path`
    """
    return os.path.join(CONFIG['local_settings']['sqlite_dir'], db_name)
