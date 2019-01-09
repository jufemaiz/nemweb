"""
Data Class
"""

import datetime
import re
import requests

from nemweb import timezone as tz

class Data: #pylint: disable=too-few-public-methods
    """
    Base Data class for Archive and Current. Abstracts out the general work
    """
    baseurl = 'https://www.nemweb.com.au'
    basepath = 'REPORTS'

    def __init__(self, dataset):
        """
        Args:
            dataset (:obj:`Dataset`):

        Returns:
            str URL
        """
        self.title = dataset.title
        self.path = dataset.path
        self.filepattern = dataset.filepattern
        self.datetimeformat = dataset.datetimeformat
        self.datetimekey = dataset.datetimekey

    @staticmethod
    def set_start_finish(start, finish):
        """
        Args:
            start (:obj:`datetime`, None):
            finish (:obj:`datetime`, None):

        Returns:
            :obj:`datetime`, :obj:`datetime`
        """
        now = datetime.datetime.utcnow().astimezone(tz.AEMOTZ)
        rstart = start
        if start is None:
            rstart = datetime.datetime(now.year,
                                       now.month,
                                       now.day,
                                       tzinfo=tz.AEMOTZ)
        rfinish = finish
        if finish is None or finish < start:
            finish = start + datetime.timedelta(days=1)

        return rstart, rfinish

    def _urlfor(self, path):
        """
        Args:
            path (str): the path to use in the request

        Returns:
            str URL
        """
        return '{0}{1}'.format(self.__class__.baseurl, path)

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
        page = requests.get('{0}/{1}/{2}/'.format(self.__class__.baseurl,
                                                  self.__class__.basepath,
                                                  self.path))
        regex = re.compile('/{0}/{1}/{2}'.format(self.__class__.basepath,
                                                 self.path,
                                                 self.filepattern))
        for link in regex.finditer(page.text):
            yield {'path': link.group(0), 'datetime': link.group(1)}
