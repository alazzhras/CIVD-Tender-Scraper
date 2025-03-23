import requests
import time
import random
import re
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup

# Header & Cookies from Browser Session
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

base_url = "https://civdmigas.skkmigas.go.id/ajax/search/tnd.jwebs?d-1789-p={page}"
page = 1
pages = 0
card_list = []

print(f'=== Start Scraping Data ===')
time.sleep(2)

# Looping for every page
while True:
    try:
        url = base_url.format(page=page)
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'lxml')
        cards = soup.find_all('div', class_='card')
        
        print(f'⏳ Collecting page(s).....', end='\r')
        
        if not cards:
            break
        
        for card in cards:
            card_list.append(card)
        
        page += 1
        pages += 1
        time.sleep(random.uniform(1, 5))
        
    except requests.exceptions.Timeout:
        print(f'⚠️ Error, timeout on page {page}. Retrying.....')
        time.sleep(3)
        
    except requests.exceptions.RequestException as e:
        print(f'❌ Request error on page {page}: {e}')
        break
        
    except Exception as e:
        print(f'❌ Unexpected error on page {page}: {e}')
        break

print(f'📝 Total {pages} page(s) loaded and {len(card_list)} data(s) found.\n')
time.sleep(2)

if not card_list:
    print("❌ No tenders found. Exiting process.")
    exit()

print(f'⏳ Processing data.....', end='\r')
time.sleep(3)

tender = []
success_count, fail_count = 0, 0

# Start Data Extraction
for idx, card in enumerate(card_list, start=1):
    try:
        # Extract Title
        title = card.select_one('h5.card-title')
        title = title.text.strip() if title else 'N/A'
        
        # Extract Invitation Type
        inv_type = card.select_one('small > span')
        inv_type = inv_type.text.strip() if inv_type else 'N/A'
        
        # Extract Tender Owner
        owner = card.select_one('div > small > strong > i')
        owner = owner.text.strip() if owner else 'N/A'
        
        # Extract Validity Date
        validity_text = card.select_one('div > div > small')
        validity_text = validity_text.text.strip() if validity_text else 'N/A'
        
        match = re.search(r'(\d{1,2} \w+ \d{4})', validity_text)
        validity_date = match.group(1) if match else 'N/A'
        
        # Extract Description
        desc = card.select_one('p.card-text')
        desc = desc.text.strip() if desc else 'N/A'
        
        # Extract Business Type
        bsn_type = card.select_one('p.tipe > span')
        bsn_type = ', '.join(bsn_type.text.strip().split()[2:]) if bsn_type else 'N/A'
        
        # Extract Procurement Type
        proc_type = card.select_one('p.tipe > span:nth-child(2)')
        proc_type = ' '.join(proc_type.text.strip().split()[3:]) if proc_type else 'N/A'
        
        # Extract Business Field
        field = card.select_one('span.field')
        field = ' '.join(field.text.strip().split()[3:]) if field else 'N/A'
        
        # Extract Attachments
        attachment_elements = card.select('a.download-file-blob')
        attachment_url_list = [
            f"https://civdmigas.skkmigas.go.id/download/tnd/ann.jwebs?id={a['data-file-id']}"
            for a in attachment_elements if a.has_attr('data-file-id')
        ]
        attachment_url = ', '.join(attachment_url_list) if attachment_url_list else 'N/A'
        
        # Append to Tender List
        tender.append({
            'Title': title,
            'Invitation Type': inv_type,
            'Owner': owner,
            'Validity Date': validity_date,
            'Bussiness Classification': bsn_type,
            'Procurement Type': proc_type,
            'Bussiness Field': field,
            'Description': desc,
            'Attachment URL': attachment_url
        })
        
        success_count += 1
        print(f'✅ {idx}/{len(card_list)}. Success: {title}')
        time.sleep(0.5)
        
    except Exception as e:
        fail_count += 1
        print(f"❌ Error processing a data: {e}")
        continue

# Save data to CSV
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
filename = f"CIVD Tender List_{timestamp}.csv"
df = pd.DataFrame(tender)
df.to_csv(filename, index=False)

print("\n=== Scraping Summary ===")
print(f"📊 Total data scraped  : {len(tender)}")
print(f"✅ Successfully scraped: {success_count}")
print(f"❌ Failed to scrape    : {fail_count}")
print(f"✅ Data saved to {filename}.")