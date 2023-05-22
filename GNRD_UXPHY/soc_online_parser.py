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
from tqdm import tqdm
plist = "I:\\hdmxpats\\grr\\MsioSerdes\\RevTGA0.5\\p2\\plb\\ux4_serdes.plist"


# spfs_path = "C:\\Users\\anandare\\OneDrive - Intel Corporation\\Documents\\DOCs\\GNRD\\UXPHY\\proliferation_from_grr\\spf3"
# temp_excel= open("C:\\Users\\anandare\\OneDrive - Intel Corporation\\Documents\\DOCs\\GNRD\\UXPHY\\proliferation_from_grr\\spf3\\temp.csv","w")
# temp_excel.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n"%('spf_name','tap','label','addrs','rdwr','data','register','binary_data','hex_data','description','reset'))
# spf_list = [os.path.join(spfs_path,x) for x in os.listdir(spfs_path)]
# flush = False
# cycle = False
# options = webdriver.ChromeOptions()
# options.add_experimental_option('debuggerAddress', 'localhost:9014')
# driver = webdriver.Chrome("C:/Users/anandare/Downloads/chromedriver_win32 (1)/chromedriver",options=options)

# def return_field(data,html):

#     tables = pd.read_html(html) # Returns list of all tables on page
#     table = tables[4]

#     register = re.findall("<font class=\"ClearFormHeaderFont\">Register: (.*?)</font><br>",html)[0]

#     df1 = table.iloc[0:]

#     df1 = df1.to_dict()

#     field = []
#     location = []
#     reset_val = []
#     desc = []
#     for key,val in df1.items():
#         for ind,row in val.items():
#             if ind == 0:
#                 continue
#             else:
#                 if key == 0:
#                     field.append(row)
#                 if key == 1:
#                     location.append(row)
#                 if key == 2:
#                     reset_val.append(row)
#                 if key == 4:
#                     desc.append(row)
#     data=data.replace("'h","")
#     data_bin = bin(int(data, 16))[2:].zfill(32)
#     data_bin = data_bin[::-1]
#     binary_data="="
#     hex_data="="
#     description="="
#     reset="="
#     for x in range(len(field)):
#         if ".." in location[x]:
#             loc = location[x].split("..")
#             field_data = data_bin[int(loc[0]):int(loc[1])+1]
#         else:
#             loc = int(location[x])
#             field_data = data_bin[loc]
#         binary_data += "\"%s = %s\"&CHAR(10)&"%(field[x],field_data[::-1])
#         hex_data += "\"%s = %s\"&CHAR(10)&"%(field[x],hex(int(field_data[::-1],2)))
#         description += "\"%s = %s\"&CHAR(10)&"%(field[x],desc[x])
#         reset += "\"%s = %s\"&CHAR(10)&"%(field[x],reset_val[x])
#     return([register,binary_data[:-1],hex_data[:-1],description[:-1],reset[:-1]])

# spfs=[]
# for spf_path in tqdm(spf_list):
#     spf_name = os.path.basename(spf_path)
#     if not(spf_name.endswith('.spf')):
#         continue
#     spf_file = open(spf_path,'r')
#     spf_str = spf_file.readlines()

#     for spf_line in spf_str:
#         match_tap = re.match('focus_tap(.*?);',spf_line)
#         if match_tap:
#             tap = match_tap.group(1)
#         match_label = re.match('label (.*?);',spf_line)
#         if match_label:
#             label = match_label.group(1)     
#         match_addrs0 = re.match('set\s*?REG_ACC\s*?->\s*?ADDR\s*?=(.*?);',spf_line)
#         if match_addrs0:
#             addrs0 = match_addrs0.group(1)
#             addrs0 = addrs0.replace("'h","").replace(" ", "")
#             addrs0 = int(addrs0, base=16)
#             if addrs0 == 0:
#                 continue
#         match_addrs = re.match('set\s*?REG_ACC\s*?->\s*?ADDR\s*?=(.*?);',spf_line)
#         if match_addrs:
#             addrs = match_addrs.group(1)    
#         match_rdwr = re.match('set\s*?REG_ACC\s*?->\s*?RD1_WR0\s*?=(.*?);',spf_line)
#         if match_rdwr:
#             rdwr = match_rdwr.group(1)
#             rdwr = rdwr.replace("'h","").replace(" ", "")
#             if rdwr == '0':
#                 rdwr = "Read"
#             else:
#                 rdwr = "Write"
#         match_data = re.match('set\s*?REG_ACC\s*?->\s*?DATA\s*?=(.*?);',spf_line)
#         if match_data:
#             data = match_data.group(1)
#         match_flush = re.match('flush;',spf_line)
#         if match_flush:
#             flush = True

