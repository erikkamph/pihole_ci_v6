from .hole import PiHole
from .models.config import PiHoleConfig
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator


class PiHoleData(object):
    api: PiHole
    coordinator: DataUpdateCoordinator[None]
    config: PiHoleConfig

    def __init__(self, api: PiHole, coordinator: DataUpdateCoordinator[None], config: PiHoleConfig):
        self.api = api
        self.coordinator = coordinator
        self.config = config