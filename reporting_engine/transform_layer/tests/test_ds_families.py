from django.test import TestCase
from transform_layer.services.data_service import DataService
from django.db import connections
import pandas
from pandas.testing import assert_frame_equal, assert_series_equal

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
    "endDate":"12/31/2020",
    "scope_type": "hierarchy",
    "scope_field":"fb_id",
    "scope_field_value":21,
    "control_type_name":"Is Grocery Service"
}



class CalculationsTestCase(unittest.TestCase):    
    def test_get_frequency_visits(self):
        expected = {
            "n_families": {
                "1":75530,"2":29221,"3":17037,"4":11730,"5":8713,"6":6931,"7":5698,"8":4898,"9":4115,"10":3470,"11":3181,"12":2867,"13":2342,"14":1889,
                "15":1691,"16":1554,"17":1339,"18":1244,"19":1101,"20":1021,"21":921,"22":797,"23":747,"24":694,"25":8863
            },
            "sum_services" :{
                "1":75530,"2":58442,"3":51111,"4":46920,"5":43565,"6":41586,"7":39886,"8":39184,"9":37035,"10":34700,"11":34991,"12":34404,"13":30446,
                "14":26446,"15":25365,"16":24864,"17":22763,"18":22392,"19":20919,"20":20420,"21":19341,"22":17534,"23":17181,"24":16656,"25":366004
            }
        }
        expected = pandas.DataFrame.from_dict(expected)
        ds = DataService(base_services_scope)
        result = ds.get_data_for_definition(26)
        resultDict = json.loads(result)
        resultFrame = pandas.DataFrame.from_dict(resultDict)
        assert_frame_equal(resultFrame, expected, rtol= REL_TOL)

        
    def test_get_household_composition(self):
        expected = {
            "family_composition_type": {
                "0":"adults_and_children",
                "1":"adults_and_seniors",
                "2":"adults_only",
                "3":"adults_seniors_and_children",
                "4":"children_and_seniors",
                "5":"children_only",
                "6":"seniors_only"
                },
            "num_families":
            {
                "0":74123,
                "1":17882,
                "2":58365,
                "3":13913,
                "4":2492,
                "5":434,
                "6":30385
            }
        }
        expected = pandas.DataFrame.from_dict(expected)
        ds = DataService(base_services_scope)
        result = ds.get_data_for_definition(28)
        resultDict = json.loads(result)
        resultFrame = pandas.DataFrame.from_dict(resultDict)
        assert_frame_equal(resultFrame, expected, rtol= REL_TOL)

    def test_get_family_comp_key_insight(self):

        # expected = {
        #     "family_composition_type": ["has_child_senior"," no_child_senior"],
        #     "num_families": [139229, 58365]
        # }
        expected = {
            "family_composition_type": {
                "0":"has_child_senior",
                "1":"no_child_senior"
                },
            "num_families":
            {
                "0":139229,
                "1":58365,
            }
        }
        expected = pandas.DataFrame.from_dict(expected)
        ds = DataService(base_services_scope)
        result = ds.get_data_for_definition(29)
        resultDict = json.loads(result)
        resultFrame = pandas.DataFrame.from_dict(resultDict)
        assert_frame_equal(resultFrame, expected, rtol= REL_TOL)

    def test_get_household_size_distribution_1_to_10(self):
        expected = {
            "avg_fam_size_roll": {
                "0": 1.0, "1": 2.0, "2": 3.0, "3": 4.0, "4": 5.0, "5": 6.0, "6": 7.0, "7": 8.0, "8": 9.0, "9": 10.0
            },
            "num_families":{
                "0": 56174, "1": 38967, "2": 29398, "3": 28081, "4": 20341, "5": 12336, "6": 6103, "7": 3144, "8": 1493, "9": 1557
            },
            "classic_roll": {
                "0": "1 - 3", "1": "1 - 3", "2": "1 - 3", "3": "4 - 6", "4": "4 - 6", "5": "4 - 6", "6": "7+", "7": "7+", "8": "7+", "9": "7+"
            }
        }
        expected = pandas.DataFrame.from_dict(expected)
        ds = DataService(base_services_scope)
        result = ds.get_data_for_definition(30)
        resultDict = json.loads(result)
        resultFrame = pandas.DataFrame.from_dict(resultDict)
        assert_frame_equal(resultFrame, expected, rtol= REL_TOL)

    def test_get_household_size_distribution_classic(self):
        expected = {
            '1 - 3':124539,
            '4 - 6':60758,
            '7+':12297
        }
        expected = pandas.Series(data = expected)
        ds = DataService(base_services_scope)
        result = ds.get_data_for_definition(31)
        resultDict = json.loads(result)
        resultFrame = pandas.Series(data = resultDict)
        assert_series_equal(resultFrame, expected, rtol= REL_TOL)


if __name__ == '__main__':
    unittest.main()