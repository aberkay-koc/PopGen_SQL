
This projects generates mock data and after some data manipulation using Python, inserts it into PostgreSQL database. I developed it to practice SQL queries. The sample SQL queries are listed below with my answers.

## Sample SQL Queries:

14. Which country has the highest earnings per capita (total company earnings ÷ population)?
```sql
SELECT c.name, (total_earnings/population) AS earnings_per_capita
FROM countries AS c
JOIN (SELECT country_id, SUM(yearly_earnings) AS total_earnings
	  FROM companies AS cm
	  GROUP BY country_id) AS y
ON c.id = y.country_id 
ORDER BY earnings_per_capita DESC
LIMIT 1;
```

15. Calculate the employee payroll as a percentage of yearly earnings for each company. Flag companies where it's more than 70%.
```sql
SELECT name, (total_payroll/yearly_earnings * 100) AS payroll_percentage
FROM companies AS cm 
JOIN (SELECT company_id, SUM(salary) AS total_payroll
	  FROM employees
	  GROUP BY company_id 
	  ) AS p ON cm.id = p.company_id
WHERE yearly_earnings > 0
 AND (total_payroll/yearly_earnings * 100) > 70;
```

16. Find the average salary of employees per sector.
```sql
SELECT cm.sector, ROUND(AVG(salary))
FROM companies AS cm
JOIN employees AS e ON cm.id = e.company_id
GROUP BY cm.sector;
```

17. Get the names of top 10 companies by employee count.
```sql
SELECT cm.name, COUNT(e.id_number) AS employee_count
FROM companies AS cm
JOIN employees AS e ON e.company_id = cm.id
GROUP BY cm.id, cm.name
ORDER BY employee_count DESC
LIMIT 10;
```

18. How many companies are there in each country?
```sql
SELECT c.name  AS country_name, COUNT(cm.id) AS company_count
FROM countries AS c
JOIN companies AS cm ON cm.country_id = c.id
GROUP BY c.id, c.name
ORDER BY country_name;
```

# Countries & Companies

This project is a Python-based application that generates, manages and analyzes data related to countries, companies, and employees. It utilizes JSON files for data storage and provides functionalities to interact with and process this data. Purpose of this project was to create data, insert it into SQL database and use this database to practice SQL queries. 

## Features

- Load and parse data from JSON files: `countries.json`, `companies.json`, and `employees.json`.
- Perform data analysis and manipulation using Python scripts.
- Mock data generation for testing purposes via `mock.py`.
- Database interactions handled through `db.py`.
- Main application logic encapsulated in `main.py`.

## Getting Started

All requirements are in requirement.txt

### Prerequisites

- Python 3.7 or higher
- Recommended: Create a virtual environment to manage dependencies.

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/aberkay-koc/countries_companies.git
   cd countries_companies
   ```

2. **Create and activate a virtual environment (optional but recommended):**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install the required dependencies:**

   ```bash
   pip install -r requirements.txt
   ```
4. **Create a .env file to connect to your PostgreSQL database:**

   ```bash
   DB_NAME=
   DB_USERNAME=
   DB_PASSWORD=
   DB_HOST=
   DB_PORT=
   ```

## Usage

- **Generate mock data:**

  ```bash
  python mock.py
  ```

  This script will create JSON files with mock data entries (10,000 employees / 150 companies / 10 countries).

  - **Run the main application:**

  ```bash
  python main.py
  ```

  This will execute the primary logic defined in `main.py`, which includes data manipulation, and insertion to PostgreSQL using functions in `db.py`.

## Project Structure

```plaintext
countries_companies/
├── countries.json       # Data file containing country information
├── companies.json       # Data file containing company information
├── employees.json       # Data file containing employee information
├── db.py                # Module for database interactions
├── main.py              # Main application script
├── mock.py              # Script for generating mock data
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
```
