
from functools import wraps
import time
import datetime
import os

import cv2 as cv
import base64
import numpy as np

import sounddevice as sd
import soundfile as sf

from volcenginesdkarkruntime import Ark
from w8_my_model import KEY as API_KEY
from w8_my_model import MODEL as ARK_MODEL


class ImageHSV:
    def __init__(self, logfile='image_info.log'):
        self.logfile = logfile

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)  # 先调用原函数获取图像
            if result is not None and isinstance(result, np.ndarray) and len(result.shape) in [2, 3]:
                img = result
                # 计算图像大小
                height, width = img.shape[:2]
                # 转换图像为 hsv 格式，计算亮度和饱和度
                hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
                avg_s, avg_v = cv.mean(hsv)[1:3]
                info_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                info_size = f'图片大小:{height}*{width}'
                info_sv = f'图片亮度:{avg_v}  图片饱和度{avg_s}'
                with open(self.logfile, 'a') as log:
                    log.write(info_time + '\n')
                    log.write(info_size + '\n')
                    log.write(info_sv + '\n')
                    log.write('\n')
            return result
        return wrapper


def img_resizer(height=100, width=200):
    '''
    修改图片大小
    '''
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            img = func(*args, **kwargs)
            if img is not None:
                resized_img = cv.resize(img, (width, height))
                return resized_img
            return None
        return wrapper
    return decorator


class ImageAlter:
    def __init__(self, client, condition, intervals=60, logfile='image_info.log',
                 save_dir='caught_images'):
        self.client = client
        self.condition = condition
        self.intervals = intervals
        self.logfile = logfile
        self.save_dir = save_dir
        self.prompt = '如果' + condition + '则返回1，否则返回0'
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

    @ImageHSV()
    @img_resizer()
    def capture_single_frame(self):
        cap = cv.VideoCapture(0)
        if not cap.isOpened():
            print("无法打开摄像头")
            return None
        ret, frame = cap.read()
        if not ret:
            print("无法读取画面")
            cap.release()
            return None
        cv.imshow('Camera Feed', frame)
        cv.waitKey(1)
        _, buffer = cv.imencode('.jpg', frame)
        frame_base64 = base64.b64encode(buffer).decode('utf-8')
        cap.release()
        return frame

    def play_sound(self, filename):
        data, fs = sf.read(filename, dtype='float32')
        sd.play(data, fs)
        sd.wait()

    def get_cap_from_ark(self, image_base64, image_format, prompt):
        response = self.client.chat.completions.create(
            model=ARK_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"{prompt}"
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/{image_format};base64,{image_base64}"
                            },
                        },
                    ],
                }
            ],
        )
        return response.choices[0].message.content
        

    def start_monitoring(self, welcome_sound):
        while True:
            frame = self.capture_single_frame()
            if frame is None:
                continue
            _, buffer = cv.imencode('.jpg', frame)
            frame_base64 = base64.b64encode(buffer).decode('utf-8')
            result = self.get_cap_from_ark(frame_base64, 'jpg', self.prompt)
            if result == '1':
                print(f"检测到特殊情形: {self.condition}")
                self.play_sound(welcome_sound)
                timestamp = time.strftime("%Y%m%d-%H%M%S")
                save_path = os.path.join(self.save_dir, f"{timestamp}.jpg")
                cv.imwrite(save_path, frame)
                print(f"特殊情形图片已保存到: {save_path}")
            else:
                print("未检测到特殊情形")
            time.sleep(self.intervals)


if __name__ == "__main__":
    client = Ark(api_key=API_KEY)
    condition = input()
    intervals = 10
    welcome_sound = r'C:\Users\Huawei\Desktop\好一个大学\课内学习\大二下\ppppp数据分析\w8-代理模式与装饰器\qq.wav'
    image_alter = ImageAlter(client, condition, intervals)
    image_alter.start_monitoring(welcome_sound)
    
