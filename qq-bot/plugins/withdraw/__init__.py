from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="withdraw",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)


from nonebot import on_notice
from nonebot.adapters.onebot.v11 import GroupRecallNoticeEvent, MessageSegment, Event
from nonebot.rule import is_type, to_me


withdraw = on_notice(rule = is_type(GroupRecallNoticeEvent))
@withdraw.handle()
async def handle_function(e : Event):
    await withdraw.finish(MessageSegment.at(e.user_id) + "？啊你刚刚说啥？")


# 测试艾特功能
from nonebot import on_message, on_keyword
from nonebot.rule import keyword
keywords_rule = keyword("test")
tome_test = on_message(rule = (to_me() & keywords_rule))
@tome_test.handle()
async def handle_function(e : Event):
    await tome_test.finish('咋了？有事看 ‘/菜单’！')