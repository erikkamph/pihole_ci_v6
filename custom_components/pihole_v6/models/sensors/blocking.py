from homeassistant.core import callback, HomeAssistant
from homeassistant.components.binary_sensor import BinarySensorDeviceClass, BinarySensorEntity, BinarySensorEntityDescription
from homeassistant.config_entries import ConfigEntry
from uuid import uuid4
from ...entity import PiHoleEntity


class PiHoleBlockingSensor(PiHoleEntity, BinarySensorEntity):
    def __init__(self, hass: HomeAssistant, config: ConfigEntry, idx: int):
        self._config = config
        self._is_on: bool | None = True
        self._idx = idx
        self.entity_description = BinarySensorEntityDescription(
            name="Pi-Hole Blocking",
            key="hole_blocking",
            translation_key="hole_blocking",
            icon="mdi:pi-hole",
            has_entity_name=True,
            device_class=BinarySensorDeviceClass.RUNNING
        )
        self._attr_device_class = self.entity_description.device_class
        self._name = self.entity_description.name
        self._attr_unique_id = f"{config.entry_id}/{self.entity_description.key}"
        self._attr_has_entity_name = True
        super().__init__(self._config.runtime_data.coordinator, self._name, config.entry_id, config, hass, self._idx)

    @property
    def has_entity_name(self):
        return self._attr_has_entity_name
    
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
        return self._attr_device_class
    
    @property
    def unique_id(self):
        return self._attr_unique_id
    
    @property
    def name(self):
        return self._name

    @property
    def icon(self):
        return self.entity_description.icon