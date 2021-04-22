from pandas.core.frame import DataFrame
import dateutil.parser as parser
import pandas as pd
import json
import transform_layer.services.data_service as data_service
import numpy as np

#data def 57
def get_service_trend_time_month(data: 'dict[DataFrame]'):
    services = data[data_service.KEY_SERVICE]
    skeleton_month = data[data_service.SKEY_MONTH]

    trend:DataFrame = skeleton_month.merge(services, how ='left', on = 'calendaryearmonth')
    trend = trend.groupby(['calendaryearmonth','calendaryearmonth_start','calendaryearmonth_name'], as_index=False).agg(n = ('research_service_key', 'count'))
    return trend.to_json()

#data def 58
def get_service_trend_time_week(data: 'dict[DataFrame]'):
    services = data[data_service.KEY_SERVICE]
    skeleton_week = data[data_service.SKEY_WEEK]

    trend:DataFrame = skeleton_week.merge(services, how ='left', on = 'sunyearweek')
    trend = trend.groupby(['sunyearweek','sunyearweek_start'], as_index=False).agg(n = ('research_service_key', 'count'))
    return trend.to_json()

# data def 59
def get_service_trend_time_day(data: 'dict[DataFrame]'):
    services = data[data_service.KEY_SERVICE]
    skeleton_day = data[data_service.SKEY_DAY]

    trend:DataFrame = skeleton_day.merge(services, how='left', on='date')
    trend = trend.groupby(['date','date_label'], as_index=False).agg(n=('research_service_key','count'))
    return trend.to_json()

# data def 60
def get_service_trend_monthy_visits_avg(data:'dict[DataFrame]'):
    services = data[data_service.KEY_SERVICE]
    skeleton_month = data[data_service.SKEY_MONTH]

    trend:DataFrame = skeleton_month.merge(services, how='left', on = 'calendaryearmonth')
    trend = trend.groupby(['research_family_key','calendaryearmonth','calendaryearmonth_start','calendaryearmonth_name'], as_index=False, dropna=False).agg(
        n_services= ('calendaryearmonth','count')
    )
    trend = trend.groupby(['calendaryearmonth','calendaryearmonth_start','calendaryearmonth_name'], as_index=False, dropna=False).agg(
        n_families=('research_family_key','count'),
        n_services=('n_services','sum')
    )
    trend['services_per_family'] = round(trend['n_services'].divide(trend['n_families']), 2).replace(np.inf, 0)
    return trend.to_json()

#data def 61
def get_service_trend_monthly_people_dup(data: 'dict[DataFrame]'):
    services = data[data_service.KEY_SERVICE]
    skeleton_month = data[data_service.SKEY_MONTH]
    trend:DataFrame = skeleton_month.merge(services, how='left', on = 'calendaryearmonth')
    trend = trend.groupby(['calendaryearmonth','calendaryearmonth_start','calendaryearmonth_name'], as_index=False, dropna=False).agg(
        served_total=('served_total','sum'))
    return trend.to_json()

#data def 62
def get_service_trend_monthly_group_dup(data: 'dict[DataFrame]'):
    services = data[data_service.KEY_SERVICE]
    skeleton_month = data[data_service.SKEY_MONTH]
    trend:DataFrame = skeleton_month.merge(services, how='left', on = 'calendaryearmonth')
    trend = trend.groupby(['calendaryearmonth','calendaryearmonth_start','calendaryearmonth_name'], as_index=False, dropna=False).agg(
        sum_children=('served_children','sum'),
        sum_adults = ('served_adults','sum'),
        sum_seniors = ('served_seniors',sum))
    return trend.to_json()

#data def 63
def get_service_trend_service_category(data: 'dict[DataFrame]'):
    services = data[data_service.KEY_SERVICE]
    skeleton_month = data[data_service.SKEY_MONTH]
    trend:DataFrame = skeleton_month.merge(services, how='left', on = 'calendaryearmonth')
    trend = trend.groupby(['calendaryearmonth','calendaryearmonth_start','calendaryearmonth_name', 'service_category_name'], as_index=False, dropna=False).agg(
        n_services=('research_service_key','count'))

    return trend.to_json()


# data def 64
def get_service_trend_comparison(data: 'dict[DataFrame]'):
    services = data[data_service.KEY_SERVICE]
    skeleton_day = data[data_service.SKEY_DAY]

    max_calendaryearmonth = services['calendaryearmonth'].max()
    monthofyear = services[services['calendaryearmonth'] == max_calendaryearmonth]
    unique_month = monthofyear['monthofyear'].unique()[0]

    services = services[services['monthofyear'] == unique_month].groupby(['calendaryear', 'calendaryearmonth', 'date'], as_index = False).agg(n = ('date', 'count'))
    services = pd.merge(services, skeleton_day, how = 'inner', on = 'date')
    services['order'] = services.index + 1

    return services.to_json()

# data def 65
def get_service_summary_dow(data: 'dict[DataFrame]'):
    services = data[data_service.KEY_SERVICE]
    skeleton_daynameofweek = data[data_service.SKEY_DNOW]
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
def get_service_summary_hod(data: 'dict[DataFrame]'):
    services = data[data_service.KEY_SERVICE]
    hod_skeleton = data[data_service.SKEY_HOD]
    hourly_services = hod_skeleton.merge(services, how = 'left', on = 'hour_of_day')
    hourly_services = hourly_services.groupby('hour_of_day', as_index = False).agg(n_services = ('research_service_key', 'count'))
    hourly_services = hod_skeleton.merge(hourly_services, how = 'left', on = 'hour_of_day')

    return hourly_services.to_json()

# data def 67
def get_service_summary_dowhod(data:'dict[DataFrame]'):
    services = data[data_service.KEY_SERVICE]
    skeleton_dowhod = data[data_service.SKEY_HOD_DOW]
    
    services = services[['research_service_key','dummy_time', 'dayofweek', 'hour_of_day']]
    services = services[services['dummy_time'] == 1]
    services = services.groupby(['dayofweek','hour_of_day'], as_index=False, dropna = False).size()
    services = services.rename(columns={"size": "n_services"})
    trend = skeleton_dowhod.merge(services, how='left', left_on = ['dayofweek','hour_of_day'], right_on = ['dayofweek','hour_of_day'] )
    
    trend = trend.fillna(0)
    trend = trend.astype({'hour_of_day':'int64', 'n_services' : 'int64'})
    return trend.to_json()

# data def 68
def get_service_trend_event(data:'dict[DataFrame]'):
    services = data[data_service.KEY_SERVICE]
    skeleton_month = data[data_service.SKEY_MONTH]
    skeleton_month = skeleton_month.merge(pd.DataFrame(services['event_name'].unique()), how='cross')
    skeleton_month = skeleton_month.rename(columns = {0: 'event_name'})

    services = services.groupby(['calendaryearmonth','event_name'], as_index = False, dropna = False).size()
    services = services.rename(columns={"size": "n_services"})
    services = skeleton_month.merge(services, how='left', on = ['calendaryearmonth', 'event_name'])
    services = services.drop(columns = ['calendaryearmonth_start', 'calendaryearmonth_name'])
    services = services.fillna(0)
    services = services.astype({'n_services':'int64'})
    return services.to_json()

