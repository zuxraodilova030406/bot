from typing import List, Dict, Any
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import CHANNEL_URL


def get_welcome_inline_keyboard() -> InlineKeyboardMarkup:
    """Inline keyboard for the welcome message."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📢 Kelinlar guruhimizga qo'shiling",
                    url=CHANNEL_URL
                )
            ],
            [
                InlineKeyboardButton(
                    text="👑 Katalog bilan tanishish",
                    callback_data="open_catalog"
                )
            ]
        ]
    )


def get_categories_inline_keyboard(categories: List[Dict[str, Any]]) -> InlineKeyboardMarkup:
    """Build inline buttons for each bridal category."""
    keyboard = []
    for cat in categories:
        keyboard.append([
            InlineKeyboardButton(
                text=f"{cat['emoji']} {cat['name']}",
                callback_data=f"cat:{cat['code']}"
            )
        ])
    
    keyboard.append([
        InlineKeyboardButton(
            text="📢 Real kelinlar video-obzorlari",
            url=CHANNEL_URL
        )
    ])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_product_navigation_keyboard(
    product_id: int,
    current_idx: int,
    total_items: int,
    category_code: str
) -> InlineKeyboardMarkup:
    """Build inline navigation buttons for browsing products within a category."""
    keyboard = []

    # 1. Order button
    keyboard.append([
        InlineKeyboardButton(
            text="🛍️ Buyurtma berish",
            callback_data=f"order_prod:{product_id}"
        )
    ])

    # 2. Navigation row (Prev / Next)
    nav_row = []
    if current_idx > 0:
        nav_row.append(
            InlineKeyboardButton(
                text="⬅️ Oldingisi",
                callback_data=f"pnav:{category_code}:{current_idx - 1}"
            )
        )
    
    # Counter in the middle
    nav_row.append(
        InlineKeyboardButton(
            text=f"{current_idx + 1} / {total_items}",
            callback_data="noop"
        )
    )

    if current_idx < total_items - 1:
        nav_row.append(
            InlineKeyboardButton(
                text="Keyingisi ➡️",
                callback_data=f"pnav:{category_code}:{current_idx + 1}"
            )
        )
    
    keyboard.append(nav_row)

    # 3. Back to categories
    keyboard.append([
        InlineKeyboardButton(
            text="⬅️ Boshqa bo'limlar",
            callback_data="open_catalog"
        )
    ])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_dress_color_keyboard() -> InlineKeyboardMarkup:
    """Keyboard for selecting dress color or choosing to upload a photo."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="⚪ Oq (Klassik)", callback_data="dress_c:Oq"),
                InlineKeyboardButton(text="🍦 Ayvori - Ivory", callback_data="dress_c:Ayvori - Ivory")
            ],
            [
                InlineKeyboardButton(text="🥂 Shampan (Champagne)", callback_data="dress_c:Shampan"),
                InlineKeyboardButton(text="📸 Rasm yuboraman", callback_data="dress_c:photo_mode")
            ],
            [
                InlineKeyboardButton(text="❌ Bekor qilish", callback_data="order_cancel")
            ]
        ]
    )


def get_delivery_inline_keyboard() -> InlineKeyboardMarkup:
    """Keyboard for selecting delivery method."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🚗 Toshkent shahri bo'ylab kuryer",
                    callback_data="deliv:Toshkent shahri (Kuryer)"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📦 Viloyatlarga pochta (BTS / UzPost)",
                    callback_data="deliv:Viloyatlarga pochta (BTS/UzPost)"
                )
            ],
            [
                InlineKeyboardButton(text="❌ Bekor qilish", callback_data="order_cancel")
            ]
        ]
    )


def get_order_confirmation_keyboard() -> InlineKeyboardMarkup:
    """Confirmation buttons for final order step."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Buyurtmani tasdiqlash",
                    callback_data="order_confirm_yes"
                ),
                InlineKeyboardButton(
                    text="❌ Bekor qilish",
                    callback_data="order_confirm_no"
                )
            ]
        ]
    )


def get_admin_main_keyboard() -> InlineKeyboardMarkup:
    """Admin panel main inline menu."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="➕ Yangi mahsulot qo'shish",
                    callback_data="admin_add_prod"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📋 Mahsulotlar ro'yxati / Tahrirlash",
                    callback_data="admin_list_prods"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📊 Umumiy statistika",
                    callback_data="admin_stats"
                ),
                InlineKeyboardButton(
                    text="📦 So'nggi buyurtmalar",
                    callback_data="admin_recent_orders"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📢 Xabar yuborish (Broadcast)",
                    callback_data="admin_broadcast"
                )
            ],
            [
                InlineKeyboardButton(
                    text="❌ Menyuni yopish",
                    callback_data="admin_close"
                )
            ]
        ]
    )


def get_admin_category_select_keyboard(categories: List[Dict[str, Any]]) -> InlineKeyboardMarkup:
    """Select category when adding a product."""
    keyboard = []
    for cat in categories:
        keyboard.append([
            InlineKeyboardButton(
                text=f"{cat['emoji']} {cat['name']}",
                callback_data=f"adm_cat_sel:{cat['code']}"
            )
        ])
    keyboard.append([
        InlineKeyboardButton(text="❌ Bekor qilish", callback_data="admin_cancel")
    ])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_admin_status_select_keyboard() -> InlineKeyboardMarkup:
    """Select product availability status."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Sotuvda bor",
                    callback_data="adm_status:available"
                )
            ],
            [
                InlineKeyboardButton(
                    text="⏳ Buyurtma asosida",
                    callback_data="adm_status:custom_order"
                )
            ],
            [
                InlineKeyboardButton(text="❌ Bekor qilish", callback_data="admin_cancel")
            ]
        ]
    )


def get_admin_product_manage_keyboard(product_id: int) -> InlineKeyboardMarkup:
    """Actions for managing a specific product in admin panel."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✏️ Narxini o'zgartirish",
                    callback_data=f"adm_edit_prc:{product_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔄 Holatni o'zgartirish",
                    callback_data=f"adm_tog_stat:{product_id}"
                ),
                InlineKeyboardButton(
                    text="🗑️ O'chirish",
                    callback_data=f"adm_del_prod:{product_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="⬅️ Ro'yxatga qaytish",
                    callback_data="admin_list_prods"
                )
            ]
        ]
    )


def get_admin_order_action_keyboard(order_id: int) -> InlineKeyboardMarkup:
    """Quick action buttons on admin order notification."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Bog'landim / Qabul qilindi",
                    callback_data=f"adm_ord_act:{order_id}:contacted"
                ),
                InlineKeyboardButton(
                    text="❌ Bekor qilindi",
                    callback_data=f"adm_ord_act:{order_id}:cancelled"
                )
            ]
        ]
    )
