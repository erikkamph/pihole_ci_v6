from .hole import PiHole
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.core import HomeAssistant
from homeassistant.const import CONF_NAME
from homeassistant.config_entries import ConfigEntry
import logging, async_timeout
from datetime import timedelta, datetime
from .exceptions import HoleException
from homeassistant.exceptions import ConfigEntryAuthFailed
from .models.const import MIN_TIME_BETWEEN_UPDATES

_LOGGER = logging.getLogger(__name__)


class PiHoleUpdateCoordinator(DataUpdateCoordinator):
    def __init__(self, hass: HomeAssistant, config: ConfigEntry):
        super().__init__(
            hass,
            _LOGGER,
            config_entry=config,
            name=config.data[CONF_NAME],
            update_interval=MIN_TIME_BETWEEN_UPDATES,
            always_update=True
        )
        self._device: PiHole | None
        self.config = config
        self._git_next_update = datetime.now()
        self._git_last_update = None

    async def _async_setup(self):
        self._device = PiHole(self.hass, self.config)
    
    async def _async_update_data(self):
        try:
            async with async_timeout.timeout(30):
                if not await self._device.verify_session():
                    await self._device.update_session()
                
                await self._device.update_blocking()
                await self._device.update_versions()
                await self._device.update_statistics()

                if datetime.now() > self._git_next_update:
                    self._git_last_update = datetime.now()
                    await self._device.update_summary("erikkamph/pihole_ci_v6")
                    self._git_next_update = self._git_last_update + timedelta(days=7)
                
                return self._device.data
        except HoleException as err:
            raise ConfigEntryAuthFailed from err
        except TimeoutError as err:
            raise UpdateFailed(f"Error communicating with API")


