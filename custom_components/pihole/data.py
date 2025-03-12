from .hole import PiHole
from .models.config import PiHoleConfig
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

type PiHoleConfigData = ConfigEntry[PiHoleData]
class PiHoleData:
    api: PiHole
    coordinator: DataUpdateCoordinator[None]
    config: PiHoleConfig