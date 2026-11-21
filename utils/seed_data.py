"""Initial catalog seed data for Sarvinoz Collection luxury bridal accessories."""

CATEGORIES_DATA = [
    {
        "code": "diademalar",
        "name": "Diademalar (Tiaras & Crowns)",
        "emoji": "👑",
        "display_order": 1,
    },
    {
        "code": "fatalar",
        "name": "Fatalar (Wedding Veils)",
        "emoji": "🕊️",
        "display_order": 2,
    },
    {
        "code": "taqinchoqlar",
        "name": "Kelinlar taqinchoqlari (Necklace & Earring Sets)",
        "emoji": "💎",
        "display_order": 3,
    },
    {
        "code": "soch_aksessuarlari",
        "name": "Soch aksessuarlari (Hairpins & Combs)",
        "emoji": "🌸",
        "display_order": 4,
    },
]

INITIAL_PRODUCTS = [
    # 1. Diademalar
    {
        "category_code": "diademalar",
        "name": "👑 \"Zuhro\" Swarovski Brilliant Diadema",
        "description": "Eng yuqori toifadagi kelinlar uchun jozibador va hashamatli qirollik diademasi. Yorug'likda kamalakdek jilolanadi.",
        "materials": "Asl Swarovski kristallari, zargarlik kumush qoplamasi, yapon mayda biserlari",
        "dimensions": "Balandligi: 6.8 sm | Aylanasi: 33 sm",
        "price": 850000,
        "photo": "https://images.unsplash.com/photo-1546804784-896d0dca3805?auto=format&fit=crop&w=800&q=80",
        "status": "available",  # Sotuvda bor
    },
    {
        "category_code": "diademalar",
        "name": "👑 \"Malika Nur\" Qirrali Kelinlik Toji",
        "description": "Klassik qirollik uslubidagi hashamatli toj. Har bir tosh qo'lda mayda simkashlik uslubida mahkamlangan.",
        "materials": "Tabiiy daryo marvaridlari, sirkon kristallari, 18K oq oltin qoplamali qotishma",
        "dimensions": "Balandligi: 8.5 sm | Aylanasi: 35 sm",
        "price": 1250000,
        "photo": "https://images.unsplash.com/photo-1535632066927-ab7c9ab60908?auto=format&fit=crop&w=800&q=80",
        "status": "custom_order",  # Buyurtma asosida
    },
    # 2. Fatalar
    {
        "category_code": "fatalar",
        "name": "🕊️ \"Ispaniya Nafosati\" 3 Metrlik Shleyf Fata",
        "description": "Yurganingizda orqangizdan nafis to'lqinlanib turuvchi hashamatli shleyfli kelinlik fatasi. Qirralari nozik biser va gipur bilan hoshiyalangan.",
        "materials": "Fransuz ipakdek mayin tullari (French soft tulle), qo'l mehnati biser kashtasi",
        "dimensions": "Uzunligi: 300 sm | Kengligi: 180 sm",
        "price": 950000,
        "photo": "https://images.unsplash.com/photo-1519741497674-611481863552?auto=format&fit=crop&w=800&q=80",
        "status": "available",
    },
    {
        "category_code": "fatalar",
        "name": "🕊️ \"Romantika\" 2 Qavatli Marvaridli Fata",
        "description": "Yuzni yopish uchun maxsus qulay qatlamga ega, marvarid tomchilari bilan bezatilgan nafis fata.",
        "materials": "Yevropa tullari, mayda marvaridlar, qulay metall taroqcha asos",
        "dimensions": "Yuqori qatlam: 75 sm | Asosiy qatlam: 120 sm",
        "price": 480000,
        "photo": "https://images.unsplash.com/photo-1583939003579-730e3918a45a?auto=format&fit=crop&w=800&q=80",
        "status": "available",
    },
    # 3. Kelinlar taqinchoqlari
    {
        "category_code": "taqinchoqlari" if False else "taqinchoqlar",
        "name": "💎 \"Sensatsiya\" Zirak va Marjon To'plami",
        "description": "Kelinlik ko'ylagining bo'yin va yelka qismini nafis ochib beruvchi ko'rkam to'plam. Teri uchun 100% xavfsiz va gipoallergen.",
        "materials": "Sirkon brilliantlari (AAA grade), marvarid qirqimlari, rodiy qoplama",
        "dimensions": "Marjon uzunligi: 42+5 sm sozlanuvchi | Zirak uzunligi: 4.5 sm",
        "price": 680000,
        "photo": "https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?auto=format&fit=crop&w=800&q=80",
        "status": "available",
    },
    {
        "category_code": "taqinchoqlar",
        "name": "💎 \"Elita Shukuhi\" Hashamatli Kelinlik Garnituri",
        "description": "Eng tantanali to'y kechalari uchun yaratilgan, ko'zni qamashtiruvchi yirik kristalli to'plam.",
        "materials": "Swarovski elementlari, kubik sirkoniylar, yaltiroq platina effekti",
        "dimensions": "Bo'yinbog' kengligi: 3 sm | Ziraklar: 5.2 sm",
        "price": 890000,
        "photo": "https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?auto=format&fit=crop&w=800&q=80",
        "status": "custom_order",
    },
    # 4. Soch aksessuarlari
    {
        "category_code": "soch_aksessuarlari",
        "name": "🌸 \"Bahor Nafasi\" Qo'l Mehnati Soch Taroqchasi",
        "description": "Kelinlar turmagini mukammal ushlab turuvchi, shoxcha ko'rinishidagi g'aroyib nafis aksessuar.",
        "materials": "Billur toshlar, mayda yapon biserlari, egiluvchan zargarlik simi",
        "dimensions": "O'lchami: 14 sm x 7.5 sm",
        "price": 320000,
        "photo": "https://images.unsplash.com/photo-1596944924616-7b38e7cfac36?auto=format&fit=crop&w=800&q=80",
        "status": "available",
    },
    {
        "category_code": "soch_aksessuarlari",
        "name": "🌸 \"Kristall Yulduzlar\" Soch To'g'nog'ichlari (5 dona)",
        "description": "Kelin turmagining istalgan qismiga qo'shimcha jilo berish uchun mo'ljallangan yengil shpilkalar to'plami.",
        "materials": "Swarovski kristallari, kumush simkashlik",
        "dimensions": "Har bir donasi: 4.5 sm",
        "price": 220000,
        "photo": "https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?auto=format&fit=crop&w=800&q=80",
        "status": "available",
    },
]
