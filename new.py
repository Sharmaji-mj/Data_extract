from selenium import webdriver
import pandas as pd
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import datetime
import os


# Headless Chrome for server use
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.binary_location = "/usr/bin/chromium"


driver = webdriver.Chrome(service=Service("/usr/bin/chromium"), options=chrome_options)

# === Open URL ===
url = "https://emagine.de/fuer-consultants/projekte/"
driver.get(url)
 
# === Handle cookie popup ===
try:
    wait = time.sleep(10)
 
    print("🔎 Waiting for cookie banner to be visible...")
    wait.until(EC.visibility_of_element_located((By.ID, "CybotCookiebotDialog")))
 
    print("🔎 Waiting for 'Alle zulassen' button to be clickable...")
    accept_btn = wait.until(EC.element_to_be_clickable((By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll")))
 
    print("🔘 Clicking 'Alle zulassen' button...")
    accept_btn.click()
 
    print("⏳ Waiting for cookie banner to disappear...")
    wait.until(EC.invisibility_of_element_located((By.ID, "CybotCookiebotDialog")))
 
    print("✅ Cookie banner accepted and closed.")
 
except Exception as e:
    print("❌ Cookie banner handling failed:", e)

