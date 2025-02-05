import pandas as pd
import seaborn as sns
import streamlit as st
import matplotlib.pyplot as plt

class CountryAnalyzer:
    
    def __init__(self, df: pd.DataFrame):
        self.df: pd.DataFrame = df
        
    def top_countries_by_population(self, n=10):
        return self.df.sort_values(by="Population", ascending=False).head(n)
    
    def highest_population_density(self, n=10):
        return self.df.sort_values(by="Population Density", ascending=False).head(10)
    
    def average_area(self):
        return self.df["Area"].mean()
    
    def largest_area_per_person(self, n=10):
        self.df["Area per Person"] = self.df["Area"] / self.df["Population"]
        return self.df.sort_values(by="Area per Person", ascending=False).head(n)


    def population_share(self):
        """Berechnet den Anteil der Bevölkerung jedes Landes an der Gesamtbevölkerung."""
        total_population = self.df["Population"].sum()
        self.df["Population Share (%)"] = (self.df["Population"] / total_population) * 100
        return self.df.sort_values(by="Population Share (%)", ascending=False)


    def extreme_area_population_ratio(self, n=10):
        """Zeigt die Länder mit der größten Differenz zwischen Fläche und Bevölkerung."""
        self.df["Area-Population Ratio"] = self.df["Area"] / self.df["Population"]
        return self.df.sort_values(by="Area-Population Ratio", ascending=False).head(n)
    
    def plot_top_countries_population(self):
            """Erstellt ein Balkendiagramm der Top 10 Länder nach Bevölkerung."""
            top_countries = self.df.sort_values(by="Population", ascending=False).head(10)

            plt.figure(figsize=(10, 6))
            sns.barplot(x="Population", y="Name", data=top_countries, palette="viridis")
            plt.xlabel("Bevölkerung")
            plt.ylabel("Land")
            plt.title("Top 10 Länder nach Bevölkerung")
            st.pyplot(plt)

    def plot_population_vs_area(self):
        """Erstellt einen Scatter-Plot für Fläche vs. Bevölkerung."""
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x="Area", y="Population", data=self.df, alpha=0.5, color="blue")
        plt.xscale("log")
        plt.yscale("log")
        plt.xlabel("Fläche (km²)")
        plt.ylabel("Bevölkerung")
        plt.title("Fläche vs. Bevölkerung")
        st.pyplot(plt)

    def plot_population_density_distribution(self):
        """Erstellt ein Histogramm der Bevölkerungsdichte."""
        plt.figure(figsize=(10, 6))
        sns.histplot(self.df["Population Density"], bins=30, kde=True, color="red")
        plt.xlabel("Bevölkerungsdichte")
        plt.ylabel("Anzahl Länder")
        plt.title("Verteilung der Bevölkerungsdichte")
        st.pyplot(plt)
