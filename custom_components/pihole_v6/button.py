from homeassistant.components.button import ButtonEntity, ButtonEntityDescription, ButtonDeviceClass
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.core import HomeAssistant, callback
from homeassistant.config_entries import ConfigEntry
from .entity import PiHoleEntity
from .coordinator import PiHoleUpdateCoordinator
from typing import Any
from enum import Enum
from .hole import PiHole
from .exceptions import HoleException
import logging

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant,
                            config: ConfigEntry,
                            async_add_entities: AddEntitiesCallback):
    buttons = []
    for key in PiHoleAction:
        button = UpdateButton(
            config.runtime_data.coordinator,
            config.entry_id,
            config,
            hass,
            ButtonEntityDescription(
                key=key.name,
                translation_key=key.name,
                name=key.name.replace("_", " ").title()
            ),
            key,
            0
        )
        buttons.append(button)

    config.runtime_data.entities = buttons
    async_add_entities(buttons)


class PiHoleAction(str, Enum):
    flush_arp = "/flush/arp"
    flush_logs = "/flush/logs"
    update_gravity = "/gravity"
    restart_dns = "/restartdns"


class UpdateButton(PiHoleEntity, ButtonEntity):
    def __init__(self,
                 coordinator: PiHoleUpdateCoordinator,
                 server_unique_id: str,
                 config: ConfigEntry,
                 hass: HomeAssistant,
                 description: ButtonEntityDescription,
                 action: PiHoleAction,
                 context: Any = None):
        super().__init__(coordinator, description.name, server_unique_id, config, hass, context)
        self._attr_device_class = ButtonDeviceClass.UPDATE
        self.entity_description = description
        self._attr_unique_id = f"{server_unique_id}/{description.key}"
        self._attr_action = action
        self._api = PiHole(hass, config)
        self._attr_icon = "mdi:gesture-tap-button"

    @property
    def action(self):
        return self._attr_action
    
    @property
    def name(self):
        return self._name
    
    async def async_press(self):
        try:
            action_url = f"action{self._attr_action.value}"
            await self._api.run_action(action_url)
        except HoleException as ex:
            _LOGGER.error(ex)

    @property
    def icon(self):
        return self._attr_icon