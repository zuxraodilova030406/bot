import logging
from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from config import ADMIN_IDS, is_admin
from database import get_product_by_id, create_order
from states.order import OrderState
from keyboards import (
    get_main_keyboard,
    get_contact_keyboard,
    get_dress_color_keyboard,
    get_delivery_inline_keyboard,
    get_order_confirmation_keyboard,
    get_admin_order_action_keyboard,
)
from utils.text import (
    CUSTOM_ORDER_INFO_TEXT,
    DRESS_MATCH_INFO_TEXT,
    format_order_summary,
    format_admin_order_notification,
)

logger = logging.getLogger(__name__)
order_router = Router(name="order_router")


# ==================== Cancellation Handler ====================

@order_router.message(F.text == "❌ Bekor qilish")
@order_router.callback_query(F.data.in_(["order_cancel", "order_confirm_no"]))
async def cancel_order(event: Message | CallbackQuery, state: FSMContext):
    """Cancel order and return to main menu."""
    await state.clear()
    user_id = event.from_user.id
    user_is_admin = is_admin(user_id)
    text = "🌸 Buyurtma jarayoni bekor qilindi. Bosh menyudasiz."

    if isinstance(event, CallbackQuery):
        try:
            await event.message.delete()
        except Exception:
            pass
        await event.message.answer(
            text=text,
            reply_markup=get_main_keyboard(is_admin=user_is_admin)
        )
        await event.answer()
    else:
        await event.answer(
            text=text,
            reply_markup=get_main_keyboard(is_admin=user_is_admin)
        )


# ==================== Entry Points ====================

@order_router.callback_query(F.data.startswith("order_prod:"))
async def start_catalog_product_order(callback: CallbackQuery, state: FSMContext):
    """Start order flow for a specific catalog product."""
    product_id = int(callback.data.split(":")[1])
    product = await get_product_by_id(product_id)

    if not product:
        await callback.answer("Kechirasiz, ushbu mahsulot topilmadi.", show_alert=True)
        return

    await state.clear()
    await state.update_data(
        order_type="catalog_item",
        product_id=product["id"],
        product_name=product["name"],
        product_price=product["price"],
        dress_photo=None
    )

    prompt = (
        f"🛍️ <b>Tanlangan mahsulot:</b> {product['name']}\n\n"
        "<b>1/5-bosqich:</b> Kelinlik ko'ylagingiz qaysi rangda?\n"
        "Quyidagi variantlardan birini tanlang yoki ko'ylagingiz/turmagingiz suratini yuboring 📸:"
    )
    await callback.message.answer(
        text=prompt,
        parse_mode="HTML",
        reply_markup=get_dress_color_keyboard()
    )
    await state.set_state(OrderState.dress_info)
    await callback.answer()


@order_router.message(F.text == "✨ Individual buyurtma")
async def start_custom_order(message: Message, state: FSMContext):
    """Start custom bridal accessory order."""
    await state.clear()
    await state.update_data(
        order_type="custom_order",
        product_id=None,
        product_name="✨ Individual buyurtma (Maxsus dizayn)",
        product_price=None,
        dress_photo=None
    )

    await message.answer(
        text=CUSTOM_ORDER_INFO_TEXT,
        parse_mode="HTML"
    )

    prompt = (
        "<b>1/5-bosqich:</b> Kelinlik ko'ylagingiz rangi qanday yoki qanday uslubdagi aksessuar xohlaysiz?\n"
        "Quyidagi tugmalardan birini tanlang, o'zingiz yozing yoki namunaviy surat yuboring 📸:"
    )
    await message.answer(
        text=prompt,
        parse_mode="HTML",
        reply_markup=get_dress_color_keyboard()
    )
    await state.set_state(OrderState.dress_info)


@order_router.message(F.text == "👰‍♀️ Ko'ylakka mos tanlash")
async def start_dress_match_consultation(message: Message, state: FSMContext):
    """Start consultation for matching accessories to the bride's wedding dress."""
    await state.clear()
    await state.update_data(
        order_type="dress_match",
        product_id=None,
        product_name="👰‍♀️ Ko'ylakka mos tanlash (Stilist maslahati)",
        product_price=None,
        dress_photo=None
    )

    await message.answer(
        text=DRESS_MATCH_INFO_TEXT,
        parse_mode="HTML"
    )

    prompt = (
        "<b>1/5-bosqich:</b> Kelinlik ko'ylagingiz rangi qanday?\n"
        "Eng ma'quli — ko'ylagingiz suratini yuborsangiz, dizaynerimiz eng mos aksessuarlarni tanlab beradi 📸:"
    )
    await message.answer(
        text=prompt,
        parse_mode="HTML",
        reply_markup=get_dress_color_keyboard()
    )
    await state.set_state(OrderState.dress_info)


# ==================== Step 1: Dress Info / Color / Photo ====================

