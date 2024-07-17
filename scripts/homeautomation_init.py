import requests

# Home Assistant URL and Token
home_assistant_url = "http://homeassistant.local:8123"
token = ""

# Temperature values
temperatures = {
    "temperature_entreplan_hall": 25,
    "temperature_entreplan_kok": 26,
    "temperature_entreplan_huvudsovrum": 23,
    "temperature_entreplan_kontor": 22,
    "temperature_entreplan_entrehall": 22,
    "temperature_vind_sovrum": 22,
    "temperature_kallare_hall": 24,
    "temperature_kallare_tvattstuga": 20,
    "temperature_kallare_garage": 24,
}

# Headers for the API request
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# Update each temperature sensor
for sensor, value in temperatures.items():
    url = f"{home_assistant_url}/api/states/sensor.{sensor}"
    data = {
        "state": value,
        "attributes": {
            "unit_of_measurement": "°C",
            "friendly_name": sensor.replace('_', ' ').title()
        }
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        print(f"{sensor} updated successfully!")
    else:
        print(f"Failed to update {sensor}. Status code: {response.status_code}")
        print(response.json())
