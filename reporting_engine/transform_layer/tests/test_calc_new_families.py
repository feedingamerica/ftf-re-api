from django.test import TestCase
from django.db import connections
import pandas
from pandas.testing import assert_frame_equal, assert_series_equal
from transform_layer.services.data_service import DataService
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
base_families = pyreadr.read_r(os.path.join(__location__, './test_data/base_families.rds'))[None]
base_members = pyreadr.read_r(os.path.join(__location__, './test_data/base_members.rds'))[None]
base_services = pyreadr.read_r(os.path.join(__location__, './test_data/base_services.rds'))[None]

#substitue the call to TEST_DATA_SERVICE.get_data_for_definition with this
#its the data that david used in his calculations
BASE_DATA = [base_services, base_families, base_members]

class CalculationsTestCase(unittest.TestCase):
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
            "adults_and_children":2622,
            "adults_and_seniors":447,
            "adults_only":2467,
            "adults_seniors_and_children":297,
            "children_and_seniors":36,
            "children_only":16,
            "seniors_only":422
        }
        #data = TEST_DATA_SERVICE.get_data_for_definition(38)
        data = BASE_DATA 
        func = calc.data_calc_function_switcher[39]
        result = func(data)
        resultFrame = pandas.read_json(result)
        assert_frame_equal(resultFrame, expected, check_like = True)

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
        resultFrame = pandas.read_json(result)
        assert_frame_equal(resultFrame, expected, check_like = True)

    #test for data def 42
    def test_get_new_fam_hh_size_dist_classic(self):
        expected = {
            '1 - 3':3965,
            '4 - 6':2040,
            '7+':302
        }
        expected = pandas.Series(data = expected)

        #data = TEST_DATA_SERVICE.get_data_for_definition(42)
        data = BASE_DATA

        func = calc.data_calc_function_switcher[42]
        result = func(data)
        resultDict = json.loads(result)
        resultFrame = pandas.Series(data = resultDict)
        assert_series_equal(resultFrame, expected)

    #test for data def 45
    def test_get_relationship_length_indv_mean(self):
        expected = 792.9765
        #data = TEST_DATA_SERVICE.get_data_for_definition(45)
        data = BASE_DATA

        func = calc.data_calc_function_switcher[45]
        result = func(data)
        self.assertTrue(math.isclose(round(result,4), expected))

    #test for data def 46
    def test_get_new_fam_dist_of_length_of_relationships_for_individuals(self):
        # NOTE 
        # Everything here is 0 because the exact numbers are not given yet 
        expected = {
            '0 - 200':0,
            '200 - 400':0,
            '400 - 600':0,
            '600 - 800':0,
            '800 - 1000':0,
            '1000 - 1200':0,
            '1200 - 1400':0,
            '1400 - 1600':0,
            '1600 - 1800':0,
            '1800 - 2000':0,
        }
        #data = TEST_DATA_SERVICE.get_data_for_definition(38)
        data = BASE_DATA 
        func = calc.data_calc_function_switcher[46]
        result = func(data)
        resultFrame = pandas.read_json(result)
        assert_frame_equal(resultFrame, expected, check_like = True)

if __name__ == '__main__':
    unittest.main()