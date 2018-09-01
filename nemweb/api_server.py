"""Module to act as the API server. Provides the ability to cache data.

Module is dependent on a data persistence layer, defaulting to JSON datasets.

Supported options are currently:

- FILE (JSON)
- Postgresql
- sqlite
"""

import collections
import json

from io import BytesIO
from collections import namedtuple
import datetime

def persist(type, rows):
    """Upserts the rows of data to a persistence layer.

    Args:
        type (str): the type of data to persist
        rows (array of dicts): the row

    Returns:
        bool

    Raises:
        Exception if cannot persist
    """
    return True
