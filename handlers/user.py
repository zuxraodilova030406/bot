import logging
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.filters import CommandStart, Command

from config import CHANNEL_URL, CHANNEL_USERNAME, is_admin
from database import (
    add_user,
    get_categories,
    get_category_by_code,
    get_products_by_category,
)
from keyboards import (
    get_main_keyboard,
    get_welcome_inline_keyboard,
    get_categories_inline_keyboard,
    get_product_navigation_keyboard,
)
from utils.text import (
    WELCOME_TEXT,
    DELIVERY_INFO_TEXT,
    CONTACT_INFO_TEXT,
    format_product_card,
)

logger = logging.getLogger(__name__)
user_router = Router(name="user_router")


@user_router.message(CommandStart())
async def cmd_start(message: Message):
    """Handle /start command: register user and show luxury bridal welcome."""
    user = message.from_user
    if user:
        await add_user(
            user_id=user.id,
            username=user.username,
            full_name=user.full_name or ""
        )

    user_is_admin = is_admin(user.id) if user else False

    # Send welcome text with reply keyboard and inline group invitation
    await message.answer(
        text=WELCOME_TEXT,
        parse_mode="HTML",
        reply_markup=get_main_keyboard(is_admin=user_is_admin),
        disable_web_page_preview=True
    )
    await message.answer(
        text="🌸 <b>«Sarvinoz Collection»</b> — to'y kuningizdagi mukammal go'zallik garovi!",
        parse_mode="HTML",
        reply_markup=get_welcome_inline_keyboard()
    )


@user_router.message(Command("help"))
async def cmd_help(message: Message):
    """Help command showing bot features."""
    help_text = (
        "👑 <b>«Sarvinoz Collection» Bot yordamchisi:</b>\n\n"
        "• <b>👑 Katalog:</b> Barcha kelinlik diademalari, fatalari va taqinchoqlarini ko'rish.\n"
        "• <b>✨ Individual buyurtma:</b> Shaxsiy o'lcham va dizayn asosida buyurtma berish.\n"
        "• <b>👰‍♀️ Ko'ylakka mos tanlash:</b> To'y ko'ylagingizga mos aksessuarlar bo'yicha maslahat.\n"
        "• <b>🚚 Yetkazib berish va To'lov:</b> Yetkazib berish narxlari va shartlari.\n"
        "• <b>📢 Telegram guruhimiz:</b> Jonli videolar va kelinlar fikrlari.\n"
        "• <b>📞 Bog'lanish:</b> Dizayner va menejer bilan to'g'ridan-to'g'ri aloqa.\n\n"
        "<i>Har qanday savol bilan bizga murojaat qilishingiz mumkin!</i>"
    )
    await message.answer(help_text, parse_mode="HTML")


# ==================== Main Menu Reply Button Handlers ====================

@user_router.message(F.text == "👑 Katalog")
async def show_catalog_reply(message: Message):
    """Display categories when user taps Katalog reply button."""
    categories = await get_categories()
    text = (
        "👑 <b>«Sarvinoz Collection» eksklyuziv kelinlik kolleksiyalari:</b>\n\n"
        "O'zingizga kerakli bo'limni tanlang:"
    )
    await message.answer(
        text=text,
        parse_mode="HTML",
        reply_markup=get_categories_inline_keyboard(categories)
    )


@user_router.callback_query(F.data == "open_catalog")
async def show_catalog_callback(callback: CallbackQuery):
    """Display categories when user clicks inline catalog button."""
    categories = await get_categories()
    text = (
        "👑 <b>«Sarvinoz Collection» eksklyuziv kelinlik kolleksiyalari:</b>\n\n"
        "O'zingizga kerakli bo'limni tanlang:"
    )
    await callback.message.answer(
        text=text,
        parse_mode="HTML",
        reply_markup=get_categories_inline_keyboard(categories)
    )
    await callback.answer()


@user_router.message(F.text == "🚚 Yetkazib berish va To'lov")
async def show_delivery_info(message: Message):
    """Display delivery and payment conditions."""
    await message.answer(
        text=DELIVERY_INFO_TEXT,
        parse_mode="HTML"
    )


