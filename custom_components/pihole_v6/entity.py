from .hole import PiHole
from homeassistant.config_entries import ConfigEntry
from .coordinator import PiHoleUpdateCoordinator
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from typing import Any
from homeassistant.helpers.device_registry import DeviceInfo
from .models.const import DOMAIN
from homeassistant.core import HomeAssistant


class PiHoleEntity(CoordinatorEntity[PiHoleUpdateCoordinator]):
    def __init__(self, 
                 coordinator: PiHoleUpdateCoordinator,
                 name: str,
                 server_unique_id: str,
                 config_entry: ConfigEntry,
                 hass: HomeAssistant,
                 context: Any | None = None):
        super().__init__(coordinator, context)
        self._name = name
        self._server_unique_id = server_unique_id
        self.api = PiHole(hass, config_entry)
    
    @property
    def device_info(self):
        return DeviceInfo(
            identifiers=set((DOMAIN, self._server_unique_id)),
            name=self.api.config.name.title(),
            manufacturer="Pi-Hole",
            configuration_url=self.api.config.api_url
        )