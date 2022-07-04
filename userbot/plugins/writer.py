import os

from PIL import Image, ImageDraw, ImageFont

from ..helpers.tools import async_searcher, text_set
from . import legend

menu_category = "extra"


@legend.legend_cmd(
    pattern="gethtml(?:\s|$)([\s\S]*)",
    command=("gethtml", menu_category),
    info={
        "header": "text or reply to html or any doc file",
        "usage": "{tr}gethtml",
    },
)
async def ghtml(e):
    txt = e.pattern_match.group(1).strip()
    if txt:
        link = e.text.split(maxsplit=1)[1]
    else:
        return await eod(e, "`Either reply to any file or give any text`")
    k = await async_searcher(link)
    with open("file.html", "w+") as f:
        f.write(k)
    await e.reply(file="file.html")


@legend.legend_cmd(
    pattern="note(?:\s|$)([\s\S]*)",
    command=("note", menu_category),
    info={
        "header": "It will write on a paper.",
        "usage": "{tr}note",
    },
)
async def note(e):
    lol = e.text
    if e.reply_to_msg_id:
        reply = await e.get_reply_message()
        text = reply.message
    elif lol:
        text = lol[5:]
    else:
        return await eod(e, "Give me Text")
    k = await eor(e, "Processing")
    img = Image.open("userbot/resources/extras/template.jpg")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("userbot/resources/fonts/assfont.ttf", 30)
    x, y = 150, 140
    lines = text_set(text)
    line_height = font.getsize("hg")[1]
    for line in lines:
        draw.text((x, y), line, fill=(1, 22, 55), font=font)
        y = y + line_height - 5
    file = "legend.jpg"
    img.save(file)
    await e.reply(file=file)
    os.remove(file)
    await k.delete()