@user_router.message(F.text == "📢 Telegram guruhimiz")
async def show_channel_info(message: Message):
    """Encourage user to join the official channel/group."""
    text = (
        f"📢 <b>Rasmiy Telegram guruhimizga xush kelibsiz!</b> ✨\n\n"
        f"«<b>Sarvinoz Collection</b>» rasmiy hamjamiyatida siz:\n"
        f"• 👰 Real kelinlarimizning foto va video fikrlari (otzivlar);\n"
        f"• 📹 Aksessuarlarning jonli, filtrsiz video-obzorlari;\n"
        f"• 💎 Har haftalik yangi to'plamlar premyerasi;\n"
        f"• 🎁 Maxsus kelinlik chegirmalaridan birinchilardan bo'lib xabardor bo'lasiz!\n\n"
        f"👉 Havola: <a href=\"{CHANNEL_URL}\">{CHANNEL_USERNAME}</a>\n"
        f"Guruhga qo'shiling va eng so'nggi go'zallik trendlarini kuzatib boring!"
    )
    await message.answer(
        text=text,
        parse_mode="HTML",
        disable_web_page_preview=False
    )


@user_router.message(F.text == "📞 Bog'lanish")
async def show_contact_info(message: Message):
    """Display admin contact information."""
    await message.answer(
        text=CONTACT_INFO_TEXT,
        parse_mode="HTML",
        disable_web_page_preview=True
    )


# ==================== Catalog Browsing Handlers ====================

@user_router.callback_query(F.data.startswith("cat:"))
async def browse_category(callback: CallbackQuery):
    """Browse products within selected category."""
    category_code = callback.data.split(":")[1]
    products = await get_products_by_category(category_code, active_only=True)
    category = await get_category_by_code(category_code)
    cat_name = category["name"] if category else "Kategoriya"

    if not products:
        await callback.answer(
            "Ushbu bo'limda hozircha mahsulotlar yangilanmoqda. Tez orada joylanadi! ✨",
            show_alert=True
        )
        return

    # Show first product in this category
    product = products[0]
    total_count = len(products)
    caption = format_product_card(product, current_index=1, total_count=total_count)
    keyboard = get_product_navigation_keyboard(
        product_id=product["id"],
        current_idx=0,
        total_items=total_count,
        category_code=category_code
    )

    try:
        await callback.message.answer_photo(
            photo=product["photo"],
            caption=caption,
            parse_mode="HTML",
            reply_markup=keyboard
        )
    except Exception as e:
        logger.warning(f"Surat yuborishda xatolik: {e}. Matn shaklida yuborilmoqda.")
        await callback.message.answer(
            text=caption,
            parse_mode="HTML",
            reply_markup=keyboard
        )

    await callback.answer()


@user_router.callback_query(F.data.startswith("pnav:"))
async def navigate_products(callback: CallbackQuery):
    """Handle Next/Previous product navigation within a category."""
    parts = callback.data.split(":")
    category_code = parts[1]
    idx = int(parts[2])

    products = await get_products_by_category(category_code, active_only=True)
    if not products or idx < 0 or idx >= len(products):
        await callback.answer("Mahsulot topilmadi.")
        return

    product = products[idx]
    total_count = len(products)
    caption = format_product_card(product, current_index=idx + 1, total_count=total_count)
    keyboard = get_product_navigation_keyboard(
        product_id=product["id"],
        current_idx=idx,
        total_items=total_count,
        category_code=category_code
    )

    try:
        media = InputMediaPhoto(
            media=product["photo"],
            caption=caption,
            parse_mode="HTML"
        )
        await callback.message.edit_media(
            media=media,
            reply_markup=keyboard
        )
    except Exception as e:
        logger.debug(f"edit_media xatolik berganda answer_photo ishlatiladi: {e}")
        try:
            await callback.message.delete()
        except Exception:
            pass
        await callback.message.answer_photo(
            photo=product["photo"],
            caption=caption,
            parse_mode="HTML",
            reply_markup=keyboard
        )

    await callback.answer()


@user_router.callback_query(F.data == "noop")
async def noop_callback(callback: CallbackQuery):
    """Counter button click does nothing."""
    await callback.answer()
