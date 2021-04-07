from pandas.core.frame import DataFrame
import dateutil.parser as parser
import pandas as pd
import json
import statistics

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
    pass

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
