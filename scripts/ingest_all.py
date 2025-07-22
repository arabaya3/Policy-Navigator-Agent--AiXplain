import pandas as pd
import requests
from bs4 import BeautifulSoup
from aixplain.factories import IndexFactory
from aixplain.modules.model.record import Record
from dotenv import load_dotenv
import socket
import time
load_dotenv()
def check_aixplain_api():
    try:
        host = 'platform-api.aixplain.com'
        socket.gethostbyname(host)
        return True
    except Exception as e:
        print(f"[NETWORK ERROR] Could not resolve {host}: {e}\nPlease check your internet connection, DNS settings, or firewall.")
        return False
def get_index_by_name(index_name, retries=5, delay=2):
    for attempt in range(retries):
        indexes = IndexFactory.list()
        print(f"[DEBUG] Available indexes: {[getattr(idx, 'name', None) for idx in indexes]}")
        for idx in indexes:
            if getattr(idx, 'name', None) == index_name:
                return idx
        if attempt < retries - 1:
            print(f"[INFO] Index '{index_name}' not found, retrying in {delay} seconds...")
            time.sleep(delay)
    raise Exception(f"Index '{index_name}' not found after {retries} retries.")
def ingest_vehicle_code(csv_path):
    index_name = "Vehicle Code Index"
    index_desc = "California Vehicle Code sections"
    df = pd.read_csv(csv_path)
    try:
        index = IndexFactory.create(name=index_name, description=index_desc)
    except Exception:
        index = get_index_by_name(index_name)
    for _, row in df.iterrows():
        index.upsert([Record(value=row['text'], attributes={"section": str(row['section']), "title": row['title']})])
    print(f"Upserted {len(df)} records to {index_name}")
def ingest_epa(url):
    index_name = "EPA Index"
    index_desc = "EPA Clean Air Act Summary"
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")
    text = "\n".join([p.get_text() for p in soup.find_all("p")])
    try:
        index = IndexFactory.create(name=index_name, description=index_desc)
    except Exception:
        index = get_index_by_name(index_name)
    index.upsert([Record(value=text, attributes={"url": url})])
    print(f"Upserted EPA summary to {index_name}")
if __name__ == "__main__":
    if not check_aixplain_api():
        exit(1)
    try:
        ingest_vehicle_code("data/vehicle_code.csv")
        ingest_epa("https://www.epa.gov/laws-regulations/summary-clean-air-act")
    except Exception as e:
        print(f"[ERROR] Ingestion failed: {e}") 