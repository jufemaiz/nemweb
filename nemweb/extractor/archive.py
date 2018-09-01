"""Module for accessing data different `ARCHIVE` nemweb datasets.

Module responsibilities, for example `dispatch_scada`:

- nemweb.dispatch_scada.data('2018-01-01T00:00:00+10:00')
    -> current / archive
    -> data acquirer
    -> tranform into datastructures
    -> return and marshal (multiple divergent requests)
    -> return data

This should return some sort of data structure for all data from the
dispatch_scada from '2018-01-01T00:00:00+10:00' until now. The method would also
support the request to a given date, along with options to yield as each request
is processed.

ArchiveData gets the ARCHIVE datasets as they are divergent from the ARCHIVE in
files stored and naming structures.
"""
import datetime
import re
import requests

from collections import namedtuple
from dateutil import parser
from io import BytesIO

from nemweb.extractor import data
from nemweb import nemfile_reader

Dataset = namedtuple('NemwebArchive',
                     ['title', 'path', 'filepattern', 'datetimeformat',
                      'datetimekey', 'stepsize'])

DATASETS = {
    "dispatch_scada": Dataset(
        title="Dispatch SCADA",
        path="Dispatch_SCADA",
        filepattern='PUBLIC_DISPATCHSCADA_(\d{12})_\d{16}.zip',
        datetimeformat="%Y%m%d%H%M",
        datetimekey="SETTLEMENTDATE",
        stepsize=300),

    "trading_is": Dataset(
        title="Trading Internodal Settlement Reports",
        path="TradingIS_Reports",
        filepattern="PUBLIC_TRADINGIS_(\d{12})_\d{16}.zip",
        datetimeformat="%Y%m%d%H%M",
        datetimekey="SETTLEMENTDATE",
        stepsize=300),

    "rooftopPV_actual": Dataset(
        title="Rooftop Photovoltaics Actual",
        path="ROOFTOP_PV/ACTUAL",
        filepattern="PUBLIC_ROOFTOP_PV_ACTUAL_(\d{14})_\d{16}.zip",
        datetimeformat="%Y%m%d%H%M00",
        datetimekey="INTERVAL_DATETIME",
        stepsize=300),

    "next_day_actual_gen": Dataset(
        title="Next Day Actual Generation",
        path="Next_Day_Actual_Gen",
        filepattern="PUBLIC_NEXT_DAY_ACTUAL_GEN_(\d{8})_\d{16}.zip",
        datetimeformat="%Y%m%d",
        datetimekey="INTERVAL_DATETIME",
        stepsize=300),

    "dispatch_is": Dataset(
        title="Dispatch Internodal Settlement Reports",
        path="DispatchIS_Reports",
        filepattern="PUBLIC_DISPATCHIS_(\d{12})_\d{16}.zip",
        datetimeformat="%Y%m%d%H%M",
        datetimekey="SETTLEMENTDATE",
        stepsize=300),

    "next_day_dispatch": Dataset(
        title="Next Day Dispatch",
        path="Next_Day_Dispatch",
        filepattern="PUBLIC_NEXT_DAY_DISPATCH_(\d{8})_\d{16}.zip",
        datetimeformat="%Y%m%d",
        datetimekey="SETTLEMENTDATE",
        stepsize=300)
}


class ArchiveData(data.Data):
    """ ArchiveData allows for access to current datasets from NEMWEB

    Attributes:
        title (str)
        path (str)
        filepattern (str)
        datetimeformat (str)
        datetimekey (str)
    """

    basepath = 'REPORTS/ARCHIVE'
    """basepath for current data"""

    def __init__(self, dataset):
        """
        Args:
            dataset (:obj:`Dataset`):
        """
        self.title = dataset.title
        self.path = dataset.path
        self.filepattern = dataset.filepattern
        self.datetimeformat = dataset.datetimeformat
        self.datetimekey = dataset.datetimekey

    def dataset(self, start=None, finish=None):
        """
        Args:
            start (:obj:`datetime`, optional): the datetime to start at. Defaults
                to start of previous day (UTC+10).
            finish (:obj:`datetime`, optional): the datetime to finish. Defaults
                to finish of start (UTC+10).

        Returns:
            array dict
        """
        now = datetime.datetime.utcnow().astimezone(AEMOTZ)
        if start == None:
            start = datetime.datetime(now.year,
                                      now.month,
                                      now.day,
                                      tzinfo=AEMOTZ)
        if finish == None:
            finish = start + datetime.timedelta(days=1)
        datasets = []

        for link in self._links():
            filedatetime = datetime.datetime.strptime(link['datetime'],
                                                      self.datetimeformat).replace(tzinfo=AEMOTZ)

            if filedatetime < start or filedatetime > finish:
                continue

            nemfile = self.download(link['path'])
            datasets.append(nemfile)

        return datasets

    def download(self, path):
        """Downloads nemweb zipfile from link into memory as a BytesIO object.
        nemfile object is returned from the byteIO object

        Args:
            path (str): the path to request

        Returns:
            :obj:`nemfile`
        """
        response = requests.get(self._urlfor(path))
        zip_bytes = BytesIO(response.content)
        nemfile = nemfile_reader.nemzip_reader(zip_bytes)
        return nemfile

    def _links(self):
        page = requests.get("{0}/{1}/{2}/".format(self.__class__.baseurl,
                                                  self.__class__.basepath,
                                                  self.path))
        regex = re.compile("/{0}/{1}/{2}".format(self.__class__.basepath,
                                                 self.path,
                                                 self.filepattern))
        for link in regex.finditer(page.text):
            yield {'path':link.group(0),'datetime':link.group(1)}
