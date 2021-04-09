from pandas.core.base import DataError
from pandas.core.frame import DataFrame
import dateutil.parser as parser
import pandas as pd
import numpy as np
import json
import statistics
import numpy as np


#data def 49
def get_geographic_breakdown_fam_county(data: 'list[DataFrame]'):
    members = data[2]
    members =members.groupby(['fips_cnty'])
    members = members.agg(n_families = ("research_family_key", "nunique"), n_indv = ("research_member_key","count"))
    return members.to_json()

#data def 50
def get_geographic_breakdown_fam_zcta(data: 'list[DataFrame]'):
     members = data[2]
     members =members.groupby(['fips_zcta'])
     members = members.agg(n_families = ("research_family_key", "nunique"), n_indv = ("research_member_key","count"))
     return members.to_json()

# data def 51
def get_services_flow_event_fips(data: 'list[DataFrame]'):
    services = data[0]
    services = services.groupby(['fips_cnty_event', 'fips_cnty_fs'], dropna=False).size().to_frame('n').reset_index()
    return services.to_json()

# data def 52
def get_distance_traveled(data: 'list[DataFrame]'):
    services = data[0]
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

#data def 47
def get_geo_coverage(data: 'list[DataFrame]'):
    families = data[1]

    families = families.assign(has_dim_geo_id=np.where(families.dimgeo_id>0, 1, 0))
    families = families.groupby('has_dim_geo_id').agg(n = ('has_dim_geo_id','size')).sort_values('has_dim_geo_id')

    num_has_geo = families.iloc[1]['n']
    sum = families['n'].sum()

    return np.round(num_has_geo / sum, 3)

#data def 48
def get_geo_breakdown_fam_state(data: 'list[DataFrame]'):
    members = data[2]

    members = members.groupby('fips_state').agg(
        n_families = ('research_family_key','nunique'),
        n_indv = ('research_family_key','size')
    )

    return members.to_json()

# data def 53
def get_direction_traveled(data: 'list[DataFrame]'):
    services = data[0]

    distance_dict = {
        'NE':list(),
        'N':list(),
        'SE':list(),
        'E':list(),
        'W':list(),
        'SW':list(),
        'NW':list(),
        'S':list()
    }

    result_dict = {
        'NE': {
            'services':0,
            'mean_distance':0,
            'median_distance':0,
            'min_distance':0,
            'max_distance':0
        },
        'N': {
            'services':0,
            'mean_distance':0,
            'median_distance':0,
            'min_distance':0,
            'max_distance':0
        },
        'SE': {
            'services':0,
            'mean_distance':0,
            'median_distance':0,
            'min_distance':0,
            'max_distance':0
        },
        'E': {
            'services':0,
            'mean_distance':0,
            'median_distance':0,
            'min_distance':0,
            'max_distance':0
        },
        'W': {
            'services':0,
            'mean_distance':0,
            'median_distance':0,
            'min_distance':0,
            'max_distance':0
        },
        'SW': {
            'services':0,
            'mean_distance':0,
            'median_distance':0,
            'min_distance':0,
            'max_distance':0
        },
        'NW': {
            'services':0,
            'mean_distance':0,
            'median_distance':0,
            'min_distance':0,
            'max_distance':0
        },
        'S': {
            'services':0,
            'mean_distance':0,
            'median_distance':0,
            'min_distance':0,
            'max_distance':0
        },
    }

    for index, row in services.iterrows():

        if row["direction"] != None:
            result_dict[row["direction"]]["services"]+=1
            distance_dict[row["direction"]].append(row["distance_miles"])

    for direction in result_dict:
        result_dict[direction]["mean_distance"] = (sum(distance_dict[direction])/len(distance_dict[direction]))
        result_dict[direction]["median_distance"] = statistics.median(distance_dict[direction])
        result_dict[direction]["min_distance"] = min(distance_dict[direction])
        result_dict[direction]["max_distance"] = max(distance_dict[direction])

    return json.dumps(result_dict)

