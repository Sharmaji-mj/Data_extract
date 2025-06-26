from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import pandas as pd
import os

HISTORY_FILE = "Questax_project_history.xlsx"

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.binary_location = "/usr/bin/chromium"
    return  webdriver.Chrome(service=Service("/usr/bin/chromedriver"), options=chrome_options)


def scroll_to_load_all(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def load_existing_history():
    if os.path.exists(HISTORY_FILE):
        return pd.read_excel(HISTORY_FILE)
    else:
        return pd.DataFrame(columns=["Project ID", "Title", "Link"])

def save_history(df):
    df.to_excel(HISTORY_FILE, index=False)

def scrape_all_projects():
    existing_df = load_existing_history()
    existing_ids = set(existing_df["Project ID"].astype(str))

    driver = setup_driver()
    new_projects = []
    try:
        driver.get("https://questax.com/projektportal/#")
        time.sleep(4)

        scroll_to_load_all(driver)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a.job.load"))
        )

        soup = BeautifulSoup(driver.page_source, "html.parser")
        project_cards = soup.select("a.job.load")

        print(f"\n📦 Checking for New Projects...\n")

        for card in project_cards:
            title_tag = card.find("h3", class_="bold")
            title = title_tag.get_text(strip=True) if title_tag else "N/A"
            project_id = str(card.get("data-id_job", "N/A"))
            link = f"https://questax.com/projektportal/#id-{project_id}"

            if project_id not in existing_ids:
                print("=" * 100)
                print(f"Title     : {title}")
                print(f"Project ID: {project_id}")
                print(f"Link      : {link}")
                print("=" * 100)
                print("\n")

                new_projects.append({
                    "Project ID": project_id,
                    "Title": title,
                    "Link": link
                })
            else:
                continue  # Skip already saved project

    finally:
        driver.quit()

    # Append new projects to history and save
    if new_projects:
        updated_df = pd.concat([existing_df, pd.DataFrame(new_projects)], ignore_index=True)
        save_history(updated_df)
        print(f"\n✅ {len(new_projects)} new projects saved to '{HISTORY_FILE}'.")
    else:
        print("\n📭 No new projects found.")

# Run the script
scrape_all_projects()
