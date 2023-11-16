from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import time
import nlp
import csv

############################################### MODULE SCRAPING ###############################################

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
    time.sleep(2)
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
    time.sleep(2)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.findAll('div',attrs={"class":"col-sm-8"})
    ls = []
    for i in table:
        ls.append(i.find('p').text)
    table = soup.find('h1',attrs={"class":"kbFQ8zbG"}).contents[-1]
    NusDseDescriptionList.append(''.join(ls))
    NusDseTitleList.append(str(table))

dsa_data = {'module_code': NusDsaModsCode, 'module_name': NusDsaTitleList, 'module_description': NusDsaDescriptionList}
dsa_df = pd.DataFrame.from_dict(dsa_data)

dse_data = {'module_code': NusDseModsCode, 'module_name': NusDseTitleList, 'module_description': NusDseDescriptionList}
dse_df = pd.DataFrame.from_dict(dse_data)

############################################### KEY CONCEPTS ###############################################

# NUS DSA
glossary_list = nlp.get_glossary_list()
tokenised = []
for index, row in dsa_df.iterrows():
    lemma = nlp.lemmatize(row['module_description'])
    tokenized_description = nlp.tokenize(lemma, ngram_range=(1, 2))
    tokenised.append(tokenized_description)

# extracting keywords associated to each module
keywords = []
for i in range(len(tokenised)):
    words = []
    for j in range(len(tokenised[i])):
        if tokenised[i][j] in glossary_list and tokenised[i][j] not in words:
            words.append(tokenised[i][j])
    keywords.append(words)
keywords = [', '.join(inner_list) for inner_list in keywords]
dsa_df['key_concepts'] = keywords

# NUS DSE
glossary_list = nlp.get_glossary_list()
tokenised = []
for index, row in dse_df.iterrows():
    lemma = nlp.lemmatize(row['module_description'])
    tokenized_description = nlp.tokenize(lemma, ngram_range=(1, 2))
    tokenised.append(tokenized_description)

# extracting keywords associated to each module
keywords = []
for i in range(len(tokenised)):
    words = []
    for j in range(len(tokenised[i])):
        if tokenised[i][j] in glossary_list and tokenised[i][j] not in words:
            words.append(tokenised[i][j])
    keywords.append(words)
keywords = [', '.join(inner_list) for inner_list in keywords]
dse_df['key_concepts'] = keywords

############################################### SENTIMENT ANALYSIS #########################################

# load the website and data
driver = webdriver.Chrome()
sentiment = SentimentIntensityAnalyzer()
nusDsaModuleScores = []
dsa_mods = dsa_df['module_code']
nusDseModuleScores = []
dse_mods = dse_df['module_code']

# extracting reviews and getting sentiment score for DSA modules
for mod_name in dsa_mods:
    print(mod_name)
    baseurl = "https://nusmods.com/courses/"
    nusmods_url = baseurl+mod_name
    driver.get(nusmods_url)
    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[src^='https://disqus']")))
    url2 = element.get_attribute("src")
    driver.get(url2)
    wait.until(EC.presence_of_element_located((By.ID, "email-signup")))
    time.sleep(2)
    reviews = driver.find_elements(By.XPATH, "//div[@class='post-message ']")
    all_reviews = ''
    for i in range(len(reviews)):
        pElements = reviews[i].find_elements(By.TAG_NAME, "p")
        review = ""
        for p in pElements:
            text = p.text
            if text!='':
                review = review + " " + text
        all_reviews = all_reviews + review.strip()
    nusDsaModuleScores.append(sentiment.polarity_scores(all_reviews)['compound'])
dsa_df['module_score'] = nusDsaModuleScores
dsa_df.to_csv('nus_dsa.csv', index = False)

# extracting reviews and getting sentiment score for DSE modules
for mod_name in dse_mods:
    baseurl = "https://nusmods.com/courses/"
    nusmods_url = baseurl+mod_name
    driver.get(nusmods_url)
    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[src^='https://disqus']")))
    url2 = element.get_attribute("src")
    driver.get(url2)
    wait.until(EC.presence_of_element_located((By.ID, "email-signup")))
    time.sleep(2)
    reviews = driver.find_elements(By.XPATH, "//div[@class='post-message ']")
    all_reviews = ''
    for i in range(len(reviews)):
        pElements = reviews[i].find_elements(By.TAG_NAME, "p")
        review = ""
        for p in pElements:
            text = p.text
            if text!='':
                review = review + " " + text
        all_reviews = all_reviews + review.strip()
    nusDseModuleScores.append(sentiment.polarity_scores(all_reviews)['compound'])
dse_df['module_score'] = nusDseModuleScores
dse_df.to_csv('nus_dse.csv', index = False)
