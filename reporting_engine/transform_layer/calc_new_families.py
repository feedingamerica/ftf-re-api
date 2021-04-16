from pandas.core.frame import DataFrame
import dateutil.parser as parser
import pandas as pd
import json
import numpy as np

import transform_layer.calc_families as calc_families


# data def 32
def get_new_families(data: 'list[DataFrame]'):
    """Calculate number of new families DataDef 32

    Arguments:
    data - data frames to fulfill definiton id

    Modifies:
    Nothing

    Returns: added_members
    added_families - new family count
    """
    
    families = data[1]
    families = families[families['timeframe_has_first_service_date']>0]
    return len(families)

# data def 33
def get_new_members(data: 'list[DataFrame]'):
    """Calculate number of new members DataDef 33

    Arguments:
    data - data frames to fulfill definiton id

    Modifies:
    Nothing

    Returns: added_members
    added_members - json of new member count

    """
    members = data[2]
    members = members[members['timeframe_has_first_service_date']>0]
    return len(members)

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

# data def 35
def get_services_to_new_families(data: 'list[DataFrame]'):
    families = data[1]
    families = families[families['timeframe_has_first_service_date']>0]
    return families['num_services'].sum()

#data def 36
def get_families_first_service(data: 'list[DataFrame]'):
    services = data[0]
    services = services[services['is_first_service_date']>0]
    return len(services)

# data def 37/38
def get_new_families_freq_visits(data: 'list[DataFrame]'):
        """Calculate frequency of visits for new families DataDef 37

        Arguments:
        data - data frames to fulfill definiton id

        Modifies:
        Nothing

        Returns: added_members
        added_members - json of number of services new families used

        """
        families = data[1]
        families = families[families['timeframe_has_first_service_date']>0]
        families = families.astype({'num_services': 'int64'})
        families = families.groupby(['num_services'])
        families = families.agg({'research_family_key': 'count', 'num_services': 'sum'})
        largeSum = families.iloc[24:].sum()
        families.at[25, 'research_family_key'] = largeSum.iloc[0]
        families.at[25, 'num_services'] = largeSum.iloc[1]
        families = families.rename(columns={'research_family_key' :'n_families', 'num_services':'sum_services'})
        families = families.head(25)
        return families.to_json()

# data def 39
def get_new_fam_household_composition(data: 'list[DataFrame]'):
    families = data[1]
    families = families[families['timeframe_has_first_service_date']>0].copy()
    return calc_families.get_household_composition(families)
    

# data def 40
def get_new_fam_composition_key_insight(data: 'list[DataFrame]'):
    families = data[1]
    families = families[families['timeframe_has_first_service_date']>0]
    result_dict = {
        "has_child_senior":0,
        "no_child_senior":0
    }
    families = families.groupby(["family_composition_type"]).count()
    if 'adults_only' in families.index:
        num_no_child_senior = int(families.at['adults_only','research_family_key'])
    else:
        num_no_child_senior = 0
    result_dict["no_child_senior"] = num_no_child_senior
    result_dict["has_child_senior"] = int(families['research_family_key'].sum()) - num_no_child_senior
    
    return json.dumps(result_dict)

#data def 41
def get_new_fam_hh_size_dist_1_to_10(data):
    """Calculate household size distibutions for families of size 1 to 10 DataDef 41

    Arguments:
    data - data frames to fulfill definiton id

    Modifies:
    Nothing

    Returns: added_members
    num_new_families - new family distribution counts 1 to 10
    """

    families = data[1]
    families = families[families['timeframe_has_first_service_date'] > 0].copy()
    return calc_families.get_household_size_distribution_1_to_10(families)

#data def 42
def get_new_fam_hh_size_dist_classic(data):
    families = data[1]
    families = families[families['timeframe_has_first_service_date'] > 0].copy()
    return calc_families.get_household_size_distribution_classic(families)

#data def 43
def get_relationship_length_fam_mean(data):
    """Calculate mean length of relationship for families DataDef 43

    Arguments:
    data - data frames to fulfill definiton id

    Modifies:
    Nothing

    Returns: added_members
    mean_relationship_length - mean relationship length of families
    """

    families = data[1]
    return families['max_days_since_first_service'].mean()

