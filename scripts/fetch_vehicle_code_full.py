import requests
from bs4 import BeautifulSoup
import csv
import time
import os
from urllib.parse import urljoin

BASE_TOC_URL = "https://leginfo.legislature.ca.gov/faces/codesTOCSelected.xhtml?tocCode=VEH&tocTitle=+Vehicle+Code+-+VEH"
BASE_SECTION_URL = "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=VEH&sectionNum={}"
BASE_URL = "https://leginfo.legislature.ca.gov"

DATA_DIR = os.path.join(os.path.dirname(__file__), '../data')
CSV_PATH = os.path.join(DATA_DIR, 'vehicle_code.csv')


def get_all_section_numbers():
    visited = set()
    section_numbers = set()
    def crawl_toc(url):
        resp = requests.get(url)
        soup = BeautifulSoup(resp.text, "html.parser")
        for link in soup.find_all("a", href=True):
            href = link['href']
            full_url = urljoin(BASE_URL, href)
            if "sectionNum=" in href:
                section_num = href.split("sectionNum=")[-1].split("&")[0]
                if section_num.isdigit() or (section_num.replace('.', '', 1).isdigit() and section_num.count('.') < 2):
                    section_numbers.add(section_num)
            elif href.startswith("/faces/codesTOCSelected.xhtml") and full_url not in visited:
                visited.add(full_url)
                crawl_toc(full_url)
    crawl_toc(BASE_TOC_URL)
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