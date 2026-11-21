import logging
from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from config import is_admin
from database import (
    get_categories,
    get_category_by_code,
    get_all_active_products,
    get_product_by_id,
    add_product,
    update_product_price,
    update_product_status,
    delete_product,
    get_total_active_products_count,
    get_total_users_count,
    get_total_orders_count,
    get_recent_orders,
    update_order_status,
    get_all_user_ids,
)
from states.admin import AddProductState, EditPriceState, BroadcastState
from keyboards import (
    get_admin_main_keyboard,
    get_admin_category_select_keyboard,
    get_admin_status_select_keyboard,
    get_admin_product_manage_keyboard,
    get_cancel_keyboard,
    get_main_keyboard,
)
from utils.text import format_price

logger = logging.getLogger(__name__)
admin_router = Router(name="admin_router")


# ==================== Admin Auth Filter Helper ====================

def check_admin(user_id: int) -> bool:
    """Helper to verify admin privilege."""
    return is_admin(user_id)


# ==================== Admin Panel Entry ====================

@admin_router.message(Command("admin"))
@admin_router.message(F.text == "🛠️ Admin Panel")
async def show_admin_panel(message: Message, state: FSMContext):
    """Entry point for admin panel."""
    if not check_admin(message.from_user.id):
        await message.answer("Kechirasiz, sizda admin huquqlari mavjud emas. 🔒")
        return

    await state.clear()
    total_prods = await get_total_active_products_count()
    total_users = await get_total_users_count()
    total_orders = await get_total_orders_count()

    admin_welcome = (
        "👑 <b>«Sarvinoz Collection» Boshqaruv Paneli</b> 🛠️\n\n"
        f"📊 <b>Hozirgi holat:</b>\n"
        f"• Faol mahsulotlar: <b>{total_prods} ta</b>\n"
        f"• Ro'yxatdan o'tgan foydalanuvchilar: <b>{total_users} nafar</b>\n"
        f"• Jami buyurtmalar: <b>{total_orders} ta</b>\n\n"
        "Quyidagi amallardan birini tanlang:"
    )
    await message.answer(
        text=admin_welcome,
        parse_mode="HTML",
        reply_markup=get_admin_main_keyboard()
    )


@admin_router.callback_query(F.data == "admin_close")
async def close_admin_panel(callback: CallbackQuery, state: FSMContext):
    """Close admin menu and return to main user view."""
    await state.clear()
    try:
        await callback.message.delete()
    except Exception:
        pass
    await callback.message.answer(
        "Admin panel yopildi. Bosh menyudasiz.",
        reply_markup=get_main_keyboard(is_admin=True)
    )
    await callback.answer()


@admin_router.callback_query(F.data == "admin_cancel")
async def cancel_admin_action(callback: CallbackQuery, state: FSMContext):
    """Cancel current admin FSM action."""
    await state.clear()
    await callback.message.answer(
        "Amal bekor qilindi.",
        reply_markup=get_admin_main_keyboard()
    )
    await callback.answer()


# ==================== Statistics ====================

@admin_router.callback_query(F.data == "admin_stats")
async def view_admin_stats(callback: CallbackQuery):
    """View bot statistics."""
    if not check_admin(callback.from_user.id):
        await callback.answer("Ruxsat berilmagan.", show_alert=True)
        return

    total_prods = await get_total_active_products_count()
    total_users = await get_total_users_count()
    total_orders = await get_total_orders_count()

    text = (
        "📊 <b>«Sarvinoz Collection» Statistikasi:</b>\n\n"
        f"👑 Faol mahsulotlar soni: <b>{total_prods} ta</b>\n"
        f"👰 Ro'yxatdan o'tgan kelinlar/mijozlar: <b>{total_users} nafar</b>\n"
        f"🛍️ Jami kelib tushgan buyurtmalar: <b>{total_orders} ta</b>\n"
    )
    await callback.message.answer(text, parse_mode="HTML", reply_markup=get_admin_main_keyboard())
    await callback.answer()


# ==================== Recent Orders ====================

