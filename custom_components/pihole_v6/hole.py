import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .models.config import PiHoleConfig
from .models.auth import PiHoleAuth
from .models.const import HEADER_CSRF, HEADER_SID
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from .exceptions import HoleException

_LOGGER = logging.getLogger(__name__)


class PiHole():
    def __init__(self, hass: HomeAssistant, config: ConfigEntry):
        self.entry = config
        self.config = PiHoleConfig(**self.entry.data)
        self.client = async_get_clientsession(hass, self.config.verify)
        self.hass = hass
        self.data = {}

    async def __call__(self, call: dict):
        method = {
            'post': self.client.post,
            'get': self.client.get,
            'delete': self.client.delete
        }
        tmp_method = call['method']
        async with method[tmp_method](**call['request']) as r:
            if r.status == 200:
                return await r.json()
            raise HoleException(await r.text())
        raise HoleException("Something unexpected happened with the request, session or client.")

    async def verify_session(self):
        request = {
            'method': 'GET',
            'request': {
                'url': f"{self.config.api_url}auth",
                'headers': {
                    HEADER_SID: self.config.sid,
                    HEADER_CSRF: self.config.csrf
                }
            }
        }
        response = await self(request)
        auth_response = PiHoleAuth(**response)
        return auth_response.session.valid
    
    async def update_session(self):
        request = {
            'method': 'POST',
            'request': {
                'url': f"{self.config.api_url}auth",
                'json': self.config.auth_data,
                'headers': {'Content-Type': 'application/json'}
            }
        }
        response = await self(request)
        auth_data = PiHoleAuth(**response)
        self.config.csrf = auth_data.session.csrf
        self.config.sid = auth_data.session.sid
        await self.hass.config_entries.async_update_entry(self.entry, data=self.config.model_dump(by_alias=True))
    
    async def update_blocking(self):
        request = {
            'method': 'GET',
            'request': {
                'url': f'{self.config.api_url}dns/blocking',
                'headers': {
                    HEADER_SID: self.config.sid,
                    HEADER_CSRF: self.config.csrf
                }
            }
        }
        response = await self(call=request)
        if "blocking" in self.data:
            self.data['blocking'] = response
        else:
            self.data.update({"blocking": response})

    async def update_versions(self):
        pass

    async def update_statistics(self):
        pass

    async def toggle(self, blocking: bool = True, timer: int = None):
        await self.verify_or_update_session()
        async with self.client.post(
            url="/dns/blocking",
            json={"blocking": blocking, "timer": timer},
            headers={
                HEADER_CSRF: self.config.csrf,
                HEADER_SID: self.config.sid
            }
        ) as r:
            if r.status == 200:
                return blocking
            raise Exception(await r.text)
