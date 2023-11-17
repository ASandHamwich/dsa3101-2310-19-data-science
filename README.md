# DataCompass - DSA3101 AY23/24 Sem 1 What is Data Science?

Data Science has been around for close to 10 years, yet there is no agreement on what the field
consists of. This leads to confusion among prospective students when they are trying to decide
between degree programs. It also leads to arguments and disagreements within and between
universities when it comes to assessing the performance of a "data science" department.
The task in this project is to analyse the similarities and differences between data science
departments using unsupervised learning techniques.



## Backend

* Ashton Low Yi
* Heng Peng Kai
* Chan Shing Yee
* Jeow Jo Anne

## Frontend

* He Zhi Yin
* Lee Xin En
* Gan Wan Yi
* Arnold Lek Jian Ming


## Objective

1. Providing a common platform for incoming undergraduate students and administration to compare 
course information between different Data Science Programs to aid them in informed decision-making.
2. Assisting university administration in identifying the strengths and weaknesses of their Data 
Science programmes relative to other universities.
3. (UX) Designing a user-friendly interface that is easy to navigate and explore different modules.
---


## Start up

To get started, 

1. Ensure that you have docker installed and have opened up docker

2. Clone this repository

`git clone "https://github.com/ASandHamwich/dsa3101-2310-19-data-science"`

3. You can run the following command in the root directory

`docker compose up -d`

4. You should have 2 container up and running:
   1. `frontend-1` - This will be hosting our frontend website (Served on port 9001)
   2. `backend-1` - This will contain the flask-api which connects the database with the frontend website (Served on port 5001)

5. Go to `http://localhost:9001` and you should be able to see the website

---

## File Structure
```bash
.
│   High fidelity wireframe.pdf
│   README.md
│   requirements.txt
│
├───backend
│       flask-backend.py
│       nlp.py
│       ntu.csv
│       ntu.py
│       ntu_db_sentiment.csv
│       nus-dsa.csv
│       nus-dse.csv
│       nus.py
│       smu.csv
│       smu.py
│       smuMods.csv
│
└───frontend
    │   app.py
    │
    ├───assets
    │       app.css
    │       course.css
    │       home.css
    │       module.css
    │       README.md
    │       search.css
    │
    ├───pages
            compare.py
            course.py
            home.css
            home.py
            modcompare.py
            module.py
            ntu_with_concepts.csv
            README.md
            search.py      
    
```
----

## How our website works
----
### Landing page
![Landing page](/../frontend/assets/images/landing_page,jpg)

In the landing page, you will see 4 Data Science Programs in the local universiites of Singapore. You can either:

1. Click on a program and view the course page
2. Click two of the checkboxes and use the compare button to view a course comparison page
----
### Course page
#Add picture of course page

The purpose of the course page is to provide you with information about the selected Data Science Program in a simple, condensed manner. In this page, you will find:
1. Course Description: a short description about the program
2. What you will learn: a pie chart showing the proportion of each subject offered under the Data Science Program, this provides additional information on the subjects the program focuses on. Hovering over a section of the pie chart will provide additional information about what the subject is and how many modules are offered.
3. Course Tree: a course tree depicting the prerequisites and relationships between the modules in the program. If you are interested in learning more about a module, clicking on its node will bring you to the corresponding module page of the selected module
   (SMU does not have links in their course tree as their prerequisite information is inaccessible to the public)
----
### Course Comparison page
#Add picture of course comparison page

The course comparison page provides a side by side view of two of your selected courses. By showing a direct comparison of two courses, it aims to:
1. Improve convenience: proespective students can look at one page instead of two or more pages to get the same amount of information on the two programs
2. Direct comparison: prospective students can view the subject pie charts and course trees together and choose the program that offers more of the subject they are interested in
----
### Module page
#Add pictures of module page 

The module page provides information on the selected module. In the module page, you will find:
1. Module description:  the module description was taken from the respective universities official module websites
2. Key concepts bar: key concepts identified in the module description are placed in the key concepts bar for prospecctive students to easily see the key concepts they will learn in this module without having to read the description for more detail. Hovering on each key concept brings up a short explanation of the concept for students who are not familiar with the technical terms
3.  Related modules sidebar: the sidebar contains similar modules to the currently selected module. The top 5 most similar modules from other universities are selected based on the similarity of their key concepts to allow proespective students to explore and compare similar modules. If you click on a module in the sidebar, it brings you to the module comparison page with the currently selected module and the similar module.
4.  Reviews: for past students of the module to leave reviews with the aim of building up a database of reviews for all data science programs in Singapore since module reviews for NTU and SMU are not available to the public.
----
### Module Comparison page
#Add pictures of module comparison page

The module comparison page brings up the module description and key concepts bar side by side for ease of comparison. To return to a single module page, click on read more for additional details as well as recommended modules.

----
### Search bar and results page
#Add pictures of search results page

If you are not in the mood for exploring modules and courses through the pages, you can directly type the module code or concept that you want to learn more about into the search bar. Doing so will bring you to the search results page with all modules containing your search phrase.

----

Have fun planning using DataCompass!
