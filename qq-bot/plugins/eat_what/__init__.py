from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="eat_what",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)

from nonebot import on_command
from nonebot import on_endswith
from nonebot.adapters import Message
from nonebot.params import CommandArg

add_menu = on_command("吃")
eat = on_endswith({"吃什么", "吃啥"})
menu_list = on_command("list_food")
del_menu = on_command("不吃")

# 添加午饭
@add_menu.handle()
async def handle_function(args: Message = CommandArg()):
    if question := args.extract_plain_text():
        with open("qq-bot/plugins/eat_what/eat_menu.txt", "r+") as f:
                list = f.readlines()
                if question + "\n" not in list:
                    f.write(question + "\n")
                    await add_menu.finish(f"{question} 添加成功!")
                else:
                    await add_menu.finish(f"{question} 已经存在!")
    # 否则
    await add_menu.finish("添加失败!")

# 吃什么
@eat.handle()
async def handle_function():
    # 监测当前时间，决定吃午饭还是晚饭
    import datetime
    now = datetime.datetime.now()

    if now.hour < 10:
        await eat.finish("现在还不到吃饭时间捏")
    with open("qq-bot/plugins/eat_what/eat_menu.txt", "r") as f:
        lunch_list = f.readlines()
        if now.hour < 9:
            await eat.finish("现在还不到吃饭时间捏")
        curr_time_str = "午饭" if now.hour < 14 else "晚饭"
    if lunch_list:
        import random
        # 列表中随机选3个
        offer_list = random.sample(lunch_list, 3)
        await eat.finish(f'提议{curr_time_str}吃{offer_list[0][:-1]}, {offer_list[1][:-1]} 或者 {offer_list[2][:-1]}')

# 查看列表
@menu_list.handle()
async def handle_function():
    with open("qq-bot/plugins/eat_what/eat_menu.txt", "r") as f:
        list = f.readlines()
    if list:
        await menu_list.finish(("列表如下：\n" + "".join(list))[:-1])
    else:
        await menu_list.finish("列表为空")

# 删除
@del_menu.handle()
async def handle_function(args: Message = CommandArg()):
    if question := args.extract_plain_text():
        with open("qq-bot/plugins/eat_what/eat_menu.txt", "r") as f:
            list = f.readlines()
        if question + "\n" in list:
            list.remove(question + "\n")
            with open("qq-bot/plugins/eat_what/eat_menu.txt", "w") as f:
                f.writelines(list)
            await del_menu.finish(f"{question} 删除成功!")
        else:
            await del_menu.finish(f"列表中没有{question}")
    else:
        await del_menu.finish("删除失败!")

