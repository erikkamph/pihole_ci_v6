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
    "active_clients": {
        "translation_key": "active_clients",
        "key": "active_clients",
        "name": "Active clients"
    },
    "gravity_size": {
        "translation_key": "gravity_size",
        "key": "gravity_size",
        "name": "Domains blocked by gravity"
    },
    "queries.total": {
        "translation_key": "total_queries",
        "key": "total_queries",
        "name": "Queries made last 24 hours"
    },
    "queries.blocked": {
        "translation_key": "blocked_queries",
        "key": "blocked_queries",
        "name": "Blocked queries last 24 hours"
    },
    "queries.percent_blocked": {
        "translation_key": "percentage_blocked",
        "key": "percentage_blocked",
        "name": "Percentage of queries blocked"
    },
    "cache.size": {
        "translation_key": "cache_size",
        "key": "cache_size",
        "name": "Cache size"
    },
    "iface.v4.name": {
        "translation_key": "iface",
        "key": "iface",
        "name": "Configured interface"
    }
}

binary_statistic_sensor = {
    "config.dhcp_active": {
        "translation_key": "dhcp_active",
        "key": "dhcp_active",
        "name": "DHCP Active"
    },
    "config.dns_dnssec": {
        "translation_key": "dnssec",
        "key": "dnssec",
        "name": "DNSSEC enabled"
    }
}


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
