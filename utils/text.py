"""Luxury Uzbek bridal text templates and formatters for Sarvinoz Collection bot."""

from config import BRAND_NAME, CHANNEL_URL, CHANNEL_USERNAME, ADMIN_USERNAME


def format_price(amount: int) -> str:
    """Format number to currency format (e.g. 850 000 so'm)."""
    return f"{amount:,}".replace(",", " ") + " so'm"


WELCOME_TEXT = f"""👑 <b>«{BRAND_NAME}» zargarlik va aksessuarlar uyiga xush kelibsiz!</b> ✨

Assalomu alaykum, muhtaram va go'zal kelinoyimiz!

Biz har bir kelinning to'y oqshomi betakror va dabdabali o'tishi uchun eng nafis qo'l mehnati namunalarini taqdim etamiz:
✨ <i>Swarovski kristallari va marvaridlar bilan bezatilgan qirollik diademalari;</i>
🕊️ <i>Fransuz tullari va nozik biserlar jilosidagi hashamatli fatalar;</i>
💎 <i>Kelinlik ko'ylagini mukammal to'ldiruvchi yorqin taqinchoqlar to'plamlari;</i>
🌸 <i>Sochlar uchun eksklyuziv taroqcha va shpilkalar.</i>

Har bir buyumimiz sizning orzuingizdagi obrazni yaratish uchun maxsus tayyorlanadi.

📢 <b>Kanalimizga ulaning:</b>
Jonli video-obzorlar, haqiqiy kelinlarimiz fikrlari va yangi kolleksiyalar bilan tanishish uchun <a href="{CHANNEL_URL}">{CHANNEL_USERNAME}</a> guruhimizga a'zo bo'ling!

<i>Quyidagi menyudan o'zingizga ma'qul bo'limni tanlang:</i>"""


DELIVERY_INFO_TEXT = f"""🚚 <b>Yetkazib berish va To'lov shartlari:</b> ✨

«<b>{BRAND_NAME}</b>» har bir buyurtmani kelinlarimizga o'zgacha mehr va hashamatli sovg'a qutisida taqdim etadi.

📍 <b>Toshkent shahri bo'ylab:</b>
• Kuryer orqali to'g'ridan-to'g'ri eshigingizgacha yetkaziladi.
• Yetkazib berish vaqti: 2–4 soat ichida (yoki o'zingizga qulay vaqtda).

📦 <b>O'zbekistonning barcha viloyatlariga:</b>
• <b>BTS Express</b> yoki <b>UzPost</b> xizmati orqali 1-2 ish kunida ishonchli yetkazib beriladi.
• Har bir aksessuar xavfsiz va mustahkam himoya qadoqlariga joylanadi.

💳 <b>To'lov turlari:</b>
• <b>Click / Payme / Uzum Bank</b> orqali onlayn to'lov;
• Naqd pul orqali (faqat Toshkent kuryeri uchun).

👑 <i>Biz kelinlarimizning har bir daqiqasini qadrlaymiz!</i>"""


CONTACT_INFO_TEXT = f"""📞 <b>«{BRAND_NAME}» bilan bog'lanish:</b> ✨

Har qanday savolingiz bo'lsa yoki shaxsiy maslahat olmoqchi bo'lsangiz, biz bilan bog'laning:

👩‍💼 <b>Menejer / Dizayner:</b> {ADMIN_USERNAME}
📢 <b>Rasmiy guruh / kanal:</b> <a href="{CHANNEL_URL}">{CHANNEL_USERNAME}</a>
📱 <b>Aloqa telefoni:</b> +998 (90) 123-45-67
⏰ <b>Ish vaqti:</b> Har kuni 09:00 dan 21:00 gacha

📍 <i>Toshkent shahri, Kelinlar aksessuarlari shourumi.</i>

Biz sizning eng baxtli kuningizda yoningizda bo'lishdan baxtiyormiz! 🌸"""


CUSTOM_ORDER_INFO_TEXT = """✨ <b>Eksklyuziv Individual Buyurtma</b> 👑

Orzuingizdagi diadema yoki fatani aynan siz xohlagandek qilib tayyorlab beramiz!

<b>Sizga qanday qulayliklar yaratiladi:</b>
1. Ko'ylagingiz fasoni, matosi va soch turmagingizga mos dizayn tanlanadi.
2. Swarovski kristallari, daryo marvaridlari yoki zargarlik simlari sizning xohishingizga ko'ra teriladi.
3. Jarayon davomida oraliq suratlar taqdim etiladi.

⏱ <i>Tayyorlanish muddati: 3 kundan 7 kungacha.</i>

Keling, buyurtma parametrlarini birgalikda aniqlashtiramiz! Quyidagi tugmani bosing:"""


DRESS_MATCH_INFO_TEXT = """👰‍♀️ <b>Ko'ylakka mos aksessuarlar tanlash xizmati</b> ✨

Kelinlik ko'ylagingiz rangiga, bezaklariga va fasoniga to'liq uyg'un keluvchi aksessuarlarni topishga yordam beramiz!

Ko'ylagingizning rasmini yoki rangini yuborsangiz, professional stilist-dizaynerimiz sizga eng mos keluvchi diademalar, fatalar va taqinchoqlar kombinatsiyasini tanlab beradi.

Quyidagi bosqichlarni to'ldiring:"""


