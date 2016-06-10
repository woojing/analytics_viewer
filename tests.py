# -*- coding: utf-8 -*-
import unittest
from helper import parse_params, map_params, ios_chunk, parse_ios_params

class AndroidParsingTest(unittest.TestCase):
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

class IosParsingTest(unittest.TestCase):
    test_log = b'''
Jun  8 15:26:57 testui-iPhone BDTv6[278] <Warning>: GoogleTagManager verbose: GoogleAnalytics 3.14 -[GAIBatchingDispatcher persist:] (GAIBatchingDispatcher.m:517): Saved hit: {
        parameters =     {
            "&_crc" = 0;
            "&_s" = 261;
            "&_u" = ".7nBL";
            "&_v" = "mi3.1.4";
            "&a" = 1100049269;
            "&aid" = "com.stonykids.bdtV2";
            "&an" = BDTv6;
            "&av" = "6.0.4";
            "&cd11" = "shop_list";
            "&cd12" = "";
            "&cd14" = "\Uc11c\Uc6b8\Ud2b9\Ubcc4\Uc2dc \Uac15\Ub0a8\Uad6c \Uc5ed\Uc0bc1\Ub3d9";
            "&cd15" = Korea;
            "&cd16" = "\Uac15\Ub0a8\Uad6c";
            "&cd17" = "\Uc5ed\Uc0bc1\Ub3d9";
            "&cd18" = "127.029541066253";
            "&cd19" = "37.4991076889491";
            "&cd20" = "";
            "&cd23" = "";
            "&cd24" = "";
            "&cd25" = "";
            "&cd26" = "";
            "&cd27" = "";
            "&cd28" = "";
            "&cd29" = "";
            "&cd31" = 0;
            "&cd32" = "\Ubaa8\Ubc14\Uc77c\Uacb0\Uc81c \Uc6b0\Uc218\Uc5c5\Uccb4\Uc21c";
            "&cd33" = 681;
            "&cd34" = 0;
            "&cd35" = "";
            "&cd40" = 1;
            "&cd41" = 3375578;
            "&cd61" = "";
            "&cd62" = "";
            "&cd63" = "";
            "&cd64" = "";
            "&cd68" = "";
            "&cd69" = "";
            "&cd70" = "";
            "&cd71" = "";
            "&cd72" = "";
            "&cd73" = "";
            "&cd74" = "";
            "&cd75" = "";
            "&cd76" = "";
            "&cd77" = "";
            "&cd79" = 1;
            "&cd80" = "";
            "&cd81" = "";
            "&cid" = "2c886bea-c66a-4a20-899a-f6665d941163";
            "&dm" = "iPhone8,2";
            "&ds" = app;
            "&ea" = "shop_list.loaded";
            "&ec" = "qa.shop_list";
            "&ni" = true;
            "&sr" = 1080x1920;
            "&t" = event;
            "&tid" = "UA-75137464-1";
            "&ul" = "ko-kr";
            "&v" = 1;
            "&z" = 4453487951715844835;
            gaiVersion = "3.14";
        };
        timestamp = "2016-06-08 06:26:57 +0000";
    }
'''

    def test_chunking_right_log(self):
        it = iter(self.test_log.splitlines())
        ga_chunk = ios_chunk(it)
        chunk = '\n'.join([str(line) for line in ga_chunk])
        params = parse_ios_params(chunk)
        self.assertEqual(params['ec'], 'qa.shop_list')
