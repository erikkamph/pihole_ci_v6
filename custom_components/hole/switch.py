from homeassistant.components.switch import SwitchEntity
from .hole import PiHole
from homeassistant.const import CONF_URL, CONF_API_KEY

class ToggleHole(SwitchEntity):
    def __init__(self, device: PiHole):
        self._attr_name = "Pi-Hole"
        self._attr_unique_id = "switch.hole"
        self._is_on = False
        self.device = device

    @property
    def icon(self):
        return "mdi:pi-hole"
    
    @property
    def is_on(self):
        return self._is_on
    
    async def async_turn_on(self, **kwargs):
        self._is_on = await self.device.turn_on()
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        self._is_on = await self.device.turn_off()
        self.async_write_ha_state()
