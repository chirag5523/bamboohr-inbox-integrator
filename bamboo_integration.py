import requests
import json
from datetime import datetime
import pandas as pd

def BambooHR_GetReport(domain, API_KEY, ReportID):
    url = f"https://api.bamboohr.com/api/gateway.php/{domain}/v1/reports/{str(ReportID)}?format=json&onlyCurrent=false"
    
    headers = {
        "Accept": "application/json",
        "Authorization": f"Basic {API_KEY}"
    }
    
    response = requests.request("GET", url, headers=headers)
    print(f"Report Status: {response.status_code}")
    
    # Parse the JSON response
    data = json.loads(response.text)
    return data

# --- Configuration (Anonymized) ---
# Replace these with your actual keys and domain names
API_KEY_MAIN = 'REPLACE_WITH_API_KEY_1'
API_KEY_SUB = 'REPLACE_WITH_API_KEY_2'
DOMAIN_MAIN = 'yourcompany'
DOMAIN_SUB = 'yourcompanysub'

number_of_iterations = 1
starting_number = 10

# --- Section 1: Main Domain Processing ---
headers_main = {
    "Accept": "application/json",
    "Authorization": f"Basic {API_KEY_MAIN}"
}

pb_final_df = pd.DataFrame()

for i in range(number_of_iterations):
    url = f"https://api.bamboohr.com/api/gateway.php/{DOMAIN_MAIN}/v1/inbox/?assigned=all&limit=50000"
    
    try:
        response = requests.get(url, headers=headers_main)
        print(f"{DOMAIN_MAIN} Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if 'items' in data:
                df = pd.json_normalize(data['items'])
                df['Company'] = 'Main Entity'
                pb_final_df = pd.concat([pb_final_df, df], ignore_index=True)
            else:
                print("No 'items' key in response")
        else:
            print(f"Request failed: {response.status_code}")
            
    except Exception as e:
        print(f"An error occurred: {e}")
        
    starting_number += 10
    print(f"Iteration {i+1} complete. Counter: {starting_number}")

# Clean up columns
cols_to_drop_pb = [c for c in pb_final_df.columns if c.startswith('timeOffRequest.dates.')]
pb_final_df = pb_final_df.drop(columns=cols_to_drop_pb)

# Enrich with Employee Report Data
# Using Report ID 363 as per original code
pb_job_raw = BambooHR_GetReport(DOMAIN_MAIN, API_KEY_MAIN, 363)
pb_job_data = pd.json_normalize(pb_job_raw['employees'])
pb_final_df = pd.merge(pb_final_df, pb_job_data, how='left', left_on='employeeId', right_on='id')


# --- Section 2: Sub-Domain Processing ---
headers_sub = {
    "Accept": "application/json",
    "Authorization": f"Basic {API_KEY_SUB}"
}

pbm_final_df = pd.DataFrame()

for i in range(number_of_iterations):
    url = f"https://api.bamboohr.com/api/gateway.php/{DOMAIN_SUB}/v1/inbox/?assigned=all&limit=50000"
    
    try:
        response = requests.get(url, headers=headers_sub)
        print(f"{DOMAIN_SUB} Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if 'items' in data:
                df = pd.json_normalize(data['items'])
                df['Company'] = 'Sub Entity'
                pbm_final_df = pd.concat([pbm_final_df, df], ignore_index=True)
            else:
                print("No 'items' key in response")
    except Exception as e:
        print(f"An error occurred: {e}")
        
    starting_number += 10

# Clean up columns
cols_to_drop_pbm = [c for c in pbm_final_df.columns if c.startswith('timeOffRequest.dates.')]
pbm_final_df = pbm_final_df.drop(columns=cols_to_drop_pbm)

# Enrich with Employee Report Data
# Using Report ID 318 as per original code
pbm_job_raw = BambooHR_GetReport(DOMAIN_SUB, API_KEY_SUB, 318)
pbm_job_data = pd.json_normalize(pbm_job_raw['employees'])
pbm_final_df = pd.merge(pbm_final_df, pbm_job_data, how='left', left_on='employeeId', right_on='id')


# --- Final Merge and Export ---
final_df = pd.concat([pbm_final_df, pb_final_df], ignore_index=True)

try:
    final_df.to_excel('BambooHR_Combined_Data.xlsx', index=False)
    print("Process complete. File saved as BambooHR_Combined_Data.xlsx")
except Exception as e:
    print(f"Could not save Excel file: {e}")