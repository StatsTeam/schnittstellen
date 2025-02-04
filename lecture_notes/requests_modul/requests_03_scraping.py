from bs4 import BeautifulSoup
import requests
import pandas as pd
from typing import Optional
import matplotlib.pyplot as plt
import streamlit as st
import seaborn as sns

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

# Ab hier Datenanalyse

def load_data(file_name: str) -> pd.DataFrame:
    """Lädt die CSV-Datei und gibt einen DataFrame zurück."""
    df = pd.read_csv(file_name)
    return df

def basic_statistics(df: pd.DataFrame) -> None:
    """Gibt grundlegende Statistiken der Daten aus."""
    st.write("## Allgemeine Statistik")
    st.write(df.describe())

def avg_wins_losses_per_year(df: pd.DataFrame) -> None:
    """Zeigt die durchschnittlichen Siege und Niederlagen pro Jahr an und visualisiert sie in Streamlit."""
    yearly_avg = df.groupby("Jahr")[["Siege", "Niederlagen"]].mean()
    
    fig, ax = plt.subplots(figsize=(10,5))
    ax.plot(yearly_avg.index, yearly_avg["Siege"], marker='o', label="Durchschnittliche Siege")
    ax.plot(yearly_avg.index, yearly_avg["Niederlagen"], marker='o', label="Durchschnittliche Niederlagen")
    
    ax.set_title("Durchschnittliche Siege und Niederlagen pro Jahr")
    ax.set_xlabel("Jahr")
    ax.set_ylabel("Anzahl")
    ax.legend()
    ax.grid()
    
    st.pyplot(fig)

def correlation_matrix(df: pd.DataFrame) -> None:
    """Zeigt eine Heatmap der Korrelationen zwischen Zahlenwerten in Streamlit."""
    numeric_df = df[["Siege", "Niederlagen", "GF", "GA", "+/-"]].astype(float)
    fig, ax = plt.subplots(figsize=(8,6))
    sns.heatmap(numeric_df.corr(), annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
    ax.set_title("Korrelationsmatrix")
    st.pyplot(fig)

def top_teams_by_goal_difference(df: pd.DataFrame, top_n: int = 10) -> None:
    """Zeigt die Top-N-Teams mit der besten und schlechtesten Tordifferenz in Streamlit."""
    df_sorted = df.sort_values(by=["+/-"], ascending=False)
    top_teams = df_sorted.head(top_n)
    worst_teams = df_sorted.tail(top_n)
    
    fig, ax = plt.subplots(figsize=(10,5))
    sns.barplot(x=top_teams["Team"], y=top_teams["+/-"], palette="Blues", ax=ax)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
    ax.set_title("Top 10 Teams mit bester Tordifferenz")
    st.pyplot(fig)
    
    fig, ax = plt.subplots(figsize=(10,5))
    sns.barplot(x=worst_teams["Team"], y=worst_teams["+/-"], palette="Reds", ax=ax)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
    ax.set_title("Top 10 Teams mit schlechtester Tordifferenz")
    st.pyplot(fig)

if __name__ == "__main__":
    df = load_data("nhl_teams_all_pages.csv")

    st.title("NHL Team Statistik Dashboard")

    if st.button("Allgemeine Statistik anzeigen"):
        basic_statistics(df)
    if st.button("Durchschnittliche Siege und Niederlagen pro Jahr anzeigen"):
        avg_wins_losses_per_year(df)
    if st.button("Korrelationsmatrix anzeigen"):
        correlation_matrix(df)
    if st.button("Top Teams nach Tordifferenz anzeigen"):
        top_teams_by_goal_difference(df)

