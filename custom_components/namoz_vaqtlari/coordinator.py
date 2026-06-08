from datetime import date, timedelta
import logging
from typing import Any

import aiohttp

from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import API_URL, CITIES, DOMAIN, UPDATE_INTERVAL_HOURS

_LOGGER = logging.getLogger(__name__)


class NamozVaqtlariCoordinator(DataUpdateCoordinator):
    def __init__(self, hass: HomeAssistant, city: str) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(hours=UPDATE_INTERVAL_HOURS),
        )
        self.city = city

    async def _async_update_data(self) -> dict[str, Any]:
        today = date.today()
        city = CITIES.get(self.city, self.city)
        params = {
            "region": city,
            "month": today.month,
        }
        session = async_get_clientsession(self.hass)
        timeout = aiohttp.ClientTimeout(total=15)
        try:
            async with session.get(API_URL, params=params, timeout=timeout) as resp:
                if resp.status != 200:
                    raise UpdateFailed(f"islomapi.uz xatosi: {resp.status}")
                data = await resp.json()

                # Faqat oy va kun bo'yicha qidirish (yil farq qilmasligi uchun)
                today_md = today.strftime("-%m-%d")
                for entry in data:
                    entry_date = entry.get("date", "")[:10]  # YYYY-MM-DD
                    if entry_date.endswith(today_md):
                        _LOGGER.debug("Bugungi namoz vaqtlari: %s", entry["times"])
                        return entry["times"]

                raise UpdateFailed(f"Bugungi ({today.day}-{today.month}) ma'lumot topilmadi")
        except UpdateFailed:
            raise
        except Exception as err:
            _LOGGER.error("islomapi.uz xatosi: %s", err)
            raise UpdateFailed(f"Xato: {err}") from err
