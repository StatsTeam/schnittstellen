class Country:
    """Repräsentiert ein Land."""
    def __init__(self, name, capital, population, area):
        self.name = name
        self.capital = capital
        self.population = population
        self.area = area
        
    def population_density(self):
        """Berechnet die Bevölkerungsdichte."""
        return round(self.population / self.area, 2) if self.area > 0 else 0