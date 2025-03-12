import logging
from datetime import timedelta
from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.core import callback

from .models.dns import PiHoleDnsBlocking
from .entity import PiHoleEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.config_entries import ConfigEntry
from .data import PiHoleConfigData

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant,
                            entry: PiHoleConfigData,
                            async_add_entities: AddEntitiesCallback):
    switches = [ToggleHole(entry.runtime_data.coordinator, 0, name=entry.runtime_data.config.name)]
    async_add_entities(switches)
    

class ToggleHole(PiHoleEntity, SwitchEntity):
    def __init__(self, coordinator, idx):
        super().__init__(coordinator, context=idx)
        self.is_on = True
        self.idx = idx

    @callback
    def _handle_coordinator_update(self) -> None:
        blocking = PiHoleDnsBlocking(**self.coordinator.data[self.idx]['blocking'])
        self.is_on = blocking.model_dump()['blocking']
        self.async_write_ha_state()

    @property
    def name(self) -> str:
        return self._name

    @property
    def icon(self) -> str:
        return "mdi:pi-hole"
    
    @property
    def unique_id(self) -> str:
        return f"{self._attr_unique_id}/Switch"
    
    @property
    def is_on(self) -> bool:
        return self.is_on
    
    async def async_turn_on(self, **kwargs):
        await self.device.toggle()
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs):
        await self.async_disable(timedelta(minutes=5).seconds)
        await self.coordinator.async_request_refresh()

    async def async_disable(self, duration: Any = None, **kwargs):
        duration_seconds = True
        if duration:
            duration_seconds = duration
        try:
            await self.device.toggle(
                blocking=False,
                timer=duration_seconds
            )
        except Exception as error:
            _LOGGER.exception(str(error), stack_info=True)
            return True
