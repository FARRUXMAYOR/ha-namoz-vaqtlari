from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import CALC_METHODS, CONF_CITY, CONF_METHOD, DOMAIN
from .coordinator import NamozVaqtlariCoordinator

PLATFORMS = ["sensor"]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    city = entry.data[CONF_CITY]
    method_name = entry.data[CONF_METHOD]
    method = CALC_METHODS.get(method_name, 3)

    coordinator = NamozVaqtlariCoordinator(hass, city, method)
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok
