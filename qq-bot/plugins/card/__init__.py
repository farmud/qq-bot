from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="card",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)

# 奖励提示语
def get_coin_message(coins):
    if coins <= 20:
        return "印堂发黑呢，摸摸。"
    elif coins <= 40:
        return "一般般啦。"
    elif coins <= 60:
        return "普通的一天诶。"
    elif coins <= 80:
        return "运气不错呢。"
    else:
        return "你是轻小说的主角嘛？！"
    

from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, Event
from .models import Session, User
from datetime import datetime, timedelta
import random

update_coins = on_command("jrrp")

def is_same_day(dt1: datetime, dt2: datetime) -> bool:
    return dt1.date() == dt2.date()


@update_coins.handle()
async def handle_update_coins(bot: Bot, event: Event):
    import hashlib
    user_id = event.get_user_id()
    user_info = await bot.get_group_member_info(group_id=event.group_id, user_id=user_id)
    user_name = user_info["card"]

    today = datetime.now().strftime('%Y%m%d')
    combined = f"{user_id}{today}"
    random.seed(combined)
    # 计算 SHA-256 哈希值
    hash_object = hashlib.sha256(combined.encode())
    hash_hex = hash_object.hexdigest()

# 将哈希值转换为整数，并取模 2 得到 0 或 1
    idx = int(hash_hex, 16) % 2
    if idx == 1:
        coins_to_add = int(random.normalvariate(75, 15))
        if coins_to_add < 50:
            coins_to_add = 50
    else:
        coins_to_add = int(random.normalvariate(25, 15))
        if coins_to_add > 50:
            coins_to_add = 50

    session = Session()
    user = session.query(User).filter_by(user_id=user_id).first()
    
    now = datetime.now()
    if user:
        if is_same_day(now, user.last_update):
            session.close()
            await update_coins.finish(f"{user_name}今天的人品值是：{coins_to_add} \n{get_coin_message(coins_to_add)}")
        else:
            user.coins += coins_to_add
            user.last_update = now
    else:
        new_user = User(user_id=user_id, coins=coins_to_add, last_update=now)
        session.add(new_user)
    session.commit()
    session.close()
    await update_coins.finish(f"{user_name}今天的人品值是：{coins_to_add} \n{get_coin_message(coins_to_add)}\n获得了{coins_to_add}个硬币。")

check_coins = on_command("coin")

@check_coins.handle()
async def handle_check_coins(bot: Bot, event: Event):
    user_id = event.get_user_id()
    user_info = await bot.get_group_member_info(group_id=event.group_id, user_id=user_id)
    user_name = user_info["card"]
    session = Session()
    user = session.query(User).filter_by(user_id=user_id).first()
    if user:
        coins = user.coins
        last_update = user.last_update
        session.close()
        await check_coins.finish(f"{user_name} 当前有{coins}个硬币。\n上次更新时间：{last_update.strftime('%Y-%m-%d %H:%M:%S')}")
    else:
        session.close()
        await check_coins.finish(f"{user_name} 还未记录硬币")