@order_router.callback_query(OrderState.dress_info, F.data.startswith("dress_c:"))
async def process_dress_color_callback(callback: CallbackQuery, state: FSMContext):
    """Handle dress color selection from inline button."""
    choice = callback.data.split(":")[1]

    if choice == "photo_mode":
        await callback.message.answer(
            "Marhamat, kelinlik ko'ylagingiz yoki rejalashtirayotgan soch turmagingiz suratini yuboring 📸:"
        )
        await callback.answer()
        return

    await state.update_data(dress_color=choice)
    await callback.answer(f"Tanlandi: {choice}")

    # Move to Step 2
    prompt = (
        f"✅ Rang tanlandi: <b>{choice}</b>\n\n"
        "<b>2/5-bosqich:</b> To'y yoki marosim qaysi sanada bo'lib o'tadi? 📅\n"
        "<i>(Masalan: 25.10.2026 yoki 'Kelasi oy o'rtalarida' — bu buyurtmani ustuvor tayyorlash uchun zarur)</i>"
    )
    await callback.message.answer(text=prompt, parse_mode="HTML")
    await state.set_state(OrderState.wedding_date)


@order_router.message(OrderState.dress_info, F.photo)
async def process_dress_photo(message: Message, state: FSMContext):
    """Handle reference photo upload for wedding dress."""
    photo_file_id = message.photo[-1].file_id
    caption = message.caption or "Surat yuborildi"
    await state.update_data(
        dress_photo=photo_file_id,
        dress_color=f"Surat yuklandi: {caption}"
    )

    await message.answer("📸 Rahmat! Ko'ylak surati qabul qilindi.")

    # Move to Step 2
    prompt = (
        "<b>2/5-bosqich:</b> To'y yoki marosim qaysi sanada bo'lib o'tadi? 📅\n"
        "<i>(Masalan: 25.10.2026 yoki 'Kuz oylarida' — buyurtmani ustuvor tayyorlash uchun)</i>"
    )
    await message.answer(text=prompt, parse_mode="HTML")
    await state.set_state(OrderState.wedding_date)


@order_router.message(OrderState.dress_info, F.text)
async def process_dress_text(message: Message, state: FSMContext):
    """Handle manual dress description / color input."""
    await state.update_data(dress_color=message.text.strip())

    prompt = (
        f"✅ Saqlandi: <b>{message.text.strip()}</b>\n\n"
        "<b>2/5-bosqich:</b> To'y yoki marosim qaysi sanada bo'lib o'tadi? 📅\n"
        "<i>(Masalan: 25.10.2026 yoki 'Kelasi hafta' — buyurtmani o'z vaqtida yetkazish uchun)</i>"
    )
    await message.answer(text=prompt, parse_mode="HTML")
    await state.set_state(OrderState.wedding_date)


# ==================== Step 2: Wedding Date ====================

@order_router.message(OrderState.wedding_date, F.text)
async def process_wedding_date(message: Message, state: FSMContext):
    """Handle wedding date input."""
    wedding_date = message.text.strip()
    await state.update_data(wedding_date=wedding_date)

    prompt = (
        f"📅 Sana saqlandi: <b>{wedding_date}</b>\n\n"
        "<b>3/5-bosqich:</b> Ismingizni kiriting 👤\n"
        "<i>(Muhtaram kelinoyimiz yoki buyurtmachi to'liq ismi)</i>:"
    )
    await message.answer(text=prompt, parse_mode="HTML")
    await state.set_state(OrderState.customer_name)


# ==================== Step 3: Customer Name ====================

@order_router.message(OrderState.customer_name, F.text)
async def process_customer_name(message: Message, state: FSMContext):
    """Handle customer name input."""
    name = message.text.strip()
    await state.update_data(customer_name=name)

    prompt = (
        f"🌸 Rahmat, <b>{name}</b>!\n\n"
        "<b>4/5-bosqich:</b> Siz bilan bog'lanishimiz uchun telefon raqamingizni yuboring 📱\n"
        "Quyidagi <b>«📱 Raqamni yuborish»</b> tugmasini bosing yoki raqamingizni yozib yuboring (Masalan: +998901234567):"
    )
    await message.answer(
        text=prompt,
        parse_mode="HTML",
        reply_markup=get_contact_keyboard()
    )
    await state.set_state(OrderState.phone_number)


# ==================== Step 4: Phone Number ====================

@order_router.message(OrderState.phone_number, F.contact)
async def process_phone_contact(message: Message, state: FSMContext):
    """Handle phone number via Telegram contact button."""
    phone = message.contact.phone_number
    if not phone.startswith("+"):
        phone = "+" + phone
    await state.update_data(phone_number=phone)
    await proceed_to_delivery_step(message, state)


@order_router.message(OrderState.phone_number, F.text)
async def process_phone_text(message: Message, state: FSMContext):
    """Handle phone number via manual text input."""
    phone = message.text.strip()

    # Basic check for phone number
    cleaned = phone.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
    if len(cleaned) < 7:
        await message.answer(
            "Iltimos, to'g'ri telefon raqam kiriting (Masalan: +998 90 123 45 67) "
            "yoki «📱 Raqamni yuborish» tugmasini bosing:"
        )
        return

    await state.update_data(phone_number=phone)
    await proceed_to_delivery_step(message, state)


