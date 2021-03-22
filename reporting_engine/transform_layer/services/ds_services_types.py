from pandas.core.frame import DataFrame
import dateutil.parser as parser
import pandas as pd
from django.db import connections
from transform_layer.services.utils import date_str_to_int, get_control_query

import copy


class ServiceTypesDataService:
    def __init__(self, scope):
        self._base_services: DataFrame = None
        self.scope = scope

    ## getter and setter for __base_services
    ##  Columns always in services:
    ##      research_service_key
    ##      research_family_key
    ##      service_id
    ##      service_name
    ##      service_category_code
    ##      service_category_name
    ##      served_total
    ##      loc_id
    @property
    def base_services(self,params):
        if self._base_services is None:
            self._base_services = self.__get_base_services(params)
        return self._base_services


    def __get_base_services(self):
        conn = connections['source_db']

        extra_join = ""
        if self.scope["scope_type"] == "hierarchy":
            table1 = "dim_hierarchies"
            left1 = right1 = "hierarchy_id"
        elif self.scope["scope_type"] == "geography":
            table1 = "dim_geos"
            left1 = "dimgeo_id"
            right1 = "id"
            extra_join = """INNER JOIN dim_hierarchies ON fact_services.hiearchy_id = dim_hiearchies.loc_id"""

        control_type_name = self.scope["control_type_name"]
        control_query = get_control_query(control_type_name)
        scope_field = self.scope["scope_field"]
        scope_value = self.scope["scope_field_value"]
        start_date = date_str_to_int(self.scope["startDate"])
        end_date = date_str_to_int(self.scope["endDate"])

        query = f"""
        SELECT
            fact_services.research_service_key,
            fact_services.research_family_key,
            fact_services.service_id,
            dim_service_types.name as service_name,
            dim_service_types.service_category_code,
            dim_service_types.service_category_name,
            fact_services.served_total,
            dim_hierarchies.loc_id
        FROM
            fact_services
            INNER JOIN dim_service_types ON fact_services.service_id = dim_service_types.id
            INNER JOIN {table1} ON fact_services.{left1} = {table1}.{right1}
            {extra_join if self.scope["scope_type"] == "geography" else ""}
        WHERE
            fact_services.service_status = 17 
            AND {control_query}
            AND fact_services.date >= {start_date} AND fact_services.date <= {end_date}
            AND {table1}.{scope_field} = {scope_value}
        """
        return pd.read_sql(query, conn)



    # data def 23
    def __get_services_summary(self):
        """Calculate number of people served DataDef 23

        Arguments:
        id - data definiton id
        params - a dictionary of values to scope the queries

        Modifies:
        Nothing

        Returns: num_served
        num_served - number of people served by service name

        """
        base_services = self.base_services().groupby(['service_name'])
        base_services = base_services.agg({'research_family_key': 'count', 'served_total': 'sum'})
        base_services = base_services.reset_index().rename(columns={'research_family_key':"Families Served", 'served_total': 'People Served'})
        return base_services.to_json()

    # data def 24
    def __get_services_category(self):
        """Calculate number of people served DataDef 24

        Arguments:
        id - data definiton id
        params - a dictionary of values to scope the queries

        Modifies:
        Nothing

        Returns: num_served
        num_served - number of people served by service category

        """
        base_services = self.base_services().groupby(['service_category_name'])
        base_services = base_services.agg({'research_family_key': 'count', 'served_total': 'sum'})
        base_services = base_services.reset_index().rename(columns={'research_family_key':"Families Served", 'served_total': 'People Served'})
        return base_services.to_json()

    # data def 25
    def __get_distribution_outlets(self):
        """Calculate number of people served DataDef 25

        Arguments:
        id - data definiton id
        params - a dictionary of values to scope the queries

        Modifies:
        Nothing

        Returns: sites_visited
        sites_visited - number of families that have made 1..n site visits

        """
        base_services = self.base_services()
        base_services = base_services.groupby('research_family_key')['loc_id'].nunique().reset_index().rename(columns={'loc_id': 'sites_visited'})
        base_services = base_services.groupby('sites_visited').agg(un_duplicated_families = ('sites_visited', 'count')).reset_index()
        base_services = base_services.sort_values(by = ['sites_visited'], ascending = [True])
        return base_services.to_json()


    def get_data_for_definition(self, id):
        data_def_function_switcher = {
            23: self.__get_services_summary.__name__,
            24: self.__get_services_category.__name__,
            25: self.__get_distribution_outlets.__name__
        }   

        func = getattr(self, data_def_function_switcher[id],  lambda _: DataFrame())
        return func()