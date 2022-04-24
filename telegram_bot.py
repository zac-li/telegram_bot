import pydf
import logging
import sys
import os
from datetime import date, time
from pytz import timezone
import shutil

from typing import Callable

from glassnode import (
    get_sopr,
    get_btc_key_stats,
    get_btc_ex_activity,
    get_eth_ex_activity,
)
from telegram import Update
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackContext,
    MessageHandler,
    Filters,
)
from constants import TELEGRAM_TOKEN, PORT, INTRO, HELP, GLOSSARY, CHAT_ID


# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update: Update, _: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_photo(
        "https://pbs.twimg.com/media/EnPTsv2XUAEeOFN?format=jpg&name=900x900"
    )
    update.message.reply_text(INTRO)
    update.message.reply_text(HELP, parse_mode="Markdown")


def help_command(update: Update, _: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text(HELP, parse_mode="Markdown")


def echo_command(update: Update, _: CallbackContext) -> None:
    """LOL."""
    update.message.reply_text(
        "Sorry bruh I don't understand what you are trying to do, try /help instead."
    )


def glossary_command(update: Update, _: CallbackContext) -> None:
    """Terminology look up."""
    update.message.reply_text(
        GLOSSARY, parse_mode="Markdown", disable_web_page_preview=True
    )


def _generate_file_for_type(
    file_type: str, f: Callable, width: int, height: int, zoom: float
) -> str:
    """ PDF retrieval / generation. """

    dir_path = os.path.dirname(os.path.realpath(__file__))
    date_str = date.today().strftime("%Y-%m-%d")
    file_name = f"{dir_path}/tmp/{file_type}/{date_str}.pdf"

    if not os.path.isfile(file_name):
        logger.info(f"Removing {dir_path}/tmp/{file_type} and recreate.")
        try:
            shutil.rmtree(f"{dir_path}/tmp/{file_type}")
        except:
            pass
        os.makedirs(f"{dir_path}/tmp/{file_type}")

        logger.info(f"Generating {file_name} via API call.")
        pdf = pydf.generate_pdf(
            f(), page_width=f"{width}mm", page_height=f"{height}mm", zoom=zoom
        )
        with open(file_name, "wb") as f:
            f.write(pdf)
    else:
        logger.info(f"{file_name} already exists, reading from local.")

    return file_name


def sopr_command(update: Update, _: CallbackContext) -> None:
    """Show SOPR when the command /help is issued."""

    file_name = _generate_file_for_type("sopr", get_sopr, 120, 120, 1.8)

    logger.info("Sending the file via Bot.")
    update.message.reply_photo(
        open(file_name, "rb"),
        caption="BTC SOPR in the past 7 days",
    )


def btc_key_command(update: Update, _: CallbackContext) -> None:
    """BTC key stats."""

    file_name = _generate_file_for_type("btc", get_btc_key_stats, 280, 220, 2.5)

    logger.info("Sending the file via Bot.")
    update.message.reply_photo(
        open(file_name, "rb"),
        caption="BTC Top / Bottom Indicators",
    )


def btc_ex_command(update: Update, _: CallbackContext) -> None:
    """BTC Exchange stats."""
    _ex_command(update, "BTC", get_btc_ex_activity)


def eth_ex_command(update: Update, _: CallbackContext) -> None:
    """ETH Exchange stats."""
    _ex_command(update, "ETH", get_eth_ex_activity)


def _ex_command(update: Update, asset: str, f: Callable) -> None:

    file_name = _generate_file_for_type(f"{asset}_ex".lower(), f, 280, 220, 2.5)

    logger.info("Sending the file via Bot.")
    update.message.reply_photo(
        open(file_name, "rb"),
        caption=f"{asset} On-Chain Exchange Activity",
    )


def remove_cache_command(update: Update, _: CallbackContext) -> None:
    """Internal command to remove cache."""
    try:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        shutil.rmtree(f"{dir_path}/tmp/")
        update.message.reply_text("Done!!")
    except:
        pass


def callback(context: CallbackContext):

    logger.info("Doing scheduled stuff.")

    file_name = _generate_file_for_type("btc", get_btc_key_stats, 280, 220, 2.5)
    context.bot.send_message(
        chat_id=CHAT_ID,
        text=f"*Digest for {date.today().strftime('%Y-%m-%d')}*",
        parse_mode="Markdown",
    )
    context.bot.send_photo(
        chat_id=CHAT_ID,
        photo=open(file_name, "rb"),
        caption="BTC Top / Bottom Indicators",
    )

    file_name = _generate_file_for_type(f"btc_ex", get_btc_ex_activity, 280, 220, 2.5)
    logger.info("Sending the file via Bot.")
    context.bot.send_photo(
        chat_id=CHAT_ID,
        photo=open(file_name, "rb"),
        caption=f"BTC On-Chain Exchange Activity",
    )


def callback_timer_set(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    logger.info(f"Chat ID: {chat_id}")
    context.job_queue.run_daily(
        callback,
        time(hour=4, minute=30, tzinfo=timezone("UTC")),
        context=chat_id,
        name=str(chat_id),
    )
    update.message.reply_text(f"Ok all set bruh.")


def callback_timer_unset(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    job_removed = _remove_job_if_exists(str(chat_id), context)
    text = (
        "Timer successfully cancelled!" if job_removed else "You have no active timer."
    )
    update.message.reply_text(text)


def _remove_job_if_exists(name: str, context: CallbackContext) -> bool:
    """Remove job with given name. Returns whether job was removed."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


def ping(_: Update, context: CallbackContext):
    """Just a ping"""
    context.bot.send_message(chat_id=CHAT_ID, text="Test")


def error(update: Update, context: CallbackContext):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main() -> None:
    """Start the bot."""
    # Create the Updater
    updater = Updater(TELEGRAM_TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("sopr", sopr_command))
    dispatcher.add_handler(CommandHandler("glossary", glossary_command))
    dispatcher.add_handler(CommandHandler("btc", btc_key_command))
    dispatcher.add_handler(CommandHandler("btc_ex", btc_ex_command))
    dispatcher.add_handler(CommandHandler("eth_ex", eth_ex_command))
    dispatcher.add_handler(
        MessageHandler(Filters.text & ~Filters.command, echo_command)
    )

    # Internal commands
    dispatcher.add_handler(CommandHandler("ping", ping))
    dispatcher.add_handler(CommandHandler("schedule", callback_timer_set))
    dispatcher.add_handler(CommandHandler("unschedule", callback_timer_unset))
    dispatcher.add_handler(CommandHandler("purge", remove_cache_command))

    # log all errors
    dispatcher.add_error_handler(error)

    # Start the Bot
    if sys.platform == "darwin":
        updater.start_polling()
    else:
        # Ref: https://github.com/python-telegram-bot/python-telegram-bot/wiki/Webhooks
        # Ref: https://github.com/liuhh02/python-telegram-bot-heroku
        # Ref: https://www.toptal.com/python/telegram-bot-tutorial-python
        updater.start_webhook(
            listen="0.0.0.0",
            port=int(PORT),
            url_path=TELEGRAM_TOKEN,
            webhook_url="https://shrouded-fjord-21568.herokuapp.com/" + TELEGRAM_TOKEN,
        )

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == "__main__":
    main()
