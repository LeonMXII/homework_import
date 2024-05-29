import os
import sqlalchemy as sq
import psycopg2

from application.db.people import get_employees
from application.salary import calculate_salary
from datetime import datetime as date

from sqlalchemy.orm import declarative_base, relationship, sessionmaker


Base = declarative_base()

class Employee(Base):
    __tablename__ = "employees"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=100), unique=True)

    def __str__(self):
        return f"Employees {self.id}: {self.name}"

class Salary(Base):
    __tablename__ = "salary"

    id = sq.Column(sq.Integer, primary_key=True)
    salary = sq.Column(sq.String(length=10), unique=False)
    id_employee = sq.Column(sq.Integer, sq.ForeignKey("employees.id"), nullable=False)
    employee = relationship(Employee, backref="salary")

    def __str__(self):
        return f"Salary {self.id}: ({self.salary}, {self.id_employee})"

def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

login = os.getenv("login")
DSN = login
engine = sq.create_engine(DSN)
create_tables(engine)


Session = sessionmaker(bind=engine)
session = Session()

session.close()
print("Таблицы созданы")

if __name__ == "__main__":
    get_employees(26, 90)
    calculate_salary(100000, 31, 20)
    date = date.now().date()
    print(date)