# data def 54
def get_windrose(data: 'list[DataFrame]'):
    services = data[0]
    services = services[services['dummy_trip'] == 1]
    services = services.sort_values(by = ['distance_miles','direction'], ascending = True)

    conditions = [
        (services['distance_miles'] < 1) & (services['direction'] == 'NE'),
        (services['distance_miles'] < 1) & (services['direction'] == 'N'),
        (services['distance_miles'] < 1) & (services['direction'] == 'SE'),
        (services['distance_miles'] < 1) & (services['direction'] == 'E'),
        (services['distance_miles'] < 1) & (services['direction'] == 'W'),
        (services['distance_miles'] < 1) & (services['direction'] == 'SW'),
        (services['distance_miles'] < 1) & (services['direction'] == 'NW'),
        (services['distance_miles'] < 1) & (services['direction'] == 'S'),
        (services['distance_miles'] < 2) & (services['direction'] == 'NE'),
        (services['distance_miles'] < 2) & (services['direction'] == 'N'),
        (services['distance_miles'] < 2) & (services['direction'] == 'SE'),
        (services['distance_miles'] < 2) & (services['direction'] == 'E'),
        (services['distance_miles'] < 2) & (services['direction'] == 'W'),
        (services['distance_miles'] < 2) & (services['direction'] == 'SW'),
        (services['distance_miles'] < 2) & (services['direction'] == 'NW'),
        (services['distance_miles'] < 2) & (services['direction'] == 'S'),
        (services['distance_miles'] < 3) & (services['direction'] == 'NE'),
        (services['distance_miles'] < 3) & (services['direction'] == 'N'),
        (services['distance_miles'] < 3) & (services['direction'] == 'SE'),
        (services['distance_miles'] < 3) & (services['direction'] == 'E'),
        (services['distance_miles'] < 3) & (services['direction'] == 'W'),
        (services['distance_miles'] < 3) & (services['direction'] == 'SW'),
        (services['distance_miles'] < 3) & (services['direction'] == 'NW'),
        (services['distance_miles'] < 3) & (services['direction'] == 'S'),
        (services['distance_miles'] < 6) & (services['direction'] == 'NE'),
        (services['distance_miles'] < 6) & (services['direction'] == 'N'),
        (services['distance_miles'] < 6) & (services['direction'] == 'SE'),
        (services['distance_miles'] < 6) & (services['direction'] == 'E'),
        (services['distance_miles'] < 6) & (services['direction'] == 'W'),
        (services['distance_miles'] < 6) & (services['direction'] == 'SW'),
        (services['distance_miles'] < 6) & (services['direction'] == 'NW'),
        (services['distance_miles'] < 6) & (services['direction'] == 'S'),
        (services['distance_miles'] < 10) & (services['direction'] == 'NE'),
        (services['distance_miles'] < 10) & (services['direction'] == 'N'),
        (services['distance_miles'] < 10) & (services['direction'] == 'SE'),
        (services['distance_miles'] < 10) & (services['direction'] == 'E'),
        (services['distance_miles'] < 10) & (services['direction'] == 'W'),
        (services['distance_miles'] < 10) & (services['direction'] == 'SW'),
        (services['distance_miles'] < 10) & (services['direction'] == 'NW'),
        (services['distance_miles'] < 10) & (services['direction'] == 'S'),
        (services['distance_miles'] < 15) & (services['direction'] == 'NE'),
        (services['distance_miles'] < 15) & (services['direction'] == 'N'),
        (services['distance_miles'] < 15) & (services['direction'] == 'SE'),
        (services['distance_miles'] < 15) & (services['direction'] == 'E'),
        (services['distance_miles'] < 15) & (services['direction'] == 'W'),
        (services['distance_miles'] < 15) & (services['direction'] == 'SW'),
        (services['distance_miles'] < 15) & (services['direction'] == 'NW'),
        (services['distance_miles'] < 15) & (services['direction'] == 'S'),
        (services['distance_miles'] < 25) & (services['direction'] == 'NE'),
        (services['distance_miles'] < 25) & (services['direction'] == 'N'),
        (services['distance_miles'] < 25) & (services['direction'] == 'SE'),
        (services['distance_miles'] < 25) & (services['direction'] == 'E'),
        (services['distance_miles'] < 25) & (services['direction'] == 'W'),
        (services['distance_miles'] < 25) & (services['direction'] == 'SW'),
        (services['distance_miles'] < 25) & (services['direction'] == 'NW'),
        (services['distance_miles'] < 25) & (services['direction'] == 'S'),
        (services['distance_miles'] >= 25) & (services['direction'] == 'NE'),
        (services['distance_miles'] >= 25) & (services['direction'] == 'N'),
        (services['distance_miles'] >= 25) & (services['direction'] == 'SE'),
        (services['distance_miles'] >= 25) & (services['direction'] == 'E'),
        (services['distance_miles'] >= 25) & (services['direction'] == 'W'),
        (services['distance_miles'] >= 25) & (services['direction'] == 'SW'),
        (services['distance_miles'] >= 25) & (services['direction'] == 'NW'),
        (services['distance_miles'] >= 25) & (services['direction'] == 'S')
    ]
    values = [
        '< 1 mile',
        '< 1 mile',
        '< 1 mile',
        '< 1 mile',
        '< 1 mile',
        '< 1 mile',
        '< 1 mile',
        '< 1 mile',
        '1 - 1.99 miles',
        '1 - 1.99 miles',
        '1 - 1.99 miles',
        '1 - 1.99 miles',
        '1 - 1.99 miles',
        '1 - 1.99 miles',
        '1 - 1.99 miles',
        '1 - 1.99 miles',
        '2 - 2.99 miles',
        '2 - 2.99 miles',
        '2 - 2.99 miles',
        '2 - 2.99 miles',
        '2 - 2.99 miles',
        '2 - 2.99 miles',
        '2 - 2.99 miles',
        '2 - 2.99 miles',
        '3 - 5.99 miles',
        '3 - 5.99 miles',
        '3 - 5.99 miles',
        '3 - 5.99 miles',
        '3 - 5.99 miles',
        '3 - 5.99 miles',
        '3 - 5.99 miles',
        '3 - 5.99 miles',
        '6 - 9.99 miles',
        '6 - 9.99 miles',
        '6 - 9.99 miles',
        '6 - 9.99 miles',
        '6 - 9.99 miles',
        '6 - 9.99 miles',
        '6 - 9.99 miles',
        '6 - 9.99 miles',
        '10 - 14.99 miles',
        '10 - 14.99 miles',
        '10 - 14.99 miles',
        '10 - 14.99 miles',
        '10 - 14.99 miles',
        '10 - 14.99 miles',
        '10 - 14.99 miles',
        '10 - 14.99 miles',
        '15 - 24.99 miles',
        '15 - 24.99 miles',
        '15 - 24.99 miles',
        '15 - 24.99 miles',
        '15 - 24.99 miles',
        '15 - 24.99 miles',
        '15 - 24.99 miles',
        '15 - 24.99 miles',
        '25+ miles',
        '25+ miles',
        '25+ miles',
        '25+ miles',
        '25+ miles',
        '25+ miles',
        '25+ miles',
        '25+ miles'
    ]

    services['distance_roll'] = np.select(conditions, values)
    services = services.groupby(['distance_roll','direction']).agg(
        services = ('research_service_key', 'count'),
        mean_distance = ('distance_miles', 'mean'),
        median_distance = ('distance_miles', 'median'),
        min_distance = ('distance_miles', 'min'),
        max_distance = ('distance_miles', 'max')
    )
    services = services.sort_values(by = 'min_distance', ascending = True)
    return services.to_json()

#data def 55
def get_sites_visited_distribution(data):
    services = data[0]
    services = services.groupby(['loc_id', 'research_family_key']).agg(services = ('research_service_key','count')).reset_index()
    services = services.groupby(['research_family_key']).agg(sites_visited = ('loc_id', 'count'))
    services = services.groupby(['sites_visited']).agg(num_families = ('sites_visited', 'count'))
    return services.to_json()

#data def 56
def get_dummy_trip_coverage(data):
    services = data[0]
    num_services = len(services)
    services = services[services['dummy_trip'] == 1]
    return round( len(services)/num_services, 4)
