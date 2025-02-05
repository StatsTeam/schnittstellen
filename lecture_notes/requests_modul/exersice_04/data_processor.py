from country import Country
from typing import List
import pandas as pd

class DataProcessor:
    
    def __init__(self, countries: List[Country]):
        self.countries: List[Country] = countries
        self.df = self.create_dataFrame()
        
    def create_dataFrame(self):
        data = []
        for country in self.countries:
            country_data = {
                "Name": country.name,
                "Capital": country.capital,
                "Population": country.population,
                "Area": country.area,
                "Population Density": country.population_density()
            }
            data.append(country_data)
        
        return pd.DataFrame(data)