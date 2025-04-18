📌 Project: AI-Powered Sales Automation & Email Tracking
🚀 Overview
This project automates the sales outreach process by:

Extracting leads from LinkedIn based on an Ideal Customer Profile (ICP)

Sending personalized email campaigns in bulk

Tracking real-time engagement (opens & clicks)

Categorizing leads (Hot/Warm/Cold) with analytics


## 📺 Demo Video

🎥 [Click here to watch the full demo on Loom](https://www.loom.com/share/3e55235d44074d00904fd14311d56c23?sid=6f7dc354-55d3-4b80-bbec-6d782dcb6ad6)




🧩 Tasks Breakdown
✅ Task 1: Scraping Based on ICP
ICP Defined: Fintech or SaaS companies in Ahmedabad, roles like CTO/CEO, size 50–200

Used Python with requests, BeautifulSoup, and Google search techniques

Extracted: Company Name, Website, Industry, Location, Contact Name

✅ Task 2: Export to Excel
Used pandas and openpyxl to export scraped data to full_icp_results.xlsx

✅ Task 3: HTML Email Template
Created dynamic email template with Jinja2

Injected placeholders like {{Name}}, {{Company}}, {{UID}}

Included tracking pixel and CTA button

✅ Task 4: Automated Email Sending
Sent emails in batch using multiple Gmail IDs with yagmail

Added delay and rotation to avoid spam detection

Automatically embedded tracking pixel in each email

✅ Task 5: Email Tracking Backend
Built a Flask app with endpoints:

/track/open → logs email opens

/track/click → logs link clicks

Logs saved in open_log_test.csv and click_log.csv

✅ Task 6: Analytics Reporting
Wrote script generate_report.py that:

Parses CSV logs

Calculates open rate, CTR, and lead status

Exports full lead report to lead_report.csv

✅ Task 7: Documentation
This file (README.md) explains each step, tools used, and automation logic

Project is publicly hosted via Render for real-time tracking

🛠️ Tools & Libraries Used
Python

Libraries: pandas, beautifulsoup4, yagmail, jinja2, openpyxl, Flask, gunicorn

Deployment: Render.com

Tracking: 1x1 transparent pixel + Flask server

Data Handling: Excel + CSV logs

📊 AI/ML Skills Applied
While the core logic is automation-driven, the project mimics a lead qualification pipeline:

Data structuring for ICP filtering

Engagement-based lead scoring (hot/warm/cold)

Dynamic content generation via Jinja2

✅ How to Run
Clone the repo and install requirements:

pip install -r requirements.txt
Run the email sender:

python email_sender.py

Run the analytics:
python generate_report.py
View/download engagement logs:

Open Log

Click Log

📁 Files Overview

File	Description
tracker.py	Flask server to track opens/clicks
email_sender.py	Email sending automation
generate_report.py	Analytics & lead categorization
email_template.html	Dynamic email body (with pixel)
requirements.txt	Python dependencies
open_log_test.csv	Tracks email opens
click_log.csv	Tracks CTA link clicks
lead_report.csv	Final categorized leads
✅ Final Output
A fully automated, trackable sales outreach system that:

Targets leads based on a defined ICP

Sends emails with tracking pixels

Monitors engagement and generates lead status
