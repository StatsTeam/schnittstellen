import requests
import json
import sqlite3
import streamlit as st
import pandas as pd

class WeatherAPI:
    """Klasse zur Interaktion mit der Open-Meteo API"""

    BASE_URL = "https://api.open-meteo.com/v1/forecast"

    @staticmethod
    def get_temperature(latitude: float, longitude: float):
        """Holt die aktuelle Temperatur für eine Stadt mit Open-Meteo."""
        url = f"{WeatherAPI.BASE_URL}?latitude={latitude}&longitude={longitude}&current_weather=true"
        
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()

            if "current_weather" in data:
                temperature = data["current_weather"]["temperature"]
                location_name = LocationService.get_location_name(latitude, longitude)
                return location_name, temperature

        except requests.RequestException as e:
            print(f"Netzwerkfehler: {e}")
        except json.JSONDecodeError:
            print("Fehler: Ungültige JSON-Antwort")
        
        return None, None

class LocationService:
    """Klasse zur Ermittlung von Ortsnamen anhand von Koordinaten."""
    BASE_URL = "https://nominatim.openstreetmap.org/reverse"
    HEADERS = {"User-Agent": "geo-request"}

    @staticmethod
    def get_location_name(latitude: float, longitude: float) -> str:
        url = f"{LocationService.BASE_URL}?lat={latitude}&lon={longitude}&format=json"
        
        try:
            response = requests.get(url, headers=LocationService.HEADERS, timeout=5)
            response.raise_for_status()
            data = response.json()

            return data.get("address", {}).get("city", "Ort nicht gefunden")

        except requests.RequestException as e:
            print(f"Netzwerkfehler: {e}")
        
        return "Ort nicht gefunden"

class WeatherDatabase:
    """Klasse zur Verwaltung der SQLite-Datenbank für Wetterdaten."""
    DB_NAME = "wetter.db"

    def __init__(self):
        self._create_database()

    def _create_database(self):
        try:
            conn = sqlite3.connect(self.DB_NAME)
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS wetterdaten (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    city TEXT,
                    latitude REAL,
                    longitude REAL,
                    temperature REAL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
        finally:
            conn.close()

    def save_weather_data(self, city, latitude, longitude, temperature):
        try:
            conn = sqlite3.connect(self.DB_NAME)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO wetterdaten (city, latitude, longitude, temperature) 
                VALUES (?, ?, ?, ?)
            """, (city, latitude, longitude, temperature))
            conn.commit()
        finally:
            conn.close()

    def get_saved_weather(self):
        try:
            conn = sqlite3.connect(self.DB_NAME)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM wetterdaten ORDER BY timestamp DESC")
            data = cursor.fetchall()
            return pd.DataFrame(data, columns=["id", "city", "latitude", "longitude", "temperature", "timestamp"])
        finally:
            conn.close()

    def delete_weather_data(self, entry_id):
        try:
            conn = sqlite3.connect(self.DB_NAME)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM wetterdaten WHERE id = ?", (entry_id,))
            conn.commit()
        finally:
            conn.close()

class WeatherApp:
    """Klasse zur Steuerung der Wetter-App mit Streamlit."""
    def __init__(self):
        self.db = WeatherDatabase()

    def run(self):
        st.title("Wetter-App mit Open-Meteo API")
        
        st.header("Neues Wetter abrufen")
        latitude = st.number_input("Breitengrad eingeben:", value=52.52)
        longitude = st.number_input("Längengrad eingeben:", value=13.41)
        
        if st.button("Wetter abrufen"):
            city, temperature = WeatherAPI.get_temperature(latitude, longitude)
            if city and temperature is not None:
                self.db.save_weather_data(city, latitude, longitude, temperature)
                st.toast(f"Temperatur in {city}: {temperature}°C", icon="✅")

        st.header("Gespeicherte Wetterstandorte anzeigen")
        saved_data = self.db.get_saved_weather()
        if not saved_data.empty:
            st.dataframe(saved_data)
            st.map(saved_data[["latitude", "longitude"]])
        else:
            st.warning("Keine Wetterdaten in der Datenbank gefunden.")

        st.header("Wetterdaten löschen")
        if not saved_data.empty:
            delete_id = st.number_input("ID des zu löschenden Eintrags eingeben:", min_value=1, step=1)
            if st.button("Eintrag löschen"):
                self.db.delete_weather_data(delete_id)
                st.toast(f"Eintrag mit ID {delete_id} wurde erfolgreich gelöscht!", icon="✅")
                st.rerun()

if __name__ == "__main__":
    app = WeatherApp()
    app.run()
