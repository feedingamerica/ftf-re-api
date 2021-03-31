from pandas.core.frame import DataFrame
import dateutil.parser as parser
import pandas as pd
from django.db import connections


import copy




    


#calculations for data_def 1
def get_services_total(data):
    services_total = data.drop_duplicates(subset = 'research_service_key', inplace = False)
    return len(services_total)

def get_undup_hh_total(data):
    hh_total = data.drop_duplicates(subset = 'research_family_key', inplace = False)
    return len(hh_total)

def get_undup_indv_total(data):
    undup_indv = data.drop_duplicates(subset = 'research_member_key', inplace = False)
    return len(undup_indv)

#data def 4
def get_services_per_uhh_avg(data):
    """Calculate number of services per family DataDef 4

    Arguments:
    id - data definiton id
    params - a dictionary of values to scope the queries

    Modifies:
    Nothing

    Returns: num_services_avg
    num_services_avg - average number of services per family

    """
    services = get_services_total(data)
    families = get_undup_hh_total(data)
    return services/families

#data def 5
def get_wminor(data):
    services = data.drop_duplicates(subset = 'research_service_key', inplace = False)
    w_minor =  services[services['served_children']>0] 
    return len(w_minor)


##  data Definition 6
####    Returns: len(services)
####        services - fact service data table, filtered on served_children == 0
def get_wominor(data):
    services = data.drop_duplicates(subset = 'research_service_key', inplace = False)
    wo_minor = services[services['served_children']==0]
    return len(wo_minor)

#data definition 7 is a duplicate of data definition 1

#Data Definitions 8
####    Returns: sen_hh_wminor
####        sen_hh_wminor - fact service data table, filtered on served_children > 0 and served_seniors > 0
def get_indv_sen_hh_wminor(data):
    services = data.drop_duplicates(subset = 'research_service_key', inplace = False)
    seniors = services[services['served_seniors']>0]
    senior_wminor = seniors[seniors['served_children']>0]
    return senior_wminor['served_seniors'].sum()

##Data Definition 9
####    Returns: sen_hh_wominor
####        sen_hh_wominor - fact service data table, filtered on served_children == 0 and served_seniors > 0
def get_indv_sen_hh_wominor(data):
    services = data.drop_duplicates(subset = 'research_service_key', inplace = False)
    seniors = services[services['served_seniors']>0]
    senior_wominor =  seniors[seniors['served_children']==0]
    return senior_wominor['served_seniors'].sum()

## DataFrame to fulfill Data Definitions 10, 20
####    Returns: sen_hh
####        sen_hh - fact service data table, filtered on served_seniors > 0
def get_sen_total(data):
    services = data.drop_duplicates(subset = 'research_service_key', inplace = False)
    seniors = services[services['served_seniors']>0]
    return seniors['served_seniors'].sum()

    ## DataFrame to fulfill Data Definition 11
####    Returns: adult_hh_wminor
####        adult_hh_wminor - fact service data table, filtered on served_children > 0 and served_adults > 0
def get_adult_wminor(data):
    services = data.drop_duplicates(subset = 'research_service_key', inplace = False)
    adults = services[services['served_adults']>0]
    adults_wminor = adults[adults['served_children']>0]
    return adults_wminor['served_adults'].sum()

    ## DataFrame to fulfill Data Definition 12
####    Returns: adult_hh_wominor
####        adult_hh_wominor - fact service data table, filtered on served_children == 0 and served_adults > 0
def get_adult_wominor(data):
    services = data.drop_duplicates(subset = 'research_service_key', inplace = False)
    adults = services[services['served_adults']>0]
    adults_wominor =  adults[adults['served_children']==0]
    return adults_wominor['served_adults'].sum()


    ## DataFrame to fulfill Data Definition 13
####    Returns: adult_hh
####        adult_hh - fact service data table, filtered on served_adults > 0

def get_adult(data):
    services = data.drop_duplicates(subset = 'research_service_key', inplace = False)
    adults =  services[services['served_adults']>0]
    return adults['served_adults'].sum()

    ## DataFrame to fulfill Data Definitions 14
####    Returns: services
####        services - fact service data table, filtered on served_children > 0
def get_indv_child_hh_wminor(data):
    services = data.drop_duplicates(subset = 'research_service_key', inplace = False)
    children = services[services['served_children']>0]
    children_served = children['served_children'].sum()
    return children_served

    ## DataFrame to fulfill Data Definition 15
####    Returns: empty
####        empty - empty data table (no such thing as children wo minors)
def get_indv_child_hh_wominor(data):
    return 0

#data definition 16
def get_indv_child_total(data):
    return get_indv_child_hh_wminor(data)

#data definition 17
def get_indv_total_hh_wminor(data):
    services = data.drop_duplicates(subset = 'research_service_key', inplace = False)
    w_child = services[services['served_children']>0]
    return w_child['served_total'].sum()

#data definition 18
def get_indv_total_hh_wominor(data):
    services = data.drop_duplicates(subset = 'research_service_key', inplace = False)
    wo_child = services[services['served_children'] == 0]
    return wo_child['served_total'].sum()

#data definition 19
def get_indv_total(data):
    services = data.drop_duplicates(subset = 'research_service_key', inplace = False)
    return services['served_total'].sum()

#data definition 20
def get_hh_wsenior(data):
    services = data.drop_duplicates(subset = 'research_service_key', inplace = False)
    w_senior = services[services['served_seniors']>0]
    return len(w_senior)

#data definition 21
def get_hh_wosenior(data):
    services = data.drop_duplicates(subset = 'research_service_key', inplace = False)
    wo_senior = services[services['served_seniors'] == 0]
    return len(wo_senior)

#data definition 22
def get_hh_grandparent(data):
    services = data.drop_duplicates(subset = 'research_service_key', inplace = False)
    seniors =  services[services['served_seniors']>0]
    seniors_w_minor = seniors[seniors['served_children']>0]
    return len(seniors_w_minor)





#