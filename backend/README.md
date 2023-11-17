# **DataCompass Back-End**

## Description

This folder contains various datasets and Python files necessary for running the website associated with the Data Science courses.

## Getting Started

### Without Docker

1. [Install Python 3.10 or above](https://www.python.org/downloads/)
2. Install dependencies
```
pip install -r requirements.txt
```

### With Docker

1. [Install Docker 19.03 or later](https://docs.docker.com/get-docker/)
```
curl https://get.docker.com | sh && sudo systemctl --now enable docker
```
2. Build the Docker container
```
docker build -t backend-1 
```
3. Run the Docker container
```
docker run -p 8000:8000 backend-1 
```

### Executing program

1. To run the Python scripts individually
```
python nlp.py
python nus_dsa.py (install nlp.py first)
python nus_dse.py (install nlp.py first)
python ntu.py
python smu.py
```
2. To start the web service
```
python flask-backend.py
```

## Documentation (function and endpoint)

### Helper Functions

`load_nus_dsa_modules`

**Description:** Load data from nus-dsa.csv file

**Parameters:** None

**Returns:** `Dict` of  `Dict` of NUS Data Science and Analytics Module Information.

---

`load_nus_dse_modules`

**Description:** Load data from nus-dse.csv file

**Parameters:** None

**Returns:** `Dict` of `Dict` of NUS Data Science and Economics Module Information.

---

`load_ntu_modules`

**Description:** Load data from ntu.csv file

**Parameters:** None

**Returns:** `Dict` of `Dict` of NTU Data Science and Artificial Intelligence Module Information.

---

`load_smu_modules`

**Description:** Load data from smu.csv file

**Parameters:** None

**Returns:** `Dict` of `Dict` of SMU Data Science and Analytics Module Information.

---

`get_prereq_dict`

**Description:** Generates a dictionary of Module Information from NUS DSA, NUS DSE, NTU DSAI and SMU DSA.

**Parameters:** None

**Returns:** `Dict` of `Dict` of Module Information from NUS DSA, NUS DSE, NTU DSAI and SMU DSA.

---

`get_all_modules`

**Description:** Generates a dictonary of all the Modules Information and Key Concepts for NUS DSA, NUS DSE, NTU DSAI and SMU DSA.

**Parameters:** None

**Returns:** `Dict` of `List` of `Dict` of all the Modules Information and Key Concepts based on the Module Description of NUS DSA, NUS DSE, NTU DSAI and SMU DSA.

### API Endpoints

`/{chosen_uni}/`

**Method:** `GET`

**Description:** Get the all the module code and a list of its prerequisites for the corresponding universities that was chosen.

**Parameters:** 
| Name | Description |
|------|-------------|
| `chosen_uni` (str) | Chosen university/universties: nus-dsa, nus-dse, ntu, smu |

**Responses:** 
<table>
<tr> 
    <th>Code</th>
    <th>Description</th>
</tr>
<tr>
<td>200</td>
<td>
    Example Value

    {
        "nus": {
            "modules": [
                {
                    "name": "DSA1101",
                    "pre-requisites": { 
                        "or": [
                            "MA1301:D",
                            "MA1301FC:D",
                            "MA1301X:D"
                        ]
                    }
                }
            ]
        }   
    }

</td>   
</tr>
<tr>
    <td>400</td>
    <td>Not found</td>
</tr>
</table>

---

`/{chosen_uni}/{module_code}/`

**Method:** `GET`

**Description:** Get the information about the module chosen of the chosen university.

**Parameters:** 
| Name | Description |
|------|-------------|
| `chosen_uni` (str) | Chosen university/universties: nus-dsa, nus-dse, ntu, smu |
| `module_code` (str) | 5-7 character long code identifying the module |

**Responses:**
<table>
<tr> 
    <th>Code</th>
    <th>Description</th>
</tr>
<tr>
<td>200</td>
<td>
    Example Value

    { 
        "key_concepts": "datum, probability, ...",
        "module_code": "DSA1101",
        "module_description": "The abundance of data being harvested from various sectors ...",
        "module_name": "Introduction to Data Science"
    }

</td>   
</tr>
<tr>
    <td>400</td>
    <td>Not found</td>
</tr>
</table>

---

`/nus-ntu-smu/all_modules/`

**Method:** `GET`

**Description:** Get all module information and key concepts from all the universities.

**Responses:**
<table>
<tr> 
    <th>Code</th>
    <th>Description</th>
</tr>
<tr>
<td>200</td>
<td>
    Example Value

    {
        "ntu": [
            {
                "Key Concepts" : null,
                "Module Code": "CZ1103",
                "Module Description": "Computational thinking (CT) is the ...",
                "Module Name": "INTRODUCTION TO COMPUTATIONAL THINKING & PROGRAMMING"
            }
        ]
    }

</td>   
</tr>
<tr>
    <td>400</td>
    <td>Not found</td>
</tr>
</table>

---

`/glossary_list/`

**Method:** `GET`

**Description:** Get the dictionary of the key concepts and its description.

**Responses:**
<table>
<tr> 
    <th>Code</th>
    <th>Description</th>
</tr>
<tr>
<td>200</td>
<td>
    Example Value

    {
        "AngularJS": "An open-source JavaScript ..."
    }

</td>   
</tr>
<tr>
    <td>400</td>
    <td>Not found</td>
</tr>
</table>

## Files:

| File | Description |
|------|-------------|
| `nus_dsa.py`, `nus_dse.py` | Code to get module data and sentiment analysis for NUS Data Science and Analytics (DSA) and Data Science and Economics (DSE) |
| `ntu.py` | Code to get module data and sentiment analysis for NTU |
| `smu.py` | Code to get module data and sentiment analysis for SMU |
| `nlp.py` | Natural Language Processing Code to summarise and generate key concepts column from module descriptuion |
| `nus_dsa.csv`, `nus_dse.csv` | CSV file containing module code, module name, module description, key concepts, reviews and sentiment rating for NUS DSA and DSE |
| `ntu.csv` | CSV file containing module code, module name, module description, key concepts, reviews and sentiment rating for NTU |
| `smuMods.csv` | Contains the module code, module name and type of module to be cleared in SMU |
| `smu.csv` | CSV file containing module code, module name, module description, key concepts, reviews and sentiment rating for SMU |
| `flask-backend.py` | Contains the multiple endpoints of our website |

## Authors

* Ashton Yi Low
* Chan Shing Yee
* Heng Peng Kai
* Jeow Jo Anne

## Version history

* 0.1
    * Initial Release
---
