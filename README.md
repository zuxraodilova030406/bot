# 👑 Sarvinoz Collection — Luxury Bridal Telegram Bot

> **«Sarvinoz Collection»** — to'y diademalari (tiaras & crowns), kelinlik fatalari (wedding veils), marvarid va sirkon taqinchoqlar to'plamlari hamda soch bezaklari bo'yicha yetakchi zargarlik va aksessuarlar brendi uchun maxsus yaratilgan professional Telegram bot.

Rasmiy Telegram hamjamiyati: [https://t.me/Sarvinozcollection1](https://t.me/Sarvinozcollection1) (`@Sarvinozcollection1`)

---

## ✨ Asosiy Imkoniyatlar va Funksiyalar

1. **👑 Kelinlik Katalogi (Bridal Catalog):**
   - 👑 **Diademalar (Tiaras & Crowns)** — Swarovski kristallari va qirollik tojlari.
   - 🕊️ **Fatalar (Wedding Veils)** — 3 metrlik fransuz tullari, biserli shleyflar va 2 qavatli klassik fatalar.
   - 💎 **Kelinlar taqinchoqlari (Jewelry Sets)** — Sirkonli marjon va ziraklar.
   - 🌸 **Soch aksessuarlari (Hairpins & Combs)** — Qo'lda ishlangan taroqcha va shpilkalar.
   - Har bir mahsulot uchun: Sifatli surat, nom, materiallar, o'lchamlar, narx (UZS) va mavjudlik holati (`✅ Sotuvda bor` / `⏳ Buyurtma asosida`).
   - Qulay navigatsiya: `[⬅️ Oldingisi] [1 / 3] [Keyingisi ➡️]` va `[🛍️ Buyurtma berish]`.

2. **🛍️ Bosqichma-bosqich Buyurtma va FSM Maslahat Tizimi:**
   - Katalogdagi har qanday mahsulot ostidagi `"🛍️ Buyurtma berish"` tugmasi orqali;
   - `"✨ Individual buyurtma"` — kelinning xohishiga ko'ra eksklyuziv model tayyorlash;
   - `"👰‍♀️ Ko'ylakka mos tanlash"` — kelinlik ko'ylagi yoki turmaki suratini yuborib, unga mos aksessuarlar tanlash;
   - **5 bosqichli tartib:**
     - 1-bosqich: Ko'ylak rangi (`Oq` / `Ayvori - Ivory` / `Shampan`) yoki ko'ylak/turmak fotosurati 📸;
     - 2-bosqich: To'y / marosim sanasi (ustuvor rejalashtirish uchun) 📅;
     - 3-bosqich: Kelinoyimiz / mijozning ismi 👤;
     - 4-bosqich: Telefon raqami (`📱 Raqamni yuborish` tugmasi yoki matn shaklida) 📱;
     - 5-bosqich: Yetkazib berish usuli (`Toshkent (Kuryer)` / `Viloyatlarga pochta BTS/UzPost`) 🚚;
   - Mijozga tasdiqlash cheki taqdim etiladi va barcha ma'lumotlar (surat, rang, to'y sanasi, telefon, Telegram profili havolasi bilan) zudlik bilan `ADMIN_ID` ga yuboriladi.

3. **🛠️ Admin Panel (`/admin` yoki `🛠️ Admin Panel` tugmasi):**
   - Faqat `.env` da ko'rsatilgan admin(lar) uchun ochiq;
   - **➕ Yangi mahsulot qo'shish:** Kategoriya tanlash -> Nom kiritish -> Materiallar & O'lchamlar -> Narx -> Foto yuklash -> Holat tanlash;
   - **📋 Mahsulotlarni boshqarish:** Narxni o'zgartirish, sotuv holatini almashtirish yoki o'chirish;
   - **📊 Statistika:** Faol mahsulotlar, jami foydalanuvchilar va buyurtmalar soni;
   - **📦 So'nggi buyurtmalar:** Oxirgi buyurtmalar tarixi va uning holatini boshqarish (`✅ Bog'landim` / `❌ Bekor qilindi`);
   - **📢 Xabar tarqatish (Broadcast):** Barcha bot a'zolariga yangilik yoki chegirmalar haqida xabar jo'natish.

4. **⚡ Asinxron Ma'lumotlar Bazasi (aiosqlite):**
   - Hech qanday tashqi og'ir server talab qilmaydi, `aiosqlite` bilan to'liq asinxron va tezkor ishlaydi;
   - Dastlabki ishga tushirishdayoq tayyor namuna mahsulotlar bilan avtomatik to'ldiriladi (Auto-seeding).

---

## 📁 Loyiha Tuzilishi

```
C:\Users\Пользователь\Desktop\bot\
├── bot.py                     # Asosiy ishga tushiruvchi fayl (Main entrypoint)
├── config.py                  # Sozlamalar va muhit o'zgaruvchilari (.env)
├── database/
│   ├── __init__.py
│   └── db.py                  # aiosqlite orqali CRUD va jadvallar boshqaruvi
├── handlers/
│   ├── __init__.py
│   ├── user.py                # Asosiy menyu, katalog va axborot bo'limlari
│   ├── order.py               # FSM buyurtma va maslahat olish jarayoni
│   └── admin.py               # Admin panel, mahsulot qo'shish/tahrirlash, statistika
├── keyboards/
│   ├── __init__.py
│   ├── default.py             # Asosiy ReplyKeyboardMarkup tugmalari
│   └── inline.py              # InlineKeyboardMarkup (katalog, navigatsiya, admin)
├── states/
│   ├── __init__.py
│   ├── order.py               # Buyurtma holatlari (FSM)
│   └── admin.py               # Admin boshqaruv holatlari (FSM)
├── utils/
│   ├── __init__.py
│   ├── text.py                # Kelinlar uchun nafis o'zbek tilidagi matnlar
│   └── seed_data.py           # Dastlabki namunaviy hashamatli mahsulotlar
├── .env                       # Shaxsiy sozlamalar (Token, Admin ID)
├── .env.example               # Namuna sozlamalar fayli
├── .gitignore                 # Git e'tiborsiz qoldiradigan fayllar
├── requirements.txt           # Kutubxonalar ro'yxati
└── README.md                  # Qo'llanma
```

---

## 🚀 Ishga Tushirish Bo'yicha Qo'llanma

### 1-qadam: Kutubxonalarni o'rnatish
Terminal (yoki PowerShell) oching va buyruqni bering:
```bash
cd "C:\Users\Пользователь\Desktop\bot"
pip install -r requirements.txt
```

### 2-qadam: `.env` faylini sozlash
`.env` faylini matn muharririda oching va o'z ma'lumotlaringizni kiriting:

```env
# Telegram @BotFather dan olingan bot token
BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz

