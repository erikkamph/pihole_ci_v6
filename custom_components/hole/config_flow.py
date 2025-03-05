import voluptuous as vol
from .const import DOMAIN
from homeassistant.const import CONF_API_KEY, CONF_URL
from homeassistant.config_entries import ConfigFlow


class HoleV6ConfigFlow(ConfigFlow, domain=DOMAIN):
    VERSION = 1
    MINOR_VERSION = 0
    
    # async def async_step_user(self, user_input = None):
    #     errors = {}

    #     if user_input:
    #         return self.async_create_entry(title="Pi-Hole V6", data=user_input)

    #     return self.async_show_form(
    #         step_id="user",
    #         data_schema=vol.Schema(
    #             {
    #                 vol.Required(
    #                     CONF_URL, msg="Pi-Hole API url", description={"suggested_value": "http://pi.hole/api"}
    #                 ): str,
    #                 vol.Required(
    #                     CONF_API_KEY, msg="Pi-Hole API Key/Password"
    #                 ): str
    #             }
    #         ),
    #         errors=errors
    #     )