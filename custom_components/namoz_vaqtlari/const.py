DOMAIN = "namoz_vaqtlari"

CONF_CITY = "city"
CONF_METHOD = "method"

CITIES = {
    "Toshkent": "Tashkent",
    "Samarqand": "Samarkand",
    "Buxoro": "Bukhara",
    "Namangan": "Namangan",
    "Andijon": "Andijan",
    "Farg'ona": "Fergana",
    "Qarshi": "Karshi",
    "Nukus": "Nukus",
    "Termiz": "Termez",
    "Navoiy": "Navoi",
    "Jizzax": "Jizzakh",
    "Urganch": "Urgench",
}

CALC_METHODS = {
    "Musulmon Olami Ligasi": 3,
    "Misra Oliy Kengashi": 5,
    "Umm al-Qura (Makka)": 4,
    "Karachi Universiteti": 1,
}

PRAYER_NAMES = {
    "Fajr": "Bomdod",
    "Sunrise": "Quyosh chiqishi",
    "Dhuhr": "Peshin",
    "Asr": "Asr",
    "Maghrib": "Shom",
    "Isha": "Xufton",
}

API_URL = "https://api.aladhan.com/v1/timingsByCity"
UPDATE_INTERVAL_HOURS = 24
