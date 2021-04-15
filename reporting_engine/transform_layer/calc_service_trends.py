from pandas.core.frame import DataFrame
import dateutil.parser as parser
import pandas as pd
import json
import numpy as np

#data def 57
def get_service_trend_time_month(data: 'list[DataFrame]'):
    services = data[0]
    skeleton_month = data[3]

    trend:DataFrame = skeleton_month.merge(services, how ='left', on = 'calendaryearmonth')
    trend = trend.groupby(['calendaryearmonth','calendaryearmonth_start','calendaryearmonth_name'], as_index=False).agg(n = ('research_service_key', 'count'))
    return trend.to_json()

#data def 58
def get_service_trend_time_week(data: 'list[DataFrame]'):
    services = data[0]
    skeleton_week = data[4]

    trend:DataFrame = skeleton_week.merge(services, how ='left', on = 'sunyearweek')
    trend = trend.groupby(['sunyearweek','sunyearweek_start'], as_index=False).agg(n = ('research_service_key', 'count'))
    return trend.to_json()

# data def 59
def get_service_trend_time_day(data: 'list[DataFrame]'):
    services = data[0]
    skeleton_day = data[5]

    trend:DataFrame = skeleton_day.merge(services, how='left', on='date')
    trend = trend.groupby(['date','date_label'], as_index=False).agg(n=('research_service_key','count'))
    return trend.to_json()

# data def 60
def get_service_trend_monthy_visits_avg(data:'list[DataFrame]'):
    services = data[0]
    skeleton_month = data[3]

    trend:DataFrame = skeleton_month.merge(services, how='left', on = 'calendaryearmonth')
    trend = trend.groupby(['research_family_key','calendaryearmonth','calendaryearmonth_start','calendaryearmonth_name'], as_index=False, dropna=False).agg(
        n_services= ('calendaryearmonth','count')
    )
    trend = trend.groupby(['calendaryearmonth','calendaryearmonth_start','calendaryearmonth_name'], as_index=False, dropna=False).agg(
        n_families=('research_family_key','count'),
        n_services=('n_services','sum')
    )
    trend['services_per_family'] = round(trend['n_services']/trend['n_families'], 2)
    return trend.to_json()

# data def 64
def get_service_trend_comparison(data: 'list[DataFrame]'):
    services = data[0]
    skeleton_day = data[5]

    max_calendaryearmonth = services['calendaryearmonth'].max()
    monthofyear = services[services['calendaryearmonth'] == max_calendaryearmonth]
    unique_month = monthofyear['monthofyear'].unique()[0]

    services = services[services['monthofyear'] == unique_month].groupby(['calendaryear', 'calendaryearmonth', 'date'], as_index = False).agg(n = ('date', 'count'))
    services = pd.merge(services, skeleton_day, how = 'inner', on = 'date')
    services['order'] = services.index + 1

    return services.to_json()

# data def 65
def get_service_summary_dow(data: 'list[DataFrame]'):
    services = data[0]
    skeleton_daynameofweek = data[6]
    skeleton_daynameofweek.index = skeleton_daynameofweek.index + 1
    sort_days_dict = {
        'Sunday': 0,
        'Monday': 1,
        'Tuesday': 2,
        'Wednesday': 3,
        'Thursday': 4,
        'Friday': 5,
        'Saturday': 6
    }

    services = pd.merge(skeleton_daynameofweek, services, how = 'left', left_index = True, right_on = 'dayofweek')
    services = services.groupby('daynameofweek').agg(n_services = ('research_service_key', 'count'))
    services = services.sort_values(by = 'daynameofweek', key = lambda x: x.map(sort_days_dict)).reset_index()

    return services.to_json()

#data def 66
def get_service_summary_hod(data: 'list[DataFrame]'):
    services = data[0]
    hod_skeleton = data[8]
    hourly_services = hod_skeleton.merge(services, how = 'left', on = 'hour_of_day')
    hourly_services = hourly_services.groupby('hour_of_day', as_index = False).agg(n_services = ('research_service_key', 'count'))
    hourly_services = hod_skeleton.merge(hourly_services, how = 'left', on = 'hour_of_day')

    return hourly_services.to_json()

# data def 68
def get_service_trend_event(data:'list[DataFrame]'):
    services = data[0]
    skeleton_month = data[3]

    trend:DataFrame = skeleton_month.merge(services, how='left', on = 'calendaryearmonth')
    trend = trend.groupby(['calendaryearmonth','event_name'], as_index = False, dropna = False).size()
    trend = trend.rename(columns={"size": "n_services"})
    return trend.to_json()

