# Python imports
import sys
import datetime
from html import unescape
from difflib import SequenceMatcher
from re import search, sub, findall
from time import strftime
from csv import reader
from typing import List, Tuple, Dict, BinaryIO
from time import sleep
from math import ceil
from os.path import basename, exists, getsize
import traceback
import smtplib
import urllib.request as urllib2
import os
import json

# Vendor imports
import requests
import pymysql
from habanero import Crossref
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.proxy import Proxy, ProxyType
from urllib.parse import quote_plus

# Crosscholar modules imports
from urlman import URLFactory, ScholarURLType,get_proxy
from scholarbase import Work, User
from timer import Requestmeter
from config import Configuration
import xlrd

import threading
import time
import random
from base64 import b64encode

if __name__ == "__main__":
    # Start request ratio counting

    #try:
    index = 1

    # mysql connection
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='',
                                 db='google_scholar',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    cursor = connection.cursor()
    connection.begin()

    scholar_info = xlrd.open_workbook('UNI-ID-Name-Site.xlsx')
    worksheet = scholar_info.sheet_by_index(0)
    while worksheet.cell(index, 3).value != xlrd.empty_cell.value:
       kw = str(worksheet.cell(index, 3).value)
       if kw.split('.')[0] == "www" or kw.split('.')[0] == "http:www" or kw.split('.')[0] == "https:www":
           kw = kw.lstrip(kw.split('.')[0]+'.')
       print("index={0}, keyword={1}".format(index, kw))

       uni_id = str(worksheet.cell(index, 0).value)
       uni_name = str(worksheet.cell(index, 1).value)
       uni_url = str(worksheet.cell(index, 3).value)
       photo_folder = str(worksheet.cell(index, 4).value)

       # Check exist page number
       cursor.execute("select COUNT(academic_id) as max_id, SUM(n_citations) as sum_citations from academic"
                      "  where uni_id = %s",
                      (uni_id,))
       row = cursor.fetchone()
       if row and row.get('max_id') and row.get('sum_citations'):
           max_id = row.get('max_id')
           sum_citations = row.get('sum_citations')
           cursor.execute("insert into universities (uni_id, uni_name, no_academics,"
                          " no_citations, uni_google_url)"
                          " values(%s, %s, %s, %s, %s)",
                          (uni_id, uni_name, max_id, sum_citations, uni_url))
       else:
           cursor.execute("insert into universities (uni_id, uni_name, no_academics,"
                          " no_citations, uni_google_url)"
                          " values(%s, %s, %s, %s, %s)",
                          (uni_id, uni_name, 0, 0, uni_url))
       connection.commit()

       index += 1
           
        #download_works(config.download_dir + "users_batch_181009_021134.csv", (21,40))
        #notify("Batch finished", "The batch finished successfully!")
    # except Exception as e:
    #     print("Error message: {0}".format(str(e)))
    # finally:
    #     connection.close()
