from datetime import timedelta
import logging
from typing import Any

import aiohttp

from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import API_URL, CITIES, DOMAIN, UPDATE_INTERVAL_HOURS

_LOGGER = logging.getLogger(__name__)


class NamozVaqtlariCoordinator(DataUpdateCoordinator):
    def __init__(self, hass: HomeAssistant, city: str, method: int) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(hours=UPDATE_INTERVAL_HOURS),
        )
        self.city = city
        self.method = method

    async def _async_update_data(self) -> dict[str, Any]:
        city_en = CITIES.get(self.city, self.city)
        params = {
            "city": city_en,
            "country": "UZ",
            "method": self.method,
        }
        session = async_get_clientsession(self.hass)
        timeout = aiohttp.ClientTimeout(total=15)
        try:
            async with session.get(API_URL, params=params, timeout=timeout) as resp:
                if resp.status != 200:
                    raise UpdateFailed(f"API xatosi: {resp.status}")
                data = await resp.json()
                _LOGGER.debug("API javob: %s", data)
                return data["data"]["timings"]
        except UpdateFailed:
            raise
        except Exception as err:
            _LOGGER.error("Namoz vaqtlari xatosi: %s", err)
            raise UpdateFailed(f"Xato: {err}") from err
