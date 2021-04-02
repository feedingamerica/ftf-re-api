import dateutil.parser as parser
from django.db import connections
import numpy as np
import pandas as pd
from pandas.core.frame import DataFrame
import json


#data def 26/27 (return same data, outputted graph just has different y axis depending on def )
def get_frequency_visits(data):
    families = data.groupby(['num_services'])
    families = families.agg({'research_family_key': 'count', 'num_services': 'sum'})
    largeSum = families.iloc[24:].sum()
    families.at[25, 'research_family_key'] = largeSum.iloc[0]
    families.at[25, 'num_services'] = largeSum.iloc[1]
    families = families.rename(columns={'research_family_key' :'n_families', 'num_services':'sum_services'})
    families = families.head(25)
    return families.to_json()

#data def 28
def get_household_composition(data):
    families = data.groupby('family_composition_type').agg(num_families = ('family_composition_type', 'count')).reset_index()
    return families.to_json()

#data def 29
def get_family_comp_key_insight(data):
    families = data.groupby('family_composition_type').agg(num_families = ('family_composition_type', 'count'))

    def choose_group(index_name):
        if index_name.find("child") >= 0 or index_name.find("senior") >= 0:
            return "has_child_senior"
        else:
            return "no_child_senior"
    families = families.groupby(by = choose_group).sum().reset_index()
    families = families.rename(columns = {"index":"family_composition_type"})


    #reset the index at the end

    return families.to_json()

#data def 30
def get_household_size_distribution_1_to_10(data):
    """Calculate Families Breakdown DataDef 30

    Arguments:
    id - data definiton id
    params - a dictionary of values to scope the queries

    Modifies:
    Nothing

    Returns: num_families
    num_families - number of families per sizes 1 to 10

    """

    families = data
    families.avg_fam_size = families.avg_fam_size.round()
    families['avg_fam_size_roll'] = np.where(families['avg_fam_size'] > 9, 10, families['avg_fam_size'])
    families['avg_fam_size_roll'] = np.where(families['avg_fam_size_roll'] == 0, 1, families['avg_fam_size_roll'])
    families = families.groupby('avg_fam_size_roll').agg(num_families = ('avg_fam_size_roll', 'count')).reset_index()

    conditions = [(families['avg_fam_size_roll'] < 4), (families['avg_fam_size_roll'] < 7), (families['avg_fam_size_roll'] >= 7)]
    choices = ['1 - 3', '4 - 6', '7+']

    families['classic_roll'] = np.select(conditions, choices)

    return families.to_json()

#data def 31
def get_household_size_distribution_classic(data):

    families = data.groupby('avg_fam_size').count()

    """ for i in range(len(families)):
        """

    framework_dict = families.to_dict()
    framework_dict = framework_dict['research_family_key']

    return_dict = {
        '1 - 3':0,
        '4 - 6':0,
        '7+':0
    }

    for key in framework_dict:
        if key >= 0 and key < 3.5:
            return_dict['1 - 3'] = return_dict['1 - 3'] + framework_dict[key]
        elif key >= 3.5 and key < 6.5:
            return_dict['4 - 6'] = return_dict['4 - 6'] + framework_dict[key]
        elif key >= 6.5:
            return_dict['7+'] = return_dict['7+'] + framework_dict[key]

    return json.dumps(return_dict)





    





