from homeassistant.core import callback, HomeAssistant
from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.config_entries import ConfigEntry
from ...exceptions import HoleException
from ...entity import PiHoleEntity


class PiHoleStatisticSensor(PiHoleEntity, SensorEntity):
    def __init__(self, coordinator, context, statistic_path: str, description: SensorEntityDescription, config: ConfigEntry, hass: HomeAssistant):
        self._name = description.name
        self._attr_available = False
        self._keyword = 'statistics'
        self._native_value = None
        self._statistic_path = statistic_path
        self.entity_description = description
        self._attr_unique_id = f"{config.entry_id}/{self.entity_description.key}"
        super().__init__(coordinator, self._name, config.entry_id, config, hass, context)

    @callback
    def _handle_coordinator_update(self):
        if self._keyword in self.coordinator.data:
            statistics = self.coordinator.data[self._keyword]
            self._native_value = statistics[self._statistic_path]
            self._attr_available = True
            self.async_write_ha_state()
        else:
            raise HoleException(f'Failed to update entity {self._attr_unique_id}')

    @property
    def native_value(self):
        return self._native_value
    
    @property
    def name(self):
        return self._name