from flask import Flask, jsonify, abort
import csv
import requests

app = Flask(__name__)

def load_smu_modules():
    smu_modules = {}
    with open('smu.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            module_name = row['Module Code']
            smu_modules[module_name] = row
    return smu_modules

smu_modules_data = load_smu_modules()

def load_nus_modules():
    nus_modules = {}
    with open('NusMods.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            module_name = row['NUS Module Code']
            nus_modules[module_name] = row
    return nus_modules

nus_modules_data = load_nus_modules()

def load_ntu_modules():
    ntu_modules = {}
    with open('ntu.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            module_name = row['Course Code']
            ntu_modules[module_name] = row
    return ntu_modules

ntu_modules_data = load_ntu_modules()

#====================================================================
# use this to build prereq tree etc.

def get_prereq_dict():
    prereqTree = {"nus": {}, "ntu": {}, "smu": {}}
    prereqTree["nus"] = {"modules": []}
    for mod in nus_modules_data.keys():
        response = requests.get(f'https://api.nusmods.com/v2/2023-2024/modules/{mod}.json')
        data = response.json()
        dic = {"name": mod,
                "pre-requisites": data.get("prereqTree", "Not Available")}
        prereqTree["nus"]["modules"].append(dic)

    prereqTree["ntu"] = {"modules": []}
    for mod in ntu_modules_data.keys():
        dic = {"name": mod,
                "pre-requisites": ntu_modules_data[mod]['Prerequisites']}
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
    if chosen_uni == "nus-dsa":
        output = {"nus": prereq_dict["nus"]}

    elif chosen_uni == "ntu-dsa":
        output = {"ntu": prereq_dict["ntu"]}

    elif chosen_uni == "smu-dsa":
        output = {"smu": prereq_dict["smu"]}

    elif chosen_uni == "nus-ntu-dsa":
        output = {"nus": prereq_dict["nus"], "ntu": prereq_dict["ntu"]}
    
    elif chosen_uni == "nus-smu-dsa":
        output = {"nus": prereq_dict["nus"], "smu": prereq_dict["smu"]}
    
    elif chosen_uni == "ntu-smu-dsa":
        output = {"ntu": prereq_dict["ntu"], "smu": prereq_dict["smu"]}
    
    elif chosen_uni == "nus-ntu-smu-dsa":
        output = {"nus": prereq_dict["nus"], "ntu": prereq_dict["ntu"], "smu": prereq_dict["smu"]}
        
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
def get_nus_module_description(module_code):
    module = nus_modules_data.get(module_code)
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




if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001)