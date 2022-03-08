import asyncio
import base64
import os
import time
from subprocess import PIPE
from subprocess import run as runapp

from userbot import legend

from ..Config import Config
from ..core.managers import eod, eor
from ..helpers import progress
from ..helpers.tools import media_type

menu_category = "tools"


@legend.legend_cmd(
    pattern="hash ([\s\S]*)",
    command=("hash", menu_category),
    info={
        "header": "Find the md5, sha1, sha256, sha512 of the string when written into a txt file.",
        "usage": "{tr}hash <text>",
        "examples": "{tr}hash LegendUserBot",
    },
)
async def gethash(hash_q):
    "Find the md5, sha1, sha256, sha512 of the string when written into a txt file."
    hashtxt_ = "".join(hash_q.text.split(maxsplit=1)[1:])
    with open("hashdis.txt", "w+") as hashtxt:
        hashtxt.write(hashtxt_)
    md5 = runapp(["md5sum", "hashdis.txt"], stdout=PIPE)
    md5 = md5.stdout.decode()
    sha1 = runapp(["sha1sum", "hashdis.txt"], stdout=PIPE)
    sha1 = sha1.stdout.decode()
    sha256 = runapp(["sha256sum", "hashdis.txt"], stdout=PIPE)
    sha256 = sha256.stdout.decode()
    sha512 = runapp(["sha512sum", "hashdis.txt"], stdout=PIPE)
    runapp(["rm", "hashdis.txt"], stdout=PIPE)
    sha512 = sha512.stdout.decode()
    ans = f"**Text : **\
            \n`{hashtxt_}`\
            \n**MD5 : **`\
            \n`{md5}`\
            \n**SHA1 : **`\
            \n`{sha1}`\
            \n**SHA256 : **`\
            \n`{sha256}`\
            \n**SHA512 : **`\
            \n`{sha512[:-1]}`\
         "
    await eor(hash_q, ans)


@legend.legend_cmd(
    pattern="base (en|de)(?:\s|$)([\s\S]*)",
    command=("base", menu_category),
    info={
        "header": "Find the base64 encoding or decoding of the given string.",
        "flags": {
            "en": "Use this to encode the given text.",
            "de": "use this to decode the given text.",
        },
        "usage": ["{tr}base en <text to encode>", "{tr}base de <encoded text>"],
        "examples": ["{tr}base en Legenduserbot", "{tr}base de TGVnZW5kQm90"],
    },
)
async def endecrypt(event):
    "To encode or decode the string using base64"
    reply_msg = await event.get_reply_message()
    mediatype = media_type(reply_msg)
    type = event.text[5:7]
    if reply_msg:
        tol = reply_msg.text
        reply_msg.media
    else:
        tol = event.text[7:]
    if tol == "":
        return await eod(event, "I need something to encode")
    if type == "en":
        if tol:
            result = base64.b64encode(bytes(tol, "utf-8")).decode("utf-8")
            results = f"**Encoded : **\n\n`{result}`"
            await eor(event, results)
        elif mediatype is None:
            result = base64.b64encode(bytes(reply_msg.message, "utf-8")).decode("utf-8")
            results = f"**Encoded : **\n\n`{result}`"
        else:
            legendevent = await eor(event, "`Encoding ...`")
            c_time = time.time()
            downloaded_file_name = await event.client.download_media(
                reply_msg,
                Config.TMP_DOWNLOAD_DIRECTORY,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, legendevent, c_time, "trying to download")
                ),
            )
            legendevent = await eor(event, "`Encoding ...`")
            with open(downloaded_file_name, "rb") as image_file:
                results = base64.b64encode(image_file.read()).decode("utf-8")
            os.remove(downloaded_file_name)
        await eor(
            legendevent, results, file_name="encodedfile.txt", caption="It's Encoded"
        )
    elif type == "de":
        try:
            lething = str(base64.b64decode(bytes(tol, "utf-8"), validate=True))[2:]
            await eor(event, "**Decoded  :**\n\n`" + lething[:-1] + "`")
        except Exception as e:
            await eod(event, f"**Error:**\n__{e}__")
