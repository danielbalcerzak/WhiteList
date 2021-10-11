import requests
import json
from datetime import datetime


# Funkcja add_nips nie przyjmuje argumentów. Zbiera pojedyncze numery NIP od użytkownika i zapisuje je do listy.
# Funkcja zwraca zebrane numery nip w postaci listy


def add_nips() -> list:
    nips = []
    accept = "t"
    while accept.lower() == "t":
        nip = input("WPROWADŹ NIP DO WERYFIKACI NA BIAłEJ LIŚCIE: ")
        nip = ''.join(nip.split())
        nips.append(nip)
        print("Jeżeli chcesz wprowadzić kolejny nip wciśnij literkę 't': ")
        accept = input("W przeciwnym razie wciśnij ENTER: ")
        print()
    return nips


# Funkcja choose_date nie przyjmuje argumentów. Służy do wyboru daty dzisiejszej, pobranej z systemu, lub wpisania
# daty w ręcznie przez użytkownika w postaci rrr-mm-dd. Funkcja zwraca string

def choose_date() -> str:
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
                return str(date)
            else:
                print("Spróbuj ponownie")
        except ValueError:
            print("Spróbuj ponownie")
        finally:
            print()

# Funckja search przyjmuje argument date, który posiada typ String oraz argument nips który posiada typ listy.
# Funkcja odpowiedzialna jest za zapytanie do interfejsu API Wykazu podatników VAT - Ministerstwo Finansów -
# Krajowa Administracja Skarbowa - Portal Gov.pl (www.gov.pl).
# Funkcja odpytuje kolejno każdy nip wprowadzony przez użytkownika, znajdujący się w liście. Informacje zwrotne
# na temat nazwy firmy lub braku firmy w bazie wyświetlane zostają w konsoli.


def search(date: str, nips: list):
    for index, nip in enumerate(nips):
        url = f"https://wl-api.mf.gov.pl/api/search/nip/{nip}?date={date}"
        response = requests.get(url)
        try:
            response.raise_for_status()
            company_data = json.loads(response.text)
            company_name = company_data['result']['subject']['name']
            print(f"{index + 1}. Szukany NIP {nip} należy do {company_name}")
        except requests.exceptions.HTTPError:
            print(f"{index + 1}. Szukany NIP {nip} nie występuje w bazie")

# Funckja iterations_search przyjmuje argument date w postaci String oraz argument nips w postaci List.
# Funckja zaprogramowana domyślnie jest na 20 iteracji szukania jednego dnia. Ilośc iteracji może zostać zmieniona przez
# użytkownika. Podczas jednej iteracji, występować będą zapytania w ilości len(nips).


def iterations_search(date: str, nips: list):
    value = 20
    try:
        value = int(input("Ile iteracji chcesz wykonać: "))
        for i in range(value):
            print(f"Zapytanie numer {i + 1} w dniu {date}")
            search(date, nips)
    except ValueError:
        print("Błędny wybór. Wykona się 20 iteracji domyślnych")
        for i in range(value):
            print(f"Zapytanie numer {i + 1} w dniu {date}")
        search(date, nips)

# Funckcja main nie przyjmuje argumentów, oraz ich nie zwraca. Kontroluje ona wykonanie programu i kieruje wywołaniami
# funkcji programu.


def main():
    nips = add_nips()
    date = choose_date()
    search(date, nips)

    # Część do odkomentowania w przypadu użycia funkcji iterującej
    # iterations_search(date, nips)


if __name__ == '__main__':
    main()
