from homeassistant.components.binary_sensor import BinarySensorEntity, BinarySensorDeviceClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .entity import PiHoleEntity
from homeassistant.helpers.entity_platform import AddEntitiesCallback

async def async_setup_entry(hass: HomeAssistant, config: ConfigEntry, async_add_entities: AddEntitiesCallback):
    entities = [IsBlocking]

    async_add_entities(
        [i(hass, config) for i in entities]
    )

class IsBlocking(PiHoleEntity, BinarySensorEntity):
    def __init__(self, hass: HomeAssistant, config: ConfigEntry):
        self._config = config
        self._hass = hass
        self._api = self._config.runtime_data.api
        self._is_on: bool | None = True
        super().__init__(self._config.runtime_data.coordinator, self._config.runtime_data.config.name, self._server_unique_id, self._config.data)
    
    async def async_update(self):
        blocking = self._api.data['blocking']
        self._is_on = blocking.is_blocking
        self.async_write_ha_state()
    
    @property
    def is_on(self) -> bool:
        return self._is_on
    
    @property
    def device_class(self) -> BinarySensorDeviceClass:
        return BinarySensorDeviceClass.RUNNING