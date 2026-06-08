from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import CALC_METHODS, CONF_CITY, CONF_METHOD, CONF_SOURCE, DOMAIN, SOURCE_ALADHAN
from .coordinator import NamozVaqtlariCoordinator

PLATFORMS = ["sensor"]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    city = entry.data[CONF_CITY]
    method_name = entry.data.get(CONF_METHOD, "Musulmon Olami Ligasi")
    method = CALC_METHODS.get(method_name, 3) if isinstance(method_name, str) else method_name
    source = entry.data.get(CONF_SOURCE, SOURCE_ALADHAN)

    coordinator = NamozVaqtlariCoordinator(hass, city, method, source)
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok
