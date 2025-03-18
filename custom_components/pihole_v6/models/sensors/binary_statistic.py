from homeassistant.components.binary_sensor import BinarySensorEntity, BinarySensorEntityDescription
from ...entity import PiHoleEntity
from homeassistant.core import HomeAssistant, callback
from homeassistant.config_entries import ConfigEntry
from ...coordinator import PiHoleUpdateCoordinator


class PiHoleBinaryStatistic(PiHoleEntity, BinarySensorEntity):
    def __init__(self, coordinator: PiHoleUpdateCoordinator, server_unique_id: str, config_entry: ConfigEntry, hass: HomeAssistant, key: str, description: BinarySensorEntityDescription, context = None):
        super().__init__(coordinator, description.name, server_unique_id, config_entry, hass, context)
        self._attr_available = False
        self._is_on = False
        self._key = key
        self._keyword = 'statistics'
        self.entity_description = description
        self._name = self.entity_description.name
        self._attr_unique_id = f"{server_unique_id}/{self.entity_description.key}"

    @callback
    def _handle_coordinator_update(self):
        if self._keyword in self.coordinator.data:
            stats = self.coordinator.data[self._keyword]
            state = stats[self._key]
            self._is_on = state
        self._attr_available = True
        self.async_write_ha_state()

    @property
    def name(self):
        return self._name
    
    @property
    def unique_id(self):
        return self._attr_unique_id
    
    @property
    def is_on(self):
        return self._is_on