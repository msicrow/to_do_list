from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from datetime import datetime

engine = create_engine("sqlite:///todo.db?check_same_thread = False")
Base = declarative_base()


class Table(Base):
    __tablename__ = "task"
    id = Column(Integer, primary_key=True)
    task = Column(String, default="default_string")
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return f"{self.id}. {self.task}"


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def menu():
    print("")
    print("1) Today's tasks")
    print("2) Add task")
    print("0) Exit")


def add_task(new_task):
    row = Table(task=new_task)
    session.add(row)
    session.commit()


def main():
    menu()
    menu_selection = int(input())
    rows = session.query(Table).all()
    if menu_selection == 1:
        if not rows:
            print("Nothing to do!")
            main()
        else:
            for row in rows:
                print(f"{row.id}) {row.task}")
            main()
    elif menu_selection == 2:
        new_task = input("Enter task\n")
        add_task(new_task)
        print("The task has been added!")
        main()
    else:
        pass


main()