@admin_router.callback_query(F.data == "admin_recent_orders")
async def view_recent_orders(callback: CallbackQuery):
    """View 5 most recent orders."""
    if not check_admin(callback.from_user.id):
        await callback.answer("Ruxsat berilmagan.", show_alert=True)
        return

    orders = await get_recent_orders(limit=5)
    if not orders:
        await callback.message.answer(
            "Hozircha buyurtmalar mavjud emas.",
            reply_markup=get_admin_main_keyboard()
        )
        await callback.answer()
        return

    text = "📦 <b>Oxirgi 5 ta buyurtma:</b>\n\n"
    for o in orders:
        status_map = {
            "yangi": "🟡 Yangi",
            "contacted": "🟢 Bog'lanildi",
            "cancelled": "🔴 Bekor qilingan"
        }
        st_text = status_map.get(o["status"], o["status"])
        prod = o.get("product_name") or "Individual buyurtma"
        text += (
            f"<b>Buyurtma #{o['id']}</b> ({st_text})\n"
            f"👤 Mijoz: {o['customer_name']} (<code>{o['phone_number']}</code>)\n"
            f"💎 Mahsulot: {prod}\n"
            f"📅 To'y sanasi: {o['wedding_date']}\n"
            f"🚚 Yetkazish: {o['delivery_type']}\n"
            f"⏱ Sana: {o['created_at']}\n"
            "---------------------------\n"
        )

    await callback.message.answer(text, parse_mode="HTML", reply_markup=get_admin_main_keyboard())
    await callback.answer()


# ==================== Order Action Callback ====================

@admin_router.callback_query(F.data.startswith("adm_ord_act:"))
async def process_order_action(callback: CallbackQuery):
    """Admin marks order as contacted or cancelled directly from notification."""
    if not check_admin(callback.from_user.id):
        await callback.answer("Ruxsat yo'q.", show_alert=True)
        return

    parts = callback.data.split(":")
    order_id = int(parts[1])
    action = parts[2]

    await update_order_status(order_id, action)

    status_name = "✅ Bog'lanildi / Qabul qilindi" if action == "contacted" else "❌ Bekor qilindi"
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.reply(
        f"Buyurtma #{order_id} holati yangilandi: <b>{status_name}</b>",
        parse_mode="HTML"
    )
    await callback.answer(f"Buyurtma #{order_id}: {status_name}")


# ==================== List & Manage Products ====================

@admin_router.callback_query(F.data == "admin_list_prods")
async def list_products_for_management(callback: CallbackQuery):
    """List active products for editing or deleting."""
    if not check_admin(callback.from_user.id):
        await callback.answer("Ruxsat yo'q.", show_alert=True)
        return

    products = await get_all_active_products()
    if not products:
        await callback.message.answer(
            "Hozircha katalogda mahsulotlar yo'q.",
            reply_markup=get_admin_main_keyboard()
        )
        await callback.answer()
        return

    await callback.message.answer(
        f"📋 <b>Barcha faol mahsulotlar ({len(products)} ta):</b>\n"
        "Tahrirlash yoki o'chirish uchun kerakli mahsulot ostidagi tugmalardan foydalaning:",
        parse_mode="HTML"
    )

    # Show first 5 products cards for quick management
    for prod in products[:6]:
        status_label = "✅ Sotuvda bor" if prod["status"] == "available" else "⏳ Buyurtma asosida"
        info = (
            f"<b>{prod['name']}</b> (ID: <code>{prod['id']}</code>)\n"
            f"Kategoriya: {prod.get('category_name', prod['category_code'])}\n"
            f"Narxi: <b>{format_price(prod['price'])}</b>\n"
            f"Holati: {status_label}\n"
            f"Materiallar: {prod.get('materials', '-')}\n"
            f"O'lchami: {prod.get('dimensions', '-')}"
        )
        keyboard = get_admin_product_manage_keyboard(prod["id"])
        try:
            await callback.message.answer_photo(
                photo=prod["photo"],
                caption=info,
                parse_mode="HTML",
                reply_markup=keyboard
            )
        except Exception:
            await callback.message.answer(
                text=info,
                parse_mode="HTML",
                reply_markup=keyboard
            )

    await callback.answer()


@admin_router.callback_query(F.data.startswith("adm_del_prod:"))
async def handle_delete_product(callback: CallbackQuery):
    """Soft delete product from catalog."""
    if not check_admin(callback.from_user.id):
        return

    product_id = int(callback.data.split(":")[1])
    await delete_product(product_id)
    await callback.answer("Mahsulot muvaffaqiyatli o'chirildi! 🗑️", show_alert=True)
    try:
        await callback.message.delete()
    except Exception:
        pass


@admin_router.callback_query(F.data.startswith("adm_tog_stat:"))
async def handle_toggle_status(callback: CallbackQuery):
    """Toggle product availability status between available and custom_order."""
    if not check_admin(callback.from_user.id):
        return

    product_id = int(callback.data.split(":")[1])
    product = await get_product_by_id(product_id)
    if not product:
        await callback.answer("Mahsulot topilmadi.")
        return

    new_status = "custom_order" if product["status"] == "available" else "available"
    await update_product_status(product_id, new_status)
    status_label = "✅ Sotuvda bor" if new_status == "available" else "⏳ Buyurtma asosida"

    await callback.answer(f"Yangi holat: {status_label}", show_alert=True)


