
This projects generates mock data and after some data manipulation using Python, inserts it into PostgreSQL database. I developed it to practice SQL queries. The sample SQL queries are listed below with my answers.

## Sample SQL Queries:

**1. You’ve been asked to identify underperforming companies. Define a metric/metrics for it and list the bottom 10 companies based on it.**

Earnings per employee
```sql
SELECT 
	cm.name AS company_name,
	ROUND((cm.yearly_earnings / COUNT(*)),2) AS earnings_per_emp
FROM employees AS e
JOIN companies AS cm ON cm.id = e.company_id
GROUP BY cm.id, cm.name, cm.yearly_earnings
HAVING COUNT(*) > 0
ORDER BY earnings_per_emp
LIMIT 10;
```

Overhead Percentage - Are payroll costs bloated vs. earnings?
```sql
SELECT
    cm.name AS company_name,
    ROUND((ts.total_salary / cm.yearly_earnings) * 100, 2) AS overhead_pct
FROM companies AS cm
JOIN (
    SELECT 
        company_id, 
        SUM(salary) AS total_salary
    FROM employees
    GROUP BY company_id
) AS ts ON cm.id = ts.company_id
WHERE cm.yearly_earnings > 0
ORDER BY overhead_pct DESC
LIMIT 10;
```
Rank based composite score: (This query creates an overall ranking of companies based on; low productivity, high payroll burden)
I combined the two metrics with 0.7(earnings_per_emp) and 0.3(overhead_pct) weights.
```sql
WITH earnings_per_emp AS (
    SELECT 
        cm.id,
        cm.name AS company_name,
        ROUND(cm.yearly_earnings / COUNT(e.id_number)) AS earnings_per_employee
    FROM companies AS cm
    JOIN employees AS e ON cm.id = e.company_id
    GROUP BY cm.id, cm.name, cm.yearly_earnings
),

overhead_pct AS (
    SELECT 
        cm.id,
        ROUND(SUM(e.salary) / cm.yearly_earnings * 100, 2) AS overhead_percentage
    FROM companies AS cm
    JOIN employees AS e ON cm.id = e.company_id
    WHERE cm.yearly_earnings > 0
    GROUP BY cm.id, cm.yearly_earnings
),

ranked AS (
    SELECT 
        epe.company_name,
        epe.earnings_per_employee,
        op.overhead_percentage,
        RANK() OVER (ORDER BY epe.earnings_per_employee ASC) AS earnings_rank,
        RANK() OVER (ORDER BY op.overhead_percentage DESC) AS overhead_rank
    FROM earnings_per_emp AS epe
    JOIN overhead_pct AS op ON epe.id = op.id
),

rank_limits AS (
    SELECT 
        MAX(earnings_rank) AS max_earnings_rank,
        MAX(overhead_rank) AS max_overhead_rank
    FROM ranked
),

weighted AS (
    SELECT 
        r.company_name,
        r.earnings_per_employee,
        r.overhead_percentage,
        ROUND(r.earnings_rank * 1.0 / rl.max_earnings_rank, 3)*100 AS earnings_score,
        ROUND(r.overhead_rank * 1.0 / rl.max_overhead_rank, 3)*100 AS overhead_score
    FROM ranked r
    CROSS JOIN rank_limits rl
)

SELECT 
    company_name,
    earnings_per_employee,
    overhead_percentage,
    earnings_score,
    overhead_score,
    ROUND((earnings_score * 0.7 + overhead_score * 0.3), 3) AS composite_score
FROM weighted
ORDER BY composite_score ASC
LIMIT 10;
```
### Resulting Table:
|company_name|earnings_per_employee|overhead_percentage|earnings_score|overhead_score                |composite_score|
|------------|---------------------|-------------------|--------------|------------------------------|---------------|
|Smith, Hall and Stewart|112503               |84.11              |0.700         |0.700                         |0.700          |
|Briggs Group|124192               |75.91              |1.300         |1.300                         |1.300          |
|Walsh Group |151461               |61.45              |2.000         |2.000                         |2.000          |
|Bailey, Buckley and Shepard|172532               |50.77              |2.700         |4.700                         |3.300          |
|Doyle-Jackson|175156               |52.92              |3.300         |3.300                         |3.300          |
|Goodman and Sons|180671               |53.22              |4.700         |2.700                         |4.100          |
|Reed-Flores |177474               |49.19              |4.000         |6.700                         |4.810          |
|Richards-Morrow|183911               |51.83              |6.000         |4.000                         |5.400          |
|White and Sons|181642               |50.33              |5.300         |6.000                         |5.510          |
|Sullivan, Taylor and Williams|189819               |50.44              |6.700         |5.300                         |6.280          |
g


