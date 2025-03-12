from pydantic import BaseModel, Field, ConfigDict, model_validator
from .const import (
    CONF_SID,
    CONF_CSRF,
    CONF_SCHEMA
)
from validators import url
from typing import Any, Optional
from homeassistant.const import (
    CONF_HOST,
    CONF_LOCATION,
    CONF_PORT,
    CONF_VERIFY_SSL,
    CONF_NAME,
    CONF_API_KEY
)


class PiHoleConfig(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True
    )

    host: str = Field(default="pi.hole", alias=CONF_HOST)
    scheme: str = Field(default="https", alias=CONF_SCHEMA)
    port: int = Field(default=443, alias=CONF_PORT)
    verify: bool = Field(default=True, alias=CONF_VERIFY_SSL)
    api_key: str = Field(default="", alias=CONF_API_KEY)
    name: str = Field(default="Pi-Hole", alias=CONF_NAME)
    location: str = Field(default="api", alias=CONF_LOCATION)
    sid: Optional[str] = Field(default="", alias=CONF_SID)
    csrf: Optional[str] = Field(default="", alias=CONF_CSRF)

    @property
    def api_url(self):
        return f"{self.scheme}://{self.host}:{self.port}/{self.location}/"
    
    @property
    def auth_data(self):
        return {"password": self.api_key}

    @model_validator(mode='before')
    @classmethod
    def validate(cls, data: Any):
        if isinstance(data, dict):
            if CONF_SCHEMA not in data:
                raise ValueError('Missing schema!')
            
            if CONF_HOST not in data:
                raise ValueError('Hostname, url or IP needs to be supplied!')
            
            if CONF_PORT not in data:
                raise ValueError('Port needs to be supplied, even if https or http!')

            if CONF_LOCATION not in data:
                raise ValueError('Location needs to be supplied!')
            
            if CONF_API_KEY not in data:
                raise ValueError('You need to supply an api key or a password to access pihole data!')
            
            hole_url = f"{data[CONF_SCHEMA]}://{data[CONF_HOST]}:{data[CONF_PORT]}/{data[CONF_LOCATION]}"
            
            if not url(hole_url):
                raise ValueError('The supplied parameters schema, host, port and location needs to make up a valid url')
        return data