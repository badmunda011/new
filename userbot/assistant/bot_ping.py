import io
import re
from collections import defaultdict
from datetime import datetime
from typing import Optional, Union
import os

from telethon import Button, events
from telethon import Button, events
from telethon.errors import UserIsBlockedError
from telethon.events import CallbackQuery, StopPropagation
from telethon.utils import get_display_name

from userbot import Config, legend

from ..core import check_owner, pool
from ..core.logger import logging
from ..core.session import tgbot
from ..helpers import reply_id
from ..helpers.utils import _format
from ..sql_helper.bot_blacklists import check_is_black_list
from ..sql_helper.bot_pms_sql import (
    add_user_to_db,
    get_user_id,
    get_user_logging,
    get_user_reply,
)
from ..sql_helper.bot_starters import add_starter_to_db, get_starter_details
from ..sql_helper.globals import delgvar, gvarstatus
from ..sql_helper.idaddar import get_all_users
from . import BOTLOG, BOTLOG_CHATID
from .botmanagers import ban_user_from_bot

LOGS = logging.getLogger(__name__)

menu_category = "bot"
botusername = Config.BOT_USERNAME

@legend.bot_cmd(
    pattern=f"^/start({botusername})?([\s]+)?$",
    incoming=True,
)
async def bot_start(event):
    chat = await event.get_chat()
    user = await legend.get_me()
    if check_is_black_list(chat.id):
        return
    LEGEND_IMG = gvarstatus("BOT_PING_PIC", "https://telegra.ph/file/a9f6a3c160977352dd595.jpg")
    start = datetime.now()
    await event.client.send_file(event.chat_id, LEGEND_IMG, caption="Checking LegendBot Ping...", buttons=GOOD)
    end = datetime.now()
    GOOD = [[Button.url("⚜ Lêɠêɳ̃dẞø† ⚜", "https://t.me/LegendBot_XD")]]
    ms = (end - start).microseconds / 1000
    LegendBoy = f"**꧁•⊹٭Ping٭⊹•꧂**\n\n   ⚜ {ms}\n   ⚜ ❝𝐌𝐲 𝐌𝐚𝐬𝐭𝐞𝐫❞ ~『{mention}』"
    await event.client.edit_message(event.chat_id, LEGEND_IMG, caption=LegendBoy, buttons=GOOD)
