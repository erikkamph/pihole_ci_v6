from homeassistant.components.binary_sensor import BinarySensorEntity, BinarySensorDeviceClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .entity import PiHoleEntity

class IsBlocking(PiHoleEntity, BinarySensorEntity):
    def __init__(self, hass: HomeAssistant, config: ConfigEntry):
        self._config = config
        self._hass = hass
        self._api = self._config.runtime_data.api
        super().__init__(self._config.runtime_data.coordinator, self._config.runtime_data.config.name, self._server_unique_id, self._config.data)
    
    async def async_update(self):
        pass