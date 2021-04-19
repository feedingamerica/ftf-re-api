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
    "endDate":"3/31/2021",
    "scope_type": "hierarchy",
    "scope_field":"loc_id",
    "scope_field_value":6,
    "control_type_name":"Is Grocery Service"
}

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

TEST_DATA_SERVICE = DataService(base_scope)
class CalculationsTestCase(unittest.TestCase):
    
    #test data def 69
    def test_get_gender_summary(self):
        expected = pandas.read_csv(
            os.path.join(__location__, './expected_results/test_family_members/family_members_hoh_gender.csv')
        ).fillna("")

        data = TEST_DATA_SERVICE.get_data_for_definition(69)
        func = calc.data_calc_function_switcher[69]
        result = func(data)
        resultFrame = pandas.read_json(result)
        assert_frame_equal(resultFrame, expected, rtol = REL_TOL)
    #test data def 71
    def test_get_skipped_generation(self):
        expected = pandas.read_csv(
            os.path.join(__location__, './expected_results/test_family_members/family_members_skipped_generation.csv'),
            index_col = 0
        ).fillna(0).reset_index().drop(columns = 'index')
        expected = expected.astype({'n_families':'int64', 'is_single_senior_w_children' : 'int64'})

        data = TEST_DATA_SERVICE.get_data_for_definition(71)
        func = calc.data_calc_function_switcher[71]
        result = func(data)
        resultFrame = pandas.read_json(result)
        self.assertTrue(len(resultFrame) == len(expected))
        resultFrame = resultFrame.sort_values(by=['n_families'], ignore_index=True)
        expected = expected.sort_values(by=['n_families'], ignore_index=True)
        assert_frame_equal(resultFrame[['is_single_senior_w_children','n_families']] , expected[['is_single_senior_w_children','n_families']], rtol = REL_TOL)

    #test data def 72
    def test_get_demo_indv_gender(self):
        expected = pandas.read_csv(
            os.path.join(__location__, './expected_results/test_family_members/family_members_demo_indv_gender.csv')
        ).fillna("")

        data = TEST_DATA_SERVICE.get_data_for_definition(72)
        func = calc.data_calc_function_switcher[72]
        result = func(data)
        resultFrame = pandas.read_json(result)
        assert_frame_equal(resultFrame, expected, rtol = REL_TOL)

    #test data def 73
    def test_get_demo_indv_age_groups(self):
        expected = pandas.read_csv(
            os.path.join(__location__, './expected_results/test_family_members/family_members_demo_indv_age_groups.csv')
        )

        data = TEST_DATA_SERVICE.get_data_for_definition(73)
        func = calc.data_calc_function_switcher[73]
        result = func(data)
        resultFrame = pandas.read_json(result)
        assert_frame_equal(resultFrame, expected, rtol = REL_TOL)

    #test data def 74
    def test_get_hh_has_age_groups(self):
        expected = pandas.read_csv(
            os.path.join(__location__, './expected_results/test_family_members/family_members_hh_has_age_groups.csv')
        )

        data = TEST_DATA_SERVICE.get_data_for_definition(74)
        func = calc.data_calc_function_switcher[74]
        result = func(data)
        resultFrame = pandas.read_json(result)
        assert_frame_equal(resultFrame, expected, rtol = REL_TOL)

    #test data def 75
    def test_get_population_pyramid(self):
        expected = pandas.read_csv(
            os.path.join(__location__, './expected_results/test_family_members/population_pyramid.csv'),
            index_col = 0
        )

        data = TEST_DATA_SERVICE.get_data_for_definition(75)
        func = calc.data_calc_function_switcher[75]
        result = func(data)
        resultFrame = pandas.read_json(result)
        assert_frame_equal(resultFrame, expected, rtol = REL_TOL)

    #test data def 76
    def test_get_demo_indv_race(self):
        expected = pandas.read_csv(
            os.path.join(__location__, './expected_results/test_family_members/demo_indv_race.csv'),
            index_col = 0
        )

        data = TEST_DATA_SERVICE.get_data_for_definition(76)
        func = calc.data_calc_function_switcher[76]
        result = func(data)
        resultFrame = pandas.read_json(result)
        assert_frame_equal(resultFrame, expected, rtol = REL_TOL)

    #test data def 77
    def test_get_demo_indv_ethnic(self):
        expected = pandas.read_csv(
            os.path.join(__location__, './expected_results/test_family_members/family_members_demo_indv_ethnic.csv'),
            index_col = 0
        ).fillna(0).reset_index().drop(columns = 'index')
        expected = expected.astype({'n_indv':'int64'})

        data = TEST_DATA_SERVICE.get_data_for_definition(77)
        func = calc.data_calc_function_switcher[77]
        result = func(data)
        resultFrame = pandas.read_json(result)
        assert_frame_equal(resultFrame, expected, rtol = REL_TOL)
    
    #data def def 78
    def test_get_demo_indv_military(self):
        expected = pandas.read_csv(
            os.path.join(__location__, './expected_results/test_family_members/family_members_demo_indv_military.csv')
        ).fillna(0)
        
        expected = expected.astype({'n_indv':'int64'})

        data = TEST_DATA_SERVICE.get_data_for_definition(78)
        func = calc.data_calc_function_switcher[78]
        result = func(data)
        resultFrame = pandas.read_json(result)
        assert_frame_equal(resultFrame, expected, rtol = REL_TOL)

    #data def 79
    def test_get_demo_indv_education(self):
        expected = pandas.read_csv(
            os.path.join(__location__, './expected_results/test_family_members/demo_indv_education.csv'),
            index_col = 0
        ).fillna(0).reset_index().drop(columns = 'index')
        
        expected = expected.astype({'n_indv':'int64'})

        data = TEST_DATA_SERVICE.get_data_for_definition(79)
        func = calc.data_calc_function_switcher[79]
        result = func(data)
        resultFrame = pandas.read_json(result)
        assert_frame_equal(resultFrame, expected, rtol = REL_TOL)

    #data def 80
    def test_get_demo_indv_employment(self):
        expected = pandas.read_csv(
            os.path.join(__location__, './expected_results/test_family_members/demo_indv_employment.csv'),
            index_col = 0
        ).fillna(0).reset_index().drop(columns = 'index')
        
        expected = expected.astype({'n_indv':'int64'})

        data = TEST_DATA_SERVICE.get_data_for_definition(80)
        func = calc.data_calc_function_switcher[80]
        result = func(data)
        resultFrame = pandas.read_json(result)
        assert_frame_equal(resultFrame, expected, rtol = REL_TOL)
    
    #data def 81
    def test_get_demo_indv_health_insurance(self):
        expected = pandas.read_csv(
            os.path.join(__location__, './expected_results/test_family_members/demo_indv_health_insurance.csv'),
            index_col = 0
        ).fillna(0).reset_index().drop(columns = 'index')
        
        expected = expected.astype({'n_indv':'int64'})

        data = TEST_DATA_SERVICE.get_data_for_definition(81)
        func = calc.data_calc_function_switcher[81]
        result = func(data)
        resultFrame = pandas.read_json(result)
        assert_frame_equal(resultFrame, expected, rtol = REL_TOL)
