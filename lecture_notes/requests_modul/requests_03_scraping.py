from bs4 import BeautifulSoup
import requests
import pandas as pd
from typing import Optional

BASE_URL: str = "https://www.scrapethissite.com/pages/forms/"
PAGE_PARAM: str = "?page_num="

def get_last_page() -> int:
    """
    Findet die letzte verfügbare Seite anhand der Paginierung.
    Falls keine Paginierung vorhanden ist oder ein Fehler auftritt, wird die Standardseite 1 zurückgegeben.
    
    Returns:
        int: Die höchste Seitenzahl oder 1, falls keine Paginierung existiert.
    """
    response: requests.Response = requests.get(BASE_URL)
    
    if response.status_code != 200:
        print("Fehler beim Laden der Hauptseite!")
        return 1  

    soup: BeautifulSoup = BeautifulSoup(response.text, "html.parser")
    pagination_links = soup.select("ul.pagination a")

    page_numbers: list[int] = [int(link.text.strip()) for link in pagination_links if link.text.strip().isdigit()]
    
    return max(page_numbers) if page_numbers else 1

def scrape_team_data() -> Optional[pd.DataFrame]:
    """
    Ruft die Daten aller Seiten ab und gibt sie als DataFrame zurück.
    
    Returns:
        Optional[pd.DataFrame]: Enthält die Team-Daten, falls erfolgreich, sonst None.
    """
    last_page: int = get_last_page()
    all_teams_data: list[list[str]] = []

    for page_num in range(1, last_page + 1):
        print(f"Lade Daten von Seite {page_num}...")
        
        url: str = BASE_URL + PAGE_PARAM + str(page_num)
        response: requests.Response = requests.get(url)

        if response.status_code != 200:
            print(f"Fehler beim Laden von Seite {page_num}")
            continue

        soup: BeautifulSoup = BeautifulSoup(response.text, "html.parser")
        teams = soup.find_all("tr", class_="team")

        for team in teams:
            team_name: str = team.find("td", class_="name").text.strip()
            year: str = team.find("td", class_="year").text.strip()
            wins: str = team.find("td", class_="wins").text.strip()
            losses: str = team.find("td", class_="losses").text.strip()
            goals_for: str = team.find("td", class_="gf").text.strip()
            goals_against: str = team.find("td", class_="ga").text.strip()
            diff: str = team.find("td", class_="diff").text.strip()

            all_teams_data.append([team_name, year, wins, losses, goals_for, goals_against, diff])

    if all_teams_data:
        df: pd.DataFrame = pd.DataFrame(all_teams_data, columns=["Team", "Jahr", "Siege", "Niederlagen", "GF", "GA", "+/-"])
        return df
    else:
        print("Keine Daten gefunden!")
        return None

def save_data_to_csv(df: pd.DataFrame, filename: str = "nhl_teams_all_pages.csv") -> None:
    """
    Speichert den DataFrame als CSV-Datei.

    Args:
        df (pd.DataFrame): Der DataFrame, der gespeichert werden soll.
        filename (str): Der Name der Datei (Standard: 'nhl_teams_all_pages.csv').

    Returns:
        None
    """
    if df is not None:
        df.to_csv(filename, index=False)
        print(f"\nDaten erfolgreich gespeichert als: {filename}")
    else:
        print("Keine Daten zum Speichern vorhanden!")

if __name__ == "__main__":
    df: Optional[pd.DataFrame] = scrape_team_data()
    save_data_to_csv(df)
