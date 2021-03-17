import json
import utils
import db
import sys
import os
# import pdb # for DEBUG

# checkers ---------------

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

# utils ---------------

def get_workspaces():
    return get_json()["workspaces"]

def get_selectec_workspace():
    return get_json()["selected"]

def set_selected_workspace(id):
    o = get_json()
    with open("ws.json", "w") as w:
        o["selected"] = id
        w.write(json.dumps(o))

def unselect_workspace(self):
    o = get_json()
    with open("ws.json", "w") as w:
        o["selected"] = -1
        w.write(json.dumps(o))

def append_workspace(ws):
    o = get_json()
    with open("ws.json", "w") as w:
        o["workspaces"].append(ws)
        w.write(json.dumps(o))
    set_selected_workspace(ws["id_ws"])

def get_json():
    with open("ws.json", "r") as w:
        return json.load(w)

# decorators ---------------

def require_any_workspace_created(f):
    # pdb.set_trace()
    def contition():
        return len(get_workspaces())>0

    def w(*args, **kwargs):    
        if (not contition()):
            print("No workspaces exists!")
            print("type: \"cwk -h\" for help to create a new workspace.")
            sys.exit(0)
        else:
            return f(*args, **kwargs)
    return w

def require_workspace_selected(f):
    def contition():
        return get_selectec_workspace()!=-1

    def w(*args, **kwargs):    
        if (not contition()):
            print("No workspaces selected!")
            print("Please, select a workspace:")
            select_workspace()
        else:
            return f(*args, **kwargs)
    return w

# interface ---------------

@require_any_workspace_created
def select_workspace():
    ws = get_workspaces()
    for w in ws:
        print(str(w["id_ws"])+". "+w["db_path"]+"\n")
    s = utils.controled_input(
        lambda s: s>=0 and s<len(ws), 
        "Select number", 
        int)
    set_selected_workspace(s)
    db.DB.load_db()

def new_workspace(tasks, file):
    ws = dict()
    ws["id_ws"] = len(get_workspaces())
    ws["tasks_file"] = file
    ws["tasks"] = tasks
    ws["db_path"] = f"data/cwk_{ws['id_ws']}.db"
    return append_workspace(ws)
    
@require_workspace_selected
def get_db_path_of_selected_ws():
    id = get_selectec_workspace()
    if (id<0): raise Exception(f"[get_db_path_of_selected_ws]: get_selectec_workspace() returns negative!\nshould be a select workspace")
    return list(filter(lambda w: w["id_ws"]==id, get_workspaces()))[0]["db_path"]


if __name__ == "__main__":
    pass