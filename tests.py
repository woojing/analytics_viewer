# -*- coding: utf-8 -*-
import unittest
from helper import parse_params, map_params

class ParsingTest(unittest.TestCase):
    test_log = '05-02 12:18:29.017 16262 16447 I GAv4    : Dry run enabled. Would have sent hit: ht=1462159108961, _v=ma8.4.87, a=1632316130, adid=bbb1d4f7-7fb6-4265-b0c8-91d0379db289, aid=com.fineapp.yogiyo, an=배달 요기요, ate=0, av=2.18.5, cd=V2/RestaurantMenu/Review/230518, cd1=20, cd10=Guest, cd11=Square, cd12=Square, cd13=contract/contract, cd14=contract/contract, cd15=3, cd16=3, cd17=, cd18=N, cd19=false, cd2=All, cd20=false, cd3=N, cd4=N, cd5=N, cd6=N, cd7=Default, cd8=Default, cd9=Guest, cid=894a3ba6-264c-41a9-a862-823a00932780, sr=1080x1776, t=screenview, tid=UA-42635603-1, ul=ko-kr, v=1'
    def test_param_parsing(self):
        params = parse_params(self.test_log)
        self.assertIn('an', params)
        self.assertEqual('배달 요기요', params['an'])

    def test_param_mapping(self):
        params = parse_params(self.test_log)
        result = map_params(params)
        self.assertIn('Application Name', result)
        self.assertEqual(result['Application Name'], "배달 요기요")
        self.assertIn('Custom Dimension 10', result)
