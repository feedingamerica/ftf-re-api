from django.test import TestCase
from django.db import connections
import pandas
from pandas.testing import assert_frame_equal, assert_series_equal
from transform_layer.services.data_service import DataService, KEY_FAMILY, KEY_MEMBER, KEY_SERVICE
import transform_layer.services.data_service as data_service
import transform_layer.calculations as calc

import json
import math
import unittest
import os
import pyreadr

#How 'off' the value returned by a data def can be before it is considered wrong
#.005 = .5% of expected
REL_TOL = .01

base_scope = {
    "startDate":"01/01/2020",
    "endDate":"12/31/2020",
    "scope_type": "hierarchy",
    "scope_field":"loc_id",
    "scope_field_value":6,
    "control_type_name":"Is Grocery Service"
}

TEST_DATA_SERVICE = DataService(base_scope)

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
base_families = pyreadr.read_r(os.path.join(__location__, './test_data/test_calc_new_families/base_families.rds'))[None]
base_members = pyreadr.read_r(os.path.join(__location__, './test_data/test_calc_new_families/base_members.rds'))[None]
base_services = pyreadr.read_r(os.path.join(__location__, './test_data/test_calc_new_families/base_services.rds'))[None]

#substitue the call to TEST_DATA_SERVICE.get_data_for_definition with this
#its the data that david used in his calculations
BASE_DATA = {
    KEY_SERVICE: base_services,
    KEY_FAMILY: base_families,
    KEY_MEMBER : base_members
}
    

class CalculationsTestCase(unittest.TestCase):
    #test for data def 32
    def test_get_new_families(self):
        expected = 6307
        data = BASE_DATA
        func = calc.data_calc_function_switcher[32]
        result = func(data)
        self.assertTrue(math.isclose(result, expected))

    #test for data def 33
    def test_get_new_members(self):
        expected = 20779
        data = BASE_DATA
        func = calc.data_calc_function_switcher[33]
        result = func(data)
        self.assertTrue(math.isclose(result, expected))

    #test for data def 34
    def test_get_new_members_to_old_families(self):
        expected = 19160
        data = BASE_DATA
        func = calc.data_calc_function_switcher[34]
        result = func(data)
        self.assertTrue(math.isclose(result, expected))

    #test for data def 35
    def test_get_services_to_new_families(self):
        expected = 22790
        data = BASE_DATA
        func = calc.data_calc_function_switcher[35]
        result = func(data)
        self.assertTrue(math.isclose(result, expected))

    #test for data def 36
    def test_get_families_first_service(self):
        expected = 6352
        data = BASE_DATA
        func = calc.data_calc_function_switcher[36]
        result = func(data)
        self.assertTrue(math.isclose(result, expected))

    #test for data def 37/38
    def test_get_new_families_freq_visits(self):
        expected = pandas.read_csv(
            os.path.join(__location__, './expected_results/results_new_fam_service_distribution.csv'),
            index_col = 'num_services'
        )
        #data = TEST_DATA_SERVICE.get_data_for_definition(38)
        data = BASE_DATA 
        func = calc.data_calc_function_switcher[37]
        result = func(data)
        resultFrame = pandas.read_json(result)
        assert_frame_equal(resultFrame, expected, check_like = True)
    
    #test for data def 39
    def test_get_new_fam_household_composition(self):
        expected = {
            "family_composition_type": {
               "0":"adults_and_children",
               "1": "adults_and_seniors",
               "2": "adults_only",
               "3": "adults_seniors_and_children",
               "4": "children_and_seniors",
               "5": "children_only",
               "6": "seniors_only"
            },
            "num_families": {
                "0":2622,
               "1": 447,
               "2": 2467,
               "3": 297,
               "4": 36,
               "5": 16,
               "6": 422
            }
        }
        #data = TEST_DATA_SERVICE.get_data_for_definition(38)
        data = BASE_DATA 
        func = calc.data_calc_function_switcher[39]
        result = func(data)
        resultDict = json.loads(result)
        self.maxDiff = None
        self.assertDictEqual(resultDict, expected)

    #test for data def 40
    def test_get_new_fam_composition_key_insight(self):
        expected = {
            "has_child_senior":3840,
            "no_child_senior":2467
        }
        #data = TEST_DATA_SERVICE.get_data_for_definition(38)
        data = BASE_DATA 
        func = calc.data_calc_function_switcher[40]
        result = func(data)
        result = json.loads(result)
        self.maxDiff = None
        self.assertDictEqual(result, expected)

    #test for data def 41
    def test_get_new_fam_hh_size_dist_1_to_10(self):
        expected = pandas.read_csv(
            os.path.join(__location__, './expected_results/results_new_fam_hh_size_dist_1_to_10.csv'),
            index_col = 'index'
        )
        data = BASE_DATA 
        func = calc.data_calc_function_switcher[41]
        result = func(data)
        resultFrame = pandas.read_json(result)
        assert_frame_equal(resultFrame, expected, check_like = True)

    #test for data def 42
    def test_get_new_fam_hh_size_dist_classic(self):
        expected = pandas.DataFrame(data = {"classic_roll": ['1 - 3', '4 - 6', '7+'], "num_families": [3965,2040,302]})

        #data = TEST_DATA_SERVICE.get_data_for_definition(42)
        data = BASE_DATA

        func = calc.data_calc_function_switcher[42]
        result = func(data)
        resultFrame = pandas.read_json(result)
        assert_frame_equal(resultFrame, expected)

    #test for data def 43
    def test_get_relationship_length_indv_mean(self):
        expected = 809.5147
        data = BASE_DATA

        func = calc.data_calc_function_switcher[43]
        result = func(data)
        self.assertTrue(math.isclose(round(result,4), expected))

    #test for data def 44
    def test_get_new_fam_dist_of_length_of_relationship(self):
        data = BASE_DATA
        func = calc.data_calc_function_switcher[44]
        result = func(data)
        resultFrame = pandas.read_json(result)
        #should be ten bins
        self.assertTrue(len(resultFrame) == 10)
        #min should be zero
        self.assertTrue(resultFrame.iloc[0]['min'] == 0)

    #test for data def 44 with null_days_since_first_service
    def test_get_new_fam_dist_of_length_of_relationship_wnulls(self):
        path = os.path.join(__location__, 'test_data', 'test_calc_new_families', 'edge_cases', 'null_days_since_first_service', 'base_families.parquet')
        families = pandas.read_parquet(path = path, engine = 'pyarrow')
        data = {
            KEY_FAMILY : families
        }
        func = calc.data_calc_function_switcher[44]
        result = func(data)
        resultFrame = pandas.read_json(result)
        #should be ten bins
        self.assertTrue(len(resultFrame) == 10)
        #min should be zero
        self.assertTrue(resultFrame.iloc[0]['min'] == 0)

    #test for data def 45
    def test_get_relationship_length_indv_mean(self):
        expected = 792.9765
        #data = TEST_DATA_SERVICE.get_data_for_definition(45)
        data = BASE_DATA

        func = calc.data_calc_function_switcher[45]
        result = func(data)
        self.assertTrue(math.isclose(round(result,4), expected))

if __name__ == '__main__':
    unittest.main()