import requests
from bs4 import BeautifulSoup, NavigableString
import pandas as pd
from selenium import webdriver
import time
import csv
NusDsaDescriptionList = []
NusDsaTitleList = []
NusDseDescriptionList = []
NusDseTitleList = []
NusDsaMainMods = ['DSA1101','CS1010S','CS2040','DSA2101','DSA2102','MA2001','MA2002','MA2311','ST2131','ST2132','CS3244','DSA3101','DSA3102','ST3131','DSE4211','DSE4212','DSA4288']
NusDsaORSpecMods = ['MA3236','MA3252','MA3227','MA3238','ST3236','MA4230','MA4251','ST4238','MA4260','MA4268','MA4270','DSA4288M']
NusDsaSMSpecMods = ['ST3232','ST3239','ST3247','ST3248','ST4231','ST4234','ST4248','ST4250','ST4253','DSA4288S']
NusDsaModsCode = NusDsaMainMods+NusDsaORSpecMods+NusDsaSMSpecMods
NusDseModsCode = ['DSE1101','CS1010S','EC1101E','CS2040','DSA2101','DSA2102','EC2101','EC2102','MA2001','MA2002','MA2311','MA2104','ST2131','MA2116','ST2132','DSA3102','DSE3101','EC3101','EC3102','EC3304','ST3131','DSE4101','EC4305','DSA4264','DSA4265','DSE4201','DSE4211','QF4211','DSE4212','QF4212','DSE4231','EC4308']
baseurl = "https://nusmods.com/courses/"
NusDsaModsURL = [baseurl+x for x in NusDsaModsCode]
NusDseModsURL = [baseurl+x for x in NusDseModsCode]
for x in range(len(NusDsaModsCode)):
    url = NusDsaModsURL[x]
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(10)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.findAll('div',attrs={"class":"col-sm-8"})
    ls = []
    for i in table:
        ls.append(i.find('p').text)
    table = soup.find('h1',attrs={"class":"kbFQ8zbG"}).contents[-1]
    NusDsaDescriptionList.append(''.join(ls))
    NusDsaTitleList.append(str(table))
for x in range(len(NusDseModsCode)):
    url = NusDseModsURL[x]
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(10)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.findAll('div',attrs={"class":"col-sm-8"})
    ls = []
    for i in table:
        ls.append(i.find('p').text)
    table = soup.find('h1',attrs={"class":"kbFQ8zbG"}).contents[-1]
    NusDseDescriptionList.append(''.join(ls))
    NusDseTitleList.append(str(table))
a = NusDsaModsCode + NusDseModsCode
b = NusDsaTitleList + NusDseTitleList
c = NusDsaDescriptionList + NusDseDescriptionList
d = ['DSA'] * len(NusDsaModsCode) + ['DSE'] * len(NusDseModsCode)
data = {'NUS Module Code': a, 'NUS Module Title': b, 'NUS Module Description': c, 'NUS DSA/DSE': d}
df = pd.DataFrame.from_dict(data)
df.to_csv('NusMods.csv', index= False)



