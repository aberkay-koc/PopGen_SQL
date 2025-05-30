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
    id INT UNIQUE PRIMARY KEY,
    name VARCHAR(72),
    population INT CHECK (population>0),
    q1_gdp DECIMAL CHECK (q1_gdp>=0),
    q2_gdp DECIMAL CHECK (q2_gdp>=0),
    q3_gdp DECIMAL CHECK (q3_gdp>=0),
    q4_gdp DECIMAL CHECK (q4_gdp>=0),
    yearly_gdp DECIMAL CHECK (yearly_gdp>=0)
    );""",

    """CREATE TABLE IF NOT EXISTS companies (
    id INT PRIMARY KEY,
    name VARCHAR,
    employee_count INT CHECK (employee_count>0),
    q1_earnings DECIMAL CHECK (q1_earnings>=0),
    q2_earnings DECIMAL CHECK (q2_earnings>=0),
    q3_earnings DECIMAL CHECK (q3_earnings>=0),
    q4_earnings DECIMAL CHECK (q4_earnings>=0),
    yearly_earnings DECIMAL CHECK (yearly_earnings>=0),
    country_id INT
    );""",

    """ALTER TABLE companies ADD FOREIGN KEY (country_id) REFERENCES countries (id);
    """

    """CREATE INDEX IF NOT EXISTS y_earnings ON companies(yearly_earnings);
    """
]

migrate_down = [
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
    population,
    q1_gdp,
    q2_gdp,
    q3_gdp,
    q4_gdp,
    yearly_gdp
    ) values %s"""
    execute_values(cursor, query, records)

# function to insert data into companies table (accepts list of tuples)
def InsertToCompanies(records):
    cursor = db.cursor()
    query = """INSERT INTO companies (
    id,
    name,
    employee_count,
    q1_earnings,
    q2_earnings,
    q3_earnings,
    q4_earnings,
    yearly_earnings,
    country_id
    ) values %s"""
    execute_values(cursor, query, records)