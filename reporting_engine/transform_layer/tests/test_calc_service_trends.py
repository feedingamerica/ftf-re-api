from unittest.case import expectedFailure
from django.test import TestCase
from django.db import connections
from numpy import int64
import pandas
from pandas.testing import assert_frame_equal, assert_series_equal
from transform_layer.services.data_service import DataService
import transform_layer.calculations as calc

import json
import math
import unittest
import os
import pyreadr

REL_TOL = .01

base_scope = {
    "startDate":"01/01/2020",
    "endDate":"12/31/2020",
    "scope_type": "hierarchy",
    "scope_field":"loc_id",
    "scope_field_value":6,
    "control_type_name":"Is Grocery Service"
}
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

TEST_DATA_SERVICE = DataService(base_scope)
class CalculationsTestCase(unittest.TestCase):
    
    #test data def 57
    def test_get_service_trend_time_month(self):
        expected = pandas.read_csv(
            os.path.join(__location__, './expected_results/test_calc_service_trends/service_trend_time_month.csv'),
            skipinitialspace= True
        ).fillna('0')
        expected['n'] = expected['n'].astype(int64)

        data = TEST_DATA_SERVICE.get_data_for_definition(57)
        func = calc.data_calc_function_switcher[57]
        result = func(data)
        resultFrame = pandas.read_json(result)
        assert_frame_equal(resultFrame, expected, rtol = REL_TOL)

    #test data def 58
    def test_get_service_trend_time_week(self):
        expected = pandas.read_csv(
            os.path.join(__location__, './expected_results/test_calc_service_trends/service_trend_time_week.csv'),
            skipinitialspace= True
        ).fillna('0')
        expected['n'] = expected['n'].astype(int64)

        data = TEST_DATA_SERVICE.get_data_for_definition(58)
        func = calc.data_calc_function_switcher[58]
        result = func(data)
        resultFrame = pandas.read_json(result)
        assert_frame_equal(resultFrame, expected, rtol = REL_TOL)

    #test data def 59
    def test_get_service_trend_time_day(self):
        expected = pandas.read_csv(
            os.path.join(__location__, './expected_results/test_calc_service_trends/service_trend_time_day.csv')
        ).fillna('0')
        expected['n'] = expected['n'].astype(int64)

        data = TEST_DATA_SERVICE.get_data_for_definition(59)
        func = calc.data_calc_function_switcher[59]
        result = func(data)
        resultFrame = pandas.read_json(result)
        assert_frame_equal(resultFrame, expected, rtol = REL_TOL)

    #test data def 60
    def test_get_service_trend_monthly_visits_avg(self):
        expected = pandas.read_csv(
            os.path.join(__location__, './expected_results/test_calc_service_trends/service_trend_monthly_visits_avg.csv')
        ).fillna('0')
        data = TEST_DATA_SERVICE.get_data_for_definition(60)
        func = calc.data_calc_function_switcher[60]
        result = func(data)
        resultFrame = pandas.read_json(result)
        self.assertTrue(len(resultFrame) == len(expected))
        assert_frame_equal(resultFrame, expected, rtol = REL_TOL)