# Sizning Telegram ID raqamingiz (@userinfobot orqali bilib olishingiz mumkin)
ADMIN_ID=123456789

# Brend nomi va ijtimoiy tarmoqlar
BRAND_NAME="Sarvinoz Collection"
CHANNEL_URL="https://t.me/Sarvinozcollection1"
CHANNEL_USERNAME="@Sarvinozcollection1"
ADMIN_USERNAME="@Sarvinoz_admin"

# Ma'lumotlar bazasi nomi
DB_NAME="sarvinoz_collection.db"
```

> **Eslatma:** Bir nechta admin bo'lsa, `ADMIN_ID` ga vergul bilan yozish mumkin: `ADMIN_ID=123456789,987654321`

### 3-qadam: Botni ishga tushirish
```bash
python bot.py
```

Bot ishga tushishi bilan:
- SQLite bazasi (`sarvinoz_collection.db`) avtomatik yaratiladi;
- Barcha toifalar va namuna diademalar, fatalar, taqinchoqlar yuklanadi;
- Telegramda botingizga `/start` buyrug'ini yuboring.

---

## 👑 Foydali Maslahatlar

- **Admin panelga kirish:** Telegram profilingiz ID si `.env` dagi `ADMIN_ID` ga mos kelishi kerak. Botda `/admin` buyrug'ini yuboring yoki menyudagi `🛠️ Admin Panel` tugmasini bosing.
- **Mahsulot qo'shishda fotosurat:** Telegram orqali sifatli fotosurat yuborsangiz, bot uning `file_id` sini avtomatik saqlab oladi.
- **Kanal integratsiyasi:** Bot ichidagi barcha havolalar rasmiy `https://t.me/Sarvinozcollection1` kanaliga yo'naltirilgan bo'lib, kelinlarni real obzorlar va otzivlarni ko'rishga undaydi.

---

## 🕒 24/7 Doimiy Ishlash Rejimini Yoqish

Botni 24 soat to'xtovsiz ishlashini ta'minlash uchun 2 xil usul tayyorlandi:

### 1-usul: O'z kompyuteringizda 24/7 orqa fonda ishlatish (Windows)
1. [`install_autostart.bat`](file:///C:/Users/Пользователь/Desktop/bot/install_autostart.bat) faylini ikki marta bosing.
   - Bu botni Windows avto-yuklanishiga (Startup) qo'shadi. Kompyuter yoqilishi bilan bot orqa fonda (hech qanday qora oyna chiqmasdan) avtomatik ishga tushadi.
2. Agar botni qo'lda fon rejimida yoqmoqchi bo'lsangiz: [`start_silent.vbs`](file:///C:/Users/Пользователь/Desktop/bot/start_silent.vbs) ni bosing.
3. Agar botni to'xtatmoqchi bo'lsangiz: [`stop_bot.bat`](file:///C:/Users/Пользователь/Desktop/bot/stop_bot.bat) ni bosing.
4. Auto-restart xususiyati ([`run_forever.bat`](file:///C:/Users/Пользователь/Desktop/bot/run_forever.bat)): Agar internet uzilsa yoki xatolik bo'lsa, bot avtomatik 5 soniyada qayta yoqiladi.

### 2-usul: Bulutli serverda (VPS / Linux) 24/7 ishlatish (Kompyuter o'chiq bo'lsa ham)
Kompyuteringizni o'chirganingizda ham bot to'xtamasligi uchun uni arzon Linux VPS serverga yuklash tavsiya etiladi:

**Variant A: Systemd servisi orqali (Tavsiya etiladi)**
1. Fayllarni serverga yuklang: `/root/bot/`
2. [`sarvinoz_bot.service`](file:///C:/Users/Пользователь/Desktop/bot/sarvinoz_bot.service) faylini `/etc/systemd/system/` ga ko'chiring:
   ```bash
   cp sarvinoz_bot.service /etc/systemd/system/
   systemctl daemon-reload
   systemctl enable --now sarvinoz_bot
   ```
3. Bot 24/7 uzluksiz ishlaydi va server qayta yoqilganda ham o'zi avtomatik ko'tariladi.

**Variant B: Docker orqali**
```bash
docker compose up -d --build
```
