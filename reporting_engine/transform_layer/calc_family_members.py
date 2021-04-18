from pandas.core.frame import DataFrame
import dateutil.parser as parser
import pandas as pd
import json
import transform_layer.services.data_service as data_service
import numpy as np

# data def 71
def get_skipped_generation(data:'dict[DataFrame]'):

    """ temp71_1 = base_members %>% 
    filter(head_of_house == "Yes") %>% 
    select(research_family_key, gender, current_age) """

    members1 = data[data_service.KEY_MEMBER]
    members1 = members1[members1['head_of_house'] == 'Yes']
    members1 = members1[['research_family_key','gender','current_age']]

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

    members2['is_child'] = np.where(members2['current_age'] < 18, 1, 0)
    members2['is_senior'] = np.where(members2['current_age'] >= 60, 1, 0)

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

    end_result = members1.merge(members2, how='left', on='research_family_key').fillna(0)
    end_result = end_result.groupby(['is_single_senior_w_children','gender'], as_index=False).agg(
        n_families=('research_family_key','count')
    )

    return end_result.to_json()

# data def 72
def get_demo_indv_gender(data:'dict[DataFrame]'):
    members = data[data_service.KEY_MEMBER]

    members = members.groupby(['gender']).agg(n_indv=('gender','count')).reset_index()
    return members.to_json()

# data def 73
def get_demo_indv_age_groups(data:'dict[DataFrame]'):
    members = data[data_service.KEY_MEMBER]
    age_bands = data[data_service.SKEY_AGE]

    age_groups:DataFrame = age_bands.merge(members, how='left', on='age_band_name_dash')
    age_groups = age_groups.groupby(['min_age', 'age_band_name_dash']).agg(n_indv=('research_member_key','count')).reset_index()
    return age_groups.to_json()

# dat def 74
def get_hh_has_age_groups(data:'dict[DataFrame]'):
    members = data[data_service.KEY_MEMBER]
    age_bands = data[data_service.SKEY_AGE]

    age_groups: DataFrame = age_bands.merge(members, how='left', on='age_band_name_dash')
    age_groups = age_groups.groupby(['research_family_key', 'min_age', 'age_band_name_dash'], as_index=False).agg(
        n_indv = ('research_member_key', 'count')
    )
    age_groups = age_groups.groupby(['min_age','age_band_name_dash'], as_index=False).agg(
        n_families_have_indv_in_group = ('research_family_key','count'),
        sum_indv = ('n_indv','sum')
    )
    return age_groups.to_json()

# data def 75
def get_population_pyramid(data:'dict[DataFrame]'):
    members = data[data_service.KEY_MEMBER]
    age_bands = data[data_service.SKEY_AGE]
    
    # Duplicate each row in age_bands so that there are two of each row, one with a male and one with a female groupby_gender column value
    # These steps are taken in order to display age groups in the output that have a value of 0 for n_indv
    age_bands['groupby_gender'] = 'F'
    temp:DataFrame = age_bands.copy()
    temp['groupby_gender'] = 'M'
    age_bands = pd.concat([age_bands, temp], ignore_index=True)

    members = pd.merge(age_bands, members, how='left', left_on=['age_band_name_dash', 'groupby_gender'], right_on=['age_band_name_dash', 'gender'])
    members['count'] = np.where(members['research_member_key'].notnull(), 1, 0)
    members = members[(members['groupby_gender'] == 'M') | (members['groupby_gender'] == 'F')]
    members = members.groupby(['min_age', 'age_band_name_dash', 'groupby_gender']).agg(n_indv=('count', 'sum')).unstack(fill_value=0).stack().reset_index()
    members = members.rename(columns={'groupby_gender': 'gender'})

    return members.to_json()

# data def 76
def get_demo_indv_race(data:'dict[DataFrame]'):
    pass

# data def 77
def get_demo_indv_ethnic(data:'dict[DataFrame]'):

    """ temp77 = left_join(x = skeleton_dm_ethnic, y = base_members %>% 
    group_by(ethnic_id) %>% 
    summarize(
    n_indv = n(), .groups = "drop"
    ), by = "ethnic_id")  """

    ethnic = data[data_service.SKEY_ETH]
    members = data[data_service.KEY_MEMBER]
    ethnic2 = ethnic.merge(members, how='left', on='ethnic_id')

    ethnic2 = ethnic2.groupby('ethnic_id', as_index=False).agg(
        n_indv=('ethnic_id','count')
    )

    ethnic = ethnic2.merge(ethnic, how='left', on='ethnic_id')

    """ seventy_seven = temp77 %>% 
    group_by(fa_rollup_ethnic) %>% summarize(n_indv = sum(n_indv), .groups = "drop") """

    ethnic = ethnic.groupby('fa_rollup_ethnic', as_index=False).agg(
        n_indv=('n_indv','sum')
    )

    return ethnic.to_json()

#data def 79
def get_demo_indv_education(data:'dict[DataFrame]'):
    members = data[data_service.KEY_MEMBER]
    skeleton = data[data_service.SKEY_EDU]

    members = members.groupby(by = 'education_id', as_index = False).agg(n_indv = ('research_member_key', 'count'))
    members = skeleton.merge(members, on = 'education_id', how = 'left')
    members = members.groupby(by = 'fa_rollup_education', as_index = False).agg(n_indv = ('n_indv', 'sum'))
    return members.to_json()

#data def 80
def get_demo_indv_employment(data:'dict[DataFrame]'):
    members = data[data_service.KEY_MEMBER]
    skeleton = data[data_service.SKEY_EMP]

    members = members.groupby(by = 'employment_id', as_index = False).agg(n_indv = ('research_member_key', 'count'))
    members = skeleton.merge(members, on = 'employment_id', how = 'left')
    #follup_employment is not an error(at least on this end of the system). The column was misspelled when it was created in the source database
    members = members.groupby(by = 'fa_follup_employment', as_index = False).agg(n_indv = ('n_indv', 'sum'))
    return members.to_json()

#data def 81
def get_demo_indv_health_insurnace(data:'dict[DataFrame]'):
    members = data[data_service.KEY_MEMBER]
    skeleton = data[data_service.SKEY_HEALTH]

    members = members.groupby(by = 'healthcare_id', as_index = False).agg(n_indv = ('research_member_key', 'count'))
    members = skeleton.merge(members, on = 'healthcare_id', how = 'left')
    members = members.groupby(by = 'fa_rollup_healthcare', as_index = False).agg(n_indv = ('n_indv', 'sum'))
    return members.to_json()