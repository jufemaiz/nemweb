"""Initialises nemweb package, loads config"""
import configparser
import os

CONFIG = configparser.RawConfigParser()
CONFIG_FILENAME = '.nemweb_config.ini'
DEFAULT_CONFIG_FILENAME = 'config_example.ini'

LOCAL_DIR = os.path.expanduser("~")
LOCAL_CONFIG_PATH = os.path.join(LOCAL_DIR, CONFIG_FILENAME)
DEFAULT_CONFIG_PATH = os.path.join(os.path.dirname(__file__), DEFAULT_CONFIG_FILENAME)

if os.path.isfile(LOCAL_CONFIG_PATH):
    print('Using local configuration file')
    CONFIG.read(LOCAL_CONFIG_PATH)
else:
    with open(DEFAULT_CONFIG_PATH, 'r') as fin:
        print(fin.read())
    print('Using default configuration file')
    CONFIG.read(DEFAULT_CONFIG_PATH)
