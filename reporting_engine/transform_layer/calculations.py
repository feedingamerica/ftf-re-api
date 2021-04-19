from .services.data_service import DataService
import transform_layer.calc_service_types as calc_service_types
import transform_layer.calc_families as calc_families
import transform_layer.calc_fact_services as calc_fact_services
import transform_layer.calc_new_families as calc_new_families
import transform_layer.calc_geographies as calc_geographies
import transform_layer.calc_service_trends as calc_service_trends
import transform_layer.calc_family_members as calc_family_members

import pandas as pd

BIG_NUM_NAMES = ["services_total", "undup_hh_total", "undup_indv_total", "services_per_uhh_avg"]
DEFAULT_CTRL = "Is Grocery Service"
DEFAULT_AGE_GROUP_ID = 8

class CalculationDispatcher:
    def __init__(self, request):

        # now on construction, it will automatically run parse request on the input request, so theres no extra in between step
        self.request = self.parse_request(request)
        data_list = request["ReportInfo"]
        self.params = request["Meta"]
        self.data_dict = CalculationDispatcher.__group_by_data_def(data_list)
        self.data_service = DataService(request["Meta"])
        
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
                data = self.data_service.get_data_for_definition(data_def["dataDefId"])
                if self.has_data(data):
                    self.params["no_data"] = False
                    func = data_calc_function_switcher[data_def["dataDefId"]]
                    data_def["value"] = func(data)
                else:
                    self.params["no_data"] = True

        return self.request["ReportInfo"]

    # static callable parse request
    @staticmethod
    def parse_request(input_dict):
        # Setting the scope type
        scope_field = input_dict["Meta"]["scope_field"]
        if scope_field.startswith("fip"):
            input_dict["Meta"]["scope_type"] = "geography"
        else:
            input_dict["Meta"]["scope_type"] = "hierarchy"
        
        # Setting the control type
        if "control_type_name" not in input_dict["Meta"]:
            input_dict["Meta"]["control_type_name"] = DEFAULT_CTRL

        if "control_age_group_id" not in input_dict["Meta"]:
            input_dict["Meta"]["control_age_group_id"] = DEFAULT_AGE_GROUP_ID

        return input_dict

    @staticmethod
    def has_data(data):
        if type(data) is list:
            # Check if services dataframe is empty
            if data[0].empty:
                return False
        elif isinstance(data, pd.DataFrame):
            if data.empty:
                return False

        return True

data_calc_function_switcher = {
        1: calc_fact_services.get_services_total,
        2: calc_fact_services.get_undup_hh_total,
        3: calc_fact_services.get_undup_indv_total,
        4: calc_fact_services.get_services_per_uhh_avg,
        5: calc_fact_services.get_wminor,
        6: calc_fact_services.get_wominor,
        7: calc_fact_services.get_services_total,
        8: calc_fact_services.get_indv_sen_hh_wminor,
        9: calc_fact_services.get_indv_sen_hh_wominor,
        10: calc_fact_services.get_sen_total,
        11: calc_fact_services.get_adult_wminor,
        12: calc_fact_services.get_adult_wominor,
        13: calc_fact_services.get_adult,
        14: calc_fact_services.get_indv_child_hh_wminor,
        15: calc_fact_services.get_indv_child_hh_wominor,
        16: calc_fact_services.get_indv_child_total,
        17: calc_fact_services.get_indv_total_hh_wminor,
        18: calc_fact_services.get_indv_total_hh_wominor,
        19: calc_fact_services.get_indv_total,
        20: calc_fact_services.get_hh_wsenior,
        21: calc_fact_services.get_hh_wosenior,
        22: calc_fact_services.get_hh_grandparent,
        23: calc_service_types.get_services_summary,
        24: calc_service_types.get_services_category,
        25: calc_service_types.get_distribution_outlets,
        26: calc_families.get_frequency_visits,
        27: calc_families.get_frequency_visits,
        28: calc_families.get_household_composition,
        29: calc_families.get_family_comp_key_insight,
        30: calc_families.get_household_size_distribution_1_to_10,
        31: calc_families.get_household_size_distribution_classic,
        32: calc_new_families.get_new_families,
        33: calc_new_families.get_new_members,
        34: calc_new_families.get_new_members_to_old_families,
        35: calc_new_families.get_services_to_new_families,
        36: calc_new_families.get_families_first_service,
        37: calc_new_families.get_new_families_freq_visits,
        38: calc_new_families.get_new_families_freq_visits,
        39: calc_new_families.get_new_fam_household_composition,
        40: calc_new_families.get_new_fam_composition_key_insight,
        41: calc_new_families.get_new_fam_hh_size_dist_1_to_10,
        42: calc_new_families.get_new_fam_hh_size_dist_classic,
        43: calc_new_families.get_relationship_length_fam_mean,
        44: calc_new_families.get_new_fam_dist_of_length_of_relationship,
        45: calc_new_families.get_relationship_length_indv_mean,
        46: calc_new_families.get_new_fam_dist_of_length_of_relationships_for_individuals,
        47: calc_geographies.get_geo_coverage,
        48: calc_geographies.get_geo_breakdown_fam_state,
        49: calc_geographies.get_geographic_breakdown_fam_county,
        50: calc_geographies.get_geographic_breakdown_fam_zcta,
        51: calc_geographies.get_services_flow_event_fips,
        52: calc_geographies.get_distance_traveled,
        53: calc_geographies.get_direction_traveled,
        54: calc_geographies.get_windrose,
        55: calc_geographies.get_sites_visited_distribution,
        56: calc_geographies.get_dummy_trip_coverage,
        57: calc_service_trends.get_service_trend_time_month,
        58: calc_service_trends.get_service_trend_time_week,
        59: calc_service_trends.get_service_trend_time_day,
        60: calc_service_trends.get_service_trend_monthy_visits_avg,
        61: calc_service_trends.get_service_trend_monthly_people_dup,
        62: calc_service_trends.get_service_trend_monthly_group_dup,
        63: calc_service_trends.get_service_trend_service_category,
        64: calc_service_trends.get_service_trend_comparison,
        65: calc_service_trends.get_service_summary_dow,
        66: calc_service_trends.get_service_summary_hod,
        67: calc_service_trends.get_service_summary_dowhod,
        68: calc_service_trends.get_service_trend_event,
        69: calc_family_members.get_gender_summary,
        71: calc_family_members.get_skipped_generation,
        72: calc_family_members.get_demo_indv_gender,
        73: calc_family_members.get_demo_indv_age_groups,
        74: calc_family_members.get_hh_has_age_groups,
        75: calc_family_members.get_population_pyramid,
        76: calc_family_members.get_demo_indv_race,
        77: calc_family_members.get_demo_indv_ethnic,
        79: calc_family_members.get_demo_indv_education,
        80: calc_family_members.get_demo_indv_employment,
        81: calc_family_members.get_demo_indv_health_insurnace
    }

