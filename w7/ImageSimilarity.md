# 异常捕获与图片相似性计算
> PIL能够实现许多图片数据的底层表示和处理，比如在相素层面进行相关分析等，并支撑常用的图像检索任务。请围绕其相关功能，结合异常捕获和自定义异常，完成如下题目。



## 1. 异常捕获。
> 实现ImageQuery类的_create_and_image方法，其利用PIL.Image类的open方法打开并返回一个Image实例，但考虑到open方法可能产生FileNotFoundError或PIL.UnidentifiedImageError，请在该方法中对这两个异常进行捕获和处理（打印或记入日志，相关信息包括打开的文件路径和详细的异常描述）。
首先构建自定义Error
```python

class ImageQueryError(Exception):
    def __init__(self):
        pass

class ImageQueryShapeNotMatchError(ImageQueryError):
    def __init__(self,image1,image2):
        self.image1 = image1
        self.image2 = image2
        self.message = f'The sizes of images are not matched'
```
再实现ImageQuery类
```python

class ImageQuery:
    def __init__(self):
        pass

    def _create_an_image(self,image_path):
        try:
            image = Image.open(image_path)
        except FileNotFoundError:
            print(f'File Not Found:{image_path}')
        except UnidentifiedImageError:
            print(f'Unidentified Image:{image_path}')
        else:
            print('图片加载成功！')
            return image

```
***测试***
```python

if __name__ == '__main__':
    #三张测试图片路径
    image1_path = r'C:\Users\Huawei\Desktop\好一个大学\课内学习\大二下\ppppp数据分析\w7-异常处理与图片相似性\test_100.png'
    image2_path = r'C:\Users\Huawei\Desktop\好一个大学\课内学习\大二下\ppppp数据分析\w7-异常处理与图片相似性\test2_100.png'
    image3_path = r'C:\Users\Huawei\Desktop\好一个大学\课内学习\大二下\ppppp数据分析\w7-异常处理与图片相似性\test3_97.png'
```



## 2. 图片的相似性计算。
> 在ImageQuery类中实现一种简单图片相似性的计算方法pixel_difference，即直接对两个图片逐相素相减，并累积求和差异的绝对值，继而除以相素总数。注意该方法可能会抛出一个叫ImageQueryShapeNotMatchError的自定义异常，其继承了ImageQueryError（本次作业自定义的顶层异常类），即当比较相似性的两张图片形状（长宽）不一致性时。请在该方法中抛出该异常，包含两个图片的形状信息。



## 3. 图片的直方图相似性计算。
>在ImageQuery类中实现更多的相似性计算方法。具体地，利用PIL.Image类的histogram方法，获取图片相素的直方图，进而用scipy.states中的相关性计算方法来得到不同的相似性，如pearson，spearman，kendall等。这些方法并不要求图片形状一致。注意，这些相似性方法还能够返回显著性。



## 4. 图片的大模型嵌入。
> 在ImageQuery类中实现基于大模型的相似性计算方法，即利用相关API(具体见Demo ali_image_embed.py或者ark_image_embed.py)首先将图片嵌入为向量，继而通过向量的余弦相似度等给出相似性大小(cos_simi.py)。注意，选一个大模型实现即可，ali和字节均提供一定的免费token额度。
