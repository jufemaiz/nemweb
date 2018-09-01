"""Module for accessing data different `CURRENT` nemweb datasets.

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

CurrentData gets the CURRENT datasets as they are divergent from the ARCHIVE in
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
from nemweb import timezone as tz

Dataset = namedtuple('NemwebCurrent',
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


class CurrentData(data.Data):
    """ CurrentData allows for access to current datasets from NEMWEB

    Attributes:
        title (str)
        path (str)
        filepattern (str)
        datetimeformat (str)
        datetimekey (str)
        stepsize (int)
    """

    basepath = 'REPORTS/CURRENT'
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
        self.stepsize = dataset.stepsize

    def dataset(self, start=None, finish=None):
        """Request a dataset for a range of datetimes. This is now timezone
        aware, with nemweb.timezone.AEMOTZ currently adoping
        'Australia/Brisbane' until Queensland finally adopt DST and a custom
        AEMO timezone of fixed UTC+10 is required.

        Args:
            start (:obj:`datetime`, optional): the datetime to start at. Defaults
                to start of previous day (UTC+10).
            finish (:obj:`datetime`, optional): the datetime to finish. Defaults
                to finish of start (UTC+10).

        Returns:
            array dict of panda
        """
        now = datetime.datetime.utcnow().astimezone(tz.AEMOTZ)

        if start == None:
            start = datetime.datetime(now.year,
                                      now.month,
                                      now.day,
                                      tzinfo=tz.AEMOTZ)

        if finish == None : finish = start + datetime.timedelta(days=1)

        dataset = {}

        for link in self._links():
            filedatetime = datetime.datetime.strptime(link['datetime'],
                                                      self.datetimeformat).replace(tzinfo=tz.AEMOTZ)

            # TODO: fix this better! Need to know the step size of the data
            if finish < filedatetime or start > filedatetime + datetime.timedelta(seconds=self.stepsize):
                print(filedatetime)
                continue

            nemfile = self.download(link['path'])

            for k in nemfile.keys():
                if k in dataset:
                    dataset[k] = dataset[k].append(nemfile[k])
                else:
                    dataset[k] = nemfile[k]

        return dataset

    def download(self, path):
        """Downloads nemweb zipfile from link into memory as a BytesIO object.
        nemfile object is returned from the byteIO object.

        TODO: review if this is better handled by a temporary file as the
        location. Likely required for supporting zip of zips (as in ARCHIVE).
        https://docs.python.org/2/library/tempfile.html

        Args:
            path (str): the path to request

        Returns:
            :obj:`nemfile`
        """
        response = requests.get(self._urlfor(path))
        zipfilestream = BytesIO(response.content)
        nemfile = nemfile_reader.nemzip_reader(zipfilestream)
        return nemfile

    def _links(self):
        """Private method to yield each link discovered.

        TODO: perhaps consider using lxml to look for the HREF property of A
        elements instead of regular expressions. This is probably a little more
        sound as it will be able to deal with changes to the file structures
        etc.

        Yields:
            dict: dict containing a path and a datetime that has been
            uncovered.
        """
        page = requests.get("{0}/{1}/{2}/".format(self.__class__.baseurl,
                                                  self.__class__.basepath,
                                                  self.path))
        regex = re.compile("/{0}/{1}/{2}".format(self.__class__.basepath,
                                                 self.path,
                                                 self.filepattern))
        for link in regex.finditer(page.text):
            yield {'path':link.group(0),'datetime':link.group(1)}
