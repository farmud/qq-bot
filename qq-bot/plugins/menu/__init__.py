from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata

from .config import Config

from nonebot import on_command
__plugin_meta__ = PluginMetadata(
    name="menu",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)

menu_request = on_command("菜单")
menu = []
menu.append("bot功能及用法如下：")
menu.append("====================")
menu.append("1. AI聊天\t\t/chat 问题")
menu.append("2. 塔罗牌\t\t/draw")
menu.append("3. 翻译\t\t/翻译 + 需要翻译的内容")
menu.append("4. 为目标生成二维码\t\t/QR内容")
menu.append("5. 疯狂星期四文案\t\t/星期四")
menu.append("6. 算卦\t\t/算卦")
menu.append("7. 今日人品\t\t/jrrp")
menu.append("8. 查看硬币数量\t\t/coin")
menu.append("9. 今天吃什么：")
menu.append("\t\t·添加食物\t\t/吃 + 食物")
menu.append("\t\t·查看列表\t\t/list_food")
menu.append("\t\t·删除食物\t\t/不吃 + 食物")
menu.append("10. 自定义相应")
menu.append("\t\t·添加关键词\t\t/add_keyword + 关键词")
menu.append("\t\t·为关键词添加别名\t\t/add_alias 关键词 别名")
menu.append("\t\t·为关键词添加响应文本\t\t/add_text 关键词 文本")
menu.append("\t\t·为关键词添加响应图片\t\t/add_picture 关键词 图片")
menu.append("\t\t·显示所有自定义关键词\t\t/keyword_list")



@menu_request.handle()
async def handle_function():
    str = ""
    for i in menu:
        str += i + "\n"
    # 去除最后一个换行符
    await menu_request.finish(str[:-1])


