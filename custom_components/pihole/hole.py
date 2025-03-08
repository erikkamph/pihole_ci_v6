from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.const import (
    CONF_LOCATION,
    CONF_HOST,
    CONF_API_KEY,
    CONF_VERIFY_SSL,
)
from .const import (
    CONF_SID,
    CONF_CSRF
)
import aiohttp

class PiHole():
    def __init__(self, hass: HomeAssistant, config: ConfigEntry):
        self.entry = config.data
        self.api_url = f"{self.entry[CONF_HOST]}/{self.entry[CONF_LOCATION]}"
        self.client = aiohttp.ClientSession(base_url=self.api_url)
    
    async def verify_or_update_session(self):
        valid = CONF_SID not in self.entry

        if CONF_SID in self.entry:
            async with self.client as session:
                async with session.get(
                    url="/auth",
                    json={"sid": self.entry[CONF_SID], "csrf": self.entry[CONF_CSRF]}) as r:
                    data = await r.json()
                valid = data['session']['valid']
        
        if not valid:
            async with self.client as session:
                async with session.post(
                    url="/auth",
                    json={"password": self.entry[CONF_API_KEY]}
                ) as r:
                    if r.status == 200:
                        data = await r.json()
                        self.entry[CONF_SID] = data['session']['sid']
                        self.entry[CONF_CSRF] = data['session']['csrf']
    
    async def toggle(self, blocking: bool = True, timer: int = None):
        await self.verify_or_update_session()
        async with self.client as session:
            async with session.post(
                url="/dns/blocking",
                json={"blocking": blocking, "timer": timer}
            ) as r:
                if r.status == 200:
                    return blocking
                raise Exception(await r.text)
