# Namoz Vaqtlari — Home Assistant Integration

O'zbekiston shaharlari uchun namoz vaqtlarini Home Assistant ga integratsiya qilish.

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)

## Xususiyatlari

- O'zbekistonning 12 ta shahri uchun namoz vaqtlari
- 4 xil hisoblash usuli
- Har kuni avtomatik yangilanish
- Avtomatizatsiya uchun sensor entities
- O'zbek va ingliz tili

## Sensorlar

Har shahar uchun 6 ta sensor yaratiladi:

| Sensor | Namoz |
|--------|-------|
| `sensor.bomdod_toshkent` | Bomdod (Fajr) |
| `sensor.quyosh_chiqishi_toshkent` | Quyosh chiqishi |
| `sensor.peshin_toshkent` | Peshin (Zuhr) |
| `sensor.asr_toshkent` | Asr |
| `sensor.shom_toshkent` | Shom (Maghrib) |
| `sensor.xufton_toshkent` | Xufton (Isha) |

## O'rnatish (HACS orqali)

1. HACS → Integrations → `+` → **Custom repositories**
2. URL: `https://github.com/YOUR_USERNAME/ha-namoz-vaqtlari`
3. Category: **Integration**
4. **Download** bosing
5. Home Assistant ni restart qiling
6. Settings → Integrations → **Add Integration** → **Namoz Vaqtlari**
7. Shahar va hisoblash usulini tanlang

## Qo'lda o'rnatish

`custom_components/namoz_vaqtlari` papkasini Home Assistant `config` papkasiga ko'chiring va restart qiling.

## API

Ma'lumotlar [Aladhan.com](https://aladhan.com) ochiq API dan olinadi.

## Litsenziya

MIT
