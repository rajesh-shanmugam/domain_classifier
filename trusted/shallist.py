#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  8 13:37:01 2017

@author: rajesh.shanmugam
"""

directory = 'BL/' 

from os import walk
import pandas as pd

categories = pd.DataFrame()
for (dirpath, dirnames, filenames) in walk(directory):
    if(len(dirnames) == 0):
        category = dirpath[len(directory):]
        print(category)

        filepath = dirpath + "/" + "domains"
        with open(filepath) as f:
            content = f.readlines()
        content = [x.strip() for x in content]
        content = pd.DataFrame(content)
        content['category'] = category
        content.columns = ['domain', 'category']
        categories = pd.concat([categories, content])
        
        #print(content)
        
categories

from pyhive import hive
conn = hive.Connection(host="YOUR_HIVE_HOST", port="PORT", username="YOU")

import pandas as pd
df = pd.read_sql("SELECT cool_stuff FROM hive_table", conn)

