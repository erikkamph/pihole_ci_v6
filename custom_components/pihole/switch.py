import logging
from datetime import timedelta
from typing import Any

import voluptuous as vol

from homeassistant.components.switch import SwitchEntity
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback, async_get_current_platform
from homeassistant.helpers import config_validation as cv

from .hole import PiHole
from .const import SERVICE_DISABLE, SERVICE_DISABLE_ATTR_DURATION

async def async_setup_entry(hass: HomeAssistant,
                            config: ConfigEntry,
                            async_add_entities: AddEntitiesCallback):

    device = PiHole(config.data)
    switch = ToggleHole(device)
    async_add_entities([switch], True)

    platform = async_get_current_platform()
    platform.async_register_entity_service(
        SERVICE_DISABLE,
        {
            vol.Required(SERVICE_DISABLE_ATTR_DURATION): vol.All(
                cv.time_period_str, cv.positive_timedelta
            )
        },
        "async_disable"
    )


class ToggleHole(SwitchEntity):
    def __init__(self, device: PiHole):
        self._attr_name = "Pi-Hole"
        self.device = device
        self._is_on = True

    @property
    def icon(self) -> str:
        return "mdi:pi-hole"
    
    @property
    def unique_id(self) -> str:
        return f"{self._attr_unique_id}/Switch"
    
    @property
    def is_on(self) -> bool:
        return self._is_on
    
    async def async_turn_on(self, **kwargs):
        self._is_on = await self.device.toggle()
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        self.disable(timedelta(minutes=5).seconds)
        self.async_write_ha_state()

    async def disable(self, duration: Any = None, **kwargs):
        duration_seconds = True
        if duration:
            duration_seconds = duration
        try:
            await self.device.toggle(
                blocking=False,
                timer=duration_seconds
            )
            await self.async_update()
        except Exception as error:
            _LOGGER.exception(str(error), stack_info=True)
