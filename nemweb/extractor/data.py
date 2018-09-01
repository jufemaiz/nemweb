"""
"""

class Data:
    """

    """
    baseurl = 'https://www.nemweb.com.au'
    basepath = 'REPORTS'

    def __init__(self):
        True

    def _urlfor(self, path):
        """
        Args:
            path (str): the path to use in the request

        Returns:
            str URL
        """
        return "{0}{1}".format(self.__class__.baseurl, path)
