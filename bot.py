import asyncio
import logging
import os
import sys

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

import aiohttp
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand

from config import (
    BOT_TOKEN,
    ADMIN_IDS,
    BRAND_NAME,
    CHANNEL_USERNAME,
)
from database import init_db
from handlers import user_router, order_router, admin_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("sarvinoz_bot")


async def start_render_health_server():
    """Start lightweight HTTP server for Render Web Service health-check."""
    port_str = os.getenv("PORT")
    if not port_str:
        return None

    try:
        port = int(port_str)
    except ValueError:
        return None

    async def handle_ping(request):
        return web.Response(
            text="👑 Sarvinoz Collection Bot is running 24/7 on Render!",
            content_type="text/plain",
            status=200
        )

    app = web.Application()
    app.router.add_get("/", handle_ping)
    app.router.add_get("/health", handle_ping)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    logger.info(f"Render Web Service salomatlik serveri 0.0.0.0:{port} da ishga tushdi.")
    return runner


async def render_keep_alive_task():
    """Background task to self-ping on Render every 10 minutes to prevent free tier sleep."""
    external_url = os.getenv("RENDER_EXTERNAL_URL") or os.getenv("PING_URL")
    if not external_url:
        return

    health_url = f"{external_url.rstrip('/')}/health"
    logger.info(f"Render 24/7 Keep-Alive faollashtirildi: {health_url}")

    await asyncio.sleep(60)
    async with aiohttp.ClientSession() as session:
        while True:
            try:
                async with session.get(health_url, timeout=15) as resp:
                    logger.info(f"Keep-Alive ping yuborildi: Status {resp.status}")
            except Exception as e:
                logger.warning(f"Keep-Alive ping xatosi: {e}")
            await asyncio.sleep(600)  # Ping every 10 minutes to stay awake 24/7


async def setup_bot_commands(bot: Bot):
    """Register menu commands in Telegram interface."""
    commands = [
        BotCommand(command="start", description="👑 Botni ishga tushirish va menyu"),
        BotCommand(command="help", description="ℹ️ Yordam va ma'lumotlar"),
        BotCommand(command="admin", description="🛠️ Boshqaruv paneli (Admin)"),
    ]
    await bot.set_my_commands(commands)


async def main():
    """Main application entry point."""
    print("=" * 60)
    print(f"✨  {BRAND_NAME.upper()} TELEGRAM BOT  ✨")
    print(f"💎  Rasmiy kanal: {CHANNEL_USERNAME}")
    print("=" * 60)

    # Validate bot token configuration
    if not BOT_TOKEN or "YOUR_TELEGRAM_BOT_TOKEN_HERE" in BOT_TOKEN:
        logger.error(
            "\n[XATOLIK] BOT_TOKEN sozlanmagan!\n"
            "Iltimos, '.env' faylini oching va Telegram @BotFather dan olingan bot tokenni kiriting:\n"
            "BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz\n"
        )
        sys.exit(1)

    # Initialize asynchronous SQLite database
    logger.info("Ma'lumotlar bazasi initsializatsiya qilinmoqda...")
    await init_db()

    # Initialize Bot instance with default HTML formatting
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    # Initialize Dispatcher with MemoryStorage for FSM
    dp = Dispatcher(storage=MemoryStorage())

    # Register routers: admin first, then order flow, then user navigation
    dp.include_router(admin_router)
    dp.include_router(order_router)
    dp.include_router(user_router)

    # Setup bot commands
    try:
        await setup_bot_commands(bot)
    except Exception as e:
        logger.warning(f"Bot buyruqlarini ro'yxatdan o'tkazishda xatolik: {e}")

    # Notify admin on startup
    for admin_id in ADMIN_IDS:
        if admin_id > 0:
            try:
                await bot.send_message(
                    chat_id=admin_id,
                    text=f"👑 <b>«{BRAND_NAME}» boti muvaffaqiyatli ishga tushirildi!</b> ✨\n"
                         f"Status: Onlayn va buyurtmalarni qabul qilishga tayyor."
                )
            except Exception as e:
                logger.debug(f"Admin ({admin_id}) ga start xabari yetib bormadi: {e}")

    logger.info("Bot muvaffaqiyatli ishga tushdi va xabarlarni kutmoqda...")

    # Start Render health server if PORT is provided
    web_runner = await start_render_health_server()
    keep_alive_task = asyncio.create_task(render_keep_alive_task())

    # Drop pending updates and start polling
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        keep_alive_task.cancel()
        if web_runner:
            await web_runner.cleanup()
        await bot.session.close()
        logger.info("Bot sessiyasi yopildi.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot to'xtatildi.")