**2. You are asked to generate a performance and workforce risk report for all companies. For each company, report:**

1. Company name and country
2. Total employee count
3. Average salary of employees
4. Earnings per employee
5. Payroll-to-earnings percentage
6. Flag companies with:
- High Payroll Risk if payroll/earnings > 70%
- Low Earnings per Employee if earnings per employee < 50,000
- Overloaded if employee count > 1000
7. Composite risk score: 1 point for each flag triggered
8. Rank all companies by risk score (highest risk first)
```sql
WITH employee_metrics AS (
    SELECT 
        e.company_id,
        COUNT(*) AS employee_count,
        AVG(e.salary) AS avg_salary,
        SUM(e.salary) AS total_payroll
    FROM employees e
    GROUP BY e.company_id
),

company_metrics AS (
    SELECT 
        c.id AS company_id,
        c.name AS company_name,
        co.name AS country,
        c.yearly_earnings,
        em.employee_count,
        em.avg_salary,
        em.total_payroll,
        ROUND(c.yearly_earnings / NULLIF(em.employee_count, 0), 2) AS earnings_per_employee,
        ROUND((em.total_payroll / NULLIF(c.yearly_earnings, 0)) * 100, 2) AS payroll_pct
    FROM companies c
    JOIN countries co ON co.id = c.country_id
    LEFT JOIN employee_metrics em ON c.id = em.company_id
),

risk_flags AS (
    SELECT 
        *,
        CASE WHEN payroll_pct > 70 THEN 'Yes' ELSE 'No' END AS high_payroll_risk,
        CASE WHEN earnings_per_employee < 50000 THEN 'Yes' ELSE 'No' END AS low_earnings_flag,
        CASE WHEN employee_count > 1000 THEN 'Yes' ELSE 'No' END AS overloaded_flag,
        -- Composite score: 1 point per risk
        (
            CASE WHEN payroll_pct > 70 THEN 1 ELSE 0 END +
            CASE WHEN earnings_per_employee < 50000 THEN 1 ELSE 0 END +
            CASE WHEN employee_count > 1000 THEN 1 ELSE 0 END
        ) AS risk_score
    FROM company_metrics
)

SELECT 
    company_name,
    country,
    employee_count,
    ROUND(avg_salary, 2) AS avg_salary,
    yearly_earnings,
    earnings_per_employee,
    payroll_pct,
    high_payroll_risk,
    low_earnings_flag,
    overloaded_flag,
    risk_score,
    RANK() OVER (ORDER BY risk_score DESC, payroll_pct DESC) AS risk_rank
FROM risk_flags
ORDER BY risk_score DESC, payroll_pct DESC
LIMIT 20;
```


**3. The HR team of Adams Inc wants to ensure fair pay. Find the 10 highest-paid employees and check whether their salaries are significantly higher than the average salary in their sector.**
```sql
SELECT 
    e.id_number,
    e.first_name,
    e.last_name,
    e.salary,
    cm.sector,
    AVG(e.salary) OVER (PARTITION BY cm.sector) AS avg_sector_salary,
    ROUND((e.salary / AVG(e.salary) OVER (PARTITION BY cm.sector)) * 100, 2) AS percent_of_avg
FROM employees e
JOIN companies cm ON e.company_id = cm.id
WHERE cm.name = 'Adams Inc'
ORDER BY e.salary DESC
LIMIT 10;
```


**4. A policymaker wants to understand how company performance relates to national GDP. Show a comparison between average company earnings and country GDP by region.**
```sql
SELECT
	c.region,
	ROUND(AVG(cm.yearly_earnings)) AS avg_comp_earnings,
	ROUND(AVG(c.yearly_gdp)) AS avg_country_gdp
FROM countries c
JOIN companies cm ON c.id = cm.country_id
GROUP BY c.region
ORDER BY c.region;
```
### Resulting Table:
|region       |avg_comp_earnings|avg_country_gdp|
|-------------|-----------------|---------------|
|Europe       |22617182         |464033024      |
|North America|21324279         |275484717      |
|South America|21182589         |370353825      |

