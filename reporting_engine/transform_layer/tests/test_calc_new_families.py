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


    #test for data def 38
    def test_get_new_fam_service_distribution(self):
        expected = pandas.read_csv(
            os.path.join(__location__, './expected_results/results_new_fam_service_distribution.csv'),
            index_col = 'num_services'
        )
        expected = expected.drop(columns='n_families')
        #data = TEST_DATA_SERVICE.get_data_for_definition(38)
        data = BASE_DATA 
        func = calc.data_calc_function_switcher[38]
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


if __name__ == '__main__':
    unittest.main()

    #test for data def 45