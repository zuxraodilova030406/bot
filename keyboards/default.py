from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_main_keyboard(is_admin: bool = False) -> ReplyKeyboardMarkup:
    """Build the luxury bridal main reply keyboard."""
    keyboard = [
        [
            KeyboardButton(text="👑 Katalog"),
            KeyboardButton(text="✨ Individual buyurtma")
        ],
        [
            KeyboardButton(text="👰‍♀️ Ko'ylakka mos tanlash"),
            KeyboardButton(text="🚚 Yetkazib berish va To'lov")
        ],
        [
            KeyboardButton(text="📢 Telegram guruhimiz"),
            KeyboardButton(text="📞 Bog'lanish")
        ]
    ]

    if is_admin:
        keyboard.append([KeyboardButton(text="🛠️ Admin Panel")])

    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        input_field_placeholder="«Sarvinoz Collection» bo'limini tanlang..."
    )


def get_contact_keyboard() -> ReplyKeyboardMarkup:
    """Keyboard requesting phone number via Telegram button or cancel."""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📱 Raqamni yuborish", request_contact=True)],
            [KeyboardButton(text="❌ Bekor qilish")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Telefon raqamingizni yuboring..."
    )


def get_cancel_keyboard() -> ReplyKeyboardMarkup:
    """Simple cancel reply keyboard."""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="❌ Bekor qilish")]
        ],
        resize_keyboard=True
    )


def get_delivery_reply_keyboard() -> ReplyKeyboardMarkup:
    """Keyboard for selecting delivery option."""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🚗 Toshkent shahri bo'ylab kuryer")],
            [KeyboardButton(text="📦 Viloyatlarga pochta (BTS/UzPost)")],
            [KeyboardButton(text="❌ Bekor qilish")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
