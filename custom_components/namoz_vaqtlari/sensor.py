from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    CONF_CITY,
    CONF_SOURCE,
    DOMAIN,
    PRAYER_NAMES_ALADHAN,
    PRAYER_NAMES_ISLOMAPI,
    SOURCE_ISLOMAPI,
)
from .coordinator import NamozVaqtlariCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator: NamozVaqtlariCoordinator = hass.data[DOMAIN][entry.entry_id]
    city = entry.data[CONF_CITY]
    source = entry.data.get(CONF_SOURCE, "")

    if source == SOURCE_ISLOMAPI:
        prayer_map = PRAYER_NAMES_ISLOMAPI
    else:
        prayer_map = PRAYER_NAMES_ALADHAN

    async_add_entities([
        NamozSensor(coordinator, prayer_key, prayer_name, city, source)
        for prayer_key, prayer_name in prayer_map.items()
    ])


class NamozSensor(CoordinatorEntity, SensorEntity):
    def __init__(
        self,
        coordinator: NamozVaqtlariCoordinator,
        prayer_key: str,
        prayer_name: str,
        city: str,
        source: str,
    ) -> None:
        super().__init__(coordinator)
        self._prayer_key = prayer_key
        self._prayer_name = prayer_name
        self._city = city
        self._source = source
        uid = f"{DOMAIN}_{city}_{prayer_key}".lower().replace(" ", "_").replace("'", "").replace("/", "_")
        self._attr_unique_id = uid
        self._attr_name = f"{prayer_name} ({city})"
        self._attr_icon = "mdi:clock-outline"

    @property
    def native_value(self) -> str | None:
        if self.coordinator.data:
            return self.coordinator.data.get(self._prayer_key)
        return None

    @property
    def extra_state_attributes(self) -> dict:
        return {
            "shahar": self._city,
            "namoz": self._prayer_name,
            "manba": self._source,
        }
