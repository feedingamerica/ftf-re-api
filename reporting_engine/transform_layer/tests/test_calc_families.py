from django.test import TestCase
from transform_layer.services.data_service import DataService
from django.db import connections
import pandas
from pandas.testing import assert_frame_equal, assert_series_equal
import transform_layer.calculations as calc

import unittest
import csv
import os 
import sys
import json
import math

#How 'off' the value returned by a data def can be before it is considered wrong
#.005 = .5% of expected
REL_TOL = .01

base_services_scope = {
    "startDate":"01/01/2020",
    "endDate":"03/31/2021",
    "scope_type": "hierarchy",
    "scope_field":"loc_id",
    "scope_field_value":6,
    "control_type_name":"Is Grocery Service"
}


#shared test data service so you don't have to make a db call for every test
#not gonna work with multithreaded tests
TEST_DATA_SERVICE = DataService(base_services_scope)
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

class CalculationsTestCase(unittest.TestCase):    
    def test_get_frequency_visits(self):
        expected = pandas.read_csv(
            os.path.join(__location__, './expected_results/test_calc_families/frequency_visits.csv'),
            skipinitialspace= True,
            index_col = 0
        )
    
        data = TEST_DATA_SERVICE.get_data_for_definition(26)
        func = calc.data_calc_function_switcher[26]
        result = func(data)
        resultFrame = pandas.read_json(result)
        assert_frame_equal(resultFrame, expected, rtol= REL_TOL)

        
    def test_get_household_composition(self):
        expected = pandas.read_csv(
            os.path.join(__location__, './expected_results/test_calc_families/household_composition.csv'),
            skipinitialspace= True
        )
        data = TEST_DATA_SERVICE.get_data_for_definition(28)
        func = calc.data_calc_function_switcher[28]
        result = func(data)
        resultFrame = pandas.read_json(result)
        assert_frame_equal(resultFrame, expected, rtol= REL_TOL)

    def test_get_family_comp_key_insight(self):
        expected = pandas.read_csv(
            os.path.join(__location__, './expected_results/test_calc_families/family_comp_key_insight.csv'),
            skipinitialspace= True
        )
        data = TEST_DATA_SERVICE.get_data_for_definition(29)
        func = calc.data_calc_function_switcher[29]
        result = func(data)
        resultFrame = pandas.read_json(result)
        assert_frame_equal(resultFrame, expected, rtol= REL_TOL)

    def test_get_household_size_distribution_1_to_10(self):
        expected = pandas.read_csv(
            os.path.join(__location__, './expected_results/test_calc_families/household_size_distribution_1_to_10.csv'),
            skipinitialspace= True
        )
        data = TEST_DATA_SERVICE.get_data_for_definition(30)
        func = calc.data_calc_function_switcher[30]
        result = func(data)
        resultFrame = pandas.read_json(result)
        assert_frame_equal(resultFrame, expected, rtol= REL_TOL)

    def test_get_household_size_distribution_classic(self):
        expected = pandas.read_csv(
            os.path.join(__location__, './expected_results/test_calc_families/household_size_distribution_classic.csv'),
            skipinitialspace= True
        )
        data = TEST_DATA_SERVICE.get_data_for_definition(31)
        func = calc.data_calc_function_switcher[31]
        result = func(data)
        resultFrame = pandas.read_json(result)
        assert_frame_equal(resultFrame, expected, rtol= REL_TOL)


if __name__ == '__main__':
    unittest.main()