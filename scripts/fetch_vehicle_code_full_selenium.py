import os
import csv
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests

# --- SETUP INSTRUCTIONS ---
# 1. pip install selenium beautifulsoup4 requests
# 2. Download ChromeDriver from https://sites.google.com/chromium.org/driver/ and place it in your PATH
# 3. Run this script: python fetch_vehicle_code_full_selenium.py

BASE_TOC_URL = "https://leginfo.legislature.ca.gov/faces/codesTOCSelected.xhtml?tocCode=VEH&tocTitle=+Vehicle+Code+-+VEH"
BASE_SECTION_URL = "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=VEH&sectionNum={}"
DATA_DIR = os.path.join(os.path.dirname(__file__), '../data')
CSV_PATH = os.path.join(DATA_DIR, 'vehicle_code.csv')


def get_all_section_numbers():
    options = Options()
    options.headless = True
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=options)
    driver.get(BASE_TOC_URL)
    # Wait for the TOC to load (may need to adjust the wait time or condition)
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='sectionNum=']"))
    )
    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()
    section_links = soup.find_all("a", href=True)
    section_numbers = set()
    for link in section_links:
        href = link['href']
        if "sectionNum=" in href:
            section_num = href.split("sectionNum=")[-1].split("&")[0]
            if section_num.isdigit() or (section_num.replace('.', '', 1).isdigit() and section_num.count('.') < 2):
                section_numbers.add(section_num)
    return sorted(section_numbers, key=lambda x: float(x) if x.replace('.', '', 1).isdigit() else x)

def fetch_section(section_num):
    url = BASE_SECTION_URL.format(section_num)
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")
    title = soup.find("h3")
    title = title.text.strip() if title else f"Section {section_num}"
    content = soup.find("div", {"class": "section"})
    text = content.text.strip() if content else ""
    return {"section": section_num, "title": title, "text": text}

def main():
    os.makedirs(DATA_DIR, exist_ok=True)
    section_numbers = get_all_section_numbers()
    print(f"Found {len(section_numbers)} sections.")
    with open(CSV_PATH, "w", newline='', encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["section", "title", "text"])
        writer.writeheader()
        for i, sec in enumerate(section_numbers):
            print(f"Fetching section {sec} ({i+1}/{len(section_numbers)})...")
            entry = fetch_section(sec)
            if entry["text"]:
                writer.writerow(entry)
            time.sleep(0.5)  # Be polite to the server
    print(f"Saved all sections to {CSV_PATH}")

if __name__ == "__main__":
    main() 