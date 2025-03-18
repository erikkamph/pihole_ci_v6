from homeassistant.core import callback
from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.importlib import async_import_module
from ...exceptions import HoleException
import logging, asyncio
from uuid import uuid4


_LOGGER = logging.getLogger(__name__)

class PiHoleStatisticSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, context, statistic_path: str, description: SensorEntityDescription):
        self._name = description.name
        self._attr_available = False
        self._keyword = 'statistics'
        self._native_value = None
        self._statistic_path = statistic_path
        self.entity_description = description
        self._attr_unique_id = f"{uuid4()}-{self.entity_description.key}-Sensor"
        super().__init__(coordinator, context)

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