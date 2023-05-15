import re
import os
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd
import pandas as pd

plist = "I:\\hdmxpats\\grr\\MsioSerdes\\RevTGA0.5\\p2\\plb\\ux4_serdes.plist"


spfs_path = "C:\\Users\\anandare\\OneDrive - Intel Corporation\\Documents\\DOCs\\GNRD\\UXPHY\\proliferation_from_grr\\spf3"

spf_list = [os.path.join(spfs_path,x) for x in os.listdir(spfs_path)]
flush = False
cycle = False
options = webdriver.ChromeOptions()
options.add_experimental_option('debuggerAddress', 'localhost:9014')
driver = webdriver.Chrome("C:/Users/anandare/Downloads/chromedriver_win32 (1)/chromedriver",options=options)
# driver.get("http://iapp257.iil.intel.com:4887/soconline/app/search.cgi?searchString=40304&DoSearch=DoSearch")
# WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//a[@onclick]"))).click()
# html = driver.page_source
# tables = pd.read_html(html) 



for spf_path in spf_list:
    spf_name = os.path.basename(spf_path)
    spf_file = open(spf_path,'r')
    spf_str = spf_file.readlines()

    for spf_line in spf_str:
        match_tap = re.match('focus_tap(.*?);',spf_line)
        if match_tap:
            tap = match_tap.group(1)
        match_label = re.match('label (.*?);',spf_line)
        if match_label:
            label = match_label.group(1)     
        match_addrs0 = re.match('set\s*?REG_ACC\s*?->\s*?ADDR\s*?=(.*?);',spf_line)
        if match_addrs0:
            addrs0 = match_addrs0.group(1)
            addrs0 = addrs0.replace("'h","").replace(" ", "")
            addrs0 = int(addrs0, base=16)
            if addrs0 == 0:
                continue
        match_addrs = re.match('set\s*?REG_ACC\s*?->\s*?ADDR\s*?=(.*?);',spf_line)
        if match_addrs:
            addrs = match_addrs.group(1)    
        match_rdwr = re.match('set\s*?REG_ACC\s*?->\s*?RD1_WR0\s*?=(.*?);',spf_line)
        if match_rdwr:
            rdwr = match_rdwr.group(1)
            rdwr = rdwr.replace("'h","").replace(" ", "")
            if rdwr == '0':
                rdwr = "Read"
            else:
                rdwr = "Write"
        match_data = re.match('set\s*?REG_ACC\s*?->\s*?DATA\s*?=(.*?);',spf_line)
        if match_data:
            data = match_data.group(1)
        match_flush = re.match('flush;',spf_line)
        if match_flush:
            flush = True

        match_cycle = re.match('cycle \d*;',spf_line)
        if match_cycle:
            cycle = True

        if cycle:
            addrs = addrs.replace("'h","").replace(" ", "")
            print(spf_name,tap,label,addrs,rdwr,data)
            # driver.get("http://iapp257.iil.intel.com:4887/soconline/app/search.cgi?searchString=%s&DoSearch=DoSearch"%addrs)
            # WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//a[@onclick]"))).click()
            # html = driver.page_source
            # tables = pd.read_html(html) 
            # print(tables[4])
            cycle = False


        
# Walking plist########################################################
# file = open(plist,'r')

# lines = file.readlines()

# for line in lines:
#     match_patlist = re.match('GlobalPList(.*?)\[',line)
#     match_pat = re.match('.*?Pat.*?_xxx_(.*?);',line)
#     # print(line)
#     if match_patlist:
#         print("Patlist: %s"%match_patlist.group(1))
#     if match_pat:
#         print("Pattern: %s"%match_pat.group(1))
######################################################################