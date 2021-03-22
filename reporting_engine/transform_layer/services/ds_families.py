import dateutil.parser as parser
from django.db import connections
import numpy as np
import pandas as pd
from pandas.core.frame import DataFrame


import copy
import json


from transform_layer.services.utils import date_str_to_int, get_control_query



class FamiliesDataService:
    def __init__(self, scope):
        self._family_services: DataFrame = None
        self.scope = scope
        
    def family_services(self):
        if self._family_services is None:
            self._family_services = self.__get_family_services(self.scope)
        return self._family_services


    def __get_family_services(self):
        conn = connections['source_db']

        table1 = ""
        left1 = right1 = ""

        if self.scope["scope_type"] == "hierarchy":
            table1 = "dim_hierarchies"
            left1 = right1 = "hierarchy_id"
        elif self.scope["scope_type"] == "geography":
            table1 = "dim_geos"
            left1 = "dimgeo_id"
            right1 = "id"

        control_type_name = self.scope["control_type_name"]
        control_query = get_control_query(control_type_name)
        scope_field = self.scope["scope_field"]
        scope_value = self.scope["scope_field_value"]
        start_date = date_str_to_int(self.scope["startDate"])
        end_date = date_str_to_int(self.scope["endDate"])

        query = f"""
        SELECT
            fact_services.research_family_key,
            COUNT(fact_services.research_service_key) AS num_services,
            AVG(fact_services.served_total) AS avg_fam_size,
            SUM(fact_services.is_first_service_date) as timeframe_has_first_service_date,
            AVG(fact_services.days_since_first_service) AS avg_days_since_first_service,
            MAX(fact_services.days_since_first_service) AS max_days_since_first_service,
            dim_family_compositions.family_composition_type
        FROM 
            fact_services
            INNER JOIN dim_families ON fact_services.research_family_key = dim_families.research_family_key
            INNER JOIN dim_family_compositions ON dim_families.family_composition_type = dim_family_compositions.id
            INNER JOIN dim_service_types ON fact_services.service_id = dim_service_types.id
            INNER JOIN {table1}  ON fact_services.{left1} = {table1}.{right1}
        WHERE
            fact_services.service_status = 17 
            AND {control_query}
            AND fact_services.date >= {start_date} AND fact_services.date <= {end_date}
            AND {table1}.{scope_field} = {scope_value}
        GROUP BY
            fact_services.research_family_key,
            dim_family_compositions.family_composition_type
        """
        
        return pd.read_sql(query, conn)


        #data def 26/27 (return same data, outputted graph just has different y axis depending on def )
    def get_frequency_visits(self):
        families = self.family_services()
        families = families.groupby(['num_services'])
        families = families.agg({'research_family_key': 'count', 'num_services': 'sum'})
        largeSum = families.iloc[24:].sum()
        families.at[25, 'research_family_key'] = largeSum.iloc[0]
        families.at[25, 'num_services'] = largeSum.iloc[1]
        families = families.rename(columns={'research_family_key' :'n_families', 'num_services':'sum_services'})
        families = families.head(25)
        return families.to_json()

    #data def 28
    def get_household_composition(self):
        families = self.family_services()
        
        families = families.groupby('family_composition_type').agg(num_families = ('family_composition_type', 'count')).reset_index()
        return families.to_json()

    #data def 29
    def get_family_comp_key_insight(self):
        families = self.family_services()
        families = families.groupby('family_composition_type').agg(num_families = ('family_composition_type', 'count'))

        def choose_group(index_name):
            if index_name.find("child") >= 0 or index_name.find("senior") >= 0:
                return "has_child_senior"
            else:
                return "no_child_senior"
        families = families.groupby(by = choose_group).sum().reset_index()
        families = families.rename(columns = {"index":"family_composition_type"})


        #reset the index at the end

        return families.to_json()

    #data def 30
    def get_household_size_distribution_1_to_10(self):
        """Calculate Families Breakdown DataDef 30

        Arguments:
        id - data definiton id
        params - a dictionary of values to scope the queries

        Modifies:
        Nothing

        Returns: num_families
        num_families - number of families per sizes 1 to 10

        """

        families = self.family_services()
        families.avg_fam_size = families.avg_fam_size.round()
        families['avg_fam_size_roll'] = np.where(families['avg_fam_size'] > 9, 10, families['avg_fam_size'])
        families['avg_fam_size_roll'] = np.where(families['avg_fam_size_roll'] == 0, 1, families['avg_fam_size_roll'])
        families = families.groupby('avg_fam_size_roll').agg(num_families = ('avg_fam_size_roll', 'count')).reset_index()

        conditions = [(families['avg_fam_size_roll'] < 4), (families['avg_fam_size_roll'] < 7), (families['avg_fam_size_roll'] >= 7)]
        choices = ['1 - 3', '4 - 6', '7+']

        families['classic_roll'] = np.select(conditions, choices)

        return families.to_json()

    #data def 31
    def get_household_size_distribution_classic(self):
        families = self.family_services()

        families = families.groupby('avg_fam_size').count()

        """ for i in range(len(families)):
            """

        framework_dict = families.to_dict()
        framework_dict = framework_dict['research_family_key']

        return_dict = {
            '1 - 3':0,
            '4 - 6':0,
            '7+':0
        }

        for key in framework_dict:
            if key >= 0 and key < 3.5:
                return_dict['1 - 3'] = return_dict['1 - 3'] + framework_dict[key]
            elif key >= 3.5 and key < 6.5:
                return_dict['4 - 6'] = return_dict['4 - 6'] + framework_dict[key]
            elif key >= 6.5:
                return_dict['7+'] = return_dict['7+'] + framework_dict[key]

        return json.dumps(return_dict)




    def get_data_for_definition(self, id):
        data_def_function_switcher = {
            26: self.get_frequency_visits.__name__,
            27: self.get_frequency_visits.__name__,
            28: self.get_household_composition.__name__,
            29: self.get_family_comp_key_insight.__name__,
            30: self.get_household_size_distribution_1_to_10.__name__,
            31: self.get_family_comp_key_insight.__name__,
        }   
 
        func = getattr(self, data_def_function_switcher[id],  lambda: None)
        return func()

    





