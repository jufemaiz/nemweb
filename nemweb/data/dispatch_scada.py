import datetime

from collections import namedtuple

from nemweb.extractor import archive
from nemweb.extractor import current
from nemweb import timezone as tz

CURRENTDATASETCOVERAGE = datetime.timedelta(days=2, minutes=5)
CURRENTDATASET = current.Dataset(title='Dispatch SCADA',
                                 path='Dispatch_SCADA',
                                 filepattern=r'PUBLIC_DISPATCHSCADA_(\d{12})_\d{16}.zip',
                                 datetimeformat='%Y%m%d%H%M',
                                 datetimekey='SETTLEMENTDATE',
                                 stepsize=300)
CURRENTDATA = current.CurrentData(CURRENTDATASET)

ARCHIVEDATASET = archive.Dataset(title='Dispatch SCADA',
                                 path='Dispatch_SCADA',
                                 filepattern=r'PUBLIC_DISPATCHSCADA_(\d{8}).zip',
                                 datetimeformat='%Y%m%d',
                                 datetimekey='SETTLEMENTDATE',
                                 stepsize=300)
ARCHIVEDATA = archive.ArchiveData(ARCHIVEDATASET)

SETTLEMENTDATEFORMAT = '%Y/%m/%d %H:%M:%S'

Datum = namedtuple('DispatchSCADADatum',
                   ['risingedge', 'fallingedge', 'duid', 'value'])

def dataset(start, finish, currentds=True):
    """This is customised for each.

    TODO: determine expected available data on nemweb for CURRENT and ARCHIVE
          and extract to deal with entire range of time

    Args:
        start (:obj:`datetime`): the start of the dataset requested
        finish (:obj:`datetime`): the finish of the dataset requested
        currentds (boolean): current data if true, archive data if false

    Returns:
        dict of pandas
    """
    result = {}

    datasets = []

    if currentds:
        datasets.append(CURRENTDATA.dataset(start, finish))
    else:
        datasets.append(ARCHIVEDATA.dataset(start, finish))

    for datas in datasets:
        for key in datas.keys():
            if key in result:
                result[key] = result[key].append(datas[key])
            else:
                result[key] = datas[key]

    return result

def standarize(datum):
    """Standardizes to a more normal dataset.

    Args:
        datum (:obj:`pandas.DataFrame`): the datum to be standarized

    Returns:
        nemweb.data.dispatch_scada.Datum namedtuple
    """
    time = datetime.datetime.strptime(datum.SETTLEMENTDATE,
                                      SETTLEMENTDATEFORMAT).replace(tzinfo=tz.AEMOTZ)
    return Datum(fallingedge=time,
                 risingedge=(time - datetime.timedelta(minutes=5)),
                 duid=datum.DUID,
                 value=float(datum.SCADAVALUE))

def nemserializer(datum, lineend=True):
    """Returns a standardized datum to a nemserialized row.

    Args:
        datum (:obj:`Datum`): a normalized datum of dispactch scada data

    Returns:
        str CSV form of a row, including line ending
    """
    return 'D,DISPATCH,UNIT_SCADA,1,{0},{1},{2}{3}'.format(
        datum.fallingedge.strftime(SETTLEMENTDATEFORMAT),
        datum.duid,
        datum.value,
        ('\n' if lineend else '')
    )
