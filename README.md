# Namoz Vaqtlari — Home Assistant Integration

<p align="center">
  <img src="icon.png" width="120" alt="Namoz Vaqtlari">
</p>

<p align="center">
  O'zbekiston shaharlari uchun namoz vaqtlarini Home Assistant ga integratsiya qilish.<br/>
  Ma'lumotlar <strong>islomapi.uz</strong> — O'zbekiston Musulmonlar Idorasi rasmiy manbasi orqali olinadi.
</p>

<p align="center">
  <a href="https://github.com/hacs/integration"><img src="https://img.shields.io/badge/HACS-Custom-orange.svg"/></a>
  <img src="https://img.shields.io/badge/version-2.2.0-blue"/>
  <img src="https://img.shields.io/badge/HA-2023.1%2B-green"/>
</p>

---

## Xususiyatlari

- 🕌 O'zbekistonning **12 ta shahri** uchun namoz vaqtlari
- 📡 **islomapi.uz** — O'zbekiston Musulmonlar Idorasi rasmiy manbasi
- ⏰ **8 ta sensor**: Bomdod, Quyosh, Ishroq, Peshin, Asr, Shom, Xufton, Tahajjud
- 🕐 Vaqtlar **"In 2 hours"** ko'rinishida (relative time)
- 🔄 Har kuni avtomatik yangilanish
- 🌐 O'zbek va ingliz tili

## Sensorlar

| Sensor | Tavsif |
|--------|--------|
| `sensor.bomdod` | Tong namozi |
| `sensor.quyosh` | Quyosh chiqishi |
| `sensor.ishroq` | Ishroq (Quyosh + 20 daqiqa) |
| `sensor.peshin` | Peshin namozi |
| `sensor.asr` | Asr namozi |
| `sensor.shom` | Shom / Iftor vaqti |
| `sensor.xufton` | Xufton namozi |
| `sensor.tahajjud` | Tahajjud (Bomdod - 1 soat) |

## O'rnatish (HACS orqali)

1. HACS → Integrations → `⋮` → **Custom repositories**
2. URL: `https://github.com/FARRUXMAYOR/ha-namoz-vaqtlari`
3. Category: **Integration** → **Add**
4. **Download** → Home Assistant restart
5. **Settings → Integrations → Add Integration → Namoz Vaqtlari**
6. Shaharni tanlang

## Qo'lda o'rnatish

`custom_components/namoz_vaqtlari` papkasini Home Assistant `config` papkasiga ko'chiring va restart qiling.

## API

Ma'lumotlar [islomapi.uz](https://islomapi.uz) — O'zbekiston Musulmonlar Idorasi rasmiy API dan olinadi.

## Litsenziya

MIT
