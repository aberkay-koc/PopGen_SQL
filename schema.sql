CREATE TABLE IF NOT EXISTS countries (
    id INT PRIMARY KEY,
    name VARCHAR(32) NOT NULL,
    region VARCHAR(32) NOT NULL,
    yearly_gdp DECIMAL CHECK (yearly_gdp>=0),
    population INT CHECK (population>=0)
    );

    CREATE TABLE IF NOT EXISTS companies (
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
    );

    CREATE TABLE IF NOT EXISTS employees (
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
    );

    ALTER TABLE companies ADD FOREIGN KEY (country_id) REFERENCES countries (id);
    
    ALTER TABLE employees ADD FOREIGN KEY (nationality) REFERENCES countries (id);
    
    ALTER TABLE employees ADD FOREIGN KEY (company_id) REFERENCES companies (id);
    

    CREATE INDEX IF NOT EXISTS y_earnings ON companies(yearly_earnings);
    