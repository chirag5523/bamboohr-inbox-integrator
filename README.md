# 🎋 BambooHR Inbox & Report Integrator

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Pandas](https://img.shields.io/badge/data-pandas-orange)

## 📖 Overview
Managing multiple BambooHR instances can be time-consuming. This tool automates the process of fetching **Inbox Items** (tasks/approvals) from different BambooHR domains and merging them with detailed **Employee Report Data**. 

The result is a single, clean PowerBI-ready Excel file containing consolidated data from across the organization.

### Key Features
* **Multi-Domain Support:** Seamlessly switches between different company domains (e.g., Main Entity and Mortgages).
* **Automated Merging:** Automatically joins inbox tasks with employee metadata (names, departments, etc.) using the `employeeId`.
* **Data Cleaning:** Dynamically identifies and removes complex nested JSON columns (like `timeOffRequest.dates`) to keep the output human-readable.
* **Security First:** Utilizes environment variables (`.env`) to ensure API keys are never hardcoded or exposed.

---

## 🛠️ Project Structure

```text
bamboohr-inbox-integrator/
├── .env                # Secret API keys (DO NOT COMMIT)
├── .gitignore          # Prevents sensitive files from being uploaded
├── README.md           # Documentation
├── requirements.txt    # Required Python libraries
└── main.py             # Core automation script

🚀 Getting Started
1. Prerequisites

    Python 3.8 or higher.

    API Access to BambooHR (you will need a personal API Key for each domain).

2. Installation

Clone the repository to your local machine:
Bash

git clone [https://github.com/your-username/bamboohr-integrator.git](https://github.com/your-username/bamboohr-integrator.git)
cd bamboohr-integrator

Install the required dependencies:
Bash

pip install -r requirements.txt

3. Configuration

Create a .env file in the root directory and add your credentials:
Plaintext

PB_API_KEY=your_base64_encoded_key_1
PBM_API_KEY=your_base64_encoded_key_2
PB_DOMAIN=purplebricks
PBM_DOMAIN=purplebricksmortgages

Note: BambooHR API keys are usually provided as a string that you should encode to Base64 (or use as provided by your admin).

⚙️ How It Works

    Authentication: The script loads keys from the .env file and sets up the Basic Auth headers.

    Extraction: It sends a GET request to the /v1/inbox endpoint to find all assigned tasks.

    Normalization: The nested JSON response is flattened into a Pandas DataFrame.

    Enrichment: The script calls a custom BambooHR Report (via Report ID) to get specific employee details.

    Joining: It performs a left merge on the employeeId to attach names and job titles to the inbox tasks.

    Output: All company data is concatenated and exported to BambooHR_Combined_Data.xlsx.

📊 Data Output Example

The final Excel file includes: | Company | Task Type | employeeId | Full Name | Department | Status | | :--- | :--- | :--- | :--- | :--- | :--- | | Purplebricks | Time Off | 1024 | Jane Doe | Finance | Pending | | PBM | Onboarding | 2055 | John Smith | Sales | In Progress |

🔒 Security

This project uses a .gitignore file to ensure that the .env file is never pushed to GitHub. Always keep your API keys private. If you believe your keys have been compromised, rotate them immediately in the BambooHR settings.
