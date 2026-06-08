from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import CONF_CITY, DOMAIN, PRAYER_NAMES
from .coordinator import NamozVaqtlariCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator: NamozVaqtlariCoordinator = hass.data[DOMAIN][entry.entry_id]
    city = entry.data[CONF_CITY]

    async_add_entities([
        NamozSensor(coordinator, key, name, city)
        for key, name in PRAYER_NAMES.items()
    ])


class NamozSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator: NamozVaqtlariCoordinator, key: str, name: str, city: str) -> None:
        super().__init__(coordinator)
        self._key = key
        self._city = city
        # Unique ID - shahar nomi bilan (lekin ko'rinishda shahar yo'q)
        uid = f"{DOMAIN}_{city}_{key}".lower().replace(" ", "_").replace("'", "").replace("/", "_")
        self._attr_unique_id = uid
        # Nom — faqat namoz nomi, shahar yo'q
        self._attr_name = name
        self._attr_icon = "mdi:clock-outline"

    @property
    def native_value(self) -> str | None:
        if self.coordinator.data:
            return self.coordinator.data.get(self._key)
        return None

    @property
    def extra_state_attributes(self) -> dict:
        return {
            "shahar": self._city,
            "manba": "islomapi.uz",
        }