Even though Europe, with its higher average GDP, also shows slightly higher company earnings pointing to a positive correlation between the two variables, the trend does not hold consistently leading to the conclusion that corporate earnings are not strictly proportional to GDP. While the Pearson R value comes out as 0.82 which would mean a strong positive correlation, the associated p-value comes out as 0.393 which tells that the correlation is not statistically significant. Most likely caused by the limited number of data points for region, 3, which reduces confidence in the robustness of the correlation.



**5. Identify all combinations of employees of natinality "Country A" and companies, even if the employee isn’t currently assigned to any company(unemployed).**
```sql
SELECT
	e.id_number,
	e.first_name,
	e.last_name,
	c.name AS nationality,
	cm.name AS company_name
FROM employees e
JOIN countries c ON c.id = e.nationality
LEFT JOIN companies cm ON cm.id = e.company_id
WHERE c.id = 1;
```
### Resulting Table:
|id_number  |first_name|last_name|nationality|company_name                  |
|-----------|----------|---------|-----------|------------------------------|
|36299713522|Molly     |Wells    |Country A  |Wilson, Dillon and Bolton     |
|22325518695|Kevin     |Marshall |Country A  |Lynch, Jenkins and Blankenship|
|23514958908|Alicia    |Hays     |Country A  |NULL                          |
|13727538969|William   |Contreras|Country A  |Smith LLC                     |
|66444557496|Sara      |May      |Country A  |Vaughn LLC                    |
.
.
.


**6. Payroll Risk Flagging - The company "Brown-Sandoval" wants you to flag the employees according to their salary levels.**
```sql
SELECT
	e.first_name || ' ' || e.last_name AS employee_name,
	c.name AS company_name,
	e.salary,
	CASE 
		WHEN salary > 100000 THEN 'High'
		WHEN salary BETWEEN 50001 AND 100000 THEN 'Medium'
		WHEN salary BETWEEN 1 AND 50000 THEN 'Low'
		WHEN salary = 0 THEN 'Unemployed'
		ELSE 'Unknown'
	END AS salary_level
FROM employees e
JOIN companies c ON c.id = e.company_id
WHERE c.name = 'Brown-Sandoval'
ORDER BY salary DESC;
```


**7. Which companies saw a significant drop in earnings in Q4 compared to Q3 (e.g., >30%)?**
```sql
SELECT
    name,
    q3_earnings,
    q4_earnings,
    ROUND(((q3_earnings - q4_earnings) / NULLIF(q3_earnings, 0)) * 100, 1) AS percentage_drop
FROM companies
WHERE 
    q3_earnings > 0 AND
    ((q3_earnings - q4_earnings) / q3_earnings) > 0.3
ORDER BY percentage_drop DESC;
```


**8. Identify employees who work in a company from a different country than their nationality.**
```sql 
SELECT 
	e.first_name, 
	e.last_name,
	cm.country_id,
	e.nationality
FROM employees AS e
JOIN companies AS cm ON cm.id = e.company_id
WHERE cm.country_id <> e.nationality;
```


**9. What is the average and median employee salaries in each region?**
```sql
SELECT 
	region, 
	ROUND(AVG(salary)), 
	PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY salary) AS median
FROM employees AS e
JOIN companies AS cm ON cm.id = e.company_id
JOIN countries AS c ON c.id = cm.country_id
WHERE salary IS NOT NULL
GROUP BY region;
```


**10. Which country has the highest earnings per capita (total company earnings ÷ population)?**
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


**11. Calculate the employee payroll as a percentage of yearly earnings for each company. Flag companies where it's more than 70%.**
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


**12. Find the average salary of employees per sector.**
```sql
SELECT cm.sector, ROUND(AVG(salary))
FROM companies AS cm
JOIN employees AS e ON cm.id = e.company_id
GROUP BY cm.sector;
```


**13. Get the names of top 10 companies by employee count.**
```sql
SELECT cm.name, COUNT(e.id_number) AS employee_count
FROM companies AS cm
JOIN employees AS e ON e.company_id = cm.id
GROUP BY cm.id, cm.name
ORDER BY employee_count DESC
LIMIT 10;
```


**14. How many companies are there in each country?**
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
