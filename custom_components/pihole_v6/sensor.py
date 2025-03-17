from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from .models.sensors.version import PiHoleVersionSensor
from .models.sensors.blocking import PiHoleBlockingSensor
from .models.sensors.statistic import PiHoleStatisticSensor
from .models.const import DOMAIN

statistic_sensors = {
    "queries.total": "Total Queries",
    "queries.blocked": "Blocked Queries",
    "queries.unique_domains": "Unique Domains",
    "queries.percent_blocked": "Percentage of ads blocked",
    "clients.active": "Number of active clients",
    "clients.total": "Total number of seen clients",
    "gravity.domains_being_blocked": "Domains being blocked by gravity lists"
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
