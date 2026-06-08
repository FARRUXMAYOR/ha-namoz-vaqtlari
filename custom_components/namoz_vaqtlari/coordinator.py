from datetime import date, datetime, timedelta
import logging
from typing import Any

import aiohttp

from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import API_URL, CITIES, DOMAIN, UPDATE_INTERVAL_HOURS

_LOGGER = logging.getLogger(__name__)


def _add_minutes(time_str: str, minutes: int) -> str:
    """HH:MM formatdagi vaqtga daqiqa qo'shish."""
    try:
        t = datetime.strptime(time_str, "%H:%M")
        t += timedelta(minutes=minutes)
        return t.strftime("%H:%M")
    except Exception:
        return time_str


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

                today_md = today.strftime("-%m-%d")
                for entry in data:
                    if entry.get("date", "")[:10].endswith(today_md):
                        times = entry["times"]
                        # Ishroq = Quyosh + 20 daqiqa
                        times["ishroq"] = _add_minutes(times.get("quyosh", ""), 20)
                        # Tahajjud = Bomdod dan 1 soat oldin
                        times["tahajjud"] = _add_minutes(times.get("tong_saharlik", ""), -60)
                        _LOGGER.debug("Namoz vaqtlari: %s", times)
                        return times

                raise UpdateFailed(f"Bugungi ma'lumot topilmadi")
        except UpdateFailed:
            raise
        except Exception as err:
            _LOGGER.error("islomapi.uz xatosi: %s", err)
            raise UpdateFailed(f"Xato: {err}") from err
