from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .models.config import PiHoleConfig
from .models.auth import PiHoleAuth
from .models.const import HEADER_CSRF, HEADER_SID
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.importlib import async_import_module
from .exceptions import HoleException, HoleVersionError
from pydantic import BaseModel
from .models.summary import PiHoleSummary
from .models.dns import PiHoleDnsBlocking
from .models.version import PiHoleVersionInfo
import pandas as pd
import logging

_LOGGER = logging.getLogger(__name__)


class PiHole():
    def __init__(self, hass: HomeAssistant, config: ConfigEntry):
        self.entry = config
        self.config = PiHoleConfig(**self.entry.data)
        self.client = async_get_clientsession(hass, self.config.verify)
        self.hass = hass
        self.data = {}

    async def __call__(self, call: dict, skip_status: bool = False):
        method = {
            'post': self.client.post,
            'get': self.client.get,
            'delete': self.client.delete
        }
        tmp_method = call['method'].lower()
        async with method[tmp_method](**call['request']) as r:
            if skip_status or r.status == 200:
                if r.content_type == "application/json":
                    return await r.json()
                else:
                    return None
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
        response = await self(request, skip_status=True)
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
        self.hass.config_entries.async_update_entry(self.entry, data=self.config.model_dump(by_alias=True))
    
    async def update_data(self, key: str, data: BaseModel | dict) -> None:
        if key in self.data:
            self.data[key] = data
        else:
            self.data.update({key: data})

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
        blocking = PiHoleDnsBlocking(**response)
        await self.update_data("blocking", blocking)

    async def update_versions(self):
        request = {
            'method': 'GET',
            'request': {
                'url': f'{self.config.api_url}info/version',
                'headers': {
                    HEADER_SID: self.config.sid,
                    HEADER_CSRF: self.config.csrf
                }
            }
        }
        response = await self(call=request)
        versions = PiHoleVersionInfo(**response)
        await self.update_data("versions", versions)

    async def update_statistics(self):
        request = {
            'method': 'GET',
            'request': {
                'url': f'{self.config.api_url}stats/summary',
                'headers': {
                    HEADER_SID: self.config.sid,
                    HEADER_CSRF: self.config.csrf
                },
                "json": {
                    "full": True
                }
            }
        }
        response = await self(call=request)
        summary = PiHoleSummary(**response).model_dump()
        await async_import_module(self.hass, "tzdata")
        df = pd.json_normalize(summary, sep='.')
        data = df.to_dict(orient='records')[0]
        await self.update_data("statistics", data)

    async def update_summary(self, summary: str):
        request = {
            'method': 'GET',
            'request': {
                'url': f'https://api.github.com/repos/{summary}/releases/latest'
            }
        }
        response = await self(call=request)
        data = {
            'latest_version': response['tag_name'],
            'release_url': response['html_url'],
            'zip_file': None if len(response['assets']) < 1 else response['assets'][0]['browser_download_url'],
            'release_notes': response['body']
        }
        await self.update_data(summary, data)

    async def toggle(self, blocking: bool = True, timer: int = None):
        if not await self.verify_session():
            await self.update_session()
        
        request = {
            'method': 'POST',
            'request': {
                'url': f"{self.config.api_url}dns/blocking",
                'json': {'blocking': blocking, 'timer': timer},
                'headers': {
                    HEADER_CSRF: self.config.csrf,
                    HEADER_SID: self.config.sid
                }
            }
        }
        await self(call=request)
    
    async def version_is_newer(self, latest_version: str | None, installed_version: str | None):
        if not latest_version or latest_version == '':
            return False
        
        if not installed_version or installed_version == '':
            raise HoleVersionError("Unknown version installed")
        
        latest = ''.join(latest_version.replace("v", "").split("."))
        installed = ''.join(installed_version.replace("v", "").split("."))
        return int(latest) > int(installed)

    async def run_action(self, action_endpoint):
        request = {
            'method': 'POST',
            'request': {
                'url': f"{self.config.api_url}{action_endpoint}",
                'headers': {
                    HEADER_CSRF: self.config.csrf,
                    HEADER_SID: self.config.sid
                }
            }
        }
        await self(call=request)