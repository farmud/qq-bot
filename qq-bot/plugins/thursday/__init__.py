from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="thursday",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)

url = "https://tools.mgtv100.com/external/v1/pear/kfc"

from nonebot import on_command
import requests
thursday = on_command("星期四",aliases={"周四", "疯狂星期四"})

@thursday.handle()
async def handle_function():
    def data_string_process(response):
        if response['code'] == 200:
            str_data = response['data']
            return str_data.replace('\\n', '\n')
        else:
            return "获取失败，请重试"
    response = requests.get(url).json()
    await thursday.finish(data_string_process(response))
    
