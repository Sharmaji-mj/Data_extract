from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd 

# Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.binary_location = "/usr/bin/chromium"

# Use correct chromedriver path
driver = webdriver.Chrome(service=Service("/usr/bin/chromedriver"), options=chrome_options)

# Open website
url = "https://emagine.de/fuer-consultants/projekte/"
driver.get(url)

# Handle cookie banner
try:
    wait = WebDriverWait(driver, 10)

    print("🔎 Waiting for cookie banner to be visible...")
    wait.until(EC.visibility_of_element_located((By.ID, "CybotCookiebotDialog")))
 
    print("🔎 Waiting for 'Alle zulassen' button to be clickable...")
    accept_btn = wait.until(EC.element_to_be_clickable((By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll")))
 
    print("🔘 Clicking 'Alle zulassen' button...")
    accept_btn.click()
 
    print("👍👍 Waiting for cookie banner to be visible...")
    wait.until(EC.visibility_of_element_located((By.ID, "CybotCookiebotDialogBodyUnderlay")))

    print("👍👍 Waiting for 'Alle zulassen' button to be clickable...")
    accept_btn = wait.until(EC.element_to_be_clickable((By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll")))
 
    print("👍👍 Clicking 'Alle zulassen' button...")
    accept_btn.click()

    print("⏳ Waiting for cookie banner to disappear...")
    wait.until(EC.invisibility_of_element_located((By.ID, "CybotCookiebotDialog")))

    print("✅ Cookie banner accepted and closed.")

except Exception as e:
    print("❌ Cookie banner handling failed:", e)

# Open the job site
url = "https://emagine.de/fuer-consultants/projekte/"
driver.get(url)
time.sleep(5)  

# Find articles inside #jar
articles = driver.find_elements(By.CSS_SELECTOR, "#jar article")
print(f"🔍 Found {len(articles)} job cards.")

# Parse each article
job_data = []

for article in articles:
    try:
        title = article.find_element(By.CSS_SELECTOR, "h2.title").text.strip()
    except:
        title = ""

    try:
        location = article.find_element(By.CSS_SELECTOR, ".address-name").text.strip()
    except:
        location = ""

    try:
        job_id = article.find_element(By.CSS_SELECTOR, ".job_id").text.strip()
    except:
        job_id = ""

    try:
        start_date = article.find_element(By.CSS_SELECTOR, ".convertedDate").text.strip()
    except:
        start_date = ""

    try:
        duration = article.find_element(By.CSS_SELECTOR, ".duration").text.strip()
    except:
        duration = ""

    try:
        link = article.find_element(By.CSS_SELECTOR, "a.single-job").get_attribute("href")
    except:
        link = ""

    # No summary available in current HTML. Placeholder:
    summary = ""

    job_data.append({
        "Title": title,
        "Location": location,
        "Job ID": job_id,
        "Start Date": start_date,
        "Duration": duration,
        "Link": link,
        "Summary": summary
    })

# Output as DataFrame
df = pd.DataFrame(job_data)
print(df.head())

# Optional: Save to Excel
df.to_excel("emagine_jobs.xlsx", index=False)

# Close browser
driver.quit()
