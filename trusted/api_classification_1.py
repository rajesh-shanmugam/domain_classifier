import time
import urllib2
import requests
import os
import sys
import json

INPUT_FILE = "sample_in.csv"
URL_COLUMN_NAME = "url"
URL_CATEGORY_COLUMN_NAME = "url_class"
CLASSIFIER_API = "http://www.trustedsource.org/en/feedback/url"
INPUT_URLS = '/mnt/sharethis/filtered/dt=20170501/part-00000-98f2e575-d6ea-4cba-9da3-68064fc483fe.json'

def simplify_domain(my_str):
    """
    Get the host name. Strip http, slashes, www etc.
    """
    domain = my_str.strip()
    domain = domain.replace("http://","")
    domain = domain.replace("https://","")
    domain = domain.replace("www.","")
    domain = domain.split("/")[0].strip()
    return domain

def get_unique_domains():
    domains = set()
    with open(INPUT_URLS) as f:
        content = f.read().splitlines()
    for domain in content:
        b =json.loads(domain)
        domains.add(simplify_domain(b['url']))
    return(list(domains))

def find_with_pattern(my_str, startPattern, endPattern):
    """
    Find the string that starts with <startPattern> and ends with <endPattern> in the orginal string <my_str>.
    Args:
        + my_str: orginal string.
        + startPattern: 
        + endPattern: 
    Returns:
        + The found string,
        + and the remained part of the orginal string.
    """
    x = my_str.find(startPattern)
    if x==-1:
        return "",my_str
    my_str = my_str[x + len(startPattern):]
    y = my_str.find(endPattern)
    if y==-1:
        return "",my_str
    return my_str[:y], my_str[y+len(endPattern):]

CATEGORY_URL = {}
domains = get_unique_domains()

def get_output_for_100_url_from_trusted_source(domains):
    #for domain in domains:
        payload = {'sid': '3A37245BBF29CBE25DFE5EAC06AB636A', 'action': 'checklist', 'product':'01-ts','file_upload':'/Users/rajesh.shanmugam/Documents/GitHub/domain_classifier/trusted/test.txt'}
        try:
            r = requests.post(CLASSIFIER_API, data=payload)
            data =  r.text
        except:
            print "CONNECTION ERROR"
            continue

        categoryDiv,tmp = find_with_pattern(data,'<b>Categorization</b>','</table>')
        items = categoryDiv.split('<td align="left" valign="top" nowrap="nowrap">')
        if len (items)>=3:
            category = items[3]
            if category.find("<br")>-1:
                category = category[:category.find("<br")]
            if category.find("- ")==0:
                category = category[2:]
            if category.find("</td>")>-1:
                category = category[:category.find("</td>")]
            if len(category)==0:
                category = "UNKNOWN"
            else:
                category = "UNKNOWN"
            print category
            CATEGORY_URL[domain] = category
    return CATEGORY_URL

categories = get_output_for_100_url_from_trusted_source(domains)
