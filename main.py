import argparse
import db
import markdown
import os
# import matplotlib.pyplot as plt
# from matplotlib import pyplot as plt
import workspace
import utils
import sqlalchemy.sql.default_comparator # for ERROR: missing dll's  
# import pdb # for DEBUG
from os import system

@workspace.require_workspace_selected
def new_record():
    tasks = db.get_all_tasks()
    print("---------Welcome to ControlWork")
    print("\tNew record: Enter the task ID")
    for task in tasks:
        print(f"ID {task.id}:\t{task.name}")
    id = input("ID:\t")
    val = int(input("Value:\t"))
    db.add_record(id, val)

@workspace.require_workspace_selected
def pie_chart_report():
    x = [i.value for i in db.get_all_tasks()]
    lbl = [i.name for i in db.get_all_tasks()]
    exp = [0.05 for i in lbl]
    print("plotting not avaliable")
    print(f"vals:\t{x}")
    print(f"labels:\t{lbl}")
    # plt.pie(x, labels=lbl, explode=exp, autopct='%1.1f%%', pctdistance=0.5, shadow=False)
    # plt.show()

@workspace.require_workspace_selected
def edit_record():
    # ------ flags 
    END = "E"
    RECORD_DELETE = "RD" 

    # ------ manager 
    def manager():
        records = db.get_all_work_records()
        one(records)
    
    # ------ views  
    def one(records):
        while(1):
            system("cls") # windows
            print("---------WorkRecords")
            utils.puts_table(records)
            print(f"{len(records)}   [x] cancel edit")
            id = utils.controled_input(
                utils.between_validator(0,len(records)),
                "option",
                int)
            if (id==len(records)): return
            flag = two(records[id])
            if (flag == END): 
                print("edit finished!")
                return END
            if (flag == RECORD_DELETE): 
                records = db.get_all_work_records()


    def two(_record):
        while(1):
            system("cls") # windows
            utils.puts_table([_record])
            print("---------RecordEdit")
            print("1. edit task")
            print("2. edit value")
            print("3. delete x_x")
            print("4. <-- back")
            print("5. finish")
            choise = utils.controled_input(
                utils.between_validator(1,5),
                "choose a option",
                int)
            if (choise == 4): return 1
            if (choise == 5): return END
            if (three(choise, _record.id) == RECORD_DELETE): return RECORD_DELETE
        
    def three(choise, id):
        if (choise==1):
            tasks = db.get_all_tasks()
            for task in tasks:
                print(f"ID {task.id}:\t{task.name}")
            nval = utils.controled_input(
                utils.between_validator(0,len(tasks)),
                "task ID (0 to go back)",
                int)
            if (nval==0): return
            db.edit_record(id, "task_id", nval)

        if (choise==2):
            nval = utils.controled_input(msj="new value (0 to go back)", type=int)
            if (nval==0): return
            db.edit_record(id, "value", nval)
        
        if (choise==3):
            nval = utils.controled_input(lambda c: c in "YNyn", "are you sure? (y/n)", str)
            if (nval in "Yy"):
                db.delete_record(id)
                input("------ press enter key to continue")
                return RECORD_DELETE
            else:
                return 1
        input("------ press enter key to continue")
    
    # ------ run
    manager()

@workspace.require_workspace_selected
def detailed_report():
    md = "# Detailed Report\n## Work Records\n"+"-"*50+"\n"

    def md_format_record(record: db.WorkRecord):
        time = ":".join(str(record.time).split(':')[:2])
        return f"### Task {record.task_id}: &emsp;{record.value} &emsp;&emsp;&emsp;&emsp; <sub>{record.date},&emsp;{time} Hrs.</sub>\n"+"-"*50+"\n"

    md += "".join(list(map(md_format_record, db.get_all_work_records())))
    if not os.path.exists("./out"):
        os.makedirs("./out")
    with open("out/DetailedReport.md", "w") as f:
        f.write(md)
    html = markdown.markdown(md)
    with open("out/DetailedReport.html", "w", encoding="utf-8", errors="xmlcharrefreplace") as output_file:
        output_file.write(html)

def init_app(file):
    with open(file) as f:
        tasks = [i.split(".")[1].strip() for i in f.readlines()]
    workspace.new_workspace(tasks, file)
    db.init(tasks)

def parse_args():
    parser = argparse.ArgumentParser(prog="cwk")
    parser.description = "This application helps you monitor the time invested in performing your tasks."
    parser.add_argument("-n", "--new", metavar="FILE",type=str, help="starts monitoring the tasks contained in the indicated FILE")
    parser.add_argument("-r", action="store_true", help="save a new record")
    parser.add_argument("-e", action="store_true", help="edit record")
    parser.add_argument("-pc", action="store_true", help="generates a pie chart report")
    parser.add_argument("-dr", action="store_true", help="generates a detailed report")
    parser.add_argument("-ws", action="store_true", help="select a workspace")
    return parser.parse_args()


if __name__ == "__main__":
    
    utils.create_json_if_not_exist()
    utils.create_dir_if_not_exist("data")
    utils.create_dir_if_not_exist("out")

    parser = parse_args()

    if (parser.new):
        init_app(parser.new)

    if (parser.r):
        db.DB.load_db()
        new_record()
    
    if (parser.e):
        db.DB.load_db()
        edit_record()

    if (parser.pc):
        db.DB.load_db()
        pie_chart_report()
    
    if (parser.dr):
        db.DB.load_db()
        detailed_report()

    if (parser.ws):
        # pdb.set_trace()
        workspace.select_workspace()