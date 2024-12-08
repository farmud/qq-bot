from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="draw",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)

from nonebot import on_command
from .draw import handle_tarot_command
from nonebot.adapters.onebot.v11 import Bot, Event

draw = on_command("draw")

@draw.handle()
async def handle_function(bot: Bot, event: Event):
    user_id = event.get_user_id()
    nick_name = (await bot.get_group_member_info(group_id=event.group_id, user_id=user_id))["card"]
    result = nick_name + handle_tarot_command(user_id)
    # 去除最后一行空行
    
    await draw.finish(result.rstrip())

