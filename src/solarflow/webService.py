import requests
from typing import List, Optional

# Basis-Konfiguration für die API-Anfragen
config = {
    "headers": {
        "Content-Type": "application/json",
        "Accept-Language": "de-DE",
        "appVersion": "4.3.1",
        "User-Agent": "Zendure/4.3.1 (iPhone; iOS 14.4.2; Scale/3.00)",
        "Accept": "*/*",
        "Authorization": "Basic Q29uc3VtZXJBcHA6NX4qUmRuTnJATWg0WjEyMw==",
        "Blade-Auth": "bearer (null)",
    },
    "timeout": 10,
}

# Funktion zum Anmelden und Abrufen des Access-Tokens
def login(username: str, password: str, token_url: str) -> Optional[str]:
    # Erstellen der Basic Auth für die Anmeldung
    auth = requests.auth._basic_auth_str(username, password)
    config["headers"]["Authorization"] = auth

    # Anfrage-Body für den Login
    auth_body = {
        "password": password,
        "account": username,
        "appId": "121c83f761305d6cf7b",
        "appType": "iOS",
        "grantType": "password",
        "tenantId": "",
    }

    try:
        response = requests.post(token_url, json=auth_body, headers=config["headers"], timeout=config["timeout"])
        response_data = response.json()
        
        if response.status_code == 200 and response_data.get("success"):
            access_token = response_data["data"].get("accessToken")
            print("Login erfolgreich, Access Token erhalten.")
            return access_token
        else:
            print("Login fehlgeschlagen:", response_data)
            return None

    except requests.RequestException as e:
        print(f"Fehler bei der Verbindung zur API: {e}")
        return None

# Funktion zum Abrufen der Geräteliste
def get_device_list(access_token: str, device_list_url: str) -> List[dict]:
    config["headers"]["Blade-Auth"] = f"bearer {access_token}"
    try:
        response = requests.post(device_list_url, headers=config["headers"], timeout=config["timeout"])
        response_data = response.json()
        
        if response.status_code == 200 and response_data.get("data"):
            device_list = response_data["data"]
            print("Geräteliste erfolgreich abgerufen.")
            return device_list
        else:
            print("Keine Geräte gefunden:", response_data)
            return []

    except requests.RequestException as e:
        print(f"Fehler beim Abrufen der Geräteliste: {e}")
        return []

# Beispiel: Nutzung der Funktionen

if __name__ == "__main__":
    username = "    " # Hier den Benutzernamen eintragen
    password = "    " # Hier das Passwort eintragen
    token_url = "https://app.zendure.tech/eu/auth/app/token"  
    device_list_url = "https://app.zendure.tech/eu/productModule/device/queryDeviceListByConsumerId"  

    # Anmeldung und Token-Abruf
    access_token = login(username, password, token_url)

    # Abrufen der Geräteliste, falls Token erfolgreich erhalten
    if access_token:
        print(access_token)
        devices = get_device_list(access_token, device_list_url)
        print("Abgerufene Geräte:", devices)
    else:
        print("Anmeldung fehlgeschlagen.")
