import streamlit as st
import pandas as pd
from scraper import Scraper
from data_processor import DataProcessor
from country_analyser import CountryAnalyzer

class CountryApp:
    def __init__(self):
        self.df = None
        self.analyzer = None

    def load_data(self):
        """Lädt und verarbeitet die Länderdaten."""
        scraper = Scraper()
        html_content = scraper.fetch_page()
        countries = scraper.parse_countries(html_content)
        processor = DataProcessor(countries)
        self.df = processor.df
        self.analyzer = CountryAnalyzer(self.df)
        st.session_state.df = self.df
        st.success("Daten erfolgreich geladen!")

    def show_data(self):
        """Zeigt die gescrapten Länderdaten als Tabelle an."""
        st.subheader("📊 Übersicht der Länderdaten")
        st.dataframe(self.df)

    def show_analysis(self):
        """Ermöglicht dem Benutzer die Auswahl einer Analyse."""
        st.sidebar.header("🔍 Datenanalyse")
        option = st.sidebar.selectbox("Wähle eine Analyse", (
            "Top 10 Länder nach Bevölkerung",
            "Länder mit der höchsten Bevölkerungsdichte",
            "Durchschnittliche Flächengröße",
            "Länder mit der größten Fläche pro Einwohner",
            "Bevölkerungsanteil pro Land",
            "Länder mit extremem Flächen-zu-Bevölkerungsverhältnis"
        ))

        if option == "Top 10 Länder nach Bevölkerung":
            st.subheader("🌍 Top 10 Länder nach Bevölkerung")
            st.dataframe(self.analyzer.top_countries_by_population())

        elif option == "Länder mit der höchsten Bevölkerungsdichte":
            st.subheader("🏙️ Länder mit der höchsten Bevölkerungsdichte")
            st.dataframe(self.analyzer.highest_population_density())

        elif option == "Durchschnittliche Flächengröße":
            st.subheader("📏 Durchschnittliche Flächengröße aller Länder")
            st.write(f"Die durchschnittliche Flächengröße beträgt {self.analyzer.average_area():,.2f} km².")

        elif option == "Länder mit der größten Fläche pro Einwohner":
            st.subheader("🗺️ Länder mit der größten Fläche pro Einwohner")
            st.dataframe(self.analyzer.largest_area_per_person())

        elif option == "Bevölkerungsanteil pro Land":
            st.subheader("📈 Bevölkerungsanteil pro Land")
            st.dataframe(self.analyzer.population_share())

        elif option == "Länder mit extremem Flächen-zu-Bevölkerungsverhältnis":
            st.subheader("📊 Länder mit extremem Flächen-zu-Bevölkerungsverhältnis")
            st.dataframe(self.analyzer.extreme_area_population_ratio())

    def run(self):
        """Startet die Streamlit-App."""
        st.title("🌍 Länderanalyse mit Web Scraping")
        st.write("Diese App zeigt verschiedene Statistiken zu Ländern weltweit.")

        # Seitenleiste mit Datenabruf-Button
        st.sidebar.header("Daten aktualisieren")
        if st.sidebar.button("Länder-Daten abrufen"):
            self.load_data()

        # Falls Daten existieren, zeige sie
        if "df" in st.session_state:
            self.df = st.session_state.df
            self.analyzer = CountryAnalyzer(self.df)
            self.show_data()
            self.show_analysis()
            self.show_visualizations()  # NEU: Visualisierungen hinzufügen!
        else:
            st.warning("Klicke auf den Button in der Seitenleiste, um Daten zu laden!")

            
    def show_visualizations(self):
        """Ermöglicht dem Benutzer die Auswahl einer Seaborn-Visualisierung."""
        st.sidebar.header("📊 Visualisierungen")
        viz_option = st.sidebar.selectbox("Wähle eine Visualisierung", (
            "Top 10 Länder nach Bevölkerung",
            "Fläche vs. Bevölkerung",
            "Verteilung der Bevölkerungsdichte"
        ))

        if viz_option == "Top 10 Länder nach Bevölkerung":
            st.subheader("📊 Top 10 Länder nach Bevölkerung (Balkendiagramm)")
            self.analyzer.plot_top_countries_population()

        elif viz_option == "Fläche vs. Bevölkerung":
            st.subheader("🌍 Fläche vs. Bevölkerung (Scatter-Plot)")
            self.analyzer.plot_population_vs_area()

        elif viz_option == "Verteilung der Bevölkerungsdichte":
            st.subheader("📈 Verteilung der Bevölkerungsdichte (Histogramm)")
            self.analyzer.plot_population_density_distribution()

