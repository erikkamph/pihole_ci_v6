import validators
from .exceptions import HoleConnectionError, HoleError 
import logging
from homeassistant.const import (
    CONF_NAME,
    CONF_HOST,
    CONF_API_KEY,
    CONF_PORT, 
    CONF_SSL,
    CONF_LOCATION
)
from typing import Any
import aiohttp

_LOGGER = logging.getLogger(__name__)


class PiHole():
    def __init__(self, config: dict[str, Any]):
        if not config[CONF_HOST]:
            raise ValueError('You need to set PI_HOLE_location!')
        
        if not config[CONF_API_KEY]:
            raise ValueError('You need to set PI_HOLE_PASSWORD in-order to get access!')
        
        if not validators.url(config[CONF_HOST]):
            raise ValueError(f'The url {config[CONF_HOST]} is not a valid url!')

        self.host = config[CONF_HOST]
        self.verify = config[CONF_SSL]
        self.key = config[CONF_API_KEY]
        self.port = config[CONF_PORT]
        self.name = config[CONF_NAME]
        self.location = config[CONF_LOCATION]

        self.host_base = self.host if self.port == 80 or self.port == 443 else f"{self.host}:{self.port}"
        self.api_base = f"{self.host_base}/{self.location}/"

    @staticmethod
    async def async_setup(data: dict) -> bool:
        service = PiHole(data)
        if await service.auth():
            _LOGGER.info("works!")
            return True
        _LOGGER.error('Invalid URL or password/api_key for pi-hole instance!')
        return False

    async def __call__(self, params: dict = {}):
        async with aiohttp.ClientSession(base_url=self.api_base) as session:
            method = {
                'POST': session.post,
                'GET': session.get
            }
            fn = method[params['method']]
            async with fn(url=params['url'], headers=params['headers'], json=params.get('json', None)) as res:
                return await res.json() if res.status == 200 else None

    async def auth(self):
        params = {
            'method': 'POST',
            'json': {'password': self.key},
            'url': 'auth',
            'headers': {'Content-Type': 'application/json'}
        }
        if (r := await self(params)) is not None:
            headers = {
                'X-FTL-SID': r['session']['sid'],
                'X-FTL-CSRF': r['session']['csrf']
            }
            return headers
        return None

    async def blocking(self):
        if (headers := await self.auth()) is not None:
            params = {
                'method': 'GET',
                'url': 'dns/blocking',
                'headers': headers
            }
            if (r := await self(params)) is not None:
                return r['blocking'] == 'enabled'
            raise HoleError('An error from the pi-hole API occurred!')
        raise HoleConnectionError('Not authorized to make calls to the API')
    
    async def version(self):
        if (headers := await self.auth()) is not None:
            params = {
                'headers': headers,
                'url': 'info/version',
                'method': 'GET'
            }
            if (r := await self(params)) is not None:
                return r
            raise HoleError('An error from the pi-hole API occurred!')
        raise HoleConnectionError('Not authorized to make calls to the API')
    
    async def toggle(self, blocking: bool = True, timer: int | None = None):
        if (headers := await self.auth()) is not None:
            params = {
                'headers': headers,
                'url': 'dns/blocking',
                'json': {
                    'blocking': blocking,
                    'timer': timer
                },
                'method': 'POST'
            }
            if (_ := await self(params)) is not None:
                return blocking
            return HoleError('An error from the pi-hole API occurred!')
        raise HoleConnectionError('Not authorized to make calls to the API')