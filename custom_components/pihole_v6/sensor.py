from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from .models.sensors.version import PiHoleVersionSensor
from .models.sensors.blocking import PiHoleBlockingSensor
from .models.const import DOMAIN


async def async_setup_entry(hass: HomeAssistant, config: ConfigEntry, async_add_entities: AddEntitiesCallback):
    sensors = []
    sensors.append(PiHoleBlockingSensor(hass, config, 0))

    version_sensors = ["core", "web", "ftl"]
    for sensor in version_sensors:
        sensors.append(PiHoleVersionSensor(hass, config, sensor, f"{sensor} version".title(), 0))

    if sensors not in hass.data[DOMAIN][config.entry_id]:
        async_add_entities(sensors)
        hass.data[DOMAIN][config.entry_id].extend(sensors)
