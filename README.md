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

4. You should have 1 container up and running:
   1. `frontend-web` - This will be hosting our frontend website (Served on port 9001)

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

Have fun planning using DataCompass!
