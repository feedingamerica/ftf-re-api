from time import daylight
from django.test import TestCase
from django.db import connections
import pandas
import numpy
from pandas.testing import assert_frame_equal, assert_series_equal
from transform_layer.services.data_service import DataService, KEY_FAMILY, KEY_MEMBER, KEY_SERVICE
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
BASE_DATA = {
    KEY_SERVICE: base_services,
    KEY_FAMILY: base_families,
    KEY_MEMBER : base_members
}


class CalculationsTestCase(unittest.TestCase):
    #test data def 47
    def test_get_geo_coverage(self):
        expected = 0.988
        data = BASE_DATA 
        func = calc.data_calc_function_switcher[47]
        result = func(data)
        self.assertTrue(math.isclose(result, expected, rel_tol = REL_TOL))

    #test data def 48
    def test_get_geo_breakdown_fam_state(self):
        expected = pandas.read_csv(
            os.path.join(__location__, './expected_results/results_geographic_breakdown_fam_state.csv'),
            dtype={'fips_state':str}
        ).fillna('<NA>')
        data = BASE_DATA
        func = calc.data_calc_function_switcher[48]
        result = func(data)
        resultFrame = pandas.read_json(result).reset_index().rename(columns={"index": "fips_state"})
        assert_frame_equal(resultFrame, expected, check_like = True)
    
    #test data def 49
    def test_get_geo_breakdown_fam_cnty(self):
        expected = pandas.read_csv(
            os.path.join(__location__, './expected_results/results_geographic_breakdown_fam_county.csv'),
            dtype={'fips_cnty':str}
        ).fillna('<NA>')
        data = BASE_DATA
        func = calc.data_calc_function_switcher[49]
        result = func(data)
        resultFrame = pandas.read_json(result).reset_index().rename(columns={"index": "fips_cnty"})
        assert_frame_equal(resultFrame, expected, check_like = True)
    
     #test data def 50
    def test_get_geo_breakdown_fam_zcta(self):
        expected = pandas.read_csv(
            os.path.join(__location__, './expected_results/results_geographic_breakdown_fam_zcta.csv'),
            dtype={'fips_zcta':str}
        ).fillna('<NA>')
        data = BASE_DATA
        func = calc.data_calc_function_switcher[50]
        result = func(data)
        resultFrame = pandas.read_json(result).reset_index().rename(columns={"index": "fips_zcta"})
        assert_frame_equal(resultFrame, expected, check_like = True)


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
        expected = pandas.read_csv(
            os.path.join(__location__, './expected_results/results_direction_traveled.csv'),
            index_col = 'direction'
        )
        data = BASE_DATA
        func = calc.data_calc_function_switcher[53]
        result = func(data)
        resultFrame = pandas.read_json(result)
        assert_frame_equal(resultFrame, expected, check_like = True)

    #test data def 54
    def test_get_windrose(self):
        expected = pandas.read_csv(
            os.path.join(__location__, './expected_results/results_data_def_54.csv'),
            index_col = 'distance_roll'
        )
        expected = expected.reset_index()
        data = BASE_DATA 
        func = calc.data_calc_function_switcher[54]
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