from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="special_keywords",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)

from nonebot import on_keyword


# 废话
feihua = on_keyword({"废话", "龙王", "话多", "话好多"})
from nonebot.adapters.onebot.v11 import Bot, Event
@feihua.handle()
async def handle_function(bot: Bot, event: Event):
    str = await bot.get_group_honor_info(group_id=event.group_id, type="talkative")
    await feihua.finish("。。。今天废话最多的龙王是" + str['current_talkative']['nickname'] + "，别天天水群了= =!")


