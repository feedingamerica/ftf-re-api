from pandas.core.frame import DataFrame
import dateutil.parser as parser
import pandas as pd

import transform_layer.calc_families as calc_families

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

#data def 38

def get_new_fam_service_distribution(data):
    families = data[1]
    families = families[families['timeframe_has_first_service_date'] > 0]
    families = families.astype({'num_services': 'int64'})
    families = families.groupby(['num_services'])
    families = families.agg({'num_services': 'sum'})
    largeSum = families.iloc[24:].sum()
    families.at[25, 'num_services'] = largeSum.iloc[0]
    families = families.rename(columns={'num_services':'sum_services'})
    families = families.head(25)
    return families.to_json()

#data def 42
def get_new_fam_hh_size_dist_classic(data):
    families = data[1]
    families = families[families['timeframe_has_first_service_date'] > 0]
    return calc_families.get_household_size_distribution_classic(families)

#data def 45
def get_relationship_length_indv_mean(data):
    members = data[2]
    return members['max_days_since_first_service'].mean()
