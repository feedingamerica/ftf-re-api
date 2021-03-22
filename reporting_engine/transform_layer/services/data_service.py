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
            return self.service_types_service.get_data_for_definition(id)
        elif id <= 31:
            return self.families_service.get_data_for_definition(id)

