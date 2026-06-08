from datetime import timedelta
import logging
from typing import Any

import aiohttp

from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    API_URL_ALADHAN,
    API_URL_ISLOMAPI,
    CITIES_ALADHAN,
    CITIES_ISLOMAPI,
    DOMAIN,
    SOURCE_ISLOMAPI,
    UPDATE_INTERVAL_HOURS,
)

_LOGGER = logging.getLogger(__name__)


class NamozVaqtlariCoordinator(DataUpdateCoordinator):
    def __init__(self, hass: HomeAssistant, city: str, method: int, source: str) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(hours=UPDATE_INTERVAL_HOURS),
        )
        self.city = city
        self.method = method
        self.source = source

    async def _async_update_data(self) -> dict[str, Any]:
        if self.source == SOURCE_ISLOMAPI:
            return await self._fetch_islomapi()
        return await self._fetch_aladhan()

    async def _fetch_aladhan(self) -> dict[str, Any]:
        city_en = CITIES_ALADHAN.get(self.city, self.city)
        params = {
            "city": city_en,
            "country": "UZ",
            "method": self.method,
        }
        session = async_get_clientsession(self.hass)
        timeout = aiohttp.ClientTimeout(total=15)
        try:
            async with session.get(API_URL_ALADHAN, params=params, timeout=timeout) as resp:
                if resp.status != 200:
                    raise UpdateFailed(f"Aladhan API xatosi: {resp.status}")
                data = await resp.json()
                _LOGGER.debug("Aladhan API javob: %s", data)
                return data["data"]["timings"]
        except UpdateFailed:
            raise
        except Exception as err:
            _LOGGER.error("Aladhan xatosi: %s", err)
            raise UpdateFailed(f"Aladhan xatosi: {err}") from err

    async def _fetch_islomapi(self) -> dict[str, Any]:
        from datetime import date
        today = date.today()
        city = CITIES_ISLOMAPI.get(self.city, self.city)
        params = {
            "region": city,
            "month": today.month,
        }
        session = async_get_clientsession(self.hass)
        timeout = aiohttp.ClientTimeout(total=15)
        try:
            async with session.get(API_URL_ISLOMAPI, params=params, timeout=timeout) as resp:
                if resp.status != 200:
                    raise UpdateFailed(f"islomapi.uz xatosi: {resp.status}")
                data = await resp.json()
                _LOGGER.debug("islomapi.uz javob (oylik): %d ta yozuv", len(data))

                # Bugungi kunni topamiz
                today_str = today.strftime("%Y-%m-%d")
                for entry in data:
                    entry_date = entry.get("date", "")[:10]
                    if entry_date == today_str:
                        _LOGGER.debug("Bugungi vaqtlar: %s", entry["times"])
                        return entry["times"]

                raise UpdateFailed(f"islomapi.uz: bugungi ({today_str}) ma'lumot topilmadi")
        except UpdateFailed:
            raise
        except Exception as err:
            _LOGGER.error("islomapi.uz xatosi: %s", err)
            raise UpdateFailed(f"islomapi.uz xatosi: {err}") from err
