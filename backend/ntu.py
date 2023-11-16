# import the necessary
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import re
# from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
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
        CCode_list.append(course_code)

        CName_list.append(rows[0].find_element(By.XPATH, "td[2]").find_element(By.TAG_NAME, "font").text)

        CDesc_list.append(rows[-1].find_element(By.XPATH, "td[1]").find_element(By.TAG_NAME, "font").text)

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

valid_module_code_format = re.compile(r"^[A-Z]{2}[0-9]{4}$")
for prereq in Preqs_list:
    preqs_clean.append(" ".join(filter(lambda x : x in ["OR", "&"] or valid_module_code_format.match(x), prereq.split())))

# # Iterate through the original list: merging text properly (here i'm just joining the Prerequisite: texts, this part no issue)
# i = 0
# while i < len(Preqs_list):
#     if Preqs_list[i] == 'Prerequisite:':
#         if i + 1 < len(Preqs_list):
#             merged_Preqs.append(Preqs_list[i] + " " + Preqs_list[i + 1])
#         i += 2  # Skip the next item
#     else:
#         merged_Preqs.append(Preqs_list[i])
#         i += 1

# # here i tried defining a function to recursively join the chunks that end with OR together
# def merging(x, term):
#     i = 0
#     merged = []
#     while i < len(x):
#         if x[i].endswith(term):
#             if i + 1 < len(x):
#                 merged.append(x[i] + ' ' + x[i+1])
#                 del x[i+1]
#             i += 1
#         else:
#             merged.append(x[i])
#             i += 1
#     return merged

# # should i condense this into a for loop?
# merged_Preqs = merging(merged_Preqs, 'OR')
# merged_Preqs = merging(merged_Preqs, 'OR ')
# merged_Preqs = merging(merged_Preqs, 'OR')
# merged_Preqs = merging(merged_Preqs, 'OR ')
# merged_Preqs = merging(merged_Preqs, 'OR')
# merged_Preqs = merging(merged_Preqs, 'OR ')

# # further cleaning up prereqs column
# merged_Preqs2 = []
# counter = 0
# for i in range(len(merged_Preqs)):
#     if not merged_Preqs[i]:
#         counter += 1
#         if counter % 2 == 0 or merged_Preqs[i-1] == 'Prerequisite: for students who fail QET' or merged_Preqs[i-1] == 'Prerequisite: H2 Maths or equivalent' or merged_Preqs[i-1] == 'Prerequisite: Only for Premier Scholars Programme students.' or merged_Preqs[i-1] == 'Prerequisite: No prior knowledge of the language. Declaration is required.':
#             continue
#         merged_Preqs2.append(merged_Preqs[i])
#     elif merged_Preqs[i] == 'Prerequisite: Placement Test or' or merged_Preqs[i] == 'Prerequisite: Year 3 standing' or merged_Preqs[i] == 'Prerequisite: Study Year 3 standing' or merged_Preqs[i] == 'Prerequisite: Placement Test or Able to read simple Arabic scripts or':
#         continue
#     else:
#         merged_Preqs2.append(merged_Preqs[i])

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
