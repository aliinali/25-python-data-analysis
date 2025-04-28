from volcenginesdkarkruntime import Ark
ark_model = 'doubao-1-5-vision-pro-32k-250115'
key = '今天晚上吃什么'

client = Ark(api_key = key)

def response_des(image_format, base64_image):
    response = client.chat.completions.create(
    # 模型的Model ID
        model = ark_model,
        messages = [
            {
                "role": "user",
                "content": [
                {
                    "type": "text",
                    "text": "请详细地描述图片内容。"      
                },
        {
          "type": "image_url",
          "image_url": {
          "url":  f"data:image/{image_format};base64,{base64_image}"
          },
        },
      ],
    }
  ],
)
    return response
    

def response_find_face(image_format, base64_image):
    response = client.chat.completions.create(
    # 模型的Model ID
        model = ark_model,
        messages = [
            {
                "role": "user",
                "content": [
                {
                    "type": "text",
                    "text":'''请找出图中所有人脸的位置，并以如下格式返回坐标列表：
[
  {"x1": ..., "y1": ..., "x2": ..., "y2": ...},
  ...
]'''      
                },
        {
          "type": "image_url",
          "image_url": {
          "url":  f"data:image/{image_format};base64,{base64_image}"
          },
        },
      ],
    }
  ],
)
    return response
