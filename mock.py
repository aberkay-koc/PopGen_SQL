from faker import Faker
import random
import json

fake = Faker()

sectors = ["Technology", "Healthcare", "Finance", "Education", "Retail", "Manufacturing"]
country_names = ["Country A", "Country B", "Country C", "Country D", "Country E", "Country F", "Country G", "Country H", "Country J", "Country K"]
regions = ["North America", "South America", "Europe"]

# Generating mock tabular data for countries
def GenerateCountries():
    country_data = []

    for i,country_name in enumerate(country_names):
        row = {
            "Country ID": i + 1,
            "Country Name": country_name,
            "Region": random.choice(regions),
        }
        country_data.append(row)
    return country_data

# Generating mock tabular data for companies
def GenerateCompanies(country_num):
    company_data = []

    for i in range(150):
        row = {
            "Company ID": i + 1,
            "Company Name": fake.company(),
            "Country ID": fake.pyint(min_value=1, max_value=country_num),
            "Sector": random.choice(sectors),
            "Q1 Earnings": fake.pyint(min_value=1000000, max_value=10000000),
            "Q2 Earnings": fake.pyint(min_value=1000000, max_value=10000000),
            "Q3 Earnings": fake.pyint(min_value=1000000, max_value=10000000),
            "Q4 Earnings": fake.pyint(min_value=1000000, max_value=10000000)
        }
        company_data.append(row)
    return company_data

# Generating mock tabular data for employees
def GenerateEmployees(company_num, country_num):
    employee_data = []

    for _ in range(10000): #number of rows
        
        if fake.pyint(min_value=1, max_value=20) > 1:  #lets say roughly 5% is unemployed
            row = {
                "ID Number": fake.unique.random_int(min=10000000000, max=99999999999),
                "SSN": fake.ssn(),     
                "First Name": fake.first_name(),
                "Last Name": fake.last_name(),
                "Date of Birth": str(fake.date_of_birth(minimum_age=18, maximum_age=65)),
                "Company ID": fake.pyint(min_value=1, max_value=company_num),
                "Email": fake.email(),
                "Phone": fake.msisdn(),
                "Salary": random.randint(30000, 150000),
                "Nationality": fake.pyint(min_value=1, max_value=country_num),
                "Sector": random.choice(sectors)
            }
            employee_data.append(row)
        else:
            row = {
                "ID Number": fake.unique.random_int(min=10000000000, max=99999999999),
                "SSN": fake.ssn(),     
                "First Name": fake.first_name(),
                "Last Name": fake.last_name(),
                "Date of Birth": str(fake.date_of_birth(minimum_age=18, maximum_age=65)),
                "Company ID": None,
                "Email": fake.email(),
                "Phone": fake.msisdn(),
                "Salary": 0,
                "Nationality": fake.pyint(min_value=1, max_value=country_num),
                "Sector": random.choice(sectors)
            }
            employee_data.append(row)
    return employee_data

def GenerateJSON():
    country_data = GenerateCountries()
    with open("countries.json", "w") as f:
        f.write(json.dumps(country_data, indent=4))
    
    company_data = GenerateCompanies(len(country_data))
    with open("companies.json", "w") as f:
        f.write(json.dumps(company_data, indent=4))

    employee_data = GenerateEmployees(len(company_data), len(country_data))
    with open("employees.json", "w") as f:
        f.write(json.dumps(employee_data, indent=4))

GenerateJSON()




