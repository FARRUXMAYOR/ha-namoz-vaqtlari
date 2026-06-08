import voluptuous as vol

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult

from .const import CALC_METHODS, CITIES, CONF_CITY, CONF_METHOD, DOMAIN


class NamozVaqtlariConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None) -> FlowResult:
        errors = {}

        if user_input is not None:
            await self.async_set_unique_id(user_input[CONF_CITY])
            self._abort_if_unique_id_configured()
            return self.async_create_entry(
                title=f"Namoz Vaqtlari – {user_input[CONF_CITY]}",
                data=user_input,
            )

        schema = vol.Schema({
            vol.Required(CONF_CITY, default="Toshkent"): vol.In(list(CITIES.keys())),
            vol.Required(CONF_METHOD, default="Musulmon Olami Ligasi"): vol.In(list(CALC_METHODS.keys())),
        })

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors,
        )
