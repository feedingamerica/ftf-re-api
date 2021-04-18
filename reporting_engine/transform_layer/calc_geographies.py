from pandas.core.base import DataError
from pandas.core.frame import DataFrame
import dateutil.parser as parser
import pandas as pd
import numpy as np
import json
import statistics
import numpy as np
from transform_layer.services.data_service import KEY_FAMILY, KEY_MEMBER, KEY_SERVICE

#data def 47
def get_geo_coverage(data: 'dict[DataFrame]'):
    families = data[KEY_FAMILY]

    families = families.assign(has_dim_geo_id=np.where(families.dimgeo_id>0, 1, 0))
    families = families.groupby('has_dim_geo_id', as_index=False).agg(n = ('has_dim_geo_id','size'))

    has_geo = families[families['has_dim_geo_id']==1]
    no_geo = families[families['has_dim_geo_id']==0]

    num_has_geo = has_geo['n'].sum()
    sum = has_geo['n'].sum() + no_geo['n'].sum()
    return np.round(num_has_geo / sum, 3)

#data def 48
def get_geo_breakdown_fam_state(data: 'dict[DataFrame]'):
    members = data[KEY_MEMBER]

    members = members.groupby('fips_state', dropna=False).agg(
        n_families = ('research_family_key','nunique'),
        n_indv = ('research_family_key','size')
    )
    # because of NA values, groupby forces index as float,
    # so to send properly float -> int -> str
    members.index = members.index.astype("Int64").astype(str)
    return members.to_json()

#data def 49
def get_geographic_breakdown_fam_county(data: 'dict[DataFrame]'):
    members = data[KEY_MEMBER]
    members =members.groupby('fips_cnty',dropna=False)
    members = members.agg(n_families = ("research_family_key", "nunique"), n_indv = ("research_member_key","count"))
    members.index = members.index.astype("Int64").astype(str)
    return members.to_json()

#data def 50
def get_geographic_breakdown_fam_zcta(data: 'dict[DataFrame]'):
     members = data[KEY_MEMBER]
     members =members.groupby('fips_zcta',dropna=False)
     members = members.agg(n_families = ("research_family_key", "nunique"), n_indv = ("research_member_key","count"))
     members.index = members.index.astype("Int64").astype(str)
     return members.to_json()

# data def 51
def get_services_flow_event_fips(data: 'dict[DataFrame]'):
    services = data[KEY_SERVICE]
    services = services.groupby(['fips_cnty_event', 'fips_cnty_fs'], dropna=False).size().to_frame('n').reset_index()
    return services.to_json()

# data def 52
def get_distance_traveled(data: 'dict[DataFrame]'):
    services = data[KEY_SERVICE]
    services = services[services['dummy_trip'] == 1]
    services = services.sort_values(by = 'distance_miles', ascending = True)

    conditions = [
        (services['distance_miles'] < 1),
        (services['distance_miles'] < 2),
        (services['distance_miles'] < 3),
        (services['distance_miles'] < 6),
        (services['distance_miles'] < 10),
        (services['distance_miles'] < 15),
        (services['distance_miles'] < 25),
        (services['distance_miles'] >= 25)
    ]
    values = [
        '< 1 mile',
        '1 - 1.99 miles',
        '2 - 2.99 miles',
        '3 - 5.99 miles',
        '6 - 9.99 miles',
        '10 - 14.99 miles',
        '15 - 24.99 miles',
        '25+ miles'
    ]
    if(len(services) == 0):
        #fill with all zeroes if no services w/ dummy_trip == 1
        v = len(values)
        services = pd.DataFrame({'distance_roll': values, 
                                'services': [0]*v, 
                                'mean_distance': [0]*v, 
                                'median_distance': [0] *v ,
                                'min_distance': [0]*v,
                                'max_distance': [0]*v})
    else:
        services['distance_roll'] = np.select(conditions, values)
        services = services.groupby('distance_roll').agg(
            services = ('research_service_key', 'count'),
            mean_distance = ('distance_miles', 'mean'),
            median_distance = ('distance_miles', 'median'),
            min_distance = ('distance_miles', 'min'),
            max_distance = ('distance_miles', 'max')
        )
        services = services.sort_values(by = 'min_distance', ascending = True)
    return services.to_json()

