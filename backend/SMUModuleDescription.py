import csv
import requests
import pandas as pd
from selenium import webdriver #have to pip install selenium
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException
import re
import pandas as pd
from pathlib import Path
import nlp

path = Path(__file__).parent

filename = path / "smuMods.csv"

# extract the rows of the file
rows = []
with open(filename, "r") as file:
    csvreader = csv.reader(file) # using csv.reader object to read the CSV file
    header = next(csvreader)
    for row in csvreader:
        rows.append(row)

SMUModuleCodes = []
for row in rows:
    if len(row) > 1:
        SMUModuleCodes.append(row[0])
    if len(row) == 4:
        if "/" in row[-1]:
            SMUModuleCodes.extend(row[-1].split("/"))
        else:
            SMUModuleCodes.append(row[-1])

SMUModules = dict()

import csv, time, re
from selenium import webdriver
from selenium.webdriver.common.by import By

timeoutDuration = 10

driver = webdriver.Chrome()
for i in range(len(SMUModuleCodes)): # iterating through the list of module codea
    # SMU url
    url = "https://publiceservices.smu.edu.sg/psc/ps/EMPLOYEE/HRMS/c/SIS_CR.SIS_CLASS_SEARCH.GBL"
    driver.get(url) # navigate to URL
    driver.find_element(By.XPATH, '//*[@tabindex="71"]').click()
    
    firstLetter = SMUModuleCodes[i][0]

    # clicking on the link based on the starting alphabet
    if firstLetter != 'A':
        element_id = f'SSR_CLSRCH_WRK2_SSR_ALPHANUM_{firstLetter}'
        first_letter_header = driver.find_element(By.ID, element_id)
        WebDriverWait(driver, timeoutDuration).until(
            EC.staleness_of(first_letter_header)
        )
        first_letter_header = driver.find_element(By.ID, element_id)
        first_letter_header.click()

    # clicking on the link based on the prefix and catalogue number
    prefix = re.sub(r'\d', '', SMUModuleCodes[i])

    catNumber = re.sub(r'[^0-9]', '', SMUModuleCodes[i])

    if prefix == "IS":
        wait = WebDriverWait(driver, timeoutDuration)
        titleElement = wait.until(EC.presence_of_element_located((By.XPATH, '//div[contains(text(), "IS - Information Systems")]')))
    elif prefix == "CS":
        wait = WebDriverWait(driver, timeoutDuration)
        titleElement = wait.until(EC.presence_of_element_located((By.XPATH, '//div[contains(text(), "CS - Computer Science")]')))
    else:
        wait = WebDriverWait(driver, timeoutDuration)
        titleElement = wait.until(EC.presence_of_element_located((By.XPATH, f'//div[contains(text(), "{prefix}")]')))

    mainBodyElement = titleElement.find_element(By.XPATH, './ancestor::tbody[1]') # from the element of the title, locate the main tbody

    catNumberElement = mainBodyElement.find_element(By.XPATH, f'.//span[contains(text(), "{catNumber}")]')
    rowElement = catNumberElement.find_element(By.XPATH, f'./ancestor::tr[1]') # locate the element of the row

    moduleNameElement = rowElement.find_element(By.XPATH, './/a[contains(@id, "DERIVED_CLSRCH")]')
    moduleName = moduleNameElement.text
    moduleNameElement.click()

    moduleDescriptionElement = WebDriverWait(driver, timeoutDuration).until(
        EC.presence_of_element_located((By.ID, 'SSR_CRSE_OFF_VW_DESCRLONG$0'))
    )
    moduleDescription = moduleDescriptionElement.text

    # adding the module description into a dictionary
    SMUModules[SMUModuleCodes[i]] = [moduleName, moduleDescription]

#================================================================================
# extracting key concepts from module description

tokenised = []
for module_code, [module_name, module_description] in SMUModules.items():
    lemma = nlp.lemmatize(module_description)
    tokenized_description = nlp.tokenize(lemma, ngram_range=(1, 2))
    # print(tokenized_description)
    tokenised.append(tokenized_description)

# extracting keywords associated to each module
glossary_list = nlp.get_glossary_list()
keywords = []
for i in range(len(tokenised)):
    words = []
    for j in range(len(tokenised[i])):
        if tokenised[i][j] in glossary_list and tokenised[i][j] not in words:
            words.append(tokenised[i][j])
    keywords.append(words)
keywords = [', '.join(inner_list) for inner_list in keywords]

# print(keywords) # a nested list
# print(len(keywords))

if len(keywords) == len(SMUModules):
    module_code = list(SMUModules.keys())
    for i in range(len(SMUModules)):
        key_concepts = keywords[i]
        SMUModules[module_code[i]].append(key_concepts)
else:
    print(f'Lists have different lengths')
# print(SMUModules)

#================================================================================
# Writing to the CSV file

filename = "smu.csv"
header = ["module_code", "module_name", "module_description", "key_concepts"]
with open(filename, 'w') as csv_file:
    writer = csv.writer(csv_file)
    # Write the header
    writer.writerow(header)
    # Write the dictionary values
    for code, [name, desc, keywords] in SMUModules.items():
        writer.writerow([code, name, desc, keywords])