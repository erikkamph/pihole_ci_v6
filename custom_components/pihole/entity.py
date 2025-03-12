from __future__ import annotations


from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator
)
from .models.config import PiHoleConfig
from .models.const import DOMAIN


class PiHoleEntity(CoordinatorEntity[DataUpdateCoordinator[None]]):
    def __init__(self,
                 coordinator: DataUpdateCoordinator[None],
                 name: str,
                 server_unique_id: str,
                 device_config: dict):
        super().__init__(coordinator)
        self.config = PiHoleConfig(**device_config)
        self._name = name
        self._server_unique_id = server_unique_id

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            identifiers={{DOMAIN, self._server_unique_id}},
            name=self._name,
            manufacturer='Pi-Hole',
            configuration_url=self.config.api_url
        )