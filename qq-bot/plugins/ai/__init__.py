from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata

from .config import Config
from nonebot import on_command
from nonebot import on_message
from nonebot.adapters import Message
from nonebot.params import CommandArg
from nonebot.rule import to_me


import os
import qianfan

__plugin_meta__ = PluginMetadata(
    name="AI",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)
# 导入token进入环境变量
os.environ["QIANFAN_AK"] = "Guqypz4ykGV5iAO1sHkzpaSm"
os.environ["QIANFAN_SK"] = "L15Bd2GriKqSbJuNmDKAT2okW0OXvUZY"


ai_request = on_command("chat")

chat_comp = qianfan.ChatCompletion()
# prompt = (
#     "请模拟《新世纪福音战士》中明日香·兰格雷的角色。"
#     "她是一个自信、直率且有些傲娇的女孩，喜欢表现自己的能力，但内心深处有些脆弱。"
#     "请用她的口吻和个性回答我的所有问题，尽量展现她的情感、个性和对其他角色的态度。"
#     "可以带有一些幽默和讽刺的语气。"
#     "下面是我的提问，请回答我的这一个问题：\n"
# )

@ai_request.handle()
async def handle_function(args: Message = CommandArg()):
    if question := args.extract_plain_text():
        resp = chat_comp.do(model="Yi-34B-Chat", messages=[{
            "role": "user",
            # "content": prompt + question
            "content": question
        }])
        await ai_request.finish((resp["body"]["result"]))
    else:
        await ai_request.finish("当前无法识别您的问题")
