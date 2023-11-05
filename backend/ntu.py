# import the necessary
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

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
    CCode = driver.find_elements(By.XPATH, "//td[@width='100']")
    for i in range(len(CCode)):
        if (CCode[i].text[:2]).isupper():
            CCode_list.append(CCode[i].text)

    # course names
    CName = driver.find_elements(By.XPATH, "//td[@width='500']")
    for j in range(len(CName)):
        if (CName[j].text[:5]).isupper():
            CName_list.append(CName[j].text)

    # course descriptions
    CDesc = driver.find_elements(By.XPATH, "//td[@width='650']")
    for k in range(len(CDesc)):
        CDesc_list.append(CDesc[k].text)

    # prereqs
    Preqs = driver.find_elements(By.XPATH, "//font[@color='#FF00FF']")
    for l in range(len(Preqs)):
        Preqs_list.append(Preqs[l].text)

driver.quit()

# Initialize an empty list to store the merged items
merged_Preqs = []

# Iterate through the original list: merging text properly (here i'm just joining the Prerequisite: texts, this part no issue)
i = 0
while i < len(Preqs_list):
    if Preqs_list[i] == 'Prerequisite:':
        if i + 1 < len(Preqs_list):
            merged_Preqs.append(Preqs_list[i] + " " + Preqs_list[i + 1])
        i += 2  # Skip the next item
    else:
        merged_Preqs.append(Preqs_list[i])
        i += 1

# here i tried defining a function to recursively join the chunks that end with OR together
def merging(x, term):
    i = 0
    merged = []
    while i < len(x):
        if x[i].endswith(term):
            if i + 1 < len(x):
                merged.append(x[i] + ' ' + x[i+1])
                del x[i+1]
            i += 1
        else:
            merged.append(x[i])
            i += 1
    return merged

# should i condense this into a for loop?
merged_Preqs = merging(merged_Preqs, 'OR')
merged_Preqs = merging(merged_Preqs, 'OR ')
merged_Preqs = merging(merged_Preqs, 'OR')
merged_Preqs = merging(merged_Preqs, 'OR ')
merged_Preqs = merging(merged_Preqs, 'OR')
merged_Preqs = merging(merged_Preqs, 'OR ')

# further cleaning up prereqs column
merged_Preqs2 = []
counter = 0
for i in range(len(merged_Preqs)):
    if not merged_Preqs[i]:
        counter += 1
        if counter % 2 == 0 or merged_Preqs[i-1] == 'Prerequisite: for students who fail QET' or merged_Preqs[i-1] == 'Prerequisite: H2 Maths or equivalent' or merged_Preqs[i-1] == 'Prerequisite: Only for Premier Scholars Programme students.':
            continue
        merged_Preqs2.append(merged_Preqs[i])
    elif merged_Preqs[i] == 'Prerequisite: Placement Test or' or merged_Preqs[i] == 'Prerequisite: Year 3 standing' or merged_Preqs[i] == 'Prerequisite: Study Year 3 standing':
        continue
    else:
        merged_Preqs2.append(merged_Preqs[i])

merged_Preqs_clean = [item.replace('Prerequisite: ', '') for item in merged_Preqs2]

# writing lists into a csv file
data = {'Course Code': CCode_list, 'Course Name': CName_list, 'Course Description': CDesc_list, 'Prerequisites': merged_Preqs_clean}
df = pd.DataFrame(data)
df = df.drop_duplicates(subset='Course Code')

# removing redundant non-DSA modules
df['Course Description'].replace('', 'Course Description unavailable. Please google for more info :)', inplace = True)
relevant = ['CS', 'CZ', 'MH', 'SC']
df = df[df['Course Code'].str[:2].isin(relevant)]

#adding reviews and sentiment score columns
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import csv
from selenium.webdriver.support import expected_conditions as EC
sentiment = SentimentIntensityAnalyzer()
driver = webdriver.Chrome()
ntuModuleCodes = df['Course Code']
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
df['Reviews'] = ntuModuleReviews
df['Score'] = ntuModuleScores

csv_file = "ntu.csv"
df.to_csv(csv_file, index=False)


