from django.test import TestCase
from transform_layer.services.data_service import DataService
from django.db import connections
import pandas
from pandas.testing import assert_frame_equal, assert_series_equal

import unittest
# import csv
# import os 
# import sys
# import json
# import math





class SkeletonsTestCase(unittest.TestCase):

    #skeletons tests
    def test_get_monthly_date_skeleton(self):
        test_scope = {
                "startDate":"01/01/2020",
                "endDate":"12/31/2020",
                "scope_type": "hierarchy",
                "scope_field":"loc_id",
                "scope_field_value":6,
                "control_type_name":"Is Grocery Service",
            }

        ds = DataService(test_scope)
        m_skeleton = ds._get_monthly_date_skeleton()
        self.assertTrue(len(m_skeleton) == 12)


    def test_get_weekly_date_skeleton(self):
        test_scope = {
            "startDate":"01/01/2019",
            "endDate":"12/31/2019",
            "scope_type": "hierarchy",
            "scope_field":"loc_id",
            "scope_field_value":6,
            "control_type_name":"Is Grocery Service",
        }
        ds = DataService(test_scope)
        w_skeleton = ds._get_weekly_date_skeleton()
        #52 * 7 = 364; +1  day means +1 extra row in the dataframe
        self.assertTrue(len(w_skeleton) == 53)
        
    def test_get_daily_date_skeleton(self):
        test_scope = {
            "startDate":"01/01/2019",
            "endDate":"12/31/2019",
            "scope_type": "hierarchy",
            "scope_field":"loc_id",
            "scope_field_value":6,
            "control_type_name":"Is Grocery Service",
        }
        ds = DataService(test_scope)
        d_skeleton = ds._get_daily_date_skeleton()
        self.assertTrue(len(d_skeleton) == 365)

