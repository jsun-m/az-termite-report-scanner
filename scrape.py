from playwright.sync_api import sync_playwright
import json

p = sync_playwright().start()

def scrape_data(addresses):  
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    
    results = []
    
    for address_details in addresses:
        try:
          # truncate address to 17 characters
          address = address_details["address"][:17]

          page.goto("https://tarf.azda.gov/index.php")
          # Fill the form (example)
          page.fill('input[name="p_address"]', address)
          page.click('input[value="Search"]')

          # Wait for results and extract
          page.wait_for_load_state('networkidle')

          from playwright.sync_api import sync_playwright

          page.wait_for_selector('table', timeout=15000)

          rows = page.query_selector_all("table.style5 tr:not(.style6)")
          
          for row in rows:
              cells = row.query_selector_all("td")
              values = [cell.inner_text().strip() for cell in cells]
              if len(values) > 0:
                results.append({
                  "address": address,
                  "values": values,
                  "distance": address_details["distance"]
                })  
        except Exception as e:
          print(e)
          continue

    browser.close()

    with open('results.json', 'w') as f:
        json.dump(results, f, indent=2)

with open('filtered_addresses', 'r') as f:
  addresses = json.load(f)

scrape_data(addresses)