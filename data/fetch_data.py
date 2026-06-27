import requests
import pandas as pd

base = "https://www.consumerfinance.gov/data-research/consumer-complaints/search/api/v1/"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

all_records = []
batch_size = 100
total_to_fetch = 5000  # adjust as needed

print(f"Fetching {total_to_fetch} complaints...")

for frm in range(0, total_to_fetch, batch_size):
    params = {
        "size": batch_size,
        "frm": frm,
        "sort": "created_date_desc"
    }
    response = requests.get(base, headers=headers, params=params)
    
    if response.status_code != 200:
        print(f"Error at frm={frm}: {response.status_code}")
        break
    
    hits = response.json()['hits']['hits']
    if not hits:
        break
        
    records = [h['_source'] for h in hits]
    all_records.extend(records)
    
    if frm % 1000 == 0:
        print(f"Fetched {frm + batch_size} records...")

df = pd.DataFrame(all_records)
print(f"\nFinal shape: {df.shape}")
print(f"Columns: {df.columns.tolist()}")
print(f"Complaints with narratives: {df['complaint_what_happened'].replace('', pd.NA).notna().sum()}")

# Save locally
df.to_csv('data/cfpb_complaints.csv', index=False)
print("Saved to data/cfpb_complaints.csv")
