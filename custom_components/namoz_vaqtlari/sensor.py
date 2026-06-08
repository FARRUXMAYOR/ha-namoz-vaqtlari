from datetime import datetime, timezone
import logging

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util import dt as dt_util

from .const import CONF_CITY, DOMAIN, PRAYER_NAMES
from .coordinator import NamozVaqtlariCoordinator

_LOGGER = logging.getLogger(__name__)


def _time_str_to_datetime(time_str: str) -> datetime | None:
    """HH:MM ni bugungi datetime ga aylantirish (timezone bilan)."""
    try:
        local_tz = dt_util.get_time_zone("Asia/Tashkent")
        today = dt_util.now(local_tz).date()
        hour, minute = map(int, time_str.split(":"))
        dt = datetime(today.year, today.month, today.day, hour, minute, 0, tzinfo=local_tz)
        return dt
    except Exception:
        return None


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
    _attr_device_class = SensorDeviceClass.TIMESTAMP
    _attr_has_entity_name = True

    def __init__(self, coordinator: NamozVaqtlariCoordinator, key: str, name: str, city: str) -> None:
        super().__init__(coordinator)
        self._key = key
        self._city = city
        uid = f"{DOMAIN}_{city}_{key}".lower().replace(" ", "_").replace("'", "").replace("/", "_")
        self._attr_unique_id = uid
        self._attr_name = name
        self._attr_icon = "mdi:clock-outline"

    @property
    def native_value(self) -> datetime | None:
        if self.coordinator.data:
            time_str = self.coordinator.data.get(self._key)
            if time_str:
                return _time_str_to_datetime(time_str)
        return None

    @property
    def extra_state_attributes(self) -> dict:
        if self.coordinator.data:
            return {
                "vaqt": self.coordinator.data.get(self._key, ""),
                "shahar": self._city,
                "manba": "islomapi.uz",
            }
        return {}
