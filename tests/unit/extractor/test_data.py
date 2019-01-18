"""pytests for nemweb/extractor/data"""

import datetime
import os
import pytest

try:
    import mock
except ImportError:
    from unittest import mock

from freezegun import freeze_time
from nemweb.extractor.current import Dataset
from nemweb.extractor.data import Data
from nemweb import timezone as tz

class TestNemwebExtractorData(object):
    def _dataset(self):
        return Dataset(title='Dispatch SCADA',
                       path='Dispatch_SCADA',
                       filepattern=r'PUBLIC_DISPATCHSCADA_(\d{12})_\d{16}.zip',
                       datetimeformat='%Y%m%d%H%M',
                       datetimekey='SETTLEMENTDATE',
                       stepsize=300)

    # Let's get testing
    def test_initialize_fail_without_dataset(self):
        try:
            d = Data()
        except TypeError:
            return

    def test_initialize_success_with_dataset(self):
        d = Data(self._dataset())

    @pytest.mark.parametrize(
        'start, finish, rstart, rfinish',
        [(
            datetime.datetime.strptime('2010-01-01', '%Y-%m-%d').astimezone(tz.AEMOTZ),
            datetime.datetime.strptime('2010-01-01', '%Y-%m-%d').astimezone(tz.AEMOTZ),
            datetime.datetime.strptime('2010-01-01', '%Y-%m-%d').astimezone(tz.AEMOTZ),
            datetime.datetime.strptime('2010-01-01', '%Y-%m-%d').astimezone(tz.AEMOTZ),
        ),(
            datetime.datetime.strptime('2010-02-01', '%Y-%m-%d').astimezone(tz.AEMOTZ),
            datetime.datetime.strptime('2010-01-01', '%Y-%m-%d').astimezone(tz.AEMOTZ),
            datetime.datetime.strptime('2010-01-01', '%Y-%m-%d').astimezone(tz.AEMOTZ),
            datetime.datetime.strptime('2010-02-01', '%Y-%m-%d').astimezone(tz.AEMOTZ),
        ),(
            datetime.datetime.strptime('2010-01-01', '%Y-%m-%d').astimezone(tz.AEMOTZ),
            datetime.datetime.strptime('2010-02-01', '%Y-%m-%d').astimezone(tz.AEMOTZ),
            datetime.datetime.strptime('2010-01-01', '%Y-%m-%d').astimezone(tz.AEMOTZ),
            datetime.datetime.strptime('2010-02-01', '%Y-%m-%d').astimezone(tz.AEMOTZ),
        ),(
            datetime.datetime.strptime('2010-02-01', '%Y-%m-%d').astimezone(tz.AEMOTZ),
            datetime.datetime.strptime('2010-01-01', '%Y-%m-%d').astimezone(tz.AEMOTZ),
            datetime.datetime.strptime('2010-01-01', '%Y-%m-%d').astimezone(tz.AEMOTZ),
            datetime.datetime.strptime('2010-02-01', '%Y-%m-%d').astimezone(tz.AEMOTZ),
        ),(
            datetime.datetime.strptime('2010-03-01', '%Y-%m-%d').astimezone(tz.AEMOTZ),
            datetime.datetime.strptime('2010-01-01', '%Y-%m-%d').astimezone(tz.AEMOTZ),
            datetime.datetime.strptime('2010-01-01', '%Y-%m-%d').astimezone(tz.AEMOTZ),
            datetime.datetime.strptime('2010-03-01', '%Y-%m-%d').astimezone(tz.AEMOTZ),
        ),(
            None,
            datetime.datetime.strptime('2009-12-31+1000', '%Y-%m-%d%z').astimezone(tz.AEMOTZ),
            datetime.datetime.strptime('2012-01-01+1000', '%Y-%m-%d%z').astimezone(tz.AEMOTZ),
            datetime.datetime.strptime('2010-03-01+1000', '%Y-%m-%d%z').astimezone(tz.AEMOTZ),
        ),(
            datetime.datetime.strptime('2010-03-01', '%Y-%m-%d').astimezone(tz.AEMOTZ),
            None,
            datetime.datetime.strptime('2010-03-01', '%Y-%m-%d').astimezone(tz.AEMOTZ),
            datetime.datetime.strptime('2010-03-02', '%Y-%m-%d').astimezone(tz.AEMOTZ),
        )]
    )
    @freeze_time("2009-12-31")
    def test_set_start_finish(self, mock_dt, start, finish, rstart, rfinish):
        mock_dt.utcnow = mock.Mock(return_value=datetime.datetime(2011, 1, 1))
        d = Data(self._dataset())
        s, f = d.set_start_finish(start, finish)

        assert s == rstart
        assert f == rfinish

    def test_current_file_handler_get_link_200(self):
        return

    def test_current_file_handler_get_link_timeout(self):
        return

    def test_current_file_handler_(self):
        return