#data def 44
def get_new_fam_dist_of_length_of_relationship(data: 'list[DataFrame]'):
    families = data[1]
    set_max = families['max_days_since_first_service'].max()
    width = set_max / 10

    conditions = [
        (families['max_days_since_first_service'] >= 0) & (families['max_days_since_first_service'] < width),
        (families['max_days_since_first_service'] >= width) & (families['max_days_since_first_service'] < width * 2),
        (families['max_days_since_first_service'] >= width * 2) & (families['max_days_since_first_service'] < width * 3),
        (families['max_days_since_first_service'] >= width * 3) & (families['max_days_since_first_service'] < width * 4),
        (families['max_days_since_first_service'] >= width * 4) & (families['max_days_since_first_service'] < width * 5),
        (families['max_days_since_first_service'] >= width * 5) & (families['max_days_since_first_service'] < width * 6),
        (families['max_days_since_first_service'] >= width * 6) & (families['max_days_since_first_service'] < width * 7),
        (families['max_days_since_first_service'] >= width * 7) & (families['max_days_since_first_service'] < width * 8),
        (families['max_days_since_first_service'] >= width * 8) & (families['max_days_since_first_service'] < width * 9),
        (families['max_days_since_first_service'] >= width * 9) & (families['max_days_since_first_service'] <= set_max)
    ]
    values = [
        '0 - ' + str(width),
        str(width) + ' - ' + str(width*2),
        str(width*2) + ' - ' + str(width*3),
        str(width*3) + ' - ' + str(width*4),
        str(width*4) + ' - ' + str(width*5),
        str(width*5) + ' - ' + str(width*6),
        str(width*6) + ' - ' + str(width*7),
        str(width*7) + ' - ' + str(width*8),
        str(width*8) + ' - ' + str(width*9),
        str(width*9) + ' - ' + str(set_max)
    ]
    sort_buckets_dict = {
        values[0]: 0,
        values[1]: 1,
        values[2]: 2,
        values[3]: 3,
        values[4]: 4,
        values[5]: 5,
        values[6]: 6,
        values[7]: 7,
        values[8]: 8,
        values[9]: 9
    }

    families['buckets'] = np.select(conditions, values)
    families = families.groupby('buckets').size().to_frame('count')
    families = families.sort_values(by = 'buckets', key = lambda x: x.map(sort_buckets_dict))

    return families['count'].to_json()

#data def 45
def get_relationship_length_indv_mean(data):
    members = data[2]
    return members['max_days_since_first_service'].mean()

# data def 46
def get_new_fam_dist_of_length_of_relationships_for_individuals(data: 'list[DataFrame]'):
    members = data[2]
    set_max = members['max_days_since_first_service'].max()
    width = set_max / 10

    conditions = [
        (members['max_days_since_first_service'] >= 0) & (members['max_days_since_first_service'] < width),
        (members['max_days_since_first_service'] >= width) & (members['max_days_since_first_service'] < width * 2),
        (members['max_days_since_first_service'] >= width * 2) & (members['max_days_since_first_service'] < width * 3),
        (members['max_days_since_first_service'] >= width * 3) & (members['max_days_since_first_service'] < width * 4),
        (members['max_days_since_first_service'] >= width * 4) & (members['max_days_since_first_service'] < width * 5),
        (members['max_days_since_first_service'] >= width * 5) & (members['max_days_since_first_service'] < width * 6),
        (members['max_days_since_first_service'] >= width * 6) & (members['max_days_since_first_service'] < width * 7),
        (members['max_days_since_first_service'] >= width * 7) & (members['max_days_since_first_service'] < width * 8),
        (members['max_days_since_first_service'] >= width * 8) & (members['max_days_since_first_service'] < width * 9),
        (members['max_days_since_first_service'] >= width * 9) & (members['max_days_since_first_service'] <= set_max)
    ]
    values = [
        '0 - ' + str(width),
        str(width) + ' - ' + str(width*2),
        str(width*2) + ' - ' + str(width*3),
        str(width*3) + ' - ' + str(width*4),
        str(width*4) + ' - ' + str(width*5),
        str(width*5) + ' - ' + str(width*6),
        str(width*6) + ' - ' + str(width*7),
        str(width*7) + ' - ' + str(width*8),
        str(width*8) + ' - ' + str(width*9),
        str(width*9) + ' - ' + str(set_max)
    ]
    sort_buckets_dict = {
        values[0]: 0,
        values[1]: 1,
        values[2]: 2,
        values[3]: 3,
        values[4]: 4,
        values[5]: 5,
        values[6]: 6,
        values[7]: 7,
        values[8]: 8,
        values[9]: 9
    }

    members['buckets'] = np.select(conditions, values)
    members = members.groupby('buckets').size().to_frame('count')
    members = members.sort_values(by = 'buckets', key = lambda x: x.map(sort_buckets_dict))

    return members['count'].to_json()


