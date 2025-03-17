from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.core import HomeAssistant, callback
from homeassistant.components.binary_sensor import BinarySensorDeviceClass, BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from uuid import uuid4


class PiHoleBlockingSensor(CoordinatorEntity, BinarySensorEntity):
    def __init__(self, config: ConfigEntry, idx: int):
        self._config = config
        self._is_on: bool | None = True
        self._name = "Pi-Hole Blocking"
        self._idx = idx
        self._attr_unique_id = f"{uuid4()}-BinarySensor"
        super().__init__(self._config.runtime_data.coordinator, self._idx)

    @callback
    def _handle_coordinator_update(self) -> None:
        blocking = self.coordinator.data['blocking']
        self._is_on = blocking.is_blocking
        self.async_write_ha_state()
    
    @property
    def is_on(self) -> bool:
        return self._is_on
    
    @property
    def device_class(self) -> BinarySensorDeviceClass:
        return BinarySensorDeviceClass.RUNNING
    
    @property
    def unique_id(self):
        return self._attr_unique_id
    
    @property
    def name(self):
        return self._name