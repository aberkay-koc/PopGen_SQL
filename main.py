from db import InitializeDB, RevertDB, SelectTables, CloseConn, InsertToCompanies, InsertToCountries, InsertToEmployees
import pandas as pd
import numpy as np

RevertDB()
InitializeDB()


# DATA MANIPULATION:

df_countries = pd.read_json("countries.json")
df_companies = pd.read_json("companies.json")
df_employees = pd.read_json("employees.json")

# adding yearly profit column to companies
df_companies["Yearly Earnings"] = df_companies[["Q1 Earnings", "Q2 Earnings", "Q3 Earnings", "Q4 Earnings"]].sum(axis=1)

# adding GDP column to countries (GDP taken as aggregated yearly earnings of companies)
df_countries["GDP"] = df_countries["Country ID"].map(df_companies.groupby("Country ID")["Yearly Earnings"].sum()).fillna(0)

# adding population to countries
population_per_country = df_employees["Nationality"].value_counts()
df_countries["Population"] = df_countries["Country ID"].map(population_per_country).fillna(0).astype(int)

# adding employee count and employee payroll to companies
df_companies["Employee Count"] = df_companies["Company ID"].map(df_employees["Company ID"].value_counts()).fillna(0).astype(int)
df_companies["Employee Payroll"] = df_companies["Company ID"].map(df_employees.groupby("Company ID")["Salary"].sum()).fillna(0)

# changing nan values assigned by pandas to None for SQL integration (pyscopg2 recognizes None)
df_employees = df_employees.fillna(np.nan).replace([np.nan], [None])

countries_records = list(df_countries.itertuples(index=False, name=None))
InsertToCountries(countries_records)

companies_records = list(df_companies.itertuples(index=False, name=None))
InsertToCompanies(companies_records)

employees_records = list(df_employees.itertuples(index=False, name=None))
InsertToEmployees(employees_records)

CloseConn()