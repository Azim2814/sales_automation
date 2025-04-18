import pandas as pd
import time
import random
from jinja2 import Environment, FileSystemLoader
import yagmail
import uuid

# === CONFIG ===
EMAIL_ACCOUNTS = [
    {"email": "azimnathani806@gmail.com", "app_password": "ykgh axre mbzk esfo"},
    {"email": "memonazim7862@gmail.com", "app_password": "afqrwmufxlcpcvsy"}
    # Add more if needed
]

TEMPLATE_FILE = "email_template.html"
EXCEL_FILE = "full_icp_results.xlsx"
BATCH_SIZE = 5
EMAIL_COLUMN = "Email"  # Ensure this column exists in your Excel!
# ==============

# Load leads
df = pd.read_excel(EXCEL_FILE)
df.dropna(subset=[EMAIL_COLUMN], inplace=True)

# Load template
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template(TEMPLATE_FILE)

# Setup counters
account_index = 0
batch_count = 0

# Loop through leads
for i, row in df.iterrows():
    # Switch account after every BATCH_SIZE emails
    if batch_count % BATCH_SIZE == 0:
        creds = EMAIL_ACCOUNTS[account_index % len(EMAIL_ACCOUNTS)]
        yag = yagmail.SMTP(creds["email"], creds["app_password"])
        account_index += 1
        print(f"\n🔄 Switched to: {creds['email']}")

    context = {
        "Name": str(row.get("Name", "there") or "there"),
        "Company": str(row.get("Company", "your company") or "your company"),
        "Title": str(row.get("Title", "Executive") or "Executive"),
        "Location": str(row.get("Location", "your area") or "your area"),
        "SenderName": "Azim Memon",
        "SenderCompany": "Nathani",  # replace with yours
        "SenderEmail": "azimnathani806@gmail.com",
        "Email": row["Email"],
        "UID": str(uuid.uuid4())
    }

    html = template.render(context)
    subject = f"Helping {context['Company']} grow with automation 🚀"
    to_email = row[EMAIL_COLUMN]

    print(f"📤 Sending to: {to_email} | From: {creds['email']}")
    try:
        yag.send(to=to_email, subject=subject, contents=html)
        time.sleep(random.uniform(5, 12))  # 💤 Randomized delay between emails
    except Exception as e:
        print(f"❌ Failed to send to {to_email}: {e}")

    batch_count += 1

print("\n✅ Campaign finished.")
