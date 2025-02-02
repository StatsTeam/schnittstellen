import requests
import json

BASE_URL = "https://httpbin.org/"
ENDPOINT_1 = "get"
ENDPOINT_2 = "redirect/3"
ENDPOINT_3 = "cookies/set?name=JohnDoe"
ENDPOINT_4 = "cookies"

try:

    session = requests.Session()

    # Cookies setzen:
    session.cookies.set("user", "JohnDoe")
    session.cookies.set("theme", "dark")

    # Cookies abrufen:
    response = session.get(BASE_URL + ENDPOINT_4)
    response.raise_for_status()

    data = response.json()
    print(json.dumps(data, indent=4))

    cookies = session.cookies
    print(f"Erhaltene Cookies: {cookies}") # <RequestsCookieJar[]>

    cookies_dict = cookies.get_dict()
    print("Cookies als Dictionary:", cookies_dict)

except requests.exceptions.HTTPError as e:
    print(f"Fehler: {e}")
except json.JSONDecodeError:
    print("Fehler: Antwort ist kein gültiges JSON!")
    


