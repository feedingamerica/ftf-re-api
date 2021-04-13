from pandas.core.frame import DataFrame
import dateutil.parser as parser
import pandas as pd
import json
import numpy as np

#data def 57
def get_service_trend_time_month(data: 'dict[Dataframe]'):
    services = data[0]
    skeleton_month = data[3]
    services = skeleton_month.merge(services, how ='left', on = 'calendaryearmonth')
    services = services.groupby(['calendaryearmonth']).agg(num_services = ('calendaryearmonth', 'count'))
    services = skeleton_month.merge(services, how = 'left', on = 'calendaryearmonth')
    services = services.sort_values(by = 'calendaryearmonth')
    return services.to_json()

#data def 58

def get_service_trend_time_week(data: 'dict[Dataframe]'):
    services = data[0]
    skeleton_week = data[4]
    services = skeleton_week.merge(services, how ='left', on = 'sunyearweek')
    services = services.groupby(['sunyearweek']).agg(num_services = ('sunyearweek', 'count'))
    services = skeleton_week.merge(services, how = 'left', on = 'sunyearweek')
    services = services.sort_values(by = 'sunyearweek')
    return services.to_json()