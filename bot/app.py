# bot/app.py
import os
import logging
from dotenv import load_dotenv
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
import httpx

load_dotenv()  # читаем .env

TOKEN = os.getenv("TELEGRAM_TOKEN")
BACKEND = os.getenv("BACKEND_URL", "http://backend:8000")

# ----------------------------------------------------------------------


async def start(update: Update, _: ContextTypes.DEFAULT_TYPE):
    kb = [[KeyboardButton("📡 Найти Wi-Fi рядом", request_location=True)]]
    await update.message.reply_text(
        "Привет! Пришли геолокацию — найду ближайшие точки Wi-Fi.",
        reply_markup=ReplyKeyboardMarkup(kb, resize_keyboard=True),
    )


async def handle_location(update: Update, _: ContextTypes.DEFAULT_TYPE):
    loc = update.message.location
    await update.message.reply_text("Ищу точки…")
    points = await get_points(loc.latitude, loc.longitude)
    if not points:
        await update.message.reply_text("Поблизости ничего не нашёл 😔")
        return
    lines = [
        f"📶 {p['bssid']}  {p['rssi']} dBm  {'🌐' if p['internet'] else '🚫'}"
        for p in points[:10]
    ]
    await update.message.reply_text("\n".join(lines))


async def get_points(lat, lon, radius=300):
    async with httpx.AsyncClient(timeout=5) as client:
        r = await client.get(
            f"{BACKEND}/points",
            params={"lat": lat, "lon": lon, "radius": radius, "limit": 100},
        )
        r.raise_for_status()
        return r.json()


# ----------------------------------------------------------------------


def main() -> None:
    if not TOKEN:
        raise RuntimeError("TELEGRAM_TOKEN not set")
    logging.basicConfig(level=logging.INFO)
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.LOCATION, handle_location))
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
