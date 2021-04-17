from pandas.core.frame import DataFrame
import dateutil.parser as parser
import pandas as pd
import json
import transform_layer.services.data_service as data_service
import numpy as np

# data def 71
def get_skipped_generation(data:'list[DataFrame]'):

    """ temp71_1 = base_members %>% 
    filter(head_of_house == "Yes") %>% 
    select(research_family_key, gender, current_age) """

    members1 = data[data_service.KEY_MEMBER]
    members1 = members1[members1['head_of_house'] == 'Yes']
    members1 = members1['research_family_key','gender','current_age']

    """ temp71_2 = base_members %>% 
    mutate(
    is_child = if_else(condition = current_age < 18, true = 1, false = 0),
    is_senior = if_else(condition = current_age >= 60, true = 1, false = 0)
    ) %>% 
    group_by(research_family_key) %>% 
    summarise(
    n_children = sum(is_child),
    n_senior = sum(is_senior),
    .groups = "drop"
    ) %>% 
    filter(
    n_senior == 1,
    n_children > 0
    ) %>% mutate(is_single_senior_w_children = 1) """

    members2 = data[data_service.KEY_MEMBER]

    families['is_child'] = np.where(members2['current_age'] < 18, 1, 0)
    families['is_senior'] = np.where(members2['current_age'] >= 60, 1, 0)

    members2 = members2.groupby('research_family_key', as_index=False).agg(
        n_children=('is_child','sum'),
        n_senior=('is_senior','sum')
    )

    members2 = members2[members2['n_senior'] == 1]
    members2 = members2[members2['n_children'] > 0]

    members2['is_single_senior_w_children'] = 1

    """ seventy_one = left_join(x = temp71_1, y = temp71_2, by = "research_family_key") %>% 
    group_by(is_single_senior_w_children, gender) %>% 
    summarise(
    n_families = n(), .groups = "drop"
    ) """

    end_result = members1.merge(members2, how='left', on='research_family_key')
    end_result = end_result.groupby(['is_single_senior_w_children','gender'], as_index=False).agg(
        n_families=('research_family_key','count')
    )

    return end_result.to_json()

# data def 72
def get_demo_indv_gender(data:'list[DataFrame]'):
    members = data[data_service.KEY_MEMBER]

    members = members.groupby(['gender']).agg(n_indv=('gender','count')).reset_index()
    return members.to_json()

# data def 77
def get_demo_indv_ethnic(data:'list[DataFrame]'):

    """ temp77 = left_join(x = skeleton_dm_ethnic, y = base_members %>% 
    group_by(ethnic_id) %>% 
    summarize(
    n_indv = n(), .groups = "drop"
    ), by = "ethnic_id")  """

    ethnic = data[data_service.SKEY_ETH]
    members = data[data_service.KEY_MEMBER]
    ethnic = ethnic.merge(members, how='left', on='ethnic_id')

    ethnic = ethnic.groupby('ethnic_id', as_index=False).agg(
        n_indv=('ethnic_id','count')
    )

    """ seventy_seven = temp77 %>% 
    group_by(fa_rollup_ethnic) %>% summarize(n_indv = sum(n_indv), .groups = "drop") """

    ethnic = ethnic.groupby('fa_rollup_ethnic', as_index=False).agg(
        n_indv=('n_indv','sum')
    )

    return ethnic.to_json()