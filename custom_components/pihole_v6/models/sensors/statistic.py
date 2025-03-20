from homeassistant.core import callback, HomeAssistant
from homeassistant.components.sensor import SensorEntity, SensorEntityDescription, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from ...exceptions import HoleException
from ...entity import PiHoleEntity
import datetime


class PiHoleStatisticSensor(PiHoleEntity, SensorEntity):
    def __init__(self, coordinator, context, statistic_path: str, description: SensorEntityDescription, config: ConfigEntry, hass: HomeAssistant):
        self._name = description.name
        self._attr_available = False
        self._keyword = 'statistics'
        self._native_value = None
        self._statistic_path = statistic_path
        self.entity_description = description
        self._attr_unique_id = f"{config.entry_id}/{self.entity_description.key}"
        self._attr_state_class = SensorStateClass.TOTAL if self._statistic_path == "gravity" else SensorStateClass.MEASUREMENT
        super().__init__(coordinator, self._name, config.entry_id, config, hass, context)

    @callback
    def _handle_coordinator_update(self):
        if self._keyword in self.coordinator.data:
            statistics = self.coordinator.data[self._keyword]

            if self._statistic_path == "gravity":
                self._native_value = statistics[f"{self._statistic_path}.domains_being_blocked"]
                epoch = statistics[f"{self._statistic_path}.last_update"]
                self._attr_last_reset = datetime.datetime.fromtimestamp(float(epoch))
            else:
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
    
    @property
    def last_reset(self):
        if hasattr(self, '_attr_last_reset'):
            return self._attr_last_reset
        return None