from django.test import TestCase
from transform_layer.services.data_service import DataService, KEY_SERVICE, KEY_MEMBER, KEY_FAMILY
from transform_layer.calculations import CalculationDispatcher
from django.db import connections
import pandas
from pandas.testing import assert_frame_equal, assert_series_equal

import unittest


class HasDataTestCase(unittest.TestCase):
    def test_has_data_empty_dataframe(self):
        data = pandas.DataFrame()
        self.assertFalse(CalculationDispatcher.has_data(data))
    def test_has_data_nonempty_dataframe(self):
        d1 = {"col1": [1,2,3,4], "col2": [5,6,7,8]}
        data =  pandas.DataFrame(d1)
        self.assertTrue(CalculationDispatcher.has_data(data))

    def test_has_data_no_services(self):
        d1 = {"col1": [1,2,3,4], "col2": [5,6,7,8]}
        data = {
            KEY_SERVICE: pandas.DataFrame(),
            KEY_MEMBER: pandas.DataFrame(d1),
            KEY_FAMILY: pandas.DataFrame(d1)
        }
        self.assertFalse(CalculationDispatcher.has_data(data))

    def test_has_data_no_members(self):
        d1 = {"col1": [1,2,3,4], "col2": [5,6,7,8]}
        data = {
            KEY_SERVICE: pandas.DataFrame(d1),
            KEY_MEMBER: pandas.DataFrame(),
            KEY_FAMILY: pandas.DataFrame(d1)
        }
        self.assertFalse(CalculationDispatcher.has_data(data))

    def test_has_data_full_dict(self):
        d1 = {"col1": [1,2,3,4], "col2": [5,6,7,8]}
        data = {
            KEY_SERVICE: pandas.DataFrame(d1),
            KEY_MEMBER: pandas.DataFrame(d1),
            KEY_FAMILY: pandas.DataFrame(d1)
        }
        self.assertTrue(CalculationDispatcher.has_data(data))

    def test_has_data_not_a_dataframe(self):
        self.assertFalse(CalculationDispatcher.has_data("hello"))





    