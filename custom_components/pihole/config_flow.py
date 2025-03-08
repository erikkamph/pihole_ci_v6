from homeassistant.config_entries import ConfigFlow
from .models.config import PiHoleConfig
from pydantic import ValidationError
import voluptuous as vol
import logging
from homeassistant.const import (
    CONF_HOST,
    CONF_LOCATION,
    CONF_PORT,
    CONF_VERIFY_SSL,
    CONF_NAME,
    CONF_API_KEY,
)
from .models.const import (
    DEFAULT_LOCATION,
    DEFAULT_API_KEY,
    DEFAULT_HOST,
    DEFAULT_NAME,
    DEFAULT_PORT,
    DEFAULT_VERIFY_SSL,
    CONF_SCHEMA,
    DOMAIN
)

_LOGGER = logging.getLogger(__name__)


class HoleV6ConfigFlow(ConfigFlow, domain=DOMAIN):
    VERSION = 1
    MINOR_VERSION = 0

    def __init__(self):
        self._config: dict = {}
    
    async def async_step_user(self, user_input = None):
        errors = {}

        if user_input:
            self._config = {
                CONF_NAME: user_input[CONF_NAME]
            }

            return await self.async_step_host()

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        CONF_NAME, default=self._config.get(CONF_NAME, DEFAULT_NAME), description="Name of pihole instance"
                    ): str
                }
            ),
            errors=errors
        )
    
    async def async_step_host(self, user_input = None):
        errors = {}

        if user_input:
            self._config[CONF_HOST] = user_input[CONF_HOST]
            self._config[CONF_PORT] = user_input[CONF_PORT]
            self._config[CONF_VERIFY_SSL] = user_input[CONF_VERIFY_SSL]
            self._config[CONF_LOCATION] = user_input[CONF_LOCATION]
            self._config[CONF_SCHEMA] = user_input[CONF_SCHEMA]

            return await self.async_step_api()

        return self.async_show_form(
            step_id="host",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_HOST, default=self._config.get(CONF_HOST, DEFAULT_HOST), description="Location of the pi.hole instance"
                    ): str,
                    vol.Required(
                        CONF_SCHEMA, default=self._config.get(CONF_SCHEMA, "http"), description="http or https schema"
                    ): str,
                    vol.Required(
                        CONF_LOCATION, default=self._config.get(CONF_LOCATION, DEFAULT_LOCATION)
                    ): str,
                    vol.Required(
                        CONF_PORT, default=self._config.get(CONF_PORT, DEFAULT_PORT)
                    ): int,
                    vol.Required(
                        CONF_VERIFY_SSL, default=self._config.get(CONF_VERIFY_SSL, DEFAULT_VERIFY_SSL)
                    ): bool
                }
            ),
            errors=errors
        )
    
    async def async_step_api(self, user_input = None):
        errors = {}

        if user_input:
            self._config[CONF_API_KEY] = user_input[CONF_API_KEY]

            try:
                validated = PiHoleConfig.model_validate(self._config)
                
                if validated:
                    return self.async_create_entry(
                        title=validated.name,
                        data=self._config
                    )
            except ValidationError as ex:
                _LOGGER.exception(ex, stack_info=True)
        
        return self.async_show_form(
            step_id='api',
            errors=errors,
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_API_KEY, default=self._config.get(CONF_API_KEY, DEFAULT_API_KEY), description="Api key or password for the pi.hole instance"
                    ): str
                }
            )
        )