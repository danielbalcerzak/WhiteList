import requests
import json
from datetime import datetime


def add_nips():
    nips = []
    accept = "t"
    while accept.lower() == "t":
        nip = input("WPROWADŹ NIP DO WERYFIKACI NA BIAłEJ LIŚCIE: ")
        nips.append(nip)
        print("Jeżeli chcesz wprowadzić kolejny nip wciśnij literkę 't': ")
        accept = input("W przeciwnym razie wciśnij ENTER: ")
        print()
    return nips


def choose_date():
    while True:
        print("WYBÓR DATY:")
        print("1. Jeżeli chcesz wybrać datę dziejszą wybierz 1")
        print("2. Jeżeli chcesz wybrać datę inną datę wybierz 2")
        try:
            choose = int(input("Wybór: "))
            if choose == 1:
                date = datetime.date(datetime.now())
                return str(date)
            elif choose == 2:
                date = input("Wprowadź datę w formacie rrrr-mm-dd: ")
                return date
            else:
                print("Spróbuj ponownie")
        except:
            print("Spróbuj ponownie")
        finally:
            print()


def search(date, nips):
    for index, nip in enumerate(nips):
        nip = ''.join(nip.split())
        url = f"https://wl-api.mf.gov.pl/api/search/nip/{nip}?date={date}"
        response = requests.get(url)
        try:
            response.raise_for_status()
            companyData = json.loads(response.text)
            companyName = companyData['result']['subject']['name']
            print(f"{index+1}. Szukany NIP {nip.strip()} należy do {companyName}")
        except:
            print(f"{index+1}. Szukany NIP {nip.strip()} nie występuje w bazie")

def iterations_search(date, nips):
    for i in range(100):
        print(f"Zapytanie numer {i+1} w dniu {date}")
        search(date, nips)


def main():
    nips = add_nips()
    date = choose_date()
    search(date, nips)
    iterations_search(date, nips)


if __name__ == '__main__':
    main()