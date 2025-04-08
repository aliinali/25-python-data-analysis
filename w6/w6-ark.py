import base64
import os
import sys
# 通过 pip install volcengine-python-sdk 安装SDK
from volcenginesdkarkruntime import Ark

#test
script_name = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(script_name,'test.jpg')


# 初始化一个Client对象，从环境变量中获取API Key
client = Ark(api_key = os.environ.get("ARK_API_KEY"))


# 定义方法将指定图片转为Base64编码
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

# 需要传给大模型的图片
#image_path = sys.argv[1]


def print_response(image_path):
    # 将图片转为Base64编码
    base64_image = encode_image(image_path)
    response = client.chat.completions.create(
        # 替换 <Model> 为模型的Model ID
        model = "doubao-1-5-vision-pro-32k-250115",
        messages = [
        {
            "role": "user",
            "content": [
            {
            "type": "text",
            "text": "识别图片中的文字。", #通过文本promot明确图片分析的任务
            },
            {
            "type": "image_url",
            "image_url": {
            #需要注意：传入Base64编码前需要增加前缀 data:image/{图片格式};base64,{Base64编码}：
            # PNG图片："url":  f"data:image/png;base64,{base64_image}"
            # JEPG图片：
            "url":  f"data:image/jpeg;base64,{base64_image}"
            # WEBP图片："url":  f"data:image/webp;base64,{base64_image}"
            #  "url":  f"data:image/<IMAGE_FORMAT>;base64,{base64_image}"
            },
            },
            ],
        }
        ],
        )
    print(response.choices[0].message.content)

#test
#print_response(image_path)
