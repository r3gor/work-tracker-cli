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

def controled_input(validator=lambda x: True, msj="input", type=str):
    try:
        s = type(input(f"{msj}:\t"))
        while not validator(s):
            print("type a valid value!")
            s = type(input(f"{msj}:\t"))
        return s
    except ValueError:
        print("ERROR: input should be: " + str(type))
        return controled_input(validator, msj, type)

def puts_table(records):
    # --- width fields
    w = dict()
    w['#'] = 3
    w['name'] = 20
    w['value'] = 5
    # --- templates
    title = f"{{:<{w['#']}}} {{:^{w['name']}}} {{:<{w['value']}}}"
    elemt = f"{{:<{w['#']}}} {{:<{w['name']}}} {{:<{w['value']}}}"
    # --- puts   
    print(title.format("#", "name", "value"))
    for i in range(len(records)):
        print(elemt.format(
            i, 
            pretty_string_adjust(records[i].task.name, w["name"]), 
            records[i].value))

def pretty_string_adjust(s, size):
    return s[:size-3]+"..." if len(s)>=size else s

def between_validator(ini, end):
    return lambda x: x>=ini and x<=end 

if __name__ == "__main__":
    # s = pretty_string_adjust("comer una pizza entera de 60 cm de radio", 20)
    # print(s)
    puts_table([])