@admin_router.callback_query(F.data.startswith("adm_edit_prc:"))
async def handle_start_edit_price(callback: CallbackQuery, state: FSMContext):
    """Start price editing flow for a product."""
    if not check_admin(callback.from_user.id):
        return

    product_id = int(callback.data.split(":")[1])
    product = await get_product_by_id(product_id)

    if not product:
        await callback.answer("Mahsulot topilmadi.")
        return

    await state.clear()
    await state.update_data(product_id=product_id)
    await callback.message.answer(
        f"<b>{product['name']}</b> uchun yangi narxni so'mda kiriting\n"
        f"(Hozirgi narxi: {format_price(product['price'])}):\n\n"
        "Faqat raqam yuboring (Masalan: <code>950000</code>):",
        parse_mode="HTML",
        reply_markup=get_cancel_keyboard()
    )
    await state.set_state(EditPriceState.new_price)
    await callback.answer()


@admin_router.message(EditPriceState.new_price, F.text)
async def process_new_price(message: Message, state: FSMContext):
    """Save new product price."""
    text = message.text.replace(" ", "").strip()
    if not text.isdigit():
        await message.answer("Iltimos, narxni faqat butun musbat raqamlar bilan kiriting (Masalan: 850000):")
        return

    new_price = int(text)
    data = await state.get_data()
    product_id = data.get("product_id")

    await update_product_price(product_id, new_price)
    await state.clear()

    await message.answer(
        f"✅ Mahsulot (ID #{product_id}) narxi muvaffaqiyatli yangilandi: <b>{format_price(new_price)}</b>",
        parse_mode="HTML",
        reply_markup=get_main_keyboard(is_admin=True)
    )


# ==================== Add New Product FSM ====================

@admin_router.callback_query(F.data == "admin_add_prod")
async def start_add_product(callback: CallbackQuery, state: FSMContext):
    """Step 1: Select category for new product."""
    if not check_admin(callback.from_user.id):
        await callback.answer("Ruxsat yo'q.", show_alert=True)
        return

    categories = await get_categories()
    await state.clear()
    await callback.message.answer(
        "➕ <b>Yangi mahsulot qo'shish</b>\n\n"
        "1/6-bosqich: Mahsulot tegishli bo'lgan kategoriyani tanlang:",
        parse_mode="HTML",
        reply_markup=get_admin_category_select_keyboard(categories)
    )
    await state.set_state(AddProductState.category)
    await callback.answer()


@admin_router.callback_query(AddProductState.category, F.data.startswith("adm_cat_sel:"))
async def process_add_category(callback: CallbackQuery, state: FSMContext):
    """Step 2: Enter product name."""
    cat_code = callback.data.split(":")[1]
    category = await get_category_by_code(cat_code)
    await state.update_data(category_code=cat_code)

    await callback.message.answer(
        f"Kategoriya tanlandi: <b>{category['name'] if category else cat_code}</b>\n\n"
        "2/6-bosqich: Mahsulot nomini kiriting\n"
        "(Masalan: <i>👑 \"Malika\" Swarovski Diadema</i>):",
        parse_mode="HTML"
    )
    await state.set_state(AddProductState.name)
    await callback.answer()


@admin_router.message(AddProductState.name, F.text)
async def process_add_name(message: Message, state: FSMContext):
    """Step 3: Enter materials and dimensions."""
    name = message.text.strip()
    await state.update_data(name=name)

    await message.answer(
        f"Nom saqlandi: <b>{name}</b>\n\n"
        "3/6-bosqich: Mahsulot materiallari va o'lchamlarini kiriting\n"
        "(Masalan: <i>Swarovski kristallari, yapon biseri | Balandligi: 7 sm, aylanasi: 32 sm</i>):",
        parse_mode="HTML"
    )
    await state.set_state(AddProductState.materials)


@admin_router.message(AddProductState.materials, F.text)
async def process_add_materials(message: Message, state: FSMContext):
    """Step 4: Enter price in UZS."""
    details = message.text.strip()
    await state.update_data(materials=details, dimensions="Standart kelinlik o'lchami")

    await message.answer(
        "4/6-bosqich: Mahsulot narxini so'mda kiriting (faqat raqamlar)\n"
        "(Masalan: <code>850000</code>):",
        parse_mode="HTML"
    )
    await state.set_state(AddProductState.price)


