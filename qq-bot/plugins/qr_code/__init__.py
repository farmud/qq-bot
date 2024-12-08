from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="QR_code",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)

url = "https://api.chenyande.cn/api/qrcode/?text="

from nonebot import on_command
import requests
from nonebot.adapters import Message
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import MessageSegment

qr_code = on_command("QR",aliases={"二维码"})

@qr_code.handle()
async def handle_function(args: Message = CommandArg()):
    if parm := args.extract_plain_text():
        response = requests.get(url + parm)
        # 返回的类型是.png图片
        if response.status_code == 200:
            await qr_code.finish(MessageSegment.image(response.content))
        else:
            await qr_code.finish("生成二维码失败，请稍后再试。")
