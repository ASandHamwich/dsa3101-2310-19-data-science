# webscrapping reviews from nus, ntu and smu mods
import pandas as pd
from selenium import webdriver #have to pip install selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

nus_df = pd.read_csv("NusMods.csv")
ntu_df = pd.read_csv("ntu.csv")
smu_df = pd.read_csv("smu.csv")

driver = webdriver.Chrome()
ntuModuleCodes = ntu_df['Course Code']
url = "https://www.nanyangmods.com/modules/"

ntuModuleReviews = {}
for moduleCode in ntuModuleCodes:
    mod_url = f'{url}{moduleCode}'
    driver.get(mod_url)
    allBodyElements = driver.find_elements(By.CLASS_NAME, "rx_body")
    allReviews = []
    for bodyElements in allBodyElements:
        pElements = bodyElements.find_elements(By.TAG_NAME, "p")
        review = ""
        for p in pElements:
            text = p.text
            review = review + " " + text
        allReviews.append(review.strip())
    ntuModuleReviews[moduleCode] = allReviews
print(ntuModuleReviews)