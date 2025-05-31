import os
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import execute_values

load_dotenv()

DB_CONFIG = {
    "database":os.getenv("DB_NAME"),
    "user":os.getenv("DB_USERNAME"),
    "password":os.getenv("DB_PASSWORD"),
    "host":os.getenv("DB_HOST"),
    "port":os.getenv("DB_PORT"),
}

# added index to yearly_earnings bc i will query it a lot (this will increase SELECT speed but will decrease insert, update, delete speeds by creating a sorted tree based on yearly_earnings)
migrate_up= [
    """CREATE TABLE IF NOT EXISTS countries (
    id INT PRIMARY KEY,
    name VARCHAR(32) NOT NULL,
    region VARCHAR(32) NOT NULL,
    yearly_gdp DECIMAL CHECK (yearly_gdp>=0),
    population INT CHECK (population>=0)
    );""",

    """CREATE TABLE IF NOT EXISTS companies (
    id INT PRIMARY KEY,
    name VARCHAR(72) NOT NULL,
    country_id INT NOT NULL,
    sector VARCHAR(32) NOT NULL,
    q1_earnings DECIMAL CHECK (q1_earnings>=0),
    q2_earnings DECIMAL CHECK (q2_earnings>=0),
    q3_earnings DECIMAL CHECK (q3_earnings>=0),
    q4_earnings DECIMAL CHECK (q4_earnings>=0),
    yearly_earnings DECIMAL CHECK (yearly_earnings>=0),
    employee_count INT CHECK (employee_count>=0),
    employee_payroll DECIMAL CHECK (employee_payroll>=0)
    );""",

    """CREATE TABLE IF NOT EXISTS employees (
    id_number VARCHAR(32) PRIMARY KEY,
    ssn VARCHAR(32) NOT NULL,
    first_name VARCHAR(32) NOT NULL,
    last_name VARCHAR(32) NOT NULL,
    date_of_birth DATE NOT NULL,
    company_id INT,
    email VARCHAR NOT NULL,
    phone_no BIGINT CHECK (phone_no>0),
    salary DECIMAL CHECK (salary>=0),
    nationality INT NOT NULL,
    sector VARCHAR(32) NOT NULL
    );""",

    """ALTER TABLE companies ADD FOREIGN KEY (country_id) REFERENCES countries (id);
    """,
    """ALTER TABLE employees ADD FOREIGN KEY (nationality) REFERENCES countries (id);
    """,
    """ALTER TABLE employees ADD FOREIGN KEY (company_id) REFERENCES companies (id);
    """,

    """CREATE INDEX IF NOT EXISTS y_earnings ON companies(yearly_earnings);
    """
]

migrate_down = [
    """DROP TABLE IF EXISTS employees;""",
    """DROP TABLE IF EXISTS companies;""",
    """DROP TABLE IF EXISTS countries;"""
]

db = psycopg2.connect(
    database=DB_CONFIG['database'],
    user=DB_CONFIG['user'],
    password=DB_CONFIG['password'],
    host=DB_CONFIG['host'],
    port=DB_CONFIG['port']
)

def InitializeDB():
    cursor = db.cursor()
    for tx in migrate_up:
        cursor.execute(tx)
    db.commit()

def RevertDB():
    cursor = db.cursor()
    for tx in migrate_down:
        cursor.execute(tx)
    db.commit()

# to check if tables exist during development
def SelectTables():
    cursor = db.cursor()
    cursor.execute("""SELECT * FROM information_schema.tables WHERE table_schema = 'public';""")
    print(cursor.fetchall())

def CloseConn():
    db.commit()
    db.close()

# function to insert data into countries table (accepts list of tuples) 
def InsertToCountries(records):
    cursor = db.cursor()
    query = """INSERT INTO countries (
    id,
    name,
    region,
    yearly_gdp,
    population
    ) values %s"""
    execute_values(cursor, query, records)

# function to insert data into companies table (accepts list of tuples)
def InsertToCompanies(records):
    cursor = db.cursor()
    query = """INSERT INTO companies (
    id,
    name,
    country_id,
    sector,
    q1_earnings,
    q2_earnings,
    q3_earnings,
    q4_earnings,
    yearly_earnings,
    employee_count,
    employee_payroll
    ) values %s"""
    execute_values(cursor, query, records)

# function to insert data into employees table (accepts list of tuples)
def InsertToEmployees(records):
    cursor = db.cursor()
    query = """INSERT INTO employees (
    id_number,
    ssn,
    first_name,
    last_name,
    date_of_birth,
    company_id,
    email,
    phone_no,
    salary,
    nationality,
    sector
    ) values %s"""
    execute_values(cursor, query, records)