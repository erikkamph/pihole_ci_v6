from homeassistant.components.switch import SwitchEntity
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from .hole import PiHole
from datetime import timedelta
from secrets import token_hex

async def async_setup_entry(hass: HomeAssistant,
                            config: ConfigEntry,
                            async_add_entities: AddEntitiesCallback):

    device = PiHole(config.data)
    switch = ToggleHole(device)
    async_add_entities([switch], True)


class ToggleHole(SwitchEntity):
    def __init__(self, device: PiHole):
        self._attr_name = "Pi-Hole"
        self._attr_unique_id = f"switch.hole_{token_hex(4)}"
        self.device = device
        self._is_on = True

    @property
    def icon(self) -> str:
        return "mdi:pi-hole"
    
    @property
    def unique_id(self) -> str:
        return f"{self.unique_id}/Switch"
    
    @property
    def is_on(self) -> bool:
        return self._is_on
    
    async def async_turn_on(self, **kwargs):
        self._is_on = await self.device.toggle()
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        timer = timedelta(minutes=5).seconds
        self._is_on = await self.device.toggle(False, timer)
        self.async_write_ha_state()
