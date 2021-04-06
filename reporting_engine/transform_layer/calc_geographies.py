from pandas.core.frame import DataFrame
import dateutil.parser as parser
import pandas as pd
import json

# data def 53
def get_direction_traveled(data: 'list[DataFrame]'):
    families = data[1]
    print(str(families.iloc[0]))
    pass

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
