import requests
import json
import sqlite3
import streamlit as st
import pandas as pd

def get_temperature(latitude: float, longitude: float):
    """Holt die aktuelle Temperatur für eine Stadt mit Open-Meteo."""

    BASE_URL = "https://api.open-meteo.com/"
    ENDPOINT_1 = f"v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"
        
    try:
        response = requests.get(BASE_URL + ENDPOINT_1, timeout=5)
        # Falls HTTP-Fehler (400-499, 500-599), Exception auslösen:
        response.raise_for_status()
        data = response.json()

        if "current_weather" in data:
            current_weather = data["current_weather"]
            temperature = current_weather["temperature"]
            location_name = get_location_name(latitude, longitude)
            print(f"Temperatur in {location_name}: {temperature}°C")
            return location_name, temperature
        else:
            print(f"Keine Wetterdaten für {latitude}, {longitude} erhalten.")
            return None, None

    except requests.exceptions.Timeout:
        print(f"Fehler: Zeitüberschreitung für {location_name}")
    except requests.exceptions.RequestException as e:
        print(f"Netzwerkfehler bei {location_name}: {e}")
    except json.JSONDecodeError:
        print(f"Fehler: Ungültige JSON-Antwort für {location_name}")
    except Exception as e:
        print(f"Unerwarteter Fehler bei {location_name}: {e}")

    return None, None
    
def get_location_name(latitude: float, longitude: float) -> str:
    """Ermittelt nur den Stadtnamen aus den Koordinaten mit der OpenStreetMap Nominatim API."""
    
    BASE_URL = "https://nominatim.openstreetmap.org/"
    ENDPOINT_1 = f"reverse?lat={latitude}&lon={longitude}&format=json"
    url = f"{BASE_URL}{ENDPOINT_1}"  
    # Laut Dokumentation muss ein User-Agent angegeben werden:
    headers = {"User-Agent": "geo-request"}  

    try:
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()
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

    except requests.exceptions.Timeout:
        print(f"Fehler: Zeitüberschreitung beim Abrufen der Ortsdaten ({latitude}, {longitude})")
    except requests.exceptions.RequestException as e:
        print(f"Netzwerkfehler bei OpenStreetMap für Koordinaten ({latitude}, {longitude}): {e}")
    except json.JSONDecodeError:
        print(f"Fehler: Ungültige JSON-Antwort für OpenStreetMap ({latitude}, {longitude})")
    except Exception as e:
        print(f"Unerwarteter Fehler: {e}")

        return "Ort nicht gefunden"

def create_database():
    """Erstellt die SQLite-Datenbank und die Tabelle wetterdaten, falls sie noch nicht existiert."""

    try:
        # Verbindung zur Datenbank herstellen (erstellt Datei, falls nicht vorhanden):
        conn = sqlite3.connect("wetter.db")
        # Cursor erstellen (ein spezielles Objekt, das SQL-Befehle ausführt):
        cursor = conn.cursor()
        # Tabelle erstellen (falls nicht vorhanden), führt ein SQL-Statement aus:
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

        # Änderungen in der Datenbank speichern:
        conn.commit()
        print("Datenbank und Tabelle wurden erfolgreich erstellt!")
    except sqlite3.DatabaseError as db_error:
        print(f"Fehler beim Erstellen der Datenbank: {db_error}")
    except sqlite3.OperationalError as op_error:
        print(f"Betriebsfehler (OperationalError): {op_error}")
    except Exception as e:
        print(f"Unerwarteter Fehler beim Erstellen der Datenbank: {e}")
    finally:
        if conn:
            conn.close()

def save_weather_data_to_db(city, latitude, longitude, temperature):
    """Speichert Wetterdaten in der SQLite-Datenbank wetter.db.""" 

    try:
        conn = sqlite3.connect("wetter.db")
        cursor = conn.cursor()

        # SQL-Befehl zum Einfügen von Daten:
        cursor.execute("""
            INSERT INTO wetterdaten (city, latitude, longitude, temperature) 
            VALUES (?, ?, ?, ?)
        """, (city, latitude, longitude, temperature))

        conn.commit() 

    except sqlite3.IntegrityError as int_error:
        # Fehler falls Einschränkungen verletzt werden:
        print(f"Integritätsfehler beim Speichern von {city}: {int_error}")
    except sqlite3.OperationalError as op_error:
        print(f"Betriebsfehler (OperationalError) bei {city}: {op_error}")
    except sqlite3.DatabaseError as db_error:
        print(f"Fehler in der Datenbank für {city}: {db_error}")
    except Exception as e:
        print(f"Unerwarteter Fehler beim Speichern von {city}: {e}")
    finally:
        if conn:
            conn.close()

