from .models.config import PiHoleConfig
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from typing import Any


class PiHoleData(object):
    _coordinator: DataUpdateCoordinator[None]
    _config: PiHoleConfig
    _entities: list[Any]

    def __init__(self, coordinator: DataUpdateCoordinator[None], config: PiHoleConfig):
        self._coordinator = coordinator
        self._config = config
        self._entities = []

    @property
    def coordinator(self) -> DataUpdateCoordinator[None]:
        return self._coordinator
    
    @property
    def config(self) -> PiHoleConfig:
        self._config
    
    @property
    def entities(self) -> list[Any]:
        return self._entities
    
    @entities.setter
    def entities(self, val: list[Any] | Any):
        if isinstance(val, list):
            self._entities.extend(val)
        else:
            self._entities.append(val)