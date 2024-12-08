from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="constellation",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)

from nonebot import on_command
from nonebot.rule import to_me
from nonebot.adapters import Message
from nonebot.params import CommandArg
import requests
constellation = on_command("星座")
prefix = "https://v.api.aa1.cn/api/xingzuo"

@constellation.handle()
async def handle_function(args: Message = CommandArg()):
    # 提取参数纯文本作为地名，并判断是否有效
    if parm := args.extract_plain_text():
        
        url = prefix + "/?msg=" + parm.rstrip("座")
        response = requests.get(url).json()
        if(response['code'] == 1):
            await constellation.finish(data_string_process(response))
        else:
            await constellation.finish("输入错误，请重新输入")
    else:
        await constellation.finish("输入错误，请重新输入")

def data_string_process(response):
    str = []
    str.append(f"星座 {response['xz']} 的查询结果为\n")
    str.append(f"贵人方位：{response['grfw']}\n")
    str.append(f"贵人星座：{response['grxz']}\n")
    str.append(f"幸运数字：{response['xysz']}\n")
    str.append(f"幸运颜色：{response['xyys']}\n")
    str.append(f"爱情运势：{response['aqys']}\n")
    str.append(f"财富运势：{response['cfys']}")
    str.append(f"事业运势：{response['syys']}\n")
    str.append(f"整体运势：{response['ztys']}\n")
    str.append(f"提示：{response['ts']}\n")
    res = ""
    for i in str:
        res += i
    return res