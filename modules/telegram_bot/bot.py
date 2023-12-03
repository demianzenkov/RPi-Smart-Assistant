# bot.py
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ConversationHandler, ContextTypes, CallbackContext
)
from telegram.error import BadRequest
from flask import Flask
import os
import sys
import asyncio

modules_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(modules_dir)

from globals import get_latest_photo_filename, get_latest_video_filename
from globals import get_longitude, get_latitude

load_dotenv()

MAC_OS_WEBCAMERA_INDEX = 1
BOT_TOKEN = os.getenv('BOT_TOKEN')

DEMIAN_CHAT_ID = 68401959

app = Flask(__name__)
active_chats = set()


@app.route('/')
def health_check():
    return "OK", 200


async def handle_intent_events(bot, events):
    print("Event handling loop started")
    while True:
        if events['send_video_event'].is_set():
            print("Sending video")
            await send_latest_video_to_all_chats(bot)
            events['send_video_event'].clear()

        if events['send_photo_event'].is_set():
            print("Sending photo")
            await send_latest_photo_to_all_chats(bot)  # Updated function call
            events['send_photo_event'].clear()

        if events['save_location_event'].is_set():
            print("Saving location")
            await send_location_to_all_chats(bot)
            events['save_location_event'].clear()

        await asyncio.sleep(0.1)


async def send_location_to_all_chats(bot):
    latitude = get_latitude()
    longitude = get_longitude()
    print(f"Sending location: {latitude}, {longitude}")
    if latitude is not None and longitude is not None:
        try:
            await bot.send_location(chat_id=DEMIAN_CHAT_ID, latitude=latitude, longitude=longitude)
        except Exception as e:
            print(f"Failed to send location: {e}")
    else:
        print("No location available to send.")


async def send_latest_video_to_all_chats(bot):
    video_filename = get_latest_video_filename()
    print(f"Sending video: {video_filename}")

    if video_filename and os.path.exists(video_filename):
        file_size = os.path.getsize(video_filename)
        print(f"Video file size: {file_size} bytes")

        if file_size < 50 * 1024 * 1024:  # Check if file size is less than 50 MB (Telegram limit)
            try:
                with open(video_filename, 'rb') as video_file:
                    await bot.send_video(chat_id=DEMIAN_CHAT_ID, video=video_file)
            except Exception as e:
                print(f"Failed to send video: {e}")
        else:
            print("Video file too large to send.")
    else:
        print(f"No video available to send or file {video_filename} does not exist.")


async def send_latest_photo_to_all_chats(bot):
    photo_filename = get_latest_photo_filename()
    # print(f"Active chats: {active_chats}")
    # print(f"Sending photo: {photo_filename}")
    if photo_filename and os.path.exists(photo_filename):
        try:
            with open(photo_filename, 'rb') as photo_file:
                await bot.send_photo(chat_id=DEMIAN_CHAT_ID, photo=photo_file)
        except Exception as e:
            print(f"Failed to send photo: {e}")
    else:
        print(f"No photo available to send or file {photo_filename} does not exist.")

def run_flask_app():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))


async def error_handler(update: Update, context: CallbackContext) -> None:
    """Handle errors caused by updates."""
    try:
        raise context.error
    except BadRequest as bad_request_error:
        if str(bad_request_error) == 'Chat not found':
            # Handle the "Chat not found" error here
            print("Error: Chat not found")


async def start(update: Update, context: CallbackContext) -> None:
    # Implementation for your start command
    chat_id = update.effective_chat.id
    active_chats.add(chat_id)
    await update.message.reply_text('Hello! This is your bot.')


async def cancel(update: Update, context: CallbackContext) -> None:
    # Implementation for your cancel command
    await update.message.reply_text('Goodbye!')


def start_telegram_bot(events):
    application = Application.builder().token(BOT_TOKEN).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={},
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    application.add_handler(conv_handler)
    application.add_error_handler(error_handler)

    # Schedule the event handling coroutine
    bot = application.bot
    asyncio.ensure_future(handle_intent_events(bot, events))

    application.run_polling()


if __name__ == '__main__':
    start_telegram_bot()
