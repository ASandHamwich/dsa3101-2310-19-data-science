# import the necessary
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import nlp

############################################### MODULE SCRAPING ###############################################

course_options = []
for i in range(1,5):
    year = f"option[@value='DSAI;;{i};F']"
    course_options.append(year)

# load the website
driver = webdriver.Chrome()
CCode_list = []
CName_list = []
CDesc_list = []
Preqs_list = []

for i in range(len(course_options)):
    # select course name from dropdown box and click
    driver.get("https://wis.ntu.edu.sg/webexe/owa/aus_subj_cont.main")
    driver.find_element(By.XPATH, f"//select[@name='r_course_yr']/{course_options[i]}").click()
    driver.find_element(By.XPATH, "//input[@value='Load Content of Course(s)']").click()

    # course codes
    driver.switch_to.frame("subjects")

    courses = driver.find_elements(By.TAG_NAME, "table")

    for course in courses:
        rows = course.find_elements(By.TAG_NAME, "tr")
        course_code = rows[0].find_element(By.XPATH, "td[1]").find_element(By.TAG_NAME, "font").text
        CCode_list.append(course_code.strip())

        CName_list.append(rows[0].find_element(By.XPATH, "td[2]").find_element(By.TAG_NAME, "font").text.strip())

        CDesc_list.append(rows[-1].find_element(By.XPATH, "td[1]").find_element(By.TAG_NAME, "font").text.strip())

        prereqs = ""
        if len(rows) > 1 and rows[1].find_element(By.XPATH, "td[1]").find_element(By.TAG_NAME, "font").text.lower() == "prerequisite:":
            for row in rows[1:]:
                first_word = row.find_element(By.XPATH, "td[1]").find_element(By.TAG_NAME, "font").text.lower()
                if first_word in ['prerequisite:', '']:
                    prereqs += row.find_element(By.XPATH, "td[2]").find_element(By.TAG_NAME, "font").text + ' '
                else:
                    break
        Preqs_list.append(prereqs.strip())

driver.quit()

# Initialize an empty list to store the merged items
preqs_clean = []

valid_module_code_format = re.compile("[A-Z]{2}[0-9]{4}|^OR$|^&$")
for prereq in Preqs_list:
    preqs_clean.append(" ".join(list(map(lambda x : valid_module_code_format.findall(x)[0] if valid_module_code_format.match(x) else '', prereq.split()))).strip())

# writing lists into a csv file
data = {'module_code': CCode_list, 'module_name': CName_list, 'module_description': CDesc_list, 'prerequisites': preqs_clean}
df = pd.DataFrame(data)
df = df.drop_duplicates(subset='module_code')

# removing redundant non-DSA modules
df['module_description'].replace('', 'Module Description unavailable. Please google for more info :)', inplace = True)
relevant = ['CS', 'CZ', 'MH', 'SC']
df = df[df['module_code'].str[:2].isin(relevant)]

############################################### KEY CONCEPTS ###############################################

glossary_list = nlp.get_glossary_list()
tokenised = []
for index, row in df.iterrows():
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
df['key_concepts'] = keywords

############################################### REVIEWS + SENTIMENTS ###############################################

#adding reviews and sentiment score columns
sentiment = SentimentIntensityAnalyzer()
driver = webdriver.Chrome()
ntuModuleCodes = df['module_code']
url = "https://www.nanyangmods.com/modules/"
ntuModuleReviews = []
ntuModuleScores = []
for moduleCode in ntuModuleCodes:
    mod_url = f'{url}{moduleCode}'
    driver.get(mod_url)
    allBodyElements = driver.find_elements(By.CLASS_NAME, "rx_body")
    allReviews = ''
    for bodyElements in allBodyElements:
        pElements = bodyElements.find_elements(By.TAG_NAME, "p")
        review = ""
        for p in pElements:
            text = p.text
            review = review + " " + text
        allReviews = allReviews + review.strip()
    ntuModuleReviews.append(allReviews)
    ntuModuleScores.append(sentiment.polarity_scores(allReviews)['compound'])
df['reviews'] = ntuModuleReviews
df['sentiment_rating'] = ntuModuleScores

csv_file = "ntu.csv"
df.to_csv(csv_file, index=False)
