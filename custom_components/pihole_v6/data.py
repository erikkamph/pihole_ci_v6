from .hole import PiHole
from .models.config import PiHoleConfig
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator


class PiHoleData(object):
    coordinator: DataUpdateCoordinator[None]
    config: PiHoleConfig

    def __init__(self, coordinator: DataUpdateCoordinator[None], config: PiHoleConfig):
        self.coordinator = coordinator
        self.config = config