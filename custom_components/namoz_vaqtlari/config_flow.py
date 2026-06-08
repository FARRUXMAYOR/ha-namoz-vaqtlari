import voluptuous as vol

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult

from .const import (
    CALC_METHODS,
    CITIES_ALADHAN,
    CONF_CITY,
    CONF_METHOD,
    CONF_SOURCE,
    DOMAIN,
    SOURCE_ALADHAN,
    SOURCE_ISLOMAPI,
    SOURCES,
)


class NamozVaqtlariConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    def __init__(self) -> None:
        self._source: str = SOURCE_ALADHAN

    async def async_step_user(self, user_input=None) -> FlowResult:
        if user_input is not None:
            self._source = user_input[CONF_SOURCE]
            if self._source == SOURCE_ISLOMAPI:
                return await self.async_step_islomapi()
            return await self.async_step_aladhan()

        schema = vol.Schema({
            vol.Required(CONF_SOURCE, default=SOURCE_ISLOMAPI): vol.In(SOURCES),
        })
        return self.async_show_form(step_id="user", data_schema=schema)

    async def async_step_aladhan(self, user_input=None) -> FlowResult:
        if user_input is not None:
            city = user_input[CONF_CITY]
            await self.async_set_unique_id(f"{city}_aladhan")
            self._abort_if_unique_id_configured()
            return self.async_create_entry(
                title=f"Namoz Vaqtlari – {city} (Aladhan)",
                data={
                    CONF_CITY: city,
                    CONF_METHOD: user_input[CONF_METHOD],
                    CONF_SOURCE: SOURCE_ALADHAN,
                },
            )
        schema = vol.Schema({
            vol.Required(CONF_CITY, default="Toshkent"): vol.In(list(CITIES_ALADHAN.keys())),
            vol.Required(CONF_METHOD, default="Musulmon Olami Ligasi"): vol.In(list(CALC_METHODS.keys())),
        })
        return self.async_show_form(step_id="aladhan", data_schema=schema)

    async def async_step_islomapi(self, user_input=None) -> FlowResult:
        from .const import CITIES_ISLOMAPI
        if user_input is not None:
            city = user_input[CONF_CITY]
            await self.async_set_unique_id(f"{city}_islomapi")
            self._abort_if_unique_id_configured()
            return self.async_create_entry(
                title=f"Namoz Vaqtlari – {city} (islomapi.uz)",
                data={
                    CONF_CITY: city,
                    CONF_METHOD: 3,
                    CONF_SOURCE: SOURCE_ISLOMAPI,
                },
            )
        schema = vol.Schema({
            vol.Required(CONF_CITY, default="Toshkent"): vol.In(list(CITIES_ISLOMAPI.keys())),
        })
        return self.async_show_form(step_id="islomapi", data_schema=schema)
