import requests
from bs4 import BeautifulSoup
import re
import os
import pandas as pd

headers = {"User-Agent": "Mozilla/5.0"}
history_file = "hays_job_history.xlsx"

# Load existing Excel history (if exists)
if os.path.exists(history_file):
    df_history = pd.read_excel(history_file)
    seen_titles = set(df_history['Title'].dropna().tolist())
else:
    df_history = pd.DataFrame(columns=[
        "Type", "Title", "Company", "Location", "Posted On", "Details", "Link"
    ])
    seen_titles = set()

# URLs for Finance and IT
urls = {
    "Finance": (
        "https://www.hays.de/en/jobsearch/job-offers/"
        "s/Finance/3/c/Germany/D1641BCE-D56C-11D3-AFB2-00105AB00B48/"
        "i/Banks-saving-banks-financial-service-providers/"
        "6E7A1D11-89E8-DE11-BAE0-0007E92E2CEA/p/1?q=&e=false&pt=false"
    ),
    "IT": (
        "https://www.hays.de/en/jobsearch/job-offers/"
        "s/IT/1/c/Germany/D1641BCE-D56C-11D3-AFB2-00105AB00B48/"
        "i/Software-DP-IT-services/"
        "D2361F07-89E8-DE11-BAE0-0007E92E2CEA/p/1?q=&e=false&pt=false"
    )
}

new_records = []

for job_type in ["Finance", "IT"]:
    print(f"\n📰 {job_type} related jobs:\n")
    url = urls[job_type]
    resp = requests.get(url, headers=headers)

    if not resp.ok:
        print(f"❌ Failed to load {job_type} page 1 (status {resp.status_code})")
        continue

    soup = BeautifulSoup(resp.content, "html.parser")
    cards = soup.find_all("div", class_="search__result")
    if not cards:
        print(f"⚠️ No {job_type} jobs found.")
        continue

    for job in cards:
        t = job.find("h4", class_="search__result__header__title")
        title = t.get_text(strip=True) if t else "N/A"

        if title in seen_titles:
            continue  # Skip if already exists

        div = job.find("div", class_="row", text=re.compile(r"Online since:"))
        posted_on = div.get_text(strip=True).replace("Online since:", "").strip() if div else "N/A"

        a = job.find("a", class_="search__result__link")
        link = a["href"] if (a and a.has_attr("href")) else ""
        if link and not link.startswith("http"):
            link = "https://www.hays.de" + link

        ct = job.find("div", class_="search__result__job__attribute__type")
        company = ct.find("div", class_="info-text").get_text(strip=True) if ct else "N/A"
        lt = job.find("div", class_="search__result__job__attribute__location")
        location = lt.find("div", class_="info-text").get_text(strip=True) if lt else "N/A"

        bullets = job.select("div.h-text ul li")
        details = " | ".join([b.get_text(strip=True) for b in bullets])  # single-line

        # Display
        print("=" * 80)
        print(f"Type      : {job_type}")
        print(f"Title     : {title}")
        print(f"Company   : {company}")
        print(f"Location  : {location}")
        print(f"Posted on : {posted_on}")
        print(f"Details   : {details}")
        print(f"Link      : {link}")
        print("=" * 80 + "\n")

        new_records.append({
            "Type": job_type,
            "Title": title,
            "Company": company,
            "Location": location,
            "Posted On": posted_on,
            "Details": details,
            "Link": link
        })

# Add new records to Excel
if new_records:
    df_new = pd.DataFrame(new_records)
    df_combined = pd.concat([df_history, df_new], ignore_index=True)
    df_combined.to_excel(history_file, index=False)
    print(f"\n✅ Added {len(new_records)} new job(s) to history file.")
else:
    print("\n✅ No new jobs found today.")