def format_product_card(product: dict, current_index: int = 1, total_count: int = 1) -> str:
    """Format single product card caption."""
    status_badge = "✅ Sotuvda bor (Darhol yetkaziladi)" if product.get("status") == "available" else "⏳ Buyurtma asosida (3–5 kun)"
    price_str = format_price(product["price"])
    prod_name = product["name"]
    desc = product.get("description") or "Hashamatli kelinlik aksessuari."
    materials = product.get("materials") or "Yuqori sifatli zargarlik qotishmasi"
    dimensions = product.get("dimensions") or "Standart qulay oʻlcham"
    
    caption = f"""{prod_name}
({current_index} / {total_count})

✨ <b>Tavsif:</b> {desc}
🌿 <b>Materiallar:</b> {materials}
📐 <b>O'lchamlari:</b> {dimensions}
💰 <b>Narxi:</b> <b>{price_str}</b>
💎 <b>Holati:</b> {status_badge}

👑 <i>«{BRAND_NAME}» — nafosat va dabdaba uygʻunligi.</i>"""
    return caption


def format_order_summary(data: dict) -> str:
    """Format summary of client order for final user confirmation."""
    order_type_names = {
        "catalog_item": "🛍️ Katalogdagi mahsulot",
        "custom_order": "✨ Individual buyurtma",
        "dress_match": "👰‍♀️ Ko'ylakka mos tanlash",
    }
    order_name = order_type_names.get(data.get("order_type"), "🛍️ Kelinlik buyurtmasi")
    product_name = data.get("product_name") or "Alohida kelishiladi"
    product_price = format_price(data["product_price"]) if data.get("product_price") else "Maslahatlashuvdan so'ng"
    dress_color = data.get("dress_color") or "Belgilanmagan"
    wedding_date = data.get("wedding_date") or "Kiritilmagan"
    customer_name = data.get("customer_name") or "Kiritilmagan"
    phone_number = data.get("phone_number") or "Kiritilmagan"
    delivery_type = data.get("delivery_type") or "Kiritilmagan"

    summary = f"""📋 <b>Buyurtmangiz tafsilotlari:</b>

👑 <b>Buyurtma turi:</b> {order_name}
💎 <b>Tanlangan mahsulot:</b> {product_name}
💰 <b>Taxminiy narxi:</b> {product_price}

🎨 <b>Ko'ylak rangi / uslubi:</b> {dress_color}
📅 <b>To'y / Tadbir sanasi:</b> {wedding_date}
👤 <b>Kelin / Buyurtmachi:</b> {customer_name}
📱 <b>Telefon raqam:</b> {phone_number}
🚚 <b>Yetkazib berish:</b> {delivery_type}

<i>Ma'lumotlar to'g'riligini tasdiqlaysizmi?</i>"""
    return summary


def format_admin_order_notification(order_id: int, data: dict, user_info: dict) -> str:
    """Format notification message sent directly to admin."""
    order_type_names = {
        "catalog_item": "🛍️ Katalogdagi mahsulot buyurtmasi",
        "custom_order": "✨ Individual eksklyuziv buyurtma",
        "dress_match": "👰‍♀️ Ko'ylakka mos tanlash so'rovi",
    }
    order_type_text = order_type_names.get(data.get("order_type"), "Yangi buyurtma")
    username_str = f"@{user_info.get('username')}" if user_info.get("username") else "Mavjud emas"
    user_id = user_info.get("user_id")
    prod_name = data.get("product_name") or "Mavjud emas (Individual)"
    prod_price = format_price(data["product_price"]) if data.get("product_price") else "Alohida hisoblanadi"
    dress_color = data.get("dress_color") or "Suratda koʻrsatilgan"
    wedding_date = data.get("wedding_date") or "Kiritilmagan"
    customer_name = data.get("customer_name") or "Kiritilmagan"
    phone_number = data.get("phone_number") or "Kiritilmagan"
    delivery_type = data.get("delivery_type") or "Kiritilmagan"

    text = f"""🔔 <b>YANGI KELINLIK BUYURTMASI #{order_id}</b> 👑

📌 <b>Turi:</b> {order_type_text}
💎 <b>Mahsulot:</b> {prod_name}
💰 <b>Narxi:</b> {prod_price}

🎨 <b>Ko'ylak rangi / fasoni:</b> {dress_color}
📅 <b>To'y sanasi:</b> <code>{wedding_date}</code>
👤 <b>Mijoz:</b> {customer_name}
📱 <b>Telefon:</b> <code>{phone_number}</code>
🚚 <b>Yetkazib berish:</b> {delivery_type}

👤 <b>Telegram profili:</b> {username_str} (ID: <code>{user_id}</code>)
🔗 <b>Mijoz havolasi:</b> <a href="tg://user?id={user_id}">Profilga o'tish</a>"""
    return text
