from typing import Dict, List

import requests
from unidecode import unidecode


def clean_text(text: str) -> str:
    text = unidecode(text).lower()
    return text


def update_sensors(
    temperature_lst: List[Dict[str, str]], hoas_url: str, hoas_token: str
):

    headers = {
        "Authorization": f"Bearer {hoas_token}",
        "Content-Type": "application/json",
    }

    for record in temperature_lst:
        clean_area_name = clean_text(record["area_name"])
        clean_room = clean_text(record["room"])
        sensor = f"temperature_{clean_area_name}_{clean_room}"

        url = f"{hoas_url}/api/states/sensor.{sensor}"
        data = {
            "state": int(record["temperature"]),
            "attributes": {
                "unit_of_measurement": "°C",
                "friendly_name": sensor.replace("_", " ").title(),
            },
        }
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            print(f"{sensor} with {data['state']}°C, updated successfully!")
        else:
            print(f"Failed to update {sensor}. Status code: {response.status_code}")
            print(response.json())
