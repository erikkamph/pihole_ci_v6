from .models.config import PiHoleConfig
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from typing import Any


class PiHoleData(object):
    _coordinator: DataUpdateCoordinator[None]
    _config: PiHoleConfig
    _entities: list[Any]
    _manifest: dict[str, Any]

    def __init__(self, coordinator: DataUpdateCoordinator[None], config: PiHoleConfig, manifest: dict[str, Any]):
        self._coordinator = coordinator
        self._config = config
        self._entities = []
        self._manifest = manifest

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

    @property
    def manifest(self):
        return self._manifest