from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

engine = create_engine("sqlite:///todo.db?check_same_thread = False")
Base = declarative_base()


class Table(Base):
    __tablename__ = "task"
    id = Column(Integer, primary_key=True)
    task = Column(String, default="default_string")
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return f"{self.id}. {self.task}"


date_today = datetime.today()
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def menu():
    print("")
    print("1) Today's tasks")
    print("2) Week's tasks")
    print("3) All tasks")
    print("4) Missed tasks")
    print("5) Add task")
    print("6) Delete task")
    print("0) Exit")
    return int(input())


def add_task():
    new_task = input("Enter task\n")
    user_deadline = input("Enter deadline in this format: YYYY-MM-DD\n")
    formatted_deadline = datetime.strptime(user_deadline, "%Y-%m-%d")
    new_row = Table(task=new_task, deadline=formatted_deadline)
    session.add(new_row)
    session.commit()
    print("The task has been added!")


def today_tasks():
    rows = session.query(Table).all()
    if not rows:  # if rows is empty
        print(f"Today {datetime.today().day} {datetime.today().strftime('%b')}")  # e.g. Today Aug 17
        print("Nothing to do!")
    else:
        today_rows = session.query(Table).filter(Table.deadline == date_today.date()).all()
        for num, row in enumerate(today_rows):
            print(f"{num + 1}. {row.task}")


def week_tasks():
    for day in range(7):
        today = datetime.today() + timedelta(days=day)
        daily_task = session.query(Table).filter(Table.deadline == today.date()).all()
        print(f"\n{today.strftime('%A')} {today.day} {today.strftime('%b')}:")
        if len(daily_task) == 0:
            print("Nothing to do!")
        for num, task in enumerate(daily_task):
            if task:
                print(f"{num + 1}. {task.task}")


def all_tasks():
    sorted_rows = session.query(Table).order_by(Table.deadline).all()
    for num, row in enumerate(sorted_rows):
        print(f"{num + 1}. {row.task}. {row.deadline.day} {row.deadline.strftime('%b')}")


def missed_tasks():
    missed_rows = session.query(Table).filter(Table.deadline < datetime.today().date()).all()
    if len(missed_rows) == 0:
        print("Nothing is missed!")
    else:
        for num, row in enumerate(missed_rows):
            print(f"{num + 1}. {row.task}. {row.deadline.day} {row.deadline.strftime('%b')}")


def delete_task():
    all_tasks()
    task_delete_num = int(input("Choose the number of the task you want to delete:\n"))
    filter_rows = session.query(Table).order_by(Table.deadline).all()
    specific_row = filter_rows[task_delete_num - 1]
    session.delete(specific_row)
    session.commit()
    print("The task has been deleted!")


if __name__ == "__main__":
    while True:
        user_input = menu()
        if user_input == 1:
            today_tasks()
        elif user_input == 2:
            week_tasks()
        elif user_input == 3:
            all_tasks()
        elif user_input == 4:
            missed_tasks()
        elif user_input == 5:
            add_task()
        elif user_input == 6:
            delete_task()
        else:
            break
