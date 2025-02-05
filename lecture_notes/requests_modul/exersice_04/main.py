from scraper import Scraper
from data_processor import DataProcessor
from country_analyser import CountryAnalyzer
from streamlit_app import CountryApp
    
if __name__ == "__main__":
    
    # Ohne Streamlit UI:
    # scraper = Scraper()
    # html_content = scraper.fetch_page()
    # countries = scraper.parse_countries(html_content)
    
    # processor = DataProcessor(countries)
    # df = processor.df
    
    # analyzer = CountryAnalyzer(df)
    
    # print("\nTop 10 Länder nach Bevölkerung:")
    # print(analyzer.top_countries_by_population())
    
    # print("\nTop 10 Länder mit der höchsten Bevölkerungsdichte:")
    # print(analyzer.highest_population_density())
    
    # print("\nDurchschnittliche Flächengröße:")
    # print(analyzer.average_area())
    
    # print("\n Länder mit der größten Fläche pro Einwohner (Flächen-Effizienz):")
    # print(analyzer.largest_area_per_person())
    
    # print("\n Verhältnis von Bevölkerung zu Weltbevölkerung:")
    # print(analyzer.population_share())
    
    # print("\n Länder mit der größten Differenz zwischen Fläche und Bevölkerung:")
    # print(analyzer.extreme_area_population_ratio())
    
    # ------------------------------ #
    # Mit Streamlit UI:
    app = CountryApp()
    app.run()
    