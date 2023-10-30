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

for i in range(len(course_options)):
    # select course name from dropdown box and click (todo: loop the DSAI courses)
    driver.get("https://wis.ntu.edu.sg/webexe/owa/aus_subj_cont.main")
    driver.find_element(By.XPATH, f"//select[@name='r_course_yr']/{course_options[i]}").click()
    driver.find_element(By.XPATH, "//input[@value='Load Content of Course(s)']").click()

    # course codes
    # relevant mods: CZ, MH, SC
    # if prereq texts don't show up when i find course names, then just delete from here. else, maybe we compile everything then delete accordingly
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

driver.quit()
# writing lists into a csv file
data = {'Course Code': CCode_list, 'Course Name': CName_list, 'Course Description': CDesc_list}
df = pd.DataFrame(data)
df = df.drop_duplicates(subset='Course Code')
csv_file = "ntu.csv"
df.to_csv(csv_file, index=False)