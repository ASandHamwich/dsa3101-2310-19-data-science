from flask import Flask, jsonify, abort
import csv
import requests
from pathlib import Path

app = Flask(__name__)

path = Path(__file__).parent

def load_smu_modules():
    smu_modules = {}
    with (path / "smu.csv").open(encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            module_name = row['module_code']
            smu_modules[module_name] = row
    return smu_modules
smu_modules_data = load_smu_modules()

def load_nus_dsa_modules():
    nus_modules = {}
    with (path / 'nus-dsa.csv').open(encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            module_name = row['module_code']
            nus_modules[module_name] = row
    return nus_modules
nus_dsa_modules_data = load_nus_dsa_modules()

def load_nus_dse_modules():
    nus_modules = {}
    with (path / 'nus-dse.csv').open(encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            module_name = row['module_code']
            nus_modules[module_name] = row
    return nus_modules
nus_dse_modules_data = load_nus_dse_modules()

def load_ntu_modules():
    ntu_modules = {}
    with (path / 'ntu.csv').open(encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            module_name = row['module_code']
            ntu_modules[module_name] = row
    return ntu_modules
ntu_modules_data = load_ntu_modules()

#====================================================================
# use this to build prereq tree etc.

def get_prereq_dict():
    prereqTree = {"nus dsa": {}, "nus dse": {}, "ntu": {}, "smu": {}}
    prereqTree["nus dsa"] = {"modules": []}
    for mod in nus_dsa_modules_data.keys():
        response = requests.get(f'https://api.nusmods.com/v2/2023-2024/modules/{mod}.json')
        data = response.json()
        dic = {"name": mod,
                "pre-requisites": data.get("prereqTree", "Not Available")}
        prereqTree["nus dsa"]["modules"].append(dic)

    prereqTree["nus dse"] = {"modules": []}
    for mod in nus_dse_modules_data.keys():
        response = requests.get(f'https://api.nusmods.com/v2/2023-2024/modules/{mod}.json')
        data = response.json()
        dic = {"name": mod,
                "pre-requisites": data.get("prereqTree", "Not Available")}
        prereqTree["nus dse"]["modules"].append(dic)

    prereqTree["ntu"] = {"modules": []}
    for mod in ntu_modules_data.keys():
        dic = {"name": mod,
                "pre-requisites": ntu_modules_data[mod]['prerequisites']}
        prereqTree["ntu"]["modules"].append(dic)
    
    prereqTree["smu"] = {"modules": []}
    for mod in smu_modules_data.keys():
        dic = {"name": mod,
                "pre-requisites": "Not Available"}
        prereqTree["smu"]["modules"].append(dic)
    return prereqTree

prereq_dict = get_prereq_dict()

@app.route('/<chosen_uni>/', methods=['GET'])
def get_prereq(chosen_uni):
    output = {}

    if chosen_uni == "nus-dsa":
        output = {"nus": prereq_dict["nus dsa"]}
    
    elif chosen_uni == "nus-dse":
        output = {"nus": prereq_dict["nus dse"]}

    elif chosen_uni == "ntu-dsa":
        output = {"ntu": prereq_dict["ntu"]}

    elif chosen_uni == "smu-dsa":
        output = {"smu": prereq_dict["smu"]}

    elif chosen_uni == "nus-ntu-dsa":
        output = {"nus": prereq_dict["nus dsa"], "ntu": prereq_dict["ntu"]}
    
    elif chosen_uni == "nus-smu-dsa":
        output = {"nus": prereq_dict["nus dsa"], "smu": prereq_dict["smu"]}
    
    elif chosen_uni == "ntu-smu-dsa":
        output = {"ntu": prereq_dict["ntu"], "smu": prereq_dict["smu"]}
    
    elif chosen_uni == "nus-ntu-smu-dsa":
        output = {"nus": prereq_dict["nus dsa"], "ntu": prereq_dict["ntu"], "smu": prereq_dict["smu"]}

    elif chosen_uni == "nus-dse-ntu-dsa":
        output = {"nus": prereq_dict["nus dse"], "ntu": prereq_dict["ntu"]}
    
    elif chosen_uni == "nus-dse-smu-dsa":
        output = {"nus": prereq_dict["nus dse"], "smu": prereq_dict["smu"]}
    
    elif chosen_uni == "nus-dse-ntu-smu-dsa":
        output = {"nus": prereq_dict["nus dse"], "ntu": prereq_dict["ntu"], "smu": prereq_dict["smu"]}

    return jsonify(output)

#====================================================================
# use this to get more information about each module for the schools

@app.route('/smu-dsa/<module_code>/', methods=['GET'])
def get_smu_module_description(module_code):
    module = smu_modules_data.get(module_code)
    if module:
        return jsonify(module)
    else:
        abort(404, description="module not found")

#====================================================================

@app.route('/nus-dsa/<module_code>/', methods=['GET'])
def get_nus_dsa_module_description(module_code):
    module = nus_dsa_modules_data.get(module_code)
    if module:
        return jsonify(module)
    else:
        abort(404, description="module not found")

@app.route('/nus-dse/<module_code>/', methods=['GET'])
def get_nus_dse_module_description(module_code):
    module = nus_dse_modules_data.get(module_code)
    if module:
        return jsonify(module)
    else:
        abort(404, description="module not found")

#====================================================================
# when user click onto the node

@app.route('/ntu-dsa/<module_code>/', methods=['GET'])
def get_ntu_module_description(module_code):
    module = ntu_modules_data.get(module_code)
    if module:
        return jsonify(module)
    else:
        abort(404, description="module not found")
#====================================================================
# Add the following function to get all modules with descriptions

def get_all_modules():
    all_modules = {"nus-dsa": [], "nus-dse": [], "ntu": [], "smu": []}

    # Add NUS modules
    for mod_code, mod_data, in nus_dsa_modules_data.items():
        all_modules["nus-dsa"].append({"Module Code": mod_code, "Module Name": mod_data.get("module_name"), "Module Description": mod_data.get("module_description"), "Key Concepts": mod_data.get("key_concepts")})

    for mod_code, mod_data, in nus_dse_modules_data.items():
        all_modules["nus-dse"].append({"Module Code": mod_code, "Module Name": mod_data.get("module_name"), "Module Description": mod_data.get("module_description"), "Key Concepts": mod_data.get("key_concepts")})

    # Add NTU modules
    for mod_code, mod_data in ntu_modules_data.items():
        all_modules["ntu"].append({"Module Code": mod_code, "Module Name": mod_data.get("module_name"), "Module Description": mod_data.get("module_description"), "Key Concepts": mod_data.get("key_concepts")})

    # Add SMU modules
    for mod_code, mod_data in smu_modules_data.items():
        all_modules["smu"].append({"Module Code": mod_code, "Module Name": mod_data.get("module_name"), "Module Description": mod_data.get("module_description"), "Key Concepts": mod_data.get("key_concepts")})
    
    return all_modules

@app.route('/nus-ntu-smu/all-modules/', methods=['GET'])
def get_all_modules_endpoint():
    modules = get_all_modules()

    # Convert the data to a JSON response
    response = jsonify(modules)
    response.status_code = 200
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