@admin_router.message(AddProductState.price, F.text)
async def process_add_price(message: Message, state: FSMContext):
    """Step 5: Upload photo."""
    text = message.text.replace(" ", "").strip()
    if not text.isdigit():
        await message.answer("Iltimos, narxni faqat raqamda kiriting (Masalan: 850000):")
        return

    price = int(text)
    await state.update_data(price=price)

    await message.answer(
        f"Narx: <b>{format_price(price)}</b>\n\n"
        "5/6-bosqich: Mahsulotning yuqori sifatli fotosuratini yuboring 📸:",
        parse_mode="HTML"
    )
    await state.set_state(AddProductState.photo)


@admin_router.message(AddProductState.photo, F.photo)
async def process_add_photo(message: Message, state: FSMContext):
    """Step 6: Choose availability status."""
    photo_file_id = message.photo[-1].file_id
    await state.update_data(photo=photo_file_id)

    await message.answer(
        "📸 Surat qabul qilindi!\n\n"
        "6/6-bosqich: Mahsulotning sotuvdagi holatini belgilang:",
        reply_markup=get_admin_status_select_keyboard()
    )
    await state.set_state(AddProductState.status)


@admin_router.callback_query(AddProductState.status, F.data.startswith("adm_status:"))
async def process_add_status(callback: CallbackQuery, state: FSMContext):
    """Save new product to database."""
    status = callback.data.split(":")[1]
    data = await state.get_data()

    new_id = await add_product(
        category_code=data["category_code"],
        name=data["name"],
        description="Sarvinoz Collection eksklyuziv kelinlik aksessuari.",
        materials=data["materials"],
        dimensions=data.get("dimensions", "Standart o'lcham"),
        price=data["price"],
        photo=data["photo"],
        status=status
    )

    await state.clear()
    status_label = "✅ Sotuvda bor" if status == "available" else "⏳ Buyurtma asosida"

    success_msg = (
        f"🎉 <b>Yangi mahsulot katalogga muvaffaqiyatli qo'shildi!</b>\n\n"
        f"ID: <code>{new_id}</code>\n"
        f"Nomi: <b>{data['name']}</b>\n"
        f"Narxi: <b>{format_price(data['price'])}</b>\n"
        f"Holati: <b>{status_label}</b>"
    )
    await callback.message.answer(
        text=success_msg,
        parse_mode="HTML",
        reply_markup=get_admin_main_keyboard()
    )
    await callback.answer("Mahsulot saqlandi!")


# ==================== Broadcast to Users ====================

@admin_router.callback_query(F.data == "admin_broadcast")
async def start_broadcast(callback: CallbackQuery, state: FSMContext):
    """Initiate broadcast message to all users."""
    if not check_admin(callback.from_user.id):
        await callback.answer("Ruxsat yo'q.", show_alert=True)
        return

    await state.clear()
    await callback.message.answer(
        "📢 <b>Barcha foydalanuvchilarga xabar yuborish:</b>\n\n"
        "Yubormoqchi bo'lgan xabaringiz matnini yoki suratli postni kiriting.\n"
        "Bekor qilish uchun «❌ Bekor qilish» deb yozing.",
        parse_mode="HTML",
        reply_markup=get_cancel_keyboard()
    )
    await state.set_state(BroadcastState.message)
    await callback.answer()


@admin_router.message(BroadcastState.message)
async def process_broadcast(message: Message, state: FSMContext, bot: Bot):
    """Execute broadcast to all registered bot users."""
    if message.text == "❌ Bekor qilish":
        await state.clear()
        await message.answer("Xabar tarqatish bekor qilindi.", reply_markup=get_main_keyboard(is_admin=True))
        return

    users = await get_all_user_ids()
    await state.clear()

    await message.answer(f"⏳ {len(users)} nafar foydalanuvchiga xabar yuborilmoqda...")

    success = 0
    failed = 0

    for user_id in users:
        try:
            await message.send_copy(chat_id=user_id)
            success += 1
        except Exception:
            failed += 1

    report = (
        "📢 <b>Xabar tarqatish yakunlandi:</b>\n\n"
        f"✅ Muvaffaqiyatli yetkazildi: <b>{success} ta</b>\n"
        f"❌ Yetkazib bo'lmadi (bloklangan/o'chirilgan): <b>{failed} ta</b>"
    )
    await message.answer(
        text=report,
        parse_mode="HTML",
        reply_markup=get_main_keyboard(is_admin=True)
    )
