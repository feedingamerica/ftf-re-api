import numpy as np
from .services.data_service import DataService
import json

import numpy


BIG_NUM_NAMES = ["services_total", "undup_hh_total", "undup_indv_total", "services_per_uhh_avg"]
DEFAULT_CTRL = "Is Grocery Service"

class CalculationDispatcher:
    def __init__(self, request):

        # now on construction, it will automatically run parse request on the input request, so theres no extra in between step
        self.request = self.parse_request(request)
        data_list = request["ReportInfo"]
        self.params = request["Scope"]
        self.data_dict = CalculationDispatcher.__group_by_data_def(data_list)
        self.data_service = DataService(request["Scope"])
        
    @staticmethod
    def __group_by_data_def(data_list):
        """Returns dict of data defs grouped by reportDictid and sorted by dataDefid
        
        data_dict is a dictionary that groups the data definitions in data_list by reportDictId
        and sorts the data definitions in each group by their dataDefId, highest to smallest.
        Does not modify data_list.
        data_dict = { 
            1: [{"reportDictId": 1, "dataDefId": 1 },   {"reportDictId": 1, "dataDefId": 2 }, ... ],
            2:  [{"reportDictId": 2, "dataDefId": 5 },   {"reportDictId": 2, "dataDefId": 6 }, ... ],
            3:  [{"reportDictId": 3, "dataDefId": 19 },   {"reportDictId": 3, "dataDefId": 20 }, ... ],
        }
        
        """

        data_dict = {}
        for item in data_list:
            entry_list = data_dict.get(item["reportDictId"])
            if entry_list is None:
                pos = item["reportDictId"]
                data_dict[pos] = [item]
            else:
                entry_list.append(item)

        for entry_list in data_dict.values():
            entry_list.sort(key = lambda e: e["dataDefId"])
        return data_dict
        
    
    #runs calculation on each data_def in data_dict
    #and appends the result of the calculation to the data_def
    #modifies: self.request
    #returns the modified data_defs as a list
    def run_calculations(self):
        for group in self.data_dict.values():
            for data_def in group:
                result = self.data_service.get_data_for_definition(data_def["dataDefId"])
                data_def["value"] = result

        return self.request["ReportInfo"]

    # static callable parse request
    @staticmethod
    def parse_request(input_dict):
        # Setting the scope type
        scope_field = input_dict["Scope"]["scope_field"]
        if scope_field.startswith("fip"):
            input_dict["Scope"]["scope_type"] = "geography"
        else:
            input_dict["Scope"]["scope_type"] = "hierarchy"
        
        # Setting the control type
        if "control_type_name" not in input_dict["Scope"]:
            input_dict["Scope"]["control_type_name"] = DEFAULT_CTRL

        return input_dict


