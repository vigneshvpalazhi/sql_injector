# SQL Injection Exploiter

## Overview

`sql_injection.py` is a Python script designed to automate the process of testing web applications for SQL injection vulnerabilities. By utilizing various SQL payloads, this script can help identify if a target application is susceptible to different types of SQL injection attacks.

## Features

- Tests for **Error-Based SQL Injection**
- Tests for **Boolean-Based Blind SQL Injection**
- Tests for **Time-Based Blind SQL Injection**
- Determines the **Number of Columns** in SQL queries
- Detects **Data Types** of columns
- Utilizes an expanded list of SQL injection payloads for comprehensive testing

## Requirements

- Python 3.x
- Required libraries:
  - `requests`
  - `colorama`

### Installation

You can install the required libraries using pip. Open your terminal and run:

```bash
pip install requests colorama



```
## Usage
To run the script, use the following command in your terminal:
```bash
python sql_injection.py <target_url>
```

Replace <target_url> with the URL you want to test for SQL injection vulnerabilities.

exapmle:python sql_injection.py http://example.com/vulnerable_page?id=1




## Script Details

### Main Functions

- **or_injection(url)**: Tests various OR-based payloads to identify error-based SQL injection.
- **error_based_injection(url)**: Checks for SQL injection by intentionally causing an error in the database.
- **order_injection(url)**: Determines the number of columns in the SQL query using the ORDER BY clause.
- **null_injection(url)**: Tests for the number of columns using a NULL-based injection technique.
- **detect_column_types(url, num_columns)**: Identifies the data types of each column in the SQL query.
- **boolean_blind_sql_injection(url)**: Tests for boolean-based blind SQL injection.
- **time_based_blind_sql_injection(url)**: Tests for time-based blind SQL injection.

### Payloads

The script contains a wide range of SQL injection payloads, including:

- Tautology-based payloads (e.g., `OR 1=1`)
- UNION-based payloads for data extraction
- Time-based payloads for blind SQL injection (e.g., `WAITFOR DELAY '0:0:5'`)



