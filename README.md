
# Countries & Companies

This project is a Python-based application that manages and analyzes data related to countries, companies, and employees. It utilizes JSON files for data storage and provides functionalities to interact with and process this data.

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
