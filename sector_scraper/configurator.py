from typing import Any, Dict, List

from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import DoubleQuotedScalarString
from unidecode import unidecode


def clean_text(text: str) -> str:
    return unidecode(text).lower()


# Function to create the YAML configuration for sensors
def create_sensor_config(temperature_lst: List[Dict[str, str]]) -> Dict[str, Any]:
    data: Dict[str, Any] = {"sensor": [{"platform": "template", "sensors": {}}]}

    for record in temperature_lst:
        clean_area_name = clean_text(record["area_name"])
        clean_room = clean_text(record["room"])
        sensor_name = f"temperature_{clean_area_name}_{clean_room}"

        data["sensor"][0]["sensors"][sensor_name] = {
            "friendly_name": DoubleQuotedScalarString(
                f"Temperature {record['area_name']} {record['room']}"
            ),
            "unit_of_measurement": DoubleQuotedScalarString("°C"),
            "value_template": DoubleQuotedScalarString(
                f"{{{{ states('sensor.{sensor_name}') | float }}}}"
            ),
            "unique_id": DoubleQuotedScalarString(f"{sensor_name}"),
        }

    return data


# Function to create the YAML configuration for automation
def create_automation_config(
    temperature_lst: List[Dict[str, str]]
) -> List[Dict[str, Any]]:
    entity_ids = [
        f"sensor.temperature_{clean_text(record['area_name'])}_{clean_text(record['room'])}"
        for record in temperature_lst
    ]
    data: List[Dict[str, Any]] = [
        {
            "id": DoubleQuotedScalarString("initialize_temperature_sensors"),
            "alias": DoubleQuotedScalarString("Initialize Temperature Sensors"),
            "description": DoubleQuotedScalarString(
                "Set initial states for temperature sensors"
            ),
            "trigger": [
                {
                    "platform": DoubleQuotedScalarString("homeassistant"),
                    "event": DoubleQuotedScalarString("start"),
                }
            ],
            "action": [
                {
                    "service": DoubleQuotedScalarString("homeassistant.update_entity"),
                    "target": {"entity_id": entity_ids},
                }
            ],
        }
    ]
    return data


def save_yaml(data: Any, filename: str):
    yaml = YAML()
    yaml.default_flow_style = False
    yaml.allow_unicode = True
    yaml.width = 1000

    with open(filename, "w") as stream:
        yaml.dump(data, stream)

    with open(filename, "r") as stream:
        yaml_output = stream.read()
        print(yaml_output)


# Example usage
if __name__ == "__main__":
    temperature_lst = [
        {"area_name": "Entréplan", "room": "Kök"},
        {"area_name": "Entréplan", "room": "Entréhall"},
        {"area_name": "Vind", "room": "LillaVinden"},
        {"area_name": "Källare", "room": "Tvättstuga"},
    ]

    sensor_config = create_sensor_config(temperature_lst)
    automation_config = create_automation_config(temperature_lst)

    print("# Sensor Configuration:")
    save_yaml(sensor_config, "output/sensor_output.yaml")

    print("\n# Automation Configuration:")
    save_yaml(automation_config, "output/automation_output.yaml")
