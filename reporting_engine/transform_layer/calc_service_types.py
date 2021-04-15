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
    #base_services = fill_gap(base_services, 'sites_visited')
    return base_services.to_json()



#requires testing on indexes
def fill_gap(dataframe, column_name):
    """Fills in the gaps between the values in the column specified by column_name of dataframe.

    Arguments:
    dataframe - the dataframe
    column_name - the column_name along which to fill in gaps


    Modifies:
    dataframe

    Returns: the dataframe filled in along column_name from 1..the maximum value in column_name.
    Ex: d = {"column_one": [1,2,4,5], "column_two": [5,5,5,5]}
        d = fill_gap(d, "column_one")

        d becomes
        column_one    column_two
        1             5  
        2             5
        3             0
        4             5
        5             5
    """
    column = dataframe[column_name].sort_values(ascending = True)
    column = column.to_numpy()
    missing_ranges = []
    for i in range(0, len(column) - 1):
        if i == 0 and column[i] != 1:
            missing_ranges.append((1,column[i]))

        if(column[i +1] != column[i] + 1):
            missing_ranges.append((column[i] + 1, column[i+1]))

    new_rows = []
    for rng in missing_ranges:
        for val in range(rng[0], rng[1]):
            new_row = {}
            for name in dataframe.columns.to_list():
                if name == column_name:
                    new_row[name] = val
                else:
                    new_row[name] = 0
            new_rows.append(new_row)
    
    new_rows = pd.DataFrame(new_rows)
    dataframe = pd.concat([dataframe, new_rows], ignore_index= True)
    dataframe = dataframe.sort_values(by = column_name, ascending = [True])
    return dataframe