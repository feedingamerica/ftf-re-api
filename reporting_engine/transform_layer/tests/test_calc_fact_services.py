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

sample_scope_1 = {
    "startDate":"2019-01-01",
    "endDate":"2019-12-31",
    "scope_type": "hierarchy",
    "scope_field":"fb_id",
    "scope_field_value":21,
    "control_type_name":"Is Grocery Service"
}


sample_scope_2 = {
    "startDate":"2019-01-01",
    "endDate":"2019-12-31",
    "scope_type": "geography",
    "scope_field":"fips_cnty",
    "scope_field_value":39049,
    "control_type_name":"Is Grocery Service"
}





#reads int_test_results.csv and returns a dictionary of expected test results for data definitions 1-22.
def read_expected_int():
    expected = {}
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    with open(os.path.join(__location__,'./int_test_results.csv'), newline = '') as csvfile:
        rownum = 0
        reader = csv.reader(csvfile, dialect = 'excel')
        for row in reader:
            if rownum != 0:
                expected[row[0]] = {
                    "mofc_value" : float(row[1]) if row[1].find(".") != -1 else int(row[1]),
                    "franklin_value" : float(row[2]) if row[2].find(".") != -1 else int(row[2])
                }
            rownum += 1
    return expected


TEST_DATA_SERVICE = DataService(sample_scope_2)
EXPECTED_INT_RESULTS = read_expected_int()

