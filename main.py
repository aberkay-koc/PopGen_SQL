from db import InitializeDB, RevertDB, SelectTables, CloseConn, InsertToCompanies, InsertToCountries
import pandas as pd

RevertDB()
InitializeDB()

# DATA MANIPULATION:
df_countries = pd.read_json("countries.json")
df_country1 = pd.read_json("country_1.json")
df_country2 = pd.read_json("country_2.json")
df_country3 = pd.read_json("country_3.json")

# Add country_id and calculate yearly earnings
dfs = [df_country1, df_country2, df_country3]
for i, df in enumerate(dfs, start= 1):
    df["country_id"] = i
    df["yearly_earnings"] = df[["q1_earnings", "q2_earnings", "q3_earnings", "q4_earnings"]].sum(axis=1)

#combining countries
df_countries_combined = pd.concat(dfs, ignore_index=True)
df_countries_combined["id"] = range(1, 31)

# Fill df_countries with aggregated earnings
for i in range(3):
    country_id = i + 1
    df_countries.iloc[i, 3] = df_countries_combined[df_countries_combined["country_id"] == country_id]["q1_earnings"].sum()
    df_countries.iloc[i, 4] = df_countries_combined[df_countries_combined["country_id"] == country_id]["q2_earnings"].sum()
    df_countries.iloc[i, 5] = df_countries_combined[df_countries_combined["country_id"] == country_id]["q3_earnings"].sum()
    df_countries.iloc[i, 6] = df_countries_combined[df_countries_combined["country_id"] == country_id]["q4_earnings"].sum()
    df_countries.iloc[i, 7] = df_countries_combined[df_countries_combined["country_id"] == country_id]["yearly_earnings"].sum()

# Rename countries
df_countries.loc[df_countries["id"] == 1, "country_name"] = "Country A"
df_countries.loc[df_countries["id"] == 2, "country_name"] = "Country B"
df_countries.loc[df_countries["id"] == 3, "country_name"] = "Country C"

print(df_countries.head())
print(df_countries_combined.head())




countries_records = list(df_countries.itertuples(index=False, name=None))
InsertToCountries(countries_records)

companies_records = list(df_countries_combined.itertuples(index=False, name=None))
InsertToCompanies(companies_records)

CloseConn()