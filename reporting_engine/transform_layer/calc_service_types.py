from pandas.core.frame import DataFrame
import dateutil.parser as parser
import pandas as pd





# data def 23
def get_services_summary(data):
    """Calculate number of people served DataDef 23

    Arguments:
    id - data definiton id
    params - a dictionary of values to scope the queries

    Modifies:
    Nothing

    Returns: num_served
    num_served - number of people served by service name

    """
    base_services = data.groupby(['service_name'])
    base_services = base_services.agg({'research_family_key': 'count', 'served_total': 'sum'})
    base_services = base_services.reset_index().rename(columns={'research_family_key':"Families Served", 'served_total': 'People Served'})
    return base_services.to_json()

# data def 24
def get_services_category(data):
    """Calculate number of people served DataDef 24

    Arguments:
    id - data definiton id
    params - a dictionary of values to scope the queries

    Modifies:
    Nothing

    Returns: num_served
    num_served - number of people served by service category

    """
    base_services = data.groupby(['service_category_name'])
    base_services = base_services.agg({'research_family_key': 'count', 'served_total': 'sum'})
    base_services = base_services.reset_index().rename(columns={'research_family_key':"Families Served", 'served_total': 'People Served'})
    return base_services.to_json()

# data def 25
def get_distribution_outlets(data):
    """Calculate number of people served DataDef 25

    Arguments:
    id - data definiton id
    params - a dictionary of values to scope the queries

    Modifies:
    Nothing

    Returns: sites_visited
    sites_visited - number of families that have made 1..n site visits

    """
    base_services = data.groupby('research_family_key')['loc_id'].nunique().reset_index().rename(columns={'loc_id': 'sites_visited'})
    base_services = base_services.groupby('sites_visited').agg(un_duplicated_families = ('sites_visited', 'count')).reset_index()
    base_services = base_services.sort_values(by = ['sites_visited'], ascending = [True])
    return base_services.to_json()


