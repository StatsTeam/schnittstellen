import requests

# Basis-URL von httpbin.org
BASE_URL = "https://httpbin.org/"

LOGIN_ENDPOINT = "cookies/set/sessionID/abcdef123456"
USER_DATA_ENDPOINT = "cookies"
LOGOUT_ENDPOINT = "cookies/delete?sessionID"

session = requests.Session()

def login():
    """Simuliert einen Login und speichert das Session-Cookie."""
    response = session.get(BASE_URL + LOGIN_ENDPOINT)
    
    # Prüfe, ob das Session-Cookie erfolgreich gespeichert wurde
    if "sessionID" in session.cookies:
        print("✅ Login erfolgreich! Session-ID gespeichert:", session.cookies.get("sessionID"))
    else:
        print("Login fehlgeschlagen! Kein Session-Cookie erhalten.")

def get_user_data():
    """Ruft die gespeicherten Cookies vom Server ab und zeigt sie an."""
    response = session.get(BASE_URL + USER_DATA_ENDPOINT)
    
    if response.status_code == 200:
        print("Server kennt folgende Cookies:")
        print(response.json())
    else:
        print("Fehler beim Abrufen der Benutzerdaten!")

def logout():
    """Löscht die Session-ID und setzt die Session zurück."""
    session.get(BASE_URL + LOGOUT_ENDPOINT)

    # Lösche alle gespeicherten Cookies
    session.cookies.clear()

    print("Erfolgreich ausgeloggt! Alle Cookies wurden entfernt.")

if __name__ == "__main__":
    print("\n--- Starte Anwendung ---\n")

    # 1. Login
    print("1. Login")
    login()

    # 2. Benutzerdaten abrufen
    print("\n2. Benutzerdaten abrufen:")
    get_user_data()

    # 3. Logout
    print("\n3. Logout:")
    logout()

    # 4. Prüfen, ob wirklich ausgeloggt wurde
    print("\n4. Benutzerdaten nach Logout abrufen:")
    get_user_data()
