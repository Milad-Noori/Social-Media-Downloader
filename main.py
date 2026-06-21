import logging
import sys

from telegram import Update
from telegram.ext import (
    Application, ApplicationBuilder, CommandHandler, MessageHandler,
    CallbackQueryHandler, ContextTypes, filters,
)
from config import BOT_TOKEN, LOG_FILE_PATH
from db.database import init_db

from handlers.start import start_handler
from handlers.force_join_handler import check_force_join_callback
from handlers.download import link_message_handler, quality_selection_callback
from handlers.plans import plans_command, request_plan_callback
from handlers.admin_panel import admin_panel_entry, admin_callback_router
from handlers.admin_subscription import handle_admin_setting_input
from handlers.admin_force_join import handle_force_join_add_input
from handlers.admin_broadcast import handle_broadcast_message_input


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE_PATH, encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger("mediabot.main")


async def generic_text_router(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    if await handle_admin_setting_input(update, context):
        return
    if await handle_force_join_add_input(update, context):
        return
    if await handle_broadcast_message_input(update, context):
        return

    await link_message_handler(update, context)


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error(f"خطای پیش‌بینی‌نشده: {context.error}", exc_info=context.error)