#         match_cycle = re.match('cycle \d*;',spf_line)
#         if match_cycle:
#             cycle = True

#         if cycle:
#             addrs2 = addrs.replace("'h","").replace(" ", "")
            
#             driver.get("http://iapp257.iil.intel.com:4887/soconline/app/search.cgi?searchString=%s&DoSearch=DoSearch"%addrs2)
#             WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[@onclick]"))).click()
#             WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[@onmouseover]"))).click()
#             html = driver.page_source
#             register,binary_data,hex_data,description,reset = return_field(data,html)[0],return_field(data,html)[1],return_field(data,html)[2],return_field(data,html)[3],return_field(data,html)[4]
#             temp_excel.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n"%(spf_name,tap,label,addrs,rdwr,data,register,binary_data,hex_data,description,reset))

#             cycle = False
# temp_excel.close

        
# Walking plist########################################################
file = open("C:/Users/anandare/source/repos/data-automations/data-automations/GNRD_UXPHY/tuple.txt",'r')
lines = file.readlines()
pat_hash={}
for line in lines:
    match_pato = re.match('d(\d{7})[A-Z,a-z](\d{7}).*?_xxx_(.*?)$',line)
    if match_pato:
        tuples= match_pato.group(1)
        tid= match_pato.group(2)
        pattern_name= match_pato.group(3)
        pat_hash[pattern_name] = tid
        # print(tuples,tid,pattern_name)
file = open(plist,'r')

lines = file.readlines()
tids=""
aaa=False
for line in lines:
    match_patlist = re.match('GlobalPList(.*?)\[',line)
    match_pat = re.match('.*?Pat.*?_xxx_(.*?);',line)
    match_end = re.match('\}',line)

    if match_patlist:
        patlist = match_patlist.group(1).replace(" ","")
        first = "level1 = level0.add(Plb(\"%s\", vrev=\'vrevDA0P\', mode=\'IOdies\',preburstplist=\'reset_Msio_hvm400_IOdie_ResetIO_SIO_Serdes\',postburstplist=\'end_gracefully_Msio_hvm400_IOdie_ResetIO_SIO_Serdes\'))"%patlist
        # print(patlist)
        # print(first)
        
    if match_pat:
        pattern = match_pat.group(1)

        if "_q0" in pattern:
            if "jtag_iso_config_q0" in pattern:
                # print(pattern)
                aaa=True
            pattern = pattern.replace("_q0","_q0n0")
            if aaa:
                # print(pattern)
                aaa=False
            if pattern in pat_hash:
                tids += pat_hash[pattern] + ','
            else:
                print(pattern)
        if "_q1" in pattern:
            pattern = pattern.replace("_q1","_q0n1")
            if pattern in pat_hash:
                tids += pat_hash[pattern] + ','
            else:
                print(pattern)
        if "_bc" in pattern:
            if pattern in pat_hash:
                tids += pat_hash[pattern] + ','
            else:
                print(pattern)

    if match_end:
        if tids =="":
            # print(patlist)
            pass
        else:
            # print(first)
            # print("levelP = level1.add(Pats(Tids(%s)))"%tids[:-1])
            pass
        tids=""

        # print("Pattern: %s"%match_pat.group(1))
######################################################################