class CalculationsTestCase(unittest.TestCase):
    
    def test_get_services_total(self):
        #how to avoid repeatedly making database requests in calculation tests?
        #might want to instantiate the data service object
        #might want to pass a connection to mock database in data_service.get_fact_service
        #make data service a singleton
        data = TEST_DATA_SERVICE.get_data_for_definition(1)
        func = calc.data_calc_function_switcher[1]
        result = func(data)
        self.assertTrue(math.isclose(result, EXPECTED_INT_RESULTS["services_total"]["franklin_value"], rel_tol = REL_TOL))
    
    def test_get_undup_hh_total(self):
        data = TEST_DATA_SERVICE.get_data_for_definition(2)
        func = calc.data_calc_function_switcher[2]
        result = func(data)
        self.assertTrue(math.isclose(result, EXPECTED_INT_RESULTS["undup_hh_total"]["franklin_value"], rel_tol = REL_TOL))
    
    def test_get_undup_indv_total(self):
        data = TEST_DATA_SERVICE.get_data_for_definition(3)
        func = calc.data_calc_function_switcher[3]
        result = func(data)
        self.assertTrue(math.isclose(result, EXPECTED_INT_RESULTS["undup_indv_total"]["franklin_value"], rel_tol = REL_TOL))

    def test_get_services_per_uhh_avg(self):
        data = TEST_DATA_SERVICE.get_data_for_definition(4)
        func = calc.data_calc_function_switcher[4]
        result = func(data)
        self.assertTrue(math.isclose(result, EXPECTED_INT_RESULTS["services_per_uhh_avg"]["franklin_value"], rel_tol = REL_TOL))

    
    #Ohio Addin
    def test_get_hh_wminor(self):
        data = TEST_DATA_SERVICE.get_data_for_definition(5)
        func = calc.data_calc_function_switcher[5]
        result = func(data)
        self.assertTrue(math.isclose(result, EXPECTED_INT_RESULTS["hh_wminor"]["franklin_value"], rel_tol = REL_TOL))
        

    def test_get_hh_wominor(self):
        data = TEST_DATA_SERVICE.get_data_for_definition(6)
        func = calc.data_calc_function_switcher[6]
        result = func(data)
        self.assertTrue(math.isclose(result, EXPECTED_INT_RESULTS["hh_wominor"]["franklin_value"], rel_tol = REL_TOL))
        
    def test_get_hh_total(self):
        data = TEST_DATA_SERVICE.get_data_for_definition(7)
        func = calc.data_calc_function_switcher[7]
        result = func(data)
        self.assertTrue(math.isclose(result, EXPECTED_INT_RESULTS["hh_total"]["franklin_value"], rel_tol = REL_TOL))
        
    def test_get_indv_sen_hh_wminor(self):
        data = TEST_DATA_SERVICE.get_data_for_definition(8)
        func = calc.data_calc_function_switcher[8]
        result = func(data)
        self.assertTrue(math.isclose(result, EXPECTED_INT_RESULTS["indv_sen_hh_wminor"]["franklin_value"], rel_tol = REL_TOL))
        
    def test_get_indv_sen_hh_wominor(self):
        data = TEST_DATA_SERVICE.get_data_for_definition(9)
        func = calc.data_calc_function_switcher[9]
        result = func(data)
        self.assertTrue(math.isclose(result, EXPECTED_INT_RESULTS["indv_sen_hh_wominor"]["franklin_value"], rel_tol = REL_TOL))

        
    def test_get_indv_sen_total(self):
        data = TEST_DATA_SERVICE.get_data_for_definition(10)
        func = calc.data_calc_function_switcher[10]
        result = func(data)
        self.assertTrue(math.isclose(result, EXPECTED_INT_RESULTS["indv_sen_total"]["franklin_value"], rel_tol = REL_TOL))
        
    def test_get_indv_adult_hh_wminor(self):
        data = TEST_DATA_SERVICE.get_data_for_definition(11)
        func = calc.data_calc_function_switcher[11]
        result = func(data)
        self.assertTrue(math.isclose(result, EXPECTED_INT_RESULTS["indv_adult_hh_wminor"]["franklin_value"], rel_tol = REL_TOL))
        
    def test_get_indv_adult_hh_wominor(self):
        data = TEST_DATA_SERVICE.get_data_for_definition(12)
        func = calc.data_calc_function_switcher[12]
        result = func(data)
        self.assertTrue(math.isclose(result, EXPECTED_INT_RESULTS["indv_adult_hh_wominor"]["franklin_value"], rel_tol = REL_TOL))
        
    def test_get_indv_adult_total(self):
        data = TEST_DATA_SERVICE.get_data_for_definition(13)
        func = calc.data_calc_function_switcher[13]
        result = func(data)
        self.assertTrue(math.isclose(result, EXPECTED_INT_RESULTS["indv_adult_total"]["franklin_value"], rel_tol = REL_TOL))
        
    def test_get_indv_child_hh_wminor(self):
        data = TEST_DATA_SERVICE.get_data_for_definition(14)
        func = calc.data_calc_function_switcher[14]
        result = func(data)
        self.assertTrue(math.isclose(result, EXPECTED_INT_RESULTS["indv_child_hh_wminor"]["franklin_value"], rel_tol = REL_TOL))
        
    def test_get_indv_child_hh_wominor(self):
        data = TEST_DATA_SERVICE.get_data_for_definition(15)
        func = calc.data_calc_function_switcher[15]
        result = func(data)
        self.assertTrue(math.isclose(result, EXPECTED_INT_RESULTS["indv_child_hh_wominor"]["franklin_value"], rel_tol = REL_TOL))
        
    def test_get_indv_child_total(self):
        data = TEST_DATA_SERVICE.get_data_for_definition(16)
        func = calc.data_calc_function_switcher[16]
        result = func(data)
        self.assertTrue(math.isclose(result, EXPECTED_INT_RESULTS["indv_child_total"]["franklin_value"], rel_tol = REL_TOL))
        
    def test_get_indv_total_hh_wminor(self):
        data = TEST_DATA_SERVICE.get_data_for_definition(17)
        func = calc.data_calc_function_switcher[17]
        result = func(data)
        self.assertTrue(math.isclose(result, EXPECTED_INT_RESULTS["indv_total_hh_wminor"]["franklin_value"], rel_tol = REL_TOL))
        
    def test_get_indv_total_hh_wominor(self):
        data = TEST_DATA_SERVICE.get_data_for_definition(18)
        func = calc.data_calc_function_switcher[18]
        result = func(data)
        self.assertTrue(math.isclose(result, EXPECTED_INT_RESULTS["indv_total_hh_wominor"]["franklin_value"], rel_tol = REL_TOL))
        
    def test_get_indv_total(self):
        data = TEST_DATA_SERVICE.get_data_for_definition(19)
        func = calc.data_calc_function_switcher[19]
        result = func(data)
        self.assertTrue(math.isclose(result, EXPECTED_INT_RESULTS["indv_total"]["franklin_value"], rel_tol = REL_TOL))
        
    # #MOFC addin
    def test_get_hh_wsenior(self):
        data = TEST_DATA_SERVICE.get_data_for_definition(20)
        func = calc.data_calc_function_switcher[20]
        result = func(data)
        self.assertTrue(math.isclose(result, EXPECTED_INT_RESULTS["hh_wsenior"]["franklin_value"], rel_tol = REL_TOL))
        
    def test_get_hh_wosenior(self):
        data = TEST_DATA_SERVICE.get_data_for_definition(21)
        func = calc.data_calc_function_switcher[21]
        result = func(data)
        self.assertTrue(math.isclose(result, EXPECTED_INT_RESULTS["hh_wosenior"]["franklin_value"], rel_tol = REL_TOL))
        
    def test_get_hh_grandparent(self):
        data = TEST_DATA_SERVICE.get_data_for_definition(22)
        func = calc.data_calc_function_switcher[22]
        result = func(data)
        self.assertTrue(math.isclose(result, EXPECTED_INT_RESULTS["hh_grandparent"]["franklin_value"], rel_tol = REL_TOL))

if __name__ == '__main__':
    unittest.main()