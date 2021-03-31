from pandas.core.frame import DataFrame
import dateutil.parser as parser
import pandas as pd
import functools

# data def 34
def get_new_members_to_old_families(data: 'list[DataFrame]'):
    """Calculate number of people served DataDef 34

    Arguments:
    data - data frames to fulfill definiton id

    Modifies:
    Nothing

    Returns: added_members
    added_members - json of new members added to families that already have been served

    """
    return functools.reduce(lambda a,b : a + b.to_json(), data)