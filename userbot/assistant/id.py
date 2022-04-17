from telethon.utils import pack_bot_file_id

import io
import re
from collections import defaultdict
from datetime import datetime
from typing import Optional, Union

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
    pattern=f"^/id({botusername})?([\s]+)?$",
    incoming=True,
)
async def bot_start(event):
    "To get id of the group or user."
    input_str = event.pattern_match.group(1)
    if input_str:
        try:
            p = await event.client.get_entity(input_str)
        except Exception as e:
            return await event.reply(f"`{e}`", 5)
        try:
            if p.first_name:
                return await event.reply(f"The id of the user `{input_str}` is `{p.id}`")
        except Exception:
            try:
                if p.title:
                    return await event.reply(
                        f"The id of the chat/channel `{p.title}` is `{p.id}`"
                    )
            except Exception as e:
                LOGS.info(str(e))
        await event.reply("`Either give input as username or reply to user`")
    elif event.reply_to_msg_id:
        r_msg = await event.get_reply_message()
        if r_msg.media:
            bot_api_file_id = pack_bot_file_id(r_msg.media)
            await event.reply(
                f"**Current Chat ID : **`{event.chat_id}`\n**From User ID: **`{r_msg.sender_id}`\n**Media File ID: **`{bot_api_file_id}`",
            )

        else:
            await event.reply(
                f"**Current Chat ID : **`{event.chat_id}`\n**From User ID: **`{r_msg.sender_id}`",
            )

    else:
        await even.reply(f"**Current Chat ID : **`{event.chat_id}`")
