from sqlalchemy import create_engine, Column, Integer, String, Date, Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, session, sessionmaker
from sqlalchemy.sql.schema import ForeignKey
from datetime import datetime
import workspace

# db management vars -------

class DB:
    Base = declarative_base()
    engine = None
    Session = None
    session = None
    def load_db():
        path = f"sqlite:///{workspace.get_db_path_of_selected_ws()}"
        DB.engine = create_engine(path)
        DB.Session = sessionmaker(bind=DB.engine)
        DB.session = DB.Session()

# models -------

class Task(DB.Base):
    __tablename__ = 'task'
    id = Column(Integer(), primary_key=True)
    name = Column(String())
    value = Column(Integer, default=0)
    work_records = relationship('WorkRecord', backref='task', lazy="dynamic")
    def __repr__(self) -> str:
        return f"<Task(name={self.name}, value={self.value})>"

class WorkRecord(DB.Base):
    __tablename__ = 'workrecord'
    id = Column(Integer, primary_key=True)
    time = Column(Time, default=datetime.now().time())
    date = Column(Date, default=datetime.now().date())
    value = Column(Integer)
    task_id = Column(Integer, ForeignKey('task.id'))
    def __repr__(self) -> str:
        return (f"<WorkRecord(time ={self.time}, "
                f"date={self.date}, "
                f"value={self.value}, "
                f"task={self.task})>")

# interface -------

def create_all():
    DB.Base.metadata.create_all(DB.engine)

def get_all_tasks():
    return DB.session.query(Task).all() #TODO error if db not created!! add raise

def get_all_work_records():
    return DB.session.query(WorkRecord).all() #TODO error if db not created!! add raise

def find_task(_id):
    return DB.session.query(Task).filter_by(id=_id).first()

def find_work_record(_id):
    return DB.session.query(WorkRecord).filter_by(id=_id).first()

def add_record(task_id, _value):
    _task = find_task(task_id)
    _task.value += _value
    record = WorkRecord(task=_task, value=_value)
    DB.session.add(record)
    DB.session.commit()

def edit_record(wr_id, campo, new_value): 
                                        # TODO: improve database design!
                                        # the "value" field in table Task is unnecessary!!
    record = find_work_record(wr_id)
    print("[DB]\tmodified record!\ndetails:")
    print("before:\t", record)
    record.task.value -= record.value

    setattr(record, campo, new_value)   # this modifies the id
                                        
    DB.session.commit() # then commit to load the respective task
                        # object to the workrecord object
    
    record.task.value += record.value # finally we edit the task 
                                      # object updated by the id before
    
    DB.session.commit() # commit changes in task object

    print("after:\t", record)
    
def delete_record(wr_id):
    r = find_work_record(wr_id)
    print("[DB]\trecord removed: ")
    print(r)
    r.task.value -= r.value
    DB.session.delete(r)
    # DB.session.query(WorkRecord).find_by(id=wr_id).delete()
    DB.session.commit()

def init(tasks_name):
    DB.load_db()
    create_all()
    DB.session.add_all(list(map(lambda t: Task(name=t), tasks_name)))
    DB.session.commit()


if __name__ == "__main__":
    DB.load_db()
    r = DB.session.query(WorkRecord)[0]
    # print(r)
    edit_record(r.id, "value", 100)
    # edit_record(r.id, "task_id", 2)