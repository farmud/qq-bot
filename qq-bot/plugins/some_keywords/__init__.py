from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="some_keywords",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)
import random
import os
from . import tools
from nonebot import on_command, on_message, get_bot
from nonebot.adapters import Message
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import MessageSegment, Event, MessageEvent
from pathlib import Path

add_keyword = on_command("add_keyword")
add_alias = on_command("add_alias")
add_text = on_command("add_text")
add_picture = on_command("add_picture")
keyword_list = on_command("keyword_list")

# 加载关键词进入内存函数
def refresh_keyword_list():
    global list
    list = []
    with open("qq-bot/plugins/some_keywords/keyword_list.txt", "r+", encoding="utf-8") as f:
        for line in f:
            keyword = line.strip()  # 去除每行末尾的换行符和空格
            if keyword:  # 确保不添加空行
                list.append(keyword)

# 加载别名-关键词映射进入内存函数
def refresh_alias_map():
    global alias_map
    alias_map = {}
    for keyword in list:
        with open(f"qq-bot/plugins/some_keywords/contents/{keyword}/alias.txt", "r", encoding="utf-8") as f:
            for line in f:
                alias = line.strip()
                if alias:
                    alias_map[alias] = keyword

# 创建关键词
@add_keyword.handle()
async def handle_function(args: Message = CommandArg()):
    if key := args.extract_plain_text():
        if key in list:
            await add_keyword.finish(f'{key}已存在！')
        else:
            list.append(key)
            with open("qq-bot/plugins/some_keywords/keyword_list.txt", "a+", encoding="utf-8") as f:
                f.write(key + "\n")
            os.mkdir(f"qq-bot/plugins/some_keywords/contents/{key}")
            os.mkdir(f"qq-bot/plugins/some_keywords/contents/{key}/picture")
            with open(f"qq-bot/plugins/some_keywords/contents/{key}/text.txt", "w", encoding="utf-8") as f:
                pass
            with open(f"qq-bot/plugins/some_keywords/contents/{key}/alias.txt", "w", encoding="utf-8") as f:
                f.write(key + "\n")
            refresh_keyword_list()
            refresh_alias_map()
            await add_keyword.finish(f'{key}添加成功！')
    else:
        await add_keyword.finish('关键词只能为纯文本，请检查后重新输入！')

# 为关键词添加别名
@add_alias.handle()
async def handle_function(args: Message = CommandArg()):
    args_list = args.extract_plain_text().strip().split()
    if len(args_list) < 2:
        await add_alias.finish('请提供两个参数，以空格分隔:（关键词 别名）')
    key = args_list[0]
    alias = args_list[1]
    if key not in list:
        await add_alias.finish(f'{key}不存在！')
    with open(f"qq-bot/plugins/some_keywords/contents/{key}/alias.txt", "a+", encoding="utf-8") as f:
        f.write(alias + "\n")
    refresh_alias_map()
    await add_alias.finish(f'{alias}添加成功！')

# 为关键词添加文本
@add_text.handle()
async def handle_function(args: Message = CommandArg()):
    args_list = args.extract_plain_text().strip().split(' ')
    if len(args_list) < 2:
        await add_alias.finish('请提供两个参数，以空格分隔:（关键词 文本）')
    key = args_list[0]
    text_list = args_list[1:]
    text = ""
    for s in text_list:
        text += s + ' '
    if key not in list:
        await add_alias.finish(f'{key}不存在！')
    with open(f"qq-bot/plugins/some_keywords/contents/{key}/text.txt", "a", encoding="utf-8") as f:
        f.write(text + "\n")
    await add_alias.finish(f'{text}添加成功！')

# 为关键词添加图片
@add_picture.handle()
async def handle_function(args: Message = CommandArg()):
    text = ""
    img_url = ""
    for seg in args:
        if seg.type == "text":
            text = seg.data["text"].strip()
        elif seg.type == "image":
            img_url = seg.data["url"]
    # 检查参数是否完整
    if not text or not img_url:
        await add_keyword.finish("请提供文本和图片，例如：/add_keyword 关键词 [图片]")
    # 检查关键词是否存在
    if text not in list:
        await add_keyword.finish(f'{text}不存在！')
    # 创建以关键词命名的目录
    save_dir = Path(f"qq-bot/plugins/some_keywords/contents/{text}/picture")
    # 下载并保存图片
    import httpx
    async with httpx.AsyncClient() as client:
        resp = await client.get(img_url)
        if resp.status_code == 200:
            # 保存图片，使用时间戳避免重名
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            img_path = save_dir / f"{timestamp}.jpg"
            img_path.write_bytes(resp.content)
            await add_keyword.finish(f"成功保存图片")
        else:
            await add_keyword.finish("图片下载失败")
            
# 响应关键词
matcher = on_message()
@matcher.handle()
async def handle_function(event: MessageEvent):
    command_msg = event.get_plaintext()
    if keyword := word_in_map(command_msg, alias_map):
        # keyword = alias_map[command_msg]
        # 将所有文本信息加载进内存
        text_list = []
        with open(f"qq-bot/plugins/some_keywords/contents/{keyword}/text.txt", "r") as f: 
            for line in f:
                res = line.strip()  # 去除每行末尾的换行符和空格
                if res:  # 确保不添加空行
                    text_list.append(res)
        # 文本条数
        text_num = len(text_list)
        # 统计图片张数
        picture_num = len(os.listdir(f"qq-bot/plugins/some_keywords/contents/{keyword}/picture"))
        if text_num + picture_num < 1:
            await matcher.finish("当前还未对该关键词设置相应内容！")
        random_int = random.randint(1, text_num + picture_num)
        text_return = random_int <= text_num 
        # 返回内容为纯文本
        if text_return:
            await matcher.finish(text_list[random_int - 1])
        else:
            picture_dir = f"qq-bot/plugins/some_keywords/contents/{keyword}/picture"
            picture_list = os.listdir(picture_dir)
            picture_path = picture_dir + "/" + picture_list[random_int - text_num - 1]
            print(picture_path)
            await matcher.finish(tools.get_picture_by_url(picture_path))

def word_in_map(msg, map):
    for key in map:
        if key in msg:
            return map[key]
    return None

# 显示所有关键词
@keyword_list.handle()
async def handle_function():
    str = "当前已添加的关键词有：\n"
    for keyword in list:
        str += keyword + "\n"
    await keyword_list.finish(str)
# ================================== init ====================================
# 初始化关键词列表
list = []
refresh_keyword_list()
# 初始化别名-关键词映射
alias_map = {}
refresh_alias_map()
# ================================ end init ==================================
