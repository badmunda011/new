from telethon.utils import pack_bot_file_id

from userbot import Config, legend

from ..core.logger import logging

LOGS = logging.getLogger(__name__)

menu_category = "bot"
botusername = Config.BOT_USERNAME


@legend.bot_cmd(
    pattern=f"^/id$",
    incoming=True,
    func=lambda e: e.is_group,
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
                return await event.reply(
                    f"The id of the user `{input_str}` is `{p.id}`"
                )
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
                f"❇ **Current Chat ID : **`{event.chat_id}`\n❇ **From User ID: **`{r_msg.sender_id}`\n**Media File ID: **`{bot_api_file_id}`",
            )

        else:
            await event.reply(
                f"**Current Chat ID : **`{event.chat_id}`\n**From User ID: **`{r_msg.sender_id}`",
            )

    else:
        await even.reply(f"**Current Chat ID : **`{event.chat_id}`")
