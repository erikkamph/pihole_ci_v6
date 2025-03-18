from homeassistant.core import callback, HomeAssistant
from homeassistant.components.binary_sensor import BinarySensorDeviceClass, BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from uuid import uuid4
from ...entity import PiHoleEntity


class PiHoleBlockingSensor(PiHoleEntity, BinarySensorEntity):
    def __init__(self, hass: HomeAssistant, config: ConfigEntry, idx: int):
        self._config = config
        self._is_on: bool | None = True
        self._name = "Pi-Hole Blocking"
        self._idx = idx
        self._attr_unique_id = f"{config.entry_id}-BinarySensor"
        super().__init__(self._config.runtime_data.coordinator, self._name, config.entry_id, config, hass, self._idx)

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