def get_saved_weather():
    """Ruft alle gespeicherten Wetterdaten aus der Datenbank ab."""
    try:
        conn = sqlite3.connect("wetter.db")
        cursor = conn.cursor()

        # Ausführen des SQL-Befehls:
        cursor.execute("SELECT * FROM wetterdaten ORDER BY timestamp DESC")
        data = cursor.fetchall()

        # Falls keine Daten vorhanden sind, leere Liste returnen:
        if not data:
            print("Keine Wetterdaten in der Datenbank gefunden.")
            return pd.DataFrame(columns=["id", "city", "latitude", "longitude", "temperature", "timestamp"])

        df = pd.DataFrame(data, columns=["id", "city", "latitude", "longitude", "temperature", "timestamp"])
        return df  
    
    except sqlite3.OperationalError as e:
        print(f"⚠️ Fehler beim Abrufen der Daten: {e}")
        return pd.DataFrame()
    
    except sqlite3.DatabaseError as e:
        print(f"Datenbankfehler: {e}")
        return pd.DataFrame()
    
    finally:
        if conn:
            conn.close()

def get_weather_by_city(city_name: str):
    """Holt Wetterdaten aus der SQLite-Datenbank für eine bestimmte Stadt."""

    try:
        if not city_name.strip():
            print("Fehler: Der Stadtname darf nicht leer sein.")
            return []
        
        conn = sqlite3.connect("wetter.db")
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM wetterdaten 
            WHERE city = ? 
            ORDER BY timestamp DESC
        """, (city_name,))

        data = cursor.fetchall()  

        if not data:
            print(f"Keine gespeicherten Wetterdaten für {city_name} gefunden.")
            return []

        return data
    
    except sqlite3.OperationalError as e:
        print(f"Fehler beim Abrufen der Daten: {e}")
        return []
    
    except sqlite3.DatabaseError as e:
        print(f"Datenbankfehler: {e}")
        return []
    
    finally:
        if conn:
            conn.close()

def delete_weather_data_by_id(entry_id: int):
    """Löscht einen Wetterdateneintrag anhand der ID aus der SQLite-Datenbank."""

    try:
        conn = sqlite3.connect("wetter.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM wetterdaten WHERE id = ?", (entry_id,))
        # Falls eine Zeile mit der gesuchten id gefunden wird, enthält data die Werte dieser Zeile als Tupel:
        data = cursor.fetchone()

        if data:
            cursor.execute("DELETE FROM wetterdaten WHERE id = ?", (entry_id,))
            conn.commit()
            st.success(f"Wetterdatensatz mit ID {entry_id} wurde gelöscht.")
        else:
            st.warning(f"Keine Daten mit ID {entry_id} gefunden.")

    except sqlite3.DatabaseError as e:
        st.error(f"Fehler beim Löschen der Daten: {e}")

    finally:
        if conn:
            conn.close()

if __name__ == "__main__":

    create_database()

    st.title("Wetter-App mit der Open-Meteo API")

    st.header("Neues Wetter abrufen")
    latitude = st.number_input("Breitengrad (Latitude) eingeben:", value=52.52)
    longitude = st.number_input("Längengrad (Longitude) eingeben:", value=13.41)
    if st.button("Wetter abrufen"):
        city, temperature = get_temperature(latitude, longitude)
        if city and temperature is not None:
            save_weather_data_to_db(city, latitude, longitude, temperature)
            st.toast(f"Temperatur in {city}: {temperature}°C", icon="✅")

    st.header("Gespeicherte Wetterstandorte anzeigen")
    saved_data = get_saved_weather()
    if not saved_data.empty:
        st.dataframe(saved_data)
        st.map(saved_data[["latitude", "longitude"]])
    else:
        st.warning("Keine Wetterdaten in der Datenbank gefunden.")

    st.header("Wetter für eine Stadt anzeigen")
    city_selection = st.selectbox("Stadt auswählen", saved_data["city"].unique() if not saved_data.empty else ["Keine Daten verfügbar"])
    if city_selection != "Keine Daten verfügbar":
        city_data = get_weather_by_city(city_selection)
    if city_data:
        st.dataframe(pd.DataFrame(city_data, columns=["id", "city", "latitude", "longitude", "temperature", "timestamp"]))
    else:
        st.warning(f"Keine gespeicherten Wetterdaten für {city_selection} gefunden.")

    st.header("Wetterdaten löschen")
    if not saved_data.empty:
        delete_id = st.number_input("ID des zu löschenden Eintrags eingeben:", min_value=1, step=1)

        if st.button("Eintrag löschen"):
            delete_weather_data_by_id(delete_id)
            st.session_state["delete_message"] = f"Eintrag mit ID {delete_id} wurde erfolgreich gelöscht!"
            st.rerun()

    # Erfolgsmeldung NACH `st.rerun()` anzeigen
    if "delete_message" in st.session_state:
        st.toast(st.session_state["delete_message"], icon="✅")
        del st.session_state["delete_message"]


