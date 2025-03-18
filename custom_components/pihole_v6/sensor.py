from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from .models.sensors.version import PiHoleVersionSensor
from .models.sensors.blocking import PiHoleBlockingSensor
from .models.sensors.statistic import PiHoleStatisticSensor
from .models.const import DOMAIN

statistic_sensors = {
    "active_clients": "Active clients",
    "gravity_size": "Domains blocked by Gravity",
    "queries.total": "Queries made last 24h",
    "queries.blocked": "Blocked queries last 24h",
    "queries.percent_blocked": "Percentage of queries blocked"
}


async def async_setup_entry(hass: HomeAssistant, config: ConfigEntry, async_add_entities: AddEntitiesCallback):
    sensors = []
    sensors.append(PiHoleBlockingSensor(config, 0))

    version_sensors = ["core", "web", "ftl"]
    for sensor in version_sensors:
        sensors.append(PiHoleVersionSensor(config, sensor, 0))

    coordinator = config.runtime_data.coordinator
    for key, val in statistic_sensors.items():
        sensors.append(PiHoleStatisticSensor(coordinator, 0, val, key))

    if sensors not in config.runtime_data.entities:
        async_add_entities(sensors)
        config.runtime_data.entities = sensors
