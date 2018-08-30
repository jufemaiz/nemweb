"""Module for reading nemfiles and zipped nemfiles into pandas dataframes"""

from io import BytesIO
from zipfile import ZipFile
import pandas as pd

class ZipFileStreamer(ZipFile):
    """ZipFileStreamer is a ZipFile subclass, with method to extract ZipFile as
    byte stream to memory.

    Attributes:
        member_count (int): number of files
    """

    def __init__(self, filename):
        """Initialises ZipFile object, and adds member_count attribute

        Args:
            filename (str): name of the file
        """
        ZipFile.__init__(self, filename)
        self.member_count = len(self.filelist)

    def extract_stream(self, member):
        """Extract a member from the archive as a byte stream or string steam,
        using its full name. 'member' may be a filename or a ZipInfo object.

        Args:
            member (str, :obj:`ZipInfo`): the member to be extracted from the
                archive

        Returns:
            :obj:`BytesIO`
        """
        return BytesIO(self.read(member))

def zip_streams(file_object):
    """Generator that yields each member of a zipfile as a BytesIO stream.
    Can take a filename or file-like object (BytesIO object) as an argument.

    Args:
        file_object

    Yields:
        :obj:`BytesIO`: Each of the files in the zip file
    """
    with ZipFileStreamer(file_object) as zipfile:
        for filename in zipfile.namelist():
            yield filename, zipfile.extract_stream(filename)

def nemfile_reader(nemfile_object):
    """Transforms the data in the nemfile_object into an appropriate data
    structure - in this case a dict containing a pandas dataframe each table in
    a nemfile.

    The fileobject needs to be plain text csv, and can be either a file or a
    stream file object.

    Args:
        nemfile_object (str, :obj:`BytesIO`): the CSV file to transform

    Returns:
        dict containing a pandas dataframe each table in a nemfile
    """
    table_dict = {}
    for line in nemfile_object.readlines():
        columns = line.decode().split(',')
        table = "{0}_{1}".format(columns[1], columns[2])

        # new table
        if columns[0] == "I":
            table_dict[table] = line

        # append data to each table
        elif columns[0] == "D":
            table_dict[table] += line

    return {table:pd.read_csv(BytesIO(table_dict[table])) for table in table_dict}

def nemzip_reader(nemzip_object):
    """The nemzip_object must be a zipped csv (nemzip), and can be either a file
    or an in stream fileobject.

    The method checks there is only a single file to unzip, unzips to a nemfile (csv) in memory,
    and passes nemfile_object to nemfile reader.

    Args:
        nemzip_object (str): the zip file to have data extracted

    Returns:
        dict containing a pandas dataframe each table in a zipped nemfile.
    """
    with ZipFileStreamer(nemzip_object) as zipfile:
        if zipfile.member_count > 1:
            raise Exception('More than one file in zipfile')

        filename = zipfile.namelist()[0]
        nemfile_object = zipfile.extract_stream(filename)
        return nemfile_reader(nemfile_object)
