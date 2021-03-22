from pandas.core.frame import DataFrame
import dateutil.parser as parser
import pandas as pd
from django.db import connections
from transform_layer.services.utils import date_str_to_int, get_control_query

import copy


class FactServicesDataService:
    _stored_scope = None
    _stored_services = None

    def __init__(self, scope):
        if(scope != FactServicesDataService._stored_scope):
            self._fact_services: DataFrame = None
            self.scope = scope
        else:
            self.scope = FactServicesDataService._stored_scope
            self._fact_services = FactServicesDataService._stored_services


    def fact_services(self):
        if self._fact_services is None:
            self._fact_services = self.__get_fact_services()
            FactServicesDataService._stored_services = self._fact_services
            FactServicesDataService._stored_scope = self.scope
        return self._fact_services
    
    ## retrieves fact_services
    def __get_fact_services(self):
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
            fs.research_service_key,
            fs.{left1},
            fs.service_status,
            fs.service_id,
            fs.research_family_key,
            fs.served_children,
            fs.served_adults,
            fs.served_seniors,
            fs.served_total,
            fsm.research_member_key
        FROM 
            fact_services AS fs
            INNER JOIN dim_service_types ON fs.service_id = dim_service_types.id
            LEFT JOIN {table1} AS t1 ON fs.{left1} = t1.{right1}
            LEFT JOIN dim_service_statuses ON fs.service_status = dim_service_statuses.status 
            LEFT JOIN fact_service_members AS fsm ON fs.research_service_key = fsm.research_service_key
        WHERE
            fs.service_status = 17
            AND {control_query}
            AND t1.{scope_field} = {scope_value}
            AND fs.date >= {start_date} AND fs.date <= {end_date}
        """

        return pd.read_sql(query, conn)


    #calculations for data_def 1
    def get_services_total(self):
        services_total = self.fact_services()
        services_total = services_total.drop_duplicates(subset = 'research_service_key', inplace = False)
        return len(services_total)

    def get_undup_hh_total(self):
        hh_total = self.fact_services()
        hh_total = hh_total.drop_duplicates(subset = 'research_family_key', inplace = False)
        return len(hh_total)

    def get_undup_indv_total(self):
        undup_indv = self.fact_services()
        undup_indv = undup_indv.drop_duplicates(subset = 'research_member_key', inplace = False)
        return len(undup_indv)

    #data def 4
    def get_services_per_uhh_avg(self):
        """Calculate number of services per family DataDef 4

        Arguments:
        id - data definiton id
        params - a dictionary of values to scope the queries

        Modifies:
        Nothing

        Returns: num_services_avg
        num_services_avg - average number of services per family

        """
        services = self.__get_services_total()
        families = self.__get_undup_hh_total()
        return services/families

    #data def 5
    def get_wminor(self):
        services = self.fact_services().drop_duplicates(subset = 'research_service_key', inplace = False)
        w_minor =  services[services['served_children']>0] 
        return len(w_minor)


    ##  data Definition 6
    ####    Returns: len(services)
    ####        services - fact service data table, filtered on served_children == 0
    def get_wominor(self):
        services = self.fact_services().drop_duplicates(subset = 'research_service_key', inplace = False)
        wo_minor = services[services['served_children']==0]
        return len(wo_minor)

    #data definition 7 is a duplicate of data definition 1

    #Data Definitions 8
    ####    Returns: sen_hh_wminor
    ####        sen_hh_wminor - fact service data table, filtered on served_children > 0 and served_seniors > 0
    def get_indv_sen_hh_wminor(self):
        services = self.fact_services.drop_duplicates(subset = 'research_service_key', inplace = False)
        seniors = services[services['served_seniors']>0]
        senior_wminor = seniors[seniors['served_children']>0]
        return senior_wminor['served_seniors'].sum()

    ##Data Definition 9
    ####    Returns: sen_hh_wominor
    ####        sen_hh_wominor - fact service data table, filtered on served_children == 0 and served_seniors > 0
    def get_indv_sen_hh_wominor(self):
        services = self.fact_services.drop_duplicates(subset = 'research_service_key', inplace = False)
        seniors = services[services['served_seniors']>0]
        senior_wominor =  seniors[seniors['served_children']==0]
        return senior_wominor['served_seniors'].sum()

    ## DataFrame to fulfill Data Definitions 10, 20
    ####    Returns: sen_hh
    ####        sen_hh - fact service data table, filtered on served_seniors > 0
    def get_sen_total(self):
        services = self.fact_services().drop_duplicates(subset = 'research_service_key', inplace = False)
        sen_total = services[services['served_seniors']>0].sum()
        return sen_total

        ## DataFrame to fulfill Data Definition 11
    ####    Returns: adult_hh_wminor
    ####        adult_hh_wminor - fact service data table, filtered on served_children > 0 and served_adults > 0
    def get_adult_wminor(self):
        services = self.fact_services().drop_duplicates(subset = 'research_service_key', inplace = False)
        adults = services[services['served_adults']>0]
        adults_wminor = adults[adults['served_children']>0]
        return adults_wminor['served_adults'].sum()

        ## DataFrame to fulfill Data Definition 12
    ####    Returns: adult_hh_wominor
    ####        adult_hh_wominor - fact service data table, filtered on served_children == 0 and served_adults > 0
    def get_adult_wominor(self):
        services = self.fact_services().drop_duplicates(subset = 'research_service_key', inplace = False)
        adults = services[services['served_adults']>0]
        adults_wominor =  adults[adults['served_children']==0]
        return adults_wominor['served_adults'].sum()
    

        ## DataFrame to fulfill Data Definition 13
    ####    Returns: adult_hh
    ####        adult_hh - fact service data table, filtered on served_adults > 0
    
    def get_adult(self):
        services = self.fact_services().drop_duplicates(subset = 'research_service_key', inplace = False)
        adults =  services[services['served_adults']>0]
        return adults['served_adults'].sum()

        ## DataFrame to fulfill Data Definitions 14
    ####    Returns: services
    ####        services - fact service data table, filtered on served_children > 0
    def get_indv_child_hh_wminor(self):
        services = self.fact_services().drop_duplicates(subset = 'research_service_key', inplace = False)
        children = services[services['served_children']>0]
        children_served = children['served_children'].sum()
        return children_served

        ## DataFrame to fulfill Data Definition 15
    ####    Returns: empty
    ####        empty - empty data table (no such thing as children wo minors)
    def get_indv_child_hh_wominor(self):
        return 0

    #data definition 16
    def get_indv_child_total(self):
        return self.get_indv_child_hh_wminor()

    #data definition 17
    def get_indv_total_hh_wminor(self):
        services = self.fact_services().drop_duplicates(subset = 'research_service_key', inplace = False)
        w_child = services[services['served_children']>0]
        return w_child['served_total'].sum()

    #data definition 18
    def get_indv_total_hh_wominor(self):
        services = self.fact_services().drop_duplicates(subset = 'research_service_key', inplace = False)
        wo_child = services[services['served_children'] == 0]
        return wo_child['served_total'].sum()

    #data definition 19
    def get_indv_total(self):
        services = self.fact_services().drop_duplicates(subset = 'research_service_key', inplace = False)
        return services['served_total'].sum()

    #data definition 20
    def get_hh_wsenior(self):
        services = self.fact_services().drop_duplicates(subset = 'research_service_key', inplace = False)
        w_senior = services[services['served_seniors']>0]
        return len(w_senior)

    #data definition 21
    def get_hh_wosenior(self):
        services = self.fact_services().drop_duplicates(subset = 'research_service_key', inplace = False)
        wo_senior = services[services['served_seniors'] == 0]
        return len(wo_senior)

    #data definition 22
    def get_hh_grandparent(self):
        services = self.fact_services().drop_duplicates(subset = 'research_service_key', inplace = False)
        seniors =  services[services['served_seniors']>0]
        seniors_w_minor = seniors[seniors['served_children']>0]
        return len(seniors_w_minor)


    def get_data_for_definition(self, id):
        data_def_function_switcher = {
                1: self.get_services_total.__name__,
                2: self.get_undup_hh_total.__name__,
                3: self.get_undup_indv_total.__name__,
                4: self.get_services_per_uhh_avg.__name__,
                5: self.get_wminor.__name__,
                6: self.get_wominor.__name__,
                7: self.get_services_total.__name__,
                8: self.get_indv_sen_hh_wminor.__name__,
                9: self.get_indv_sen_hh_wominor.__name__,
                10: self.get_sen_total.__name__,
                11: self.get_adult_wminor.__name__,
                12: self.get_adult_wominor.__name__,
                13: self.get_adult.__name__,
                14: self.get_indv_child_hh_wminor.__name__,
                15: self.get_indv_child_hh_wominor.__name__,
                16: self.get_indv_child_total.__name__,
                17: self.get_indv_total_hh_wminor.__name__,
                18: self.get_indv_total_hh_wominor.__name__,
                19: self.get_indv_total.__name__,
                20: self.get_hh_wsenior.__name__,
                21: self.get_hh_wosenior.__name__,
                22: self.get_hh_grandparent.__name__
            }

 
        func = getattr(self, data_def_function_switcher[id],  lambda : None)
        return func()


#