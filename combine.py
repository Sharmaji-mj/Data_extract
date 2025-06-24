from selenium import webdriver
import pandas as pd
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import datetime
import os

# Dates
t_day = datetime.datetime.now()
if t_day.weekday() == 0:  # Monday

    yesterday = (t_day - datetime.timedelta(days=3)).date()
else:

    yesterday = (t_day - datetime.timedelta(days=1)).date()


# Headless Chrome for server use
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")

def fetch_tenders(url, yesterday, cpv_name):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get(url)
    time.sleep(10)

    rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")
    data = []
    for row in rows:
        cols = row.find_elements(By.TAG_NAME, "td")
        if cols and len(cols) >= 5:
            notice_elem = cols[1].find_element(By.TAG_NAME, "a")
            notice_number = notice_elem.text.strip()
            notice_link = notice_elem.get_attribute("href")
            description = cols[2].text.strip()
            country = cols[3].text.strip()
            publication_date_str = cols[4].text.strip()
            try:
                deadline = cols[5].text.strip()
            except IndexError:
                deadline = ""

            publication_date = datetime.datetime.strptime(publication_date_str, "%d/%m/%Y").date()
            if publication_date == yesterday:
                di={
                    "Notice Number": notice_number,
                    "Link": notice_link,
                    "Description": description,
                    "Country": country,
                    "Publication Date": publication_date_str,
                    "Deadline": deadline,
                    "CPV Group": cpv_name
                }
                data.append(di)
                

    driver.quit()
    return pd.DataFrame(data)

# URL params
yr = t_day.strftime("%Y")
mt = t_day.strftime("%m")

url_it = f"https://ted.europa.eu/en/search/result?search-scope=ACTIVE&scope=ACTIVE&onlyLatestVersions=false&facet.cpv=comp%2C72000000&facet.contract-nature=services&facet.place-of-performance=SPCY%2CDEU&facet.publication-date={yr}%2C{mt}&sortColumn=publication-number&sortOrder=DESC&page=1"

url_fin = f"https://ted.europa.eu/en/search/result?search-scope=ACTIVE&scope=ACTIVE&onlyLatestVersions=false&facet.cpv=fina&facet.contract-nature=services&facet.place-of-performance=SPCY%2CDEU&facet.publication-date={yr}%2C{mt}&sortColumn=publication-number&sortOrder=DESC&page=1"

# Scrape both
df_it = fetch_tenders(url_it, yesterday, "IT/Consulting")

df_fin = fetch_tenders(url_fin, yesterday, "Financial Services")

# Combine
df_all = pd.concat([df_it, df_fin], ignore_index=True)


# Update history file
history_file = "tender_history.xlsx"
if os.path.exists(history_file):
    df_history = pd.read_excel(history_file)
    df_updated = pd.concat([df_history, df_all], ignore_index=True)
    df_updated = df_updated.drop_duplicates(subset=["Notice Number"])
else:
    df_updated = df_all

df_updated.to_excel(history_file, index=False)


if df_all.empty:
    print("No new tender")
else:
    for index, row in df_all.iterrows():
        print("=" * 100)
        print(f"Notice Number   : {row['Notice Number']}")
        print(f"Link            : {row['Link']}")
        print(f"Description     : {row['Description']}")
        print(f"Country         : {row['Country']}")
        print(f"Publication Date: {row['Publication Date']}")
        print(f"Deadline        : {row['Deadline']}")
        print(f"CPV Group       : {row['CPV Group']}")
        print("=" * 100)
        print("\n")





    