# data def 53
def get_direction_traveled(data: 'dict[DataFrame]'):
    services = data[KEY_SERVICE]
    services = services[services['dummy_trip'] == 1]

    if(len(services) == 0):
        #fill with all zeroes if no services w/ dummy_trip == 1
        directions = ['N', 'NE','E', 'SE', 'S', 'SW', 'W', 'NW'] 
        v = len(directions)
        services = pd.DataFrame({'direction': directions, 
                                'services': [0]*v, 
                                'mean_distance': [0]*v, 
                                'median_distance': [0] *v ,
                                'min_distance': [0]*v,
                                'max_distance': [0]*v})
    else:
        services = services.groupby('direction').agg(
            services = ('research_service_key', 'count'),
            mean_distance = ('distance_miles', 'mean'),
            median_distance = ('distance_miles', 'median'),
            min_distance = ('distance_miles', 'min'),
            max_distance = ('distance_miles', 'max')
        )
        services = services.sort_values(by = 'min_distance', ascending = True)
    return services.to_json()

# data def 54
def get_windrose(data: 'dict[DataFrame]'):
    services = data[KEY_SERVICE]
    services = services[services['dummy_trip'] == 1]
    services = services.sort_values(by = ['distance_miles','direction'], ascending = True)

    conditions = [
        (services['distance_miles'] < 1),
        (services['distance_miles'] < 2),
        (services['distance_miles'] < 3),
        (services['distance_miles'] < 6),
        (services['distance_miles'] < 10),
        (services['distance_miles'] < 15),
        (services['distance_miles'] < 25),
        (services['distance_miles'] >= 25),
    ]
    values = [
        '< 1 mile',
        '1 - 1.99 miles',
        '2 - 2.99 miles',
        '3 - 5.99 miles',
        '6 - 9.99 miles',
        '10 - 14.99 miles',
        '15 - 24.99 miles',
        '25+ miles'
    ]

    if(len(services) == 0):
        #fill with all zeroes if no services w/ dummy_trip == 1
        directions = ['N', 'NE','E', 'SE', 'S', 'SW', 'W', 'NW']
        direction_values = []
        distance_roll_values = []
       
        for val in values:
            for direction in directions:
                direction_values += [direction] 
                distance_roll_values += [val]

        v = len(directions) * len(values)
        services = pd.DataFrame({'direction': direction_values, 
                                 'distance_roll': distance_roll_values,
                                'services': [0]*v, 
                                'mean_distance': [0]*v, 
                                'median_distance': [0] *v ,
                                'min_distance': [0]*v,
                                'max_distance': [0]*v})
        #have to sort but shouldn't reset index here b/c have 
        #already split 'direction' and 'distance_roll' into their own columns
        #services = services.sort_values(by = ['distance_roll','direction'], ascending = True)
    else:
        services['distance_roll'] = np.select(conditions, values)
        services = services.groupby(['distance_roll','direction']).agg(
            services = ('research_service_key', 'count'),
            mean_distance = ('distance_miles', 'mean'),
            median_distance = ('distance_miles', 'median'),
            min_distance = ('distance_miles', 'min'),
            max_distance = ('distance_miles', 'max')
        )
        services = services.sort_values(by = ['min_distance', 'direction'], ascending = True)
        services = services.reset_index()
    return services.to_json()

#data def 55
def get_sites_visited_distribution(data):
    services = data[KEY_SERVICE]
    services = services.groupby(['loc_id', 'research_family_key']).agg(services = ('research_service_key','count')).reset_index()
    services = services.groupby(['research_family_key']).agg(sites_visited = ('loc_id', 'count'))
    services = services.groupby(['sites_visited']).agg(num_families = ('sites_visited', 'count'))
    return services.to_json()

#data def 56
def get_dummy_trip_coverage(data):
    services = data[KEY_SERVICE]
    num_services = len(services)
    services = services[services['dummy_trip'] == 1]
    return round( len(services)/num_services, 4)
