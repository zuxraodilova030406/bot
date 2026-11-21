"""Keyboards package for Sarvinoz Collection bot."""
from .default import (
    get_main_keyboard,
    get_contact_keyboard,
    get_cancel_keyboard,
    get_delivery_reply_keyboard,
)
from .inline import (
    get_welcome_inline_keyboard,
    get_categories_inline_keyboard,
    get_product_navigation_keyboard,
    get_dress_color_keyboard,
    get_delivery_inline_keyboard,
    get_order_confirmation_keyboard,
    get_admin_main_keyboard,
    get_admin_category_select_keyboard,
    get_admin_status_select_keyboard,
    get_admin_product_manage_keyboard,
    get_admin_order_action_keyboard,
)

__all__ = [
    "get_main_keyboard",
    "get_contact_keyboard",
    "get_cancel_keyboard",
    "get_delivery_reply_keyboard",
    "get_welcome_inline_keyboard",
    "get_categories_inline_keyboard",
    "get_product_navigation_keyboard",
    "get_dress_color_keyboard",
    "get_delivery_inline_keyboard",
    "get_order_confirmation_keyboard",
    "get_admin_main_keyboard",
    "get_admin_category_select_keyboard",
    "get_admin_status_select_keyboard",
    "get_admin_product_manage_keyboard",
    "get_admin_order_action_keyboard",
]
