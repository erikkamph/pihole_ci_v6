from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.components.sensor import SensorEntityDescription
from homeassistant.components.binary_sensor import BinarySensorEntityDescription
from .models.sensors.version import PiHoleVersionSensor
from .models.sensors.blocking import PiHoleBlockingSensor
from .models.sensors.statistic import PiHoleStatisticSensor
from .models.sensors.binary_statistic import PiHoleBinaryStatistic

statistic_sensors = {
    "clients.active": {
        "name": "Active clients (last 24 hours)",
        "translation_key": "active_clients",
        "key": "active_clients",
        "unit_of_measurement": "clients",
        "has_entity_name": True,
        "icon": "mdi:devices"
    },
    "clients.total": {
        "name": "Total clients",
        "translation_key": "total_clients",
        "key": "total_clients",
        "unit_of_measurement": "clients",
        "has_entity_name": True,
        "icon": "mdi:devices"
    },
    "queries.total": {
        "name": "Total queries made",
        "translation_key": "total_queries",
        "key": "total_queries",
        "unit_of_measurement": "queries",
        "has_entity_name": True,
        "icon": ""
    },
    "queries.blocked": {
        "name": "Blocked queries",
        "translation_key": "blocked_queries",
        "key": "blocked_queries",
        "unit_of_measurement": "queries",
        "has_entity_name": True,
        "icon": "mdi:close-octagon-outline"
    },
    "queries.percent_blocked": {
        "name": "Percentage of queries blocked",
        "translation_key": "blocked_percentage",
        "key": "blocked_percentage",
        "unit_of_measurement": "%",
        "has_entity_name": True,
        "icon": "mdi:close-octagon-outline",
        "suggested_display_precision": 2
    },
    "queries.forwarded": {
        "name": "Number of queries forwarded",
        "translation_key": "forwarded_queries",
        "key": "forwarded_queries",
        "unit_of_measurement": "queries",
        "has_entity_name": True,
        "icon": "mdi:forwardburger"
    },
    "gravity": {
        "name": "Number of domains blocked by Gravity",
        "translation_key": "gravity_statistics",
        "key": "gravity_statistics",
        "unit_of_measurement": "domains",
        "has_entity_name": True,
        "icon": "mdi:domain"
    }
}

binary_statistic_sensor = {}


async def async_setup_entry(hass: HomeAssistant, config: ConfigEntry, async_add_entities: AddEntitiesCallback):
    sensors = []
    sensors.append(PiHoleBlockingSensor(hass, config, 0))

    version_sensors = ["core", "web", "ftl"]
    for sensor in version_sensors:
        sensors.append(PiHoleVersionSensor(hass, config, sensor, 0))

    coordinator = config.runtime_data.coordinator
    for key in statistic_sensors.keys():
        description = SensorEntityDescription(**statistic_sensors[key])
        sensors.append(PiHoleStatisticSensor(coordinator, 0, key, description, config, hass))

    for key in binary_statistic_sensor.keys():
        description = BinarySensorEntityDescription(**binary_statistic_sensor[key])
        sensors.append(PiHoleBinaryStatistic(coordinator, config.entry_id, config, hass, key, description, 0))

    if sensors not in config.runtime_data.entities:
        async_add_entities(sensors)
        config.runtime_data.entities = sensors
