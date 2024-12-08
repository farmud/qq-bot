# 根据图片路径返回MessageSegment对象
def get_picture_by_url(str):
    import base64
    from nonebot.adapters.onebot.v11 import MessageSegment
    # 通过路径读取图片
    with open(str, 'rb') as img_file:
        img_base64 = base64.b64encode(img_file.read()).decode('utf-8')
        return MessageSegment.image(f"base64://{img_base64}")
    
# 判断是否为图片
def is_image(str):
    if(str.endswith("jpg") or str.endswith("png")):
        return True
    return False