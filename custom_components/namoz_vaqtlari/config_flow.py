import voluptuous as vol

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult

from .const import CITIES, CONF_CITY, DOMAIN


class NamozVaqtlariConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None) -> FlowResult:
        if user_input is not None:
            city = user_input[CONF_CITY]
            await self.async_set_unique_id(city)
            self._abort_if_unique_id_configured()
            return self.async_create_entry(
                title=f"Namoz Vaqtlari – {city}",
                data={CONF_CITY: city},
            )

        schema = vol.Schema({
            vol.Required(CONF_CITY, default="Toshkent"): vol.In(list(CITIES.keys())),
        })
        return self.async_show_form(step_id="user", data_schema=schema)
