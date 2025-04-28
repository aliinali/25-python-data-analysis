from PIL import Image, ImageDraw
import base64
import numpy as np
import os
from w9_model import key, response_des, response_find_face
from volcenginesdkarkruntime import Ark

client = Ark(api_key = key)

#可视化
def draw_box_on_image(image_path, boxs, outline_color="red", width=2):
    """
    在图片上画多个框。
    """
    image = Image.open(image_path).convert("RGB")
    draw = ImageDraw.Draw(image)
    for box in boxs:
        # 从字典中取出坐标
        x1, y1, x2, y2 = box["x1"], box["y1"], box["x2"], box["y2"]
    
        # 画矩形
        draw.rectangle([x1, y1, x2, y2], outline=outline_color, width=width)
    
    return image

class FaceDataLoader:
    def __init__(self,path):
        self._path = path   #图片目录的路径
        self.num = 0  #处理的图片在list中的index
        self.image_path = self._path + '\\'+ os.listdir(self._path)[self.num] #正在处理的图片路径(绝对路径)

    def image_generator(self):
        '''
        生成图片数据的ndarry并返回
        '''
        image = Image.open(self.image_path)
        return np.array(image)

    def __iter__(self):
        self.num = 0
        return self
    
    def __next__(self):
        '''
        以ndarry形式迭代返回图片数据
        '''
        if self.num >=  self.__len__():
            raise StopIteration
        else:
            self.image_path = self._path + '\\'+ os.listdir(self._path)[self.num]
            image_array = self.image_generator()
            self.num += 1
            return image_array
        
    def __len__(self):
        '''
        返回数据集图片数量
        '''
        return len(os.listdir(self._path))

    def __getitem__(self,index):
        '''
        实例函数 通过index返回ndarray
        '''
        self.num = index
        return self.image_generator()

    def image_caption_generator(self):
        '''
        图片描述
        '''
        self.num = 0 #重置
        while(self.num < 5): #测试前5张
        #把图片转为base64
            self.image_path = self._path + '\\'+ os.listdir(self._path)[self.num] #正在处理的图片路径(绝对路径)
            with open(self.image_path, 'rb') as i_f:
                b64_image = base64.b64encode(i_f.read()).decode('utf-8')
            response = response_des('jpg', b64_image)
            yield response.choices[0].message.content
            self.num += 1


    def face_box_generator(self):
        '''
        计算人脸坐标
        '''
        self.num = 0  #重置
        while(self.num < 5):  #测试前5张
            self.image_path = self._path + '\\'+ os.listdir(self._path)[self.num] #正在处理的图片路径(绝对路径)
            #转为base64
            with open(self.image_path, 'rb') as i_f:
                b64_image = base64.b64encode(i_f.read()).decode('utf-8')
            response = response_find_face('jpg',b64_image)
            yield response.choices[0].message.content
            self.num += 1


if __name__ == '__main__':
    path = r"F:\WIDER_test\images\4--Dancing"
    facedataloader = FaceDataLoader(path)
    print(len(facedataloader))

    image_info = facedataloader.image_caption_generator()
    image_face = facedataloader.face_box_generator()

    for image_array in facedataloader:
        print(image_array)

    for i in range(5):
        print(facedataloader[i])

    for info in image_info:
        print(info)

    i = 1
    for face in image_face:
        print(face)
        boxs = eval(face)
        draw_box_on_image(facedataloader.image_path, boxs).save(r"C:\Users\Huawei\Desktop\好一个大学\课内学习\大二下\ppppp数据分析\w9\result_imgs\{}.jpg".format(i))
        i += 1



    
        
