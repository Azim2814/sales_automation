import json
import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from googlesearch import search

# ---------- SETTINGS ----------
COOKIES_FILE = "linkedin_cookies.json"
QUERY = "Fintech OR SaaS companies in Ahmedabad with 50-200 employees CTO OR CEO site:linkedin.com"
NUM_RESULTS = 15
OUTPUT_FILE = "full_icp_results.xlsx"
# ------------------------------

def load_cookies(driver, cookies_file):
    with open(cookies_file, 'r') as f:
        cookies = json.load(f)
    driver.get("https://www.linkedin.com")
    for cookie in cookies:
        cookie.pop("sameSite", None)
        cookie.pop("storeId", None)
        cookie.pop("id", None)
        try:
            driver.add_cookie(cookie)
        except Exception as e:
            print("Skipping cookie:", cookie.get("name"), "-", str(e))
    driver.get("https://www.linkedin.com/feed")

# def scrape_linkedin(driver, url):
#     driver.get(url)
#     time.sleep(3)
#     soup = BeautifulSoup(driver.page_source, 'html.parser')
#     data = {"URL": url}

#     if "/in/" in url:
#         data["Type"] = "Profile"
#         data["Name"] = soup.select_one("h1").text.strip() if soup.select_one("h1") else "N/A"
#         title_tag = soup.find("div", class_="text-body-medium")
#         data["Title"] = title_tag.text.strip() if title_tag else "N/A"
#         location_tag = soup.select_one("span.text-body-small")
#         data["Location"] = location_tag.text.strip() if location_tag else "N/A"
#         data["Company"] = "N/A"

#     elif "/company/" in url:
#         data["Type"] = "Company"
#         data["Name"] = "N/A"
#         data["Title"] = "N/A"
#         company_tag = soup.select_one("h1")
#         data["Company"] = company_tag.text.strip() if company_tag else "N/A"
#         loc_tag = soup.find("div", class_="org-top-card-summary-info-list__info-item")
#         data["Location"] = loc_tag.text.strip() if loc_tag else "N/A"
#     else:
#         data["Type"] = "Unknown"
#         data["Name"] = data["Title"] = data["Company"] = data["Location"] = "N/A"

#     return data
def scrape_linkedin(driver, url):
    driver.get(url)
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    data = {"URL": url}

    if "/in/" in url:
        data["Type"] = "Profile"
        data["Name"] = soup.select_one("h1").text.strip() if soup.select_one("h1") else "N/A"
        title_tag = soup.find("div", class_="text-body-medium")
        data["Title"] = title_tag.text.strip() if title_tag else "N/A"

        # Try to get company from Experience section
        company_tag = soup.find("span", class_="t-14 t-normal")
        data["Company"] = company_tag.text.strip() if company_tag else "N/A"

        # Location fix: skip 3rd degree label
        # location_tag = soup.find("span", string=lambda s: s and "degree connection" not in s)
        # data["Location"] = location_tag.text.strip() if location_tag else "N/A"

        location_tag = soup.find("span", class_="text-body-small inline t-black--light break-words")
        data["Location"] = location_tag.text.strip() if location_tag else "N/A"

    elif "/company/" in url:
        data["Type"] = "Company"
        data["Name"] = "N/A"
        data["Title"] = "N/A"
        company_tag = soup.select_one("h1")
        data["Company"] = company_tag.text.strip() if company_tag else "N/A"
        loc_tag = soup.find("div", class_="org-top-card-summary-info-list__info-item")
        data["Location"] = loc_tag.text.strip() if loc_tag else "N/A"
    else:
        data["Type"] = "Unknown"
        data["Name"] = data["Title"] = data["Company"] = data["Location"] = "N/A"

    return data


def main():
    print(f"🔍 Searching Google for: {QUERY}")
    linkedin_urls = list(search(QUERY, num_results=NUM_RESULTS))
    print(f"🔗 Found {len(linkedin_urls)} LinkedIn URLs")

    options = Options()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)

    print("🔐 Logging into LinkedIn...")
    load_cookies(driver, COOKIES_FILE)
    time.sleep(3)

    print("🕵️ Scraping LinkedIn profiles/companies...")
    all_data = []
    for url in linkedin_urls:
        print("➡️", url)
        try:
            data = scrape_linkedin(driver, url)
            all_data.append(data)
        except Exception as e:
            print("❌ Error scraping", url, "-", str(e))

    driver.quit()

    print("💾 Saving to Excel...")
    df = pd.DataFrame(all_data)
    df.to_excel(OUTPUT_FILE, index=False)
    print(f"✅ Done! Data saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
