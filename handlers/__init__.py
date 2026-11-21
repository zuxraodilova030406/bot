"""Handlers package for Sarvinoz Collection bot."""
from .user import user_router
from .order import order_router
from .admin import admin_router

__all__ = ["user_router", "order_router", "admin_router"]
