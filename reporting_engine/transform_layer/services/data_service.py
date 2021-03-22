from pandas.core.frame import DataFrame
import dateutil.parser as parser
import pandas as pd
from django.db import connections
from transform_layer.services.ds_fact_services import FactServicesDataService
from transform_layer.services.ds_families import FamiliesDataService
from transform_layer.services.ds_services_types import ServiceTypesDataService

import copy

SCOPE_HIERARCHY = "hierarchy"
SCOPE_GEOGRAPHY = "geography"

class DataService:
    __scope:str = None

    def __init__(self, scope):
        self.scope = scope
        self.fact_services_service = FactServicesDataService(self.scope)
        self.families_service = FamiliesDataService(self.scope)
        self.service_types_service = ServiceTypesDataService(self.scope)


    # ## returns DataFrame for a specific data definition
    # @classmethod
    # def get_data_for_definition(cls, id, params):
    #     if( params != cls.__scope):
    #         cls.__fact_services = None
    #         cls.__base_services = None
    #         cls.__family_services = None
    #         cls.__scope = copy.deepcopy(params)
    #     func = cls.data_def_function_switcher.get(id, cls.get_data_def_error)
    #     return func(params)


    
    ## returns DataFrame for a specific data definition
    def get_data_for_definition(self, id):
        if id>=1 and id <= 22:
            return self.fact_services_service.get_data_for_definition(id)
        elif id <= 25:
            return self.families_service.get_data_for_definition(id)
        elif id <= 31:
            return self.service_types_service.get_data_for_definition(id)






    ## DataFrame to fulfill Data Definition 1
    ####    Returns: services
    ####        families - unduplicated families data table
    @staticmethod
    def __get_num_services(params):
        services = Data_Service.fact_services(params)
        return services.drop_duplicates(subset = 'research_service_key', inplace = False)
    
    ## DataFrame to fulfill Data Definition 2
    ####    Returns: services
    ####        families - unduplicated families data table
    @staticmethod
    def __get_undup_hh(params):
        services = Data_Service.fact_services(params)
        return services.drop_duplicates(subset = 'research_family_key', inplace = False)
    
    ## DataFrame to fulfill Data Definiton 3
    ####    Returns: services
    ####        inidividuals - unduplicated individuals data table
    @staticmethod
    def __get_undup_indv(params):
        services = Data_Service.fact_services(params)
        return services.drop_duplicates(subset = 'research_member_key', inplace = False)
    
    ## DataFrames to fulfill Data Definiton 4
    ####    Returns: (services, families)
    ####        services - fact service data table
    ####        families - unduplicated families data table
    @staticmethod
    def __fact_services_and_uhh(params):
        return Data_Service.__get_num_services(params), Data_Service.__get_undup_hh(params)
    
    ## DataFrame to fulfill Data Definitions 5, 14, 16, 17
    ####    Returns: services
    ####        services - fact service data table, filtered on served_children > 0
    @staticmethod
    def __get_wminor(params):
        services = Data_Service.fact_services(params).drop_duplicates(subset = 'research_service_key', inplace = False)
        return services[services['served_children']>0]
    
    ## DataFrame to fulfill Data Definition 6
    ####    Returns: services
    ####        services - fact service data table, filtered on served_children == 0
    @staticmethod
    def __get_wominor(params):
        services = Data_Service.fact_services(params).drop_duplicates(subset = 'research_service_key', inplace = False)
        return services[services['served_children']==0]
    
    ## DataFrame to fulfill Data Definitions 8, 18, 22
    ####    Returns: sen_hh_wminor
    ####        sen_hh_wminor - fact service data table, filtered on served_children > 0 and served_seniors > 0
    @staticmethod
    def __get_sen_wminor(params):
        seniors = Data_Service.__get_sen(params).drop_duplicates(subset = 'research_service_key', inplace = False)
        return seniors[seniors['served_children']>0]
    
    ## DataFrame to fulfill Data Definition 9
    ####    Returns: sen_hh_wominor
    ####        sen_hh_wominor - fact service data table, filtered on served_children == 0 and served_seniors > 0
    @staticmethod
    def __get_sen_wominor(params):
        seniors = Data_Service.__get_sen(params).drop_duplicates(subset = 'research_service_key', inplace = False)
        return seniors[seniors['served_children']==0]
    
    ## DataFrame to fulfill Data Definitions 10, 20
    ####    Returns: sen_hh
    ####        sen_hh - fact service data table, filtered on served_seniors > 0
    @staticmethod
    def __get_sen(params):
        services = Data_Service.fact_services(params).drop_duplicates(subset = 'research_service_key', inplace = False)
        return services[services['served_seniors']>0]
    
    ## DataFrame to fulfill Data Definition 11
    ####    Returns: adult_hh_wminor
    ####        adult_hh_wminor - fact service data table, filtered on served_children > 0 and served_adults > 0
    @staticmethod
    def __get_adult_wminor(params):
        adults = Data_Service.__get_adult(params).drop_duplicates(subset = 'research_service_key', inplace = False)
        return adults[adults['served_children']>0]
    
    ## DataFrame to fulfill Data Definition 12
    ####    Returns: adult_hh_wominor
    ####        adult_hh_wominor - fact service data table, filtered on served_children == 0 and served_adults > 0
    @staticmethod
    def __get_adult_wominor(params):
        adults = Data_Service.__get_adult(params).drop_duplicates(subset = 'research_service_key', inplace = False)
        return adults[adults['served_children']==0]
    
    ## DataFrame to fulfill Data Definition 13
    ####    Returns: adult_hh
    ####        adult_hh - fact service data table, filtered on served_adults > 0
    @staticmethod
    def __get_adult(params):
        services = Data_Service.fact_services(params).drop_duplicates(subset = 'research_service_key', inplace = False)
        return services[services['served_adults']>0]
    

    
    ## DataFrame to fulfill Data Definition 21
    ####    Returns services_wosenior
    ####        services_wosenior - fact service data table, filtered on served_serniors == 0
    @staticmethod
    def __get_wosenior(params):
        services = Data_Service.fact_services(params).drop_duplicates(subset = 'research_service_key', inplace = False)
        return services[services['served_seniors']==0]




    ## Data Defintion Switcher
    # usage:
    #   func = data_def_function_switcher.get(id)
    #   func()
    data_def_function_switcher = {
            1: __get_num_services.__func__,
            2: __get_undup_hh.__func__,
            3: __get_undup_indv.__func__,
            4: __fact_services_and_uhh.__func__,
            5: __get_wminor.__func__,
            6: __get_wominor.__func__,
            7: __get_num_services.__func__,
            8: __get_sen_wminor.__func__,
            9: __get_sen_wominor.__func__,
            10: __get_sen.__func__,
            11: __get_adult_wminor.__func__,
            12: __get_adult_wominor.__func__,
            13: __get_adult.__func__,
            14: __get_wminor.__func__,
            15: __get_child_wominor.__func__,
            16: __get_wminor.__func__,
            17: __get_wminor.__func__,
            18: __get_wominor.__func__,
            19: __get_num_services.__func__,
            20: __get_sen.__func__,
            21: __get_wosenior.__func__,
            22: __get_sen_wminor.__func__,
        }
