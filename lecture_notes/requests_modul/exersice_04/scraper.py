from bs4 import BeautifulSoup
import requests
from typing import List
from country import Country

class Scraper:
    
    URL = "https://www.scrapethissite.com/pages/simple/"
    
    def fetch_page(self):
        response = requests.get(self.URL)
        if response.status_code == 200:
            return response.text
        else:
            raise Exception(f"Fehler beim Abrufen der Seite: {response.status_code}")
    
    def parse_countries(self, html: str) -> List[Country]:
        
        soup = BeautifulSoup(html, "html.parser")
        country_elements = soup.find_all("div", class_="country")
        
        countries: List[Country] = []
        for country in country_elements:
            name = country.find("h3", class_="country-name").text.strip()
            capital = country.find("span", class_="country-capital").text.strip()
            population = int(country.find("span", class_="country-population").text.strip().replace(',', ''))
            area = float(country.find("span", class_="country-area").text.strip().replace(',', ''))
            
            countries.append(Country(name, capital, population, area))
        return countries