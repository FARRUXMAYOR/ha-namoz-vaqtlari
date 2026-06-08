from datetime import timedelta
import logging
from typing import Any

import aiohttp

from homeassistant.core import HomeAssistant
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
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(API_URL, params=params, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                    if resp.status != 200:
                        raise UpdateFailed(f"API xatosi: {resp.status}")
                    data = await resp.json()
                    return data["data"]["timings"]
        except aiohttp.ClientError as err:
            raise UpdateFailed(f"Ulanish xatosi: {err}") from err
        except (KeyError, ValueError) as err:
            raise UpdateFailed(f"Ma'lumot xatosi: {err}") from err
