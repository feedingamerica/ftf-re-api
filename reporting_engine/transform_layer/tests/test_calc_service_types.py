from django.test import TestCase
from django.db import connections
import pandas
from pandas.testing import assert_frame_equal, assert_series_equal
from transform_layer.services.data_service import DataService
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
    "endDate":"12/31/2020",
    "scope_type": "hierarchy",
    "scope_field":"fb_id",
    "scope_field_value":21,
    "control_type_name":"Is Grocery Service"
}

json_test_results = {
    "result_label": ["service_summary_service","service_category_service", "distribution_outlets"],
    "mofc_value": [
        '{"service_name":{"0":"Backpack w\\/ Food","1":"CSFP Box","2":"Disaster Box","3":"Emergency - Prepack - 1 day","4":"Emergency - Prepack - 10 day","5":"Emergency - Prepack - '
        '2 day","6":"Emergency - Prepack - 3 day","7":"Food - Box - 1 day","8":"Food - Box - 2 day","9":"Food - Holiday Box","10":"Food - Senior Box","11":"Healthy Box","12":"Home '
        'Delivered Food","13":"Mobile Pantry - Choice","14":"Mobile Pantry - Senior","15":"Pantry - Choice - 10 day","16":"Pantry - Choice - 14 day","17":"Pantry - Choice - '
        '1day","18":"Pantry - Choice - 3 day","19":"Pantry - Choice - 4 day","20":"Pantry - Choice - 5 day","21":"Pantry - Choice - 6 day","22":"Pantry - Choice - 7 '
        'day","23":"Pantry - Choice - 8 day","24":"Pantry - Choice - 9 day","25":"Pantry - Prepack - 14 day","26":"Pantry - Prepack - 3 day","27":"Pantry - Prepack - 3 day - '
        'Vegetarian","28":"Pantry - Prepack - 4 day","29":"Pantry - Prepack - 5 day","30":"Pantry - Prepack - 6 day","31":"Pantry - Prepack - 7 day","32":"Pantry - Prepack - 8 '
        'day","33":"Pantry - Prepack - 9 day","34":"Pantry - Prepack\\/Choice - 3 day","35":"Pantry - Prepack\\/Choice - 4 day","36":"Pantry - Prepack\\/Choice - 5 '
        'day","37":"Pantry - Special Dietary Needs - 3 day","38":"Prepack - Perishables only","39":"Produce & Protein","40":"Produce \\/ Mobile Market","41":"Produce '
        'Market","42":"Rx - Produce","43":"Snack Bag","44":"Special - Perishables only","45":"TEFAP"},"Families '
        'Served":{"0":173,"1":6149,"2":73,"3":599,"4":4,"5":239,"6":497,"7":190,"8":368,"9":13373,"10":2173,"11":1,"12":1773,"13":29458,"14":1545,"15":1332,"16":2197,"17":65336,"18":303571,"19":35831,"20":59866,"21":6790,"22":16919,"23":2049,"24":1048,"25":3444,"26":97550,"27":2,"28":11237,"29":28965,"30":2338,"31":98123,"32":5,"33":1878,"34":596,"35":66,"36":865,"37":1,"38":5473,"39":27111,"40":191074,"41":120216,"42":1440,"43":381,"44":25638,"45":4},"People '
        'Served":{"0":750,"1":11712,"2":272,"3":1482,"4":9,"5":895,"6":1268,"7":616,"8":1537,"9":47112,"10":3084,"11":5,"12":4765,"13":79066,"14":2309,"15":3479,"16":5849,"17":227452,"18":965629,"19":115220,"20":190225,"21":21308,"22":59012,"23":6062,"24":2649,"25":8215,"26":290223,"27":9,"28":36120,"29":105112,"30":7995,"31":340291,"32":14,"33":5996,"34":1601,"35":199,"36":2386,"37":4,"38":19428,"39":95428,"40":546296,"41":370530,"42":4833,"43":689,"44":84918,"45":19}}',
        '{"service_category_name":{"0":"CSFP","1":"Choice Pantry","2":"Prepack Pantry","3":"Produce"},"Families ''Served":{"0":6149,"1":553054,"2":264917,"3":343841},"People '
        'Served":{"0":11712,"1":1773692,"2":860664,"3":1026005}}',
        '{"sites_visited":{"0":1,"1":2,"2":3,"3":4,"4":5,"5":6,"6":7,"7":8,"8":9,"9":10,"10":11,"11":12,"12":13,"13":14,"14":15,"15":16,"16":17,"17":18,"18":19,"19":20,"20":22,"21":23,"22":24,"23":28,"24":29},"un_duplicated_families":{"0":132981,"1":37029,"2":14403,"3":6363,"4":3072,"5":1646,"6":939,"7":489,"8":313,"9":201,"10":125,"11":79,"12":53,"13":35,"14":31,"15":22,"16":11,"17":7,"18":2,"19":5,"20":2,"21":4,"22":2,"23":1,"24":1}}'],
}



def read_expected_json():
    expected = {}

    for i in range(len(json_test_results['result_label'])):
        expected[json_test_results['result_label'][i]] = {
            "mofc_value": json_test_results["mofc_value"][i]
        }

    return expected

EXPECTED_JSON_RESULTS = read_expected_json()


#shared test data service so you don't have to make a db call for every test
#not gonna work with multithreaded tests
TEST_DATA_SERVICE = DataService(base_services_scope)



class CalculationsTestCase(unittest.TestCase):
    
    
    # Base services
    def test_get_services_summary(self):
        data = TEST_DATA_SERVICE.get_data_for_definition(23)
        func = calc.data_calc_function_switcher[23]
        result = func(data)
        result = pandas.DataFrame.from_dict(json.loads(result))
        expected = json.loads(EXPECTED_JSON_RESULTS["service_summary_service"]["mofc_value"])
        expected = pandas.DataFrame.from_dict(expected)
        assert_frame_equal(result, expected, rtol= REL_TOL)

        
    def test_get_services_category(self):
        data = TEST_DATA_SERVICE.get_data_for_definition(24)
        func = calc.data_calc_function_switcher[24]
        result = func(data)
        result = pandas.DataFrame.from_dict(json.loads(result))
        expected = json.loads(EXPECTED_JSON_RESULTS["service_category_service"]["mofc_value"])
        expected = pandas.DataFrame.from_dict(expected)
        assert_frame_equal(result, expected, rtol= REL_TOL)


    def test_get_distribution_outlets(self):
        data = TEST_DATA_SERVICE.get_data_for_definition(25)
        func = calc.data_calc_function_switcher[25]
        result = func(data)
        result = pandas.DataFrame.from_dict(json.loads(result))
        expected = json.loads(EXPECTED_JSON_RESULTS["distribution_outlets"]["mofc_value"])
        expected = pandas.DataFrame.from_dict(expected)
        assert_frame_equal(result, expected, rtol= REL_TOL)

if __name__ == '__main__':
    unittest.main()