import pandas as pd

# === Load Data ===
open_log = pd.read_csv("open_log_test.csv", names=["Timestamp", "Email", "UID", "Status"], skiprows=1)
click_log = pd.read_csv("click_log.csv", names=["Timestamp", "Email", "Status"], skiprows=1)

# Get unique email lists
opens = set(open_log["Email"])
clicks = set(click_log["Email"])

# Load full email list (from campaign file)
df = pd.read_excel("full_icp_results.xlsx")

statuses = []

# === Categorize Leads ===
for email in df["Email"]:
    if email in opens and email in clicks:
        statuses.append("Hot")     # Opened + Clicked
    elif email in opens:
        statuses.append("Warm")    # Only Opened
    else:
        statuses.append("Cold")    # No interaction
df["Status"] = statuses

# === Metrics ===
total = len(df)
opened = len(opens)
clicked = len(clicks)
hot = statuses.count("Hot")
cold = statuses.count("Cold")

# === Report ===
print("\n📊 Campaign Analytics:")
print(f"Total Emails Sent:      {total}")
print(f"Unique Opens:           {opened}")
print(f"Open Rate:              {opened / total:.0%}")
print(f"Unique Clicks:          {clicked}")
print(f"Click-through Rate:     {clicked / total:.0%}")
print(f"Hot Leads (Clicked):    {hot}")
print(f"Cold Leads (No action): {cold}")

# === Save Detailed Lead Report ===
df.to_csv("lead_report.csv", index=False)
print("\n✅ Saved full report to lead_report.csv")
