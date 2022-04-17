import os
import re
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


import pygments
import requests
from pygments.formatters import ImageFormatter
from pygments.lexers import Python3Lexer
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.utils import get_extension
from urlextract import URLExtract

from userbot import legend

from ..Config import Config
from ..core.events import MessageEdited
from ..core.logger import logging
from ..core.managers import eod, eor
from ..helpers.tools import media_type
from ..helpers.utils import pastetext, reply_id



@legend.bot_cmd(
    pattern=f"^/paste({botusername})?([\s]+)?$",
    incoming=True,
)
async def pasta(event);
    reply = await event.get_reply_message()
    pastetype = "p"
    try:
        extension = ext[0].replace("-", "")
    except IndexError:
        extension = None
    if reply and reply.media:
        mediatype = media_type(reply)
        if mediatype == "Document":
            d_file_name = await event.client.download_media(reply, Config.TEMP_DIR)
            if extension is None:
                extension = get_extension(reply.document)
            with open(d_file_name, "r") as f:
                text_to_print = f.read()
    if extension and extension.startswith("."):
        extension = extension[1:]
    try:
        response = await pastetext(text_to_print, pastetype, extension)
        if "error" in response:
            return await event.reply(
                "**Error while pasting text:**\n`Unable to process your request may be pastebins are down.`",
            )

        result = ""
        if pastebins[response["bin"]] != pastetype:
            result += f"<b>{get_key(pastetype)} is down, So </b>"
        result += f"<b>Pasted to: <a href={response['url']}>{response['bin']}</a></b>"
        if response["raw"] != "":
            result += f"\n<b>Raw link: <a href={response['raw']}>Raw</a></b>"
        await event.reply(result, link_preview=False, parse_mode="html")
    except Exception as e:
        await event.reply(f"**Error while pasting text:**\n`{e}`")
