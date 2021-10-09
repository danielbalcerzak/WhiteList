import requests
import json

nip = input("Wprowadz NIP: ")
date = input("Wprowadz datę w formacie rrrr-mm-dd: ")

for i in range(100):
    url = f"https://wl-api.mf.gov.pl/api/search/nip/{nip}?date={date}"
    response = requests.get(url)
    response.raise_for_status()
    companyData = json.loads(response.text)
    companyName = companyData['result']['subject']['name']
    print(f"{i+1}: Szukany NIP należy do {companyName}")
    print("hurra")

blabla