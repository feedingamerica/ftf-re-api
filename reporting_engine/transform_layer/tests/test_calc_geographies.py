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
base_families = pyreadr.read_r(os.path.join(__location__, './test_data/test_calc_geographies/base_families.rds'))[None]
base_members = pyreadr.read_r(os.path.join(__location__, './test_data/test_calc_geographies/base_members.rds'))[None]
base_services = pyreadr.read_r(os.path.join(__location__, './test_data/test_calc_geographies/base_services.rds'))[None]

#substitue the call to TEST_DATA_SERVICE.get_data_for_definition with this
#its the data that david used in his calculations
BASE_DATA = [base_services, base_families, base_members]


class CalculationsTestCase(unittest.TestCase):

    #test data def 51
    def test_get_services_flow_event_fips(self):
        expected = pandas.read_csv(
            os.path.join(__location__, './expected_results/results_services_flow_event_fips.csv'),
            index_col = 'index'
        )
        data = BASE_DATA 
        func = calc.data_calc_function_switcher[51]
        result = func(data)
        resultFrame = pandas.read_json(result)
        assert_frame_equal(resultFrame, expected, check_like = True)

    #test data def 52
    def test_get_distance_traveled(self):
        expected = pandas.read_csv(
            os.path.join(__location__, './expected_results/results_distance_traveled.csv'),
            index_col = 'distance_roll'
        )
        data = BASE_DATA 
        func = calc.data_calc_function_switcher[52]
        result = func(data)
        resultFrame = pandas.read_json(result)
        assert_frame_equal(resultFrame, expected, check_like = True)

    #test data def 53
    def test_direction_traveled(self):
        expected = {
        'NE': {
            'services':4434,
            'mean_distance':6.011814,
            'median_distance':2.676118,
            'min_distance':0.265377,
            'max_distance':95.08928
        },
        'N': {
            'services':3159,
            'mean_distance':11.899266,
            'median_distance':6.077369,
            'min_distance':0.345854,
            'max_distance':102.40609
        },
        'SE': {
            'services':28775,
            'mean_distance':7.657749,
            'median_distance':4.906900,
            'min_distance':0.345854,
            'max_distance':125.65186
        },
        'E': {
            'services':24284,
            'mean_distance':5.852088,
            'median_distance':5.316541,
            'min_distance':0.435930,
            'max_distance':118.44905
        },
        'W': {
            'services':2242,
            'mean_distance':11.870164,
            'median_distance':7.312024,
            'min_distance':0.435941,
            'max_distance':94.26391
        },
        'SW': {
            'services':19922,
            'mean_distance':9.566677,
            'median_distance':9.596235,
            'min_distance':0.530754,
            'max_distance':135.71163
        },
        'NW': {
            'services':1650,
            'mean_distance': 20.327712,
            'median_distance':20.232065,
            'min_distance':0.740874,
            'max_distance':105.66228
        },
        'S': {
            'services':30089,
            'mean_distance':9.155085,
            'median_distance':9.139874,
            'min_distance':0.871847,
            'max_distance':180.99612
        },
        }
        expected = pandas.DataFrame.from_dict(expected)
        data = BASE_DATA 
        func = calc.data_calc_function_switcher[55]
        result = func(data)
        resultFrame = pandas.read_json(result)
        assert_frame_equal(resultFrame, expected, check_like = True)

    #test data def 55
    def test_sites_visited_distribution(self):
        expected = {
            "num_families": {
                1 : 26133
            }
        }
        expected = pandas.DataFrame.from_dict(expected)
        data = BASE_DATA 
        func = calc.data_calc_function_switcher[55]
        result = func(data)
        resultFrame = pandas.read_json(result)
        assert_frame_equal(resultFrame, expected, check_like = True)

    #test data def 56
    def test_dummy_trip_coverage(self):
        expected = .9913
        data = BASE_DATA
        func = calc.data_calc_function_switcher[56]
        result = func(data)
        self.assertTrue(math.isclose(result, expected, rel_tol = 1e-04))