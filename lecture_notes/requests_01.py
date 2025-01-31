import requests
import json

def get_temperature(locations: list):
    """Holt die aktuelle Temperatur für eine Liste von Standorten mit Open-Meteo und speichert die Ergebnisse."""

    BASE_URL = "https://api.open-meteo.com/"
    temperature_storage = []

    for location in locations:
        latitude = location["latitude"]
        longitude = location["longitude"]
        location_name = get_location_name(latitude, longitude)

        ENDPOINT_1 = f"v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"
        response = requests.get(BASE_URL + ENDPOINT_1)

        if response.status_code == 200:
            data = response.json()
            current_weather = data["current_weather"]
            temperature = current_weather["temperature"]

            temperature_storage.append({
                "city": location_name,
                "latitude": latitude,
                "longitude": longitude,
                "temperature": temperature
            })
            print(f"Temperatur in {location_name}: {temperature}°C")
            
        else:
            print(f"Fehler beim Abrufen der Wetterdaten für {location_name}")
            temperature_storage.append({
                "city": location_name,
                "latitude": latitude,
                "longitude": longitude,
                "temperature": None
            })

    return temperature_storage  # 🔹 Am Ende die gesamte Liste zurückgeben!
    
def get_location_name(latitude: float, longitude: float) -> str:
    """Ermittelt nur den Stadtnamen aus den Koordinaten mit der OpenStreetMap Nominatim API."""
    
    BASE_URL = "https://nominatim.openstreetmap.org/"
    ENDPOINT_1 = f"reverse?lat={latitude}&lon={longitude}&format=json"
    url = f"{BASE_URL}{ENDPOINT_1}"  
    # Laut Dokumentation muss ein User-Agent angegeben werden:
    headers = {"User-Agent": "geo-request"}  
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()

        if "address" in data:
            address = data["address"]
            
            if "city" in address:
                return address["city"]
            elif "town" in address:
                return address["town"]
            elif "village" in address:
                return address["village"]
            elif "hamlet" in address:
                return address["hamlet"]
        return "Ort nicht gefunden"
    else:
        return "Fehler bei der Anfrage"


if __name__ == "__main__":

    locations = [
        {"latitude": 52.52, "longitude": 13.41},  # Berlin
        {"latitude": 48.85, "longitude": 2.35},   # Paris
        {"latitude": 40.71, "longitude": -74.01}, # New York
        {"latitude": 35.68, "longitude": 139.69}  # Tokio
    ]

    temperature_data = get_temperature(locations)
    print(json.dumps(temperature_data, indent=4, sort_keys=True, ensure_ascii=False))