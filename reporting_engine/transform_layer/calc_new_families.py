from pandas.core.frame import DataFrame
import dateutil.parser as parser
import pandas as pd

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
    members = data[2]
    members = members[members['timeframe_has_first_service_date']>0]
    members = members[members['dim_families_timeframe_has_first_service_date']>0]
    return len(members)