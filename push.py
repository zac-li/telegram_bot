import logging
from datetime import date

from telegram import Bot

from constants import TELEGRAM_TOKEN, CHAT_ID, DIGEST
from telegram_bot import _generate_file_for_type
from glassnode import get_btc_ex_activity, get_btc_key_stats

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)


bot = Bot(token=TELEGRAM_TOKEN)

logger.info("Starting daily push.")

file_name = _generate_file_for_type("btc", get_btc_key_stats, 280, 220, 2.5)
bot.send_message(
    chat_id=CHAT_ID,
    text=DIGEST.format(time=date.today().strftime("%Y-%m-%d")),
    parse_mode="Markdown",
    disable_web_page_preview=True,
)
bot.send_photo(
    chat_id=CHAT_ID,
    photo=open(file_name, "rb"),
    caption="BTC Top / Bottom Indicators",
)

file_name = _generate_file_for_type(f"btc_ex", get_btc_ex_activity, 280, 220, 2.5)
logger.info("Sending the file via Bot.")
bot.send_photo(
    chat_id=CHAT_ID,
    photo=open(file_name, "rb"),
    caption=f"BTC On-Chain Exchange Activity",
)
