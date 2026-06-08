DOMAIN = "namoz_vaqtlari"

CONF_CITY = "city"
CONF_METHOD = "method"
CONF_SOURCE = "source"

# API manbalar
SOURCE_ALADHAN = "Aladhan.com (Xalqaro)"
SOURCE_ISLOMAPI = "islomapi.uz (O'zbekiston rasmiy)"

SOURCES = [SOURCE_ALADHAN, SOURCE_ISLOMAPI]

# Aladhan uchun shaharlar (uzbek nomi → ingliz nomi)
CITIES_ALADHAN = {
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

# islomapi.uz uchun shaharlar (uzbek nomi → API region nomi)
CITIES_ISLOMAPI = {
    "Toshkent": "Toshkent",
    "Samarqand": "Samarqand",
    "Buxoro": "Buxoro",
    "Namangan": "Namangan",
    "Andijon": "Andijon",
    "Farg'ona": "Farg'ona",
    "Qarshi": "Qarshi",
    "Nukus": "Nukus",
    "Termiz": "Termiz",
    "Navoiy": "Navoiy",
    "Jizzax": "Jizzax",
    "Urganch": "Urganch",
}

CALC_METHODS = {
    "Musulmon Olami Ligasi": 3,
    "Misra Oliy Kengashi": 5,
    "Umm al-Qura (Makka)": 4,
    "Karachi Universiteti": 1,
}

# Aladhan sensor kalitlari
PRAYER_NAMES_ALADHAN = {
    "Fajr":    "Bomdod",
    "Sunrise": "Quyosh chiqishi",
    "Dhuhr":   "Peshin",
    "Asr":     "Asr",
    "Maghrib": "Shom",
    "Isha":    "Xufton",
}

# islomapi.uz sensor kalitlari (saharlik va iftor qo'shimcha)
PRAYER_NAMES_ISLOMAPI = {
    "tong_saharlik": "Saharlik",
    "quyosh":        "Quyosh chiqishi",
    "peshin":        "Peshin",
    "asr":           "Asr",
    "shom_iftor":    "Shom / Iftor",
    "hufton":        "Xufton",
}

API_URL_ALADHAN = "https://api.aladhan.com/v1/timingsByCity"
API_URL_ISLOMAPI = "https://islomapi.uz/api/monthly"
UPDATE_INTERVAL_HOURS = 24
