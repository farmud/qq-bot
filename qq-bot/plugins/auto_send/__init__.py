from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="auto_send",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)


from nonebot import on_message, require, get_bots
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Bot
from datetime import datetime, timedelta
import random
# 用于存储群最后消息时间的字典
group_last_message_time = {}

# 定义消息处理器
message_handler = on_message()

# 定义回复内容
reply_list = ["好冷清，我还以为我们永远有话说", "hlq,whywwmyyyhs",
              "你们说话啊，你们又在卷了？怎么突然不说话了？我好害怕，好怕你们又学到新东西了，看你们学到新知识比我亏钱都还要难受，本来学了一个月就觉得很幸福了，现在在这个群，每天被你们洗脑，让我觉得只要一秒钟不学习都是不行的，虽然现在每天都在学，但是这个群却给我无时无刻不在学习的感觉，我真的好累"]

@message_handler.handle()
async def _(event: GroupMessageEvent):
    # 更新群最后消息时间
    group_last_message_time[event.group_id] = datetime.now()

# 获取定时任务调度器
scheduler = require("nonebot_plugin_apscheduler").scheduler

# 定义定时任务
@scheduler.scheduled_job("interval", minutes=5)
async def check_group_activity():
    now = datetime.now()
    for bot in get_bots().values():
        # groups = await bot.get_group_list()
        # for group in groups:
        #     group_id = group["group_id"]
        group_id = 477641968
        last_time = group_last_message_time.get(group_id)
        if last_time and (now - last_time) > timedelta(hours=5) and (now.hour >= 10 and now.hour <= 24):
            try:
                await bot.send_group_msg(group_id=group_id, message=random.choice(reply_list))
                # 重置最后消息时间，避免重复发送
                group_last_message_time[group_id] = now
            except Exception as e:
                print(f"发送消息到群 {group_id} 失败: {e}")
