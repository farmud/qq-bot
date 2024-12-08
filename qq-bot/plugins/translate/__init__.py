from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="translate",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)

from nonebot import on_command
import requests
from nonebot.adapters import Message
from nonebot.params import CommandArg
translate = on_command("翻译")
url = "https://api.52vmy.cn/api/query/fanyi?msg="


@translate.handle()
async def handle_function(args: Message = CommandArg()):

    def data_string_process(response):
            if response['code'] != 200:
                return "获取失败，请重试"
            str_data = response['data']['target']
            return "翻译结果为:\n" + str_data
    
    if question := args.extract_plain_text():
        response = requests.get(url + question).json()
        await translate.finish(data_string_process(response))
    else:
         await translate.finish("当前无法识别您的问题")

