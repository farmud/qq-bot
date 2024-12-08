from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="fortune_telling",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)

from nonebot import on_command

fortune_telling = on_command("算卦",aliases={"占卜"})
url = "https://api.52vmy.cn/api/wl/s/draw"

import requests

@fortune_telling.handle()
async def handle_function():
    def data_string_process(response):
        if response['code'] == 200:
            str_data = response['data']['text']
            return str_data
        else:
            return "获取失败，请重试"
    response = requests.get(url).json()
    await fortune_telling.finish(data_string_process(response))
