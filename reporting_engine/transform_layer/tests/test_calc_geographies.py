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