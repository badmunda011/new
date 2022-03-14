from userbot import legend

from ..core.managers import eor

menu_category = "useless"


@legend.legend_cmd(
    pattern="row(?: |$)([\s\S]*)",
    command=("row", menu_category),
    info={
        "header": "...",
        "note": "..",
        "usage": [
            "{tr}trt <row> ; <button>",
        ],
    },
)
async def button(event):
    input_str = event.pattern_match.group(1)
    a = (await event.get_reply_message()).reply_markup
    if a:
        if ";" in input_str:
            olo, text = input_str.split(";")
        else:
            await eor(event, "Check Syntax Of this cmd")
        b = f"a.rows[{olo}].buttons[{text}].text"
        c = f"a.rows[{olo}].buttons[{text}].url"
        sweetie = f"**Text** : {b}\n**URL** :{c}"
        await eor(event, sweetie)
    else:
        await eor(event, "Check information of this cmd")
