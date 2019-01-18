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
        """Sets the start and finish values appropriately given desired start
        and finish values.

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
        if finish is None:
            rfinish = rstart + datetime.timedelta(days=1)
        else:
            rfinish = finish.astimezone(tz.AEMOTZ)
            if finish < rstart:
                rfinish = rstart
                rstart = finish

        return rstart, rfinish

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
        response = self.get_page(path)
        zipfilestream = BytesIO(response.content)
        nemfile = nemfile_reader.nemzip_reader(zipfilestream)
        return nemfile

    def url_for(self, path):
        """Returns the url based on a path.

        Args:
            path (str): the path to use in the request

        Returns:
            str URL
        """
        return '{0}{1}'.format(self.__class__.baseurl, path)

    def get_index_page(self):
        """Returns the index page.

        Returns:
            :obj:`requests.Response`
        """
        return requests.get('{0}/{1}/{2}/'.format(self.__class__.baseurl,
                                                  self.__class__.basepath,
                                                  self.path))

    def get_page(self, path):
        """Returns the a request.Response for a path.

        Args:
            path (str): the path to request

        Returns:
            :obj:`requests.Response`
        """
        return requests.get(self.url_for(path))

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
        page = self._get_page()
        regex = self._regex()

        for link in _regex().finditer(page.text):
            yield {'path': link.group(0), 'datetime': link.group(1)}

    def _regex(self):
        """Returns the regular expression to match pages links to files for
        download.

        Returns:
            :obj:`re.Pattern`
        """
        regex = re.compile('/{0}/{1}/{2}'.format(self.__class__.basepath,
                                                 self.path,
                                                 self.filepattern))
