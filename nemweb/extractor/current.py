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
from collections import namedtuple
from io import BytesIO
import requests

from nemweb import nemfile_reader
from nemweb import timezone as tz
from nemweb.extractor import data


Dataset = namedtuple('NemwebCurrent',
                     ['title', 'path', 'filepattern', 'datetimeformat',
                      'datetimekey', 'stepsize'])

DATASETS = {
    'dispatch_scada': Dataset(
        title='Dispatch SCADA',
        path='Dispatch_SCADA',
        filepattern=r'PUBLIC_DISPATCHSCADA_(\d{12})_\d{16}.zip',
        datetimeformat='%Y%m%d%H%M',
        datetimekey='SETTLEMENTDATE',
        stepsize=300),

    'trading_is': Dataset(
        title='Trading Internodal Settlement Reports',
        path='TradingIS_Reports',
        filepattern=r'PUBLIC_TRADINGIS_(\d{12})_\d{16}.zip',
        datetimeformat='%Y%m%d%H%M',
        datetimekey='SETTLEMENTDATE',
        stepsize=300),

    'rooftopPV_actual': Dataset(
        title='Rooftop Photovoltaics Actual',
        path='ROOFTOP_PV/ACTUAL',
        filepattern=r'PUBLIC_ROOFTOP_PV_ACTUAL_(\d{14})_\d{16}.zip',
        datetimeformat='%Y%m%d%H%M00',
        datetimekey='INTERVAL_DATETIME',
        stepsize=300),

    'next_day_actual_gen': Dataset(
        title='Next Day Actual Generation',
        path='Next_Day_Actual_Gen',
        filepattern=r'PUBLIC_NEXT_DAY_ACTUAL_GEN_(\d{8})_\d{16}.zip',
        datetimeformat='%Y%m%d',
        datetimekey='INTERVAL_DATETIME',
        stepsize=300),

    'dispatch_is': Dataset(
        title='Dispatch Internodal Settlement Reports',
        path='DispatchIS_Reports',
        filepattern=r'PUBLIC_DISPATCHIS_(\d{12})_\d{16}.zip',
        datetimeformat='%Y%m%d%H%M',
        datetimekey='SETTLEMENTDATE',
        stepsize=300),

    'next_day_dispatch': Dataset(
        title='Next Day Dispatch',
        path='Next_Day_Dispatch',
        filepattern=r'PUBLIC_NEXT_DAY_DISPATCH_(\d{8})_\d{16}.zip',
        datetimeformat='%Y%m%d',
        datetimekey='SETTLEMENTDATE',
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
        self.stepsize = dataset.stepsize
        super(CurrentData, self).__init__(dataset)

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
        start, finish = self.set_start_finish(start, finish)

        dataset = {}

        for link in self._links():
            filedatetime_s = datetime.datetime.strptime(
                link['datetime'],
                self.datetimeformat
            ).replace(tzinfo=tz.AEMOTZ)

            filedatetime_f = filedatetime_s + datetime.timedelta(seconds=self.stepsize)

            # TODO: fix this better! Need to know the step size of the data
            if finish < filedatetime_s or start > filedatetime_f:
                print(filedatetime_s)
                continue

            nemfile = self.download(link['path'])

            for key in nemfile.keys():
                if key in dataset:
                    dataset[key] = dataset[key].append(nemfile[key])
                else:
                    dataset[key] = nemfile[key]

        return dataset