async def proceed_to_delivery_step(message: Message, state: FSMContext):
    """Move to delivery selection step."""
    prompt = (
        "📱 Telefon raqam saqlandi!\n\n"
        "<b>5/5-bosqich:</b> Sizga qaysi yetkazib berish usuli qulay? 🚚\n"
        "Variantlardan birini tanlang:"
    )
    # Remove reply keyboard and send inline delivery choices
    await message.answer(
        text="Yetkazib berish usulini tanlang:",
        reply_markup=ReplyKeyboardRemove()
    )
    await message.answer(
        text=prompt,
        parse_mode="HTML",
        reply_markup=get_delivery_inline_keyboard()
    )
    await state.set_state(OrderState.delivery_type)


# ==================== Step 5: Delivery Selection & Summary ====================

@order_router.callback_query(OrderState.delivery_type, F.data.startswith("deliv:"))
async def process_delivery_choice(callback: CallbackQuery, state: FSMContext):
    """Handle delivery selection and show final confirmation receipt."""
    delivery_choice = callback.data.split(":")[1]
    await state.update_data(delivery_type=delivery_choice)

    data = await state.get_data()
    summary_text = format_order_summary(data)

    dress_photo = data.get("dress_photo")
    if dress_photo:
        try:
            await callback.message.answer_photo(
                photo=dress_photo,
                caption=summary_text,
                parse_mode="HTML",
                reply_markup=get_order_confirmation_keyboard()
            )
        except Exception:
            await callback.message.answer(
                text=summary_text,
                parse_mode="HTML",
                reply_markup=get_order_confirmation_keyboard()
            )
    else:
        await callback.message.answer(
            text=summary_text,
            parse_mode="HTML",
            reply_markup=get_order_confirmation_keyboard()
        )

    await state.set_state(OrderState.confirm)
    await callback.answer()


# ==================== Final Confirmation Handler ====================

@order_router.callback_query(OrderState.confirm, F.data == "order_confirm_yes")
async def finalize_order(callback: CallbackQuery, state: FSMContext, bot: Bot):
    """Save order to database and forward to admin."""
    data = await state.get_data()
    user = callback.from_user

    # Save to SQLite database
    try:
        order_id = await create_order(
            user_id=user.id,
            order_type=data.get("order_type", "catalog_item"),
            product_id=data.get("product_id"),
            dress_color=data.get("dress_color", "Ko'rsatilmagan"),
            dress_photo=data.get("dress_photo"),
            wedding_date=data.get("wedding_date", "Ko'rsatilmagan"),
            customer_name=data.get("customer_name", "Kelin"),
            phone_number=data.get("phone_number", "Ko'rsatilmagan"),
            delivery_type=data.get("delivery_type", "Toshkent shahri (Kuryer)")
        )
    except Exception as e:
        logger.error(f"Buyurtmani bazaga saqlashda xatolik: {e}")
        order_id = 1

    # Send warm confirmation to the bride
    user_is_admin = is_admin(user.id)
    success_text = (
        f"👑 <b>Buyurtmangiz muvaffaqiyatli qabul qilindi! (Buyurtma #{order_id})</b> ✨\n\n"
        f"Hurmatli <b>{data.get('customer_name')}</b>, «<b>Sarvinoz Collection</b>» ni tanlaganingiz uchun tashakkur!\n\n"
        "Tez orada professional menejerimiz siz bilan bog'lanib, barcha detallarni tasdiqlaydi.\n"
        "To'y oqshomingizda eng go'zal va maftunkor bo'lishingizga chin dildan tilakdoshmiz! 💖"
    )
    await callback.message.answer(
        text=success_text,
        parse_mode="HTML",
        reply_markup=get_main_keyboard(is_admin=user_is_admin)
    )

    # Forward order notification to all configured admins
    user_info = {
        "user_id": user.id,
        "username": user.username,
        "full_name": user.full_name
    }
    admin_notification = format_admin_order_notification(order_id, data, user_info)
    admin_keyboard = get_admin_order_action_keyboard(order_id)
    dress_photo = data.get("dress_photo")

    for admin_id in ADMIN_IDS:
        if admin_id <= 0:
            continue
        try:
            if dress_photo:
                await bot.send_photo(
                    chat_id=admin_id,
                    photo=dress_photo,
                    caption=admin_notification,
                    parse_mode="HTML",
                    reply_markup=admin_keyboard
                )
            else:
                await bot.send_message(
                    chat_id=admin_id,
                    text=admin_notification,
                    parse_mode="HTML",
                    reply_markup=admin_keyboard
                )
        except Exception as e:
            logger.warning(f"Adminga ({admin_id}) xabar yuborishda xatolik: {e}")

    await state.clear()
    await callback.answer("Buyurtmangiz qabul qilindi! ✨", show_alert=True)
