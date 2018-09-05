import datetime

from collections import namedtuple

import pandas as pd

from nemweb.extractor import archive
from nemweb.extractor import current
from nemweb import timezone as tz

CURRENTDATASETCOVERAGE = datetime.timedelta(days=2, minutes=5)
CURRENTDATASET = current.Dataset(title="Dispatch SCADA",
                                 path="Dispatch_SCADA",
                                 filepattern='PUBLIC_DISPATCHSCADA_(\d{12})_\d{16}.zip',
                                 datetimeformat="%Y%m%d%H%M",
                                 datetimekey="SETTLEMENTDATE",
                                 stepsize=300)
CURRENTDATA = current.CurrentData(CURRENTDATASET)

ARCHIVEDATASET = archive.Dataset(title="Dispatch SCADA",
                                 path="Dispatch_SCADA",
                                 filepattern='PUBLIC_DISPATCHSCADA_(\d{8}).zip',
                                 datetimeformat="%Y%m%d",
                                 datetimekey="SETTLEMENTDATE",
                                 stepsize=300)
ARCHIVEDATA = archive.ArchiveData(ARCHIVEDATASET)

SETTLEMENTDATEFORMAT = '%Y/%m/%d %H:%M:%S'

Datum = namedtuple('DispatchSCADADatum',
                   ['risingedge', 'fallingedge', 'duid', 'value'])

def dataset(start, finish):
    """This is customised for each.

    Args:
        start (:obj:`datetime`): the start of the dataset requested
        finish (:obj:`datetime`): the finish of the dataset requested

    Returns:
        dict of pandas
    """
    dataset = {}

    datasets = []

    now = datetime.datetime.utcnow().astimezone(tz.AEMOTZ)

    if True:
        datasets.append(CURRENTDATA.dataset(start, finish))
    if False:
        datasets.append(ARCHIVEDATA.dataset(start, finish))

    for d in datasets:
        for k in d.keys():
            if k in dataset:
                dataset[k] = dataset[k].append(d[k])
            else:
                dataset[k] = d[k]

    return dataset

def standarize(datum):
    """Standardizes to a more normal dataset.

    Args:
        datum (:obj:`pandas.DataFrame`): the datum to be standarized

    Returns:
        nemweb.data.dispatch_scada.Datum namedtuple
    """
    t = datetime.datetime.strptime(datum.SETTLEMENTDATE,
                                   SETTLEMENTDATEFORMAT).replace(tzinfo=tz.AEMOTZ)
    return Datum(fallingedge=t,
                 risingedge=(t - datetime.timedelta(minutes=5)),
                 duid=datum.DUID,
                 value=float(datum.SCADAVALUE))

def nemserializer(datum, lineend=True):
    """Returns a standardized datum to a nemserialized row.

    Args:
        datum (:obj:`Datum`): a normalized datum of dispactch scada data

    Returns:
        str CSV form of a row, including line ending
    """
    return "D,DISPATCH,UNIT_SCADA,1,{0},{1},{2}{3}".format(datum.fallingedge.strftime(SETTLEMENTDATEFORMAT),
                                                           datum.duid,
                                                           datum.value,
                                                           ("\n" if lineend else ''))
