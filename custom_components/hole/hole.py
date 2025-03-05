import os
import validators
from .exceptions import HoleConnectionError, HoleError 
import logging
import httpx

_LOGGER = logging.getLogger(__name__)


class PiHole():
    def __init__(self,
                 pi_hole_api_url: str = os.getenv('PI_HOLE_API_URL', None),
                 pi_hole_password: str = os.getenv('PI_HOLE_PASSWORD', None)):
        if not pi_hole_api_url:
            raise ValueError('You need to set PI_HOLE_API_URL!')
        
        if not pi_hole_password:
            raise ValueError('You need to set PI_HOLE_PASSWORD in-order to get access!')
        
        if not validators.url(pi_hole_api_url):
            raise ValueError(f'The url {pi_hole_api_url} is not a valid url!')

        self.api = pi_hole_api_url
        self.verify = 'https' in self.api
        self.key = pi_hole_password
    
    @staticmethod
    async def async_setup(data: dict) -> bool:
        service = PiHole(
            pi_hole_api_url=data['url'],
            pi_hole_password=data['api_key']
        )
        if await service.auth():
            _LOGGER.info("works!")
            return True
        _LOGGER.error('Invalid URL or password/api_key for pi-hole instance!')
        return False

    async def __call__(self, params: dict = {}):
        async with httpx.AsyncClient(verify='https' in params['url']) as client:
            req = httpx.Request(**params)
            r = await client.send(req)
            if r.status_code == 200:
                response = r.json()
                return response
            _LOGGER.exception(r.text, stack_info=True)
            return None
        
    async def auth(self):
        params = {
            'method': 'POST',
            'json': {'password': self.key},
            'url': f'{self.api}/auth',
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
                'url': f'{self.api}/dns/blocking',
                'headers': headers
            }
            if (r := await self(params)) is not None:
                return r['blocking']
            raise HoleError('An error from the pi-hole API occurred!')
        raise HoleConnectionError('Not authorized to make calls to the API')
    
    async def version(self):
        if (headers := await self.auth()) is not None:
            params = {
                'headers': headers,
                'url': f'{self.api}/info/version',
                'method': 'GET'
            }
            if (r := await self(params)) is not None:
                return r
            raise HoleError('An error from the pi-hole API occurred!')
        raise HoleConnectionError('Not authorized to make calls to the API')
    
    async def turn_off(self):
        if (headers := await self.auth()) is not None:
            params = {
                'headers': headers,
                'url': f'{self.api}/dns/blocking',
                'json': {
                    'blocking': False,
                    'timer': 500
                },
                'method': 'POST'
            }
            if (r := await self(params)) is not None:
                return r['blocking']
            return HoleError('An error from the pi-hole API occurred!')
        raise HoleConnectionError('Not authorized to make calls to the API')

    async def turn_on(self):
        if (headers := await self.auth()) is not None:
            params = {
                'headers': headers,
                'url': f'{self.api}/dns/blocking',
                'json': {
                    'blocking': True,
                },
                'method': 'POST'
            }
            if (r := await self(params)) is not None:
                return r['blocking']
            return HoleError('An error from the pi-hole API occurred!')
        raise HoleConnectionError('Not authorized to make calls to the API')