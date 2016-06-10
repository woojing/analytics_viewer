# -*- coding: utf-8 -*-
import os
import re
import itertools
import subprocess
import functools

def ios_chunk(line_it):
    chunk_start = b': GoogleAnalytics '
    chunk_end = b'timestamp = '
    it = itertools.dropwhile(lambda x: chunk_start not in x, line_it)
    next(it)
    return itertools.takewhile(lambda x: chunk_end not in x, it)

def parse_ios_params(chunk):
    param_pattern = re.compile(r'"&([^\s.]*?)"\s=\s"*(.*?)"*;')
    params = param_pattern.findall(chunk)
    return dict(params)

def parse_params(line):
    param_pattern = re.compile(r'([^\s.]*?)=([^,]*)')
    params = param_pattern.findall(line)
    return dict(params)

def map_params(params):
    # ref. https://developers.google.com/analytics/devguides/collection/protocol/v1/parameters
    map_table = {
        "v":"Protocol Version",
        "tid":"Tracking ID / Web Property ID",
        "aip":"Anonymize IP",
        "ds":"Data Source",
        "qt":"Queue Time",
        "z":"Cache Buster",
        "cid":"Client ID",
        "uid":"User ID",
        "sc":"Session Control",
        "uip":"IP Override",
        "ua":"User Agent Override",
        "geoid":"Geographical Override",
        "dr":"Document Referrer",
        "cn":"Campaign Name",
        "cs":"Campaign Source",
        "cm":"Campaign Medium",
        "ck":"Campaign Keyword",
        "cc":"Campaign Content",
        "ci":"Campaign ID",
        "gclid":"Google AdWords ID",
        "dclid":"Google Display Ads ID",
        "sr":"Screen Resolution",
        "vp":"Viewport size",
        "de":"Document Encoding",
        "sd":"Screen Colors",
        "ul":"User Language",
        "je":"Java Enabled",
        "fl":"Flash Version",
        "t":"Hit type",
        "ni":"Non-Interaction Hit",
        "dl":"Document location URL",
        "dh":"Document Host Name",
        "dp":"Document Path",
        "dt":"Document Title",
        "cd":"Screen Name",
        "linkid":"Link ID",
        "an":"Application Name",
        "aid":"Application ID",
        "av":"Application Version",
        "aiid":"Application Installer ID",
        "ec":"Event Category",
        "ea":"Event Action",
        "el":"Event Label",
        "ev":"Event Value",
        "ti":"Transaction ID",
        "ta":"Transaction Affiliation",
        "tr":"Transaction Revenue",
        "ts":"Transaction Shipping",
        "tt":"Transaction Tax",
        "in":"Item Name",
        "ip":"Item Price",
        "iq":"Item Quantity",
        "ic":"Item Code",
        "iv":"Item Category",
        "cu":"Currency Code",
        "ti":"Transaction ID",
        "ta":"Affiliation",
        "tr":"Revenue",
        "tt":"Tax",
        "ts":"Shipping",
        "tcc":"Coupon Code",
        "pal":"Product Action List",
        "cos":"Checkout Step",
        "col":"Checkout Step Option",
        "promoa":"Promotion Action",
        "sn":"Social Network",
        "sa":"Social Action",
        "st":"Social Action Target",
        "utc":"User timing category",
        "utv":"User timing variable name",
        "utt":"User timing time",
        "utl":"User timing label",
        "plt":"Page Load Time",
        "dns":"DNS Time",
        "pdt":"Page Download Time",
        "rrt":"Redirect Response Time",
        "tcp":"TCP Connect Time",
        "srt":"Server Response Time",
        "dit":"DOM Interactive Time",
        "clt":"Content Load Time",
        "exd":"Exception Description",
        "exf":"Is Exception Fatal?",
        "xid":"Experiment ID",
        "xvar":"Experiment Variant",
        "pa": "Product Action",
    }
    pattern_map_table = {
        r"pr(\d+)id": "Product %s SKU",
        r"pr(\d+)nm": "Product %s Name",
        r"pr(\d+)br": "Product %s Brand",
        r"pr(\d+)ca": "Product %s Category",
        r"pr(\d+)va": "Product %s Variant",
        r"pr(\d+)pr": "Product %s Price",
        r"pr(\d+)qt": "Product %s Quantity",
        r"pr(\d+)cc": "Product %s Coupon Code",
        r"pr(\d+)ps": "Product %s Position",
        r"pr(\d+)cd(\d+)": "Product %s Custom Dimension %s",
        r"pr(\d+)cm(\d+)": "Product %s Custom Metric %s",
        r"il(\d+)nm": "Impression %s Product List Name",
        r"il(\d+)pi(\d+)id": "Impression %s Product %s SKU",
        r"il(\d+)pi(\d+)nm": "Impression %s Product %s Name",
        r"il(\d+)pi(\d+)br": "Impression %s Product %s Brand",
        r"il(\d+)pi(\d+)ca": "Impression %s Product %s Category",
        r"il(\d+)pi(\d+)va": "Impression %s Product %s Variant",
        r"il(\d+)pi(\d+)ps": "Impression %s Product %s Position",
        r"il(\d+)pi(\d+)pr": "Impression %s Product %s Price",
        r"il(\d+)pi(\d+)cd(\d+)": "Impression %s Product %s Custom Dimension %s",
        r"il(\d+)pi(\d+)cm(\d+)": "Impression %s Product %s Custom Metric %s",
        r"promo(\d+)id": "Promotion %s ID",
        r"promo(\d+)nm": "Promotion %s Name",
        r"promo(\d+)cr": "Promotion %s Creative",
        r"promo(\d+)ps": "Promotion %s Position",
        r"cd(\d+)": "Custom Dimension %s",
        r"cm(\d+)": "Custom Metric %s",
    }
    result_dict = dict()
    for k, v in params.items():
        if k in map_table:
            result_dict[map_table[k]] = v
            continue
        for kp, vp in pattern_map_table.items():
            pattern_match = re.match(kp, k)
            if not pattern_match:
                continue
            result_dict[vp % pattern_match.groups()] = v
            break
    return result_dict

@functools.lru_cache()
def is_ios():
    try:
        proc = subprocess.Popen(['idevice_id', '-l'], env=os.environ, stdout=subprocess.PIPE)
    except FileNotFoundError:
        return False
    output, error = proc.communicate()
    output = output.splitlines()
    if len(output) > 0:
        return True
    else:
        return False

@functools.lru_cache()
def is_android():
    try:
        proc = subprocess.Popen(['adb', 'devices'], env=os.environ, stdout=subprocess.PIPE)
    except FileNotFoundError:
        return False
    output, error = proc.communicate()
    output = output.splitlines()
    if len(output) > 2:
        return True
    else:
        return False
