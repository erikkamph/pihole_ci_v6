from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .models.config import PiHoleConfig
from .models.auth import PiHoleAuth
from .models.const import HEADER_CSRF, HEADER_SID
import aiohttp

class PiHole():
    def __init__(self, hass: HomeAssistant, config: ConfigEntry):
        self.entry = config
        self.config = PiHoleConfig(**self.entry.data)
        self.client = aiohttp.ClientSession(base_url=self.config.api_url)
        self.hass = hass
    
    async def verify_or_update_session(self):
        valid = self.config.sid not in self.entry

        if self.config.sid in self.entry:
            async with self.client as session:
                async with session.get(
                    url="/auth",
                    json={"sid": self.config.sid, "csrf": self.config.csrf}) as r:
                    data = await r.json()
                    auth = PiHoleAuth(**data)
                valid = auth.session.valid
        
        if not valid:
            async with self.client as session:
                async with session.post(
                    url="/auth",
                    json=self.config.auth_data
                ) as r:
                    if r.status == 200:
                        data = await r.json()
                        auth = PiHoleAuth(**data)
                        self.config.sid = auth.session.sid
                        self.config.csrf = auth.session.csrf
                        await self.hass.config_entries.async_update_entry(entry=self.entry, data=self.config.model_dump(by_alias=True))
    
    async def toggle(self, blocking: bool = True, timer: int = None):
        await self.verify_or_update_session()
        async with self.client as session:
            async with session.post(
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
