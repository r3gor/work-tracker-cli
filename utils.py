import os
import json

def create_json_if_not_exist():
    if not os.path.exists("ws.json"):
        print("ws.json doesn't exist!")
        print("creating ws.json base...")
        d = dict()
        d["selected"] = -1
        d["workspaces"] = []
        with open("ws.json", "w") as f:
            f.write(json.dumps(d))
    else:
        return

def create_dir_if_not_exist(dir: str):
    if not os.path.exists(dir):
        print(f"{dir} doesn't exist!")
        print(f"creating {dir} ...")
        os.mkdir(dir)
    else:
        return

def controled_input(validator, msj, type):
    s = type(input(f"{msj}:\t"))
    while not validator(s):
        print("type a valid value!")
        s = type(input(f"{msj}:\t"))
    return s