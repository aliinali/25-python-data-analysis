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

其中image1_path刻意改过
```python

if __name__ == '__main__':
    #三张测试图片路径
    image1_path = r'C:\Users\Huawei\Desktop\好一个大学\课内学习\大二下\ppppp数据分析\w7-异常处理与图片相似性\test_100.png'
    image2_path = r'C:\Users\Huawei\Desktop\好一个大学\课内学习\大二下\ppppp数据分析\w7-异常处理与图片相似性\test2_100.png'
    image3_path = r'C:\Users\Huawei\Desktop\好一个大学\课内学习\大二下\ppppp数据分析\w7-异常处理与图片相似性\test3_97.png'
```

***输出***
```python
File Not Found:C:\Users\Huawei\Desktop\好一个大学\课内学习\大二下\ppppp数据分析\w7-异常处理与图片相似性\test_100.png
图片加载成功！
图片加载成功！
```

## 2. 图片的相似性计算。
> 在ImageQuery类中实现一种简单图片相似性的计算方法pixel_difference，即直接对两个图片逐相素相减，并累积求和差异的绝对值，继而除以相素总数。注意该方法可能会抛出一个叫ImageQueryShapeNotMatchError的自定义异常，其继承了ImageQueryError（本次作业自定义的顶层异常类），即当比较相似性的两张图片形状（长宽）不一致性时。请在该方法中抛出该异常，包含两个图片的形状信息。

先检查图片size，大小不一致即捕获NotMatchedError。计算时将image转换为‘RGB’数值计算

```python
def pixel_difference(self,image1,image2):
        '''
        图片像素相似性计算
        '''
        if image1.size == image2.size:
            width,height = image2.size
            total_pixel_difference = 0
            image1 = image1.convert('RGB')
            image2 = image2.convert('RGB')
            for x in range(width):
                for y in range(height):
                    r1, g1, b1 = image1.getpixel((x,y))
                    r2, g2, b2 = image2.getpixel((x,y))
                    total_pixel_difference += sum(abs(a - b) for a, b in zip((r1, g1, b1), (r2, g2, b2)))

            pixel_difference = abs(total_pixel_difference)/(width*height)
            return pixel_difference
```
 


## 3. 图片的直方图相似性计算。
>在ImageQuery类中实现更多的相似性计算方法。具体地，利用PIL.Image类的histogram方法，获取图片相素的直方图，进而用scipy.states中的相关性计算方法来得到不同的相似性，如pearson，spearman，kendall等。这些方法并不要求图片形状一致。注意，这些相似性方法还能够返回显著性。

先把图片转为灰色（否则Pearson系数格外的小），转为直方图后计算Pearson相关系数
```python
    def histogram_difference(self,image1,image2):
        image1 = image1.convert('L')
        image2 = image2.convert('L')
        ins1 = image1.histogram()
        ins2 = image2.histogram()
        pearson = pearsonr(ins1,ins2)
        return pearson[0]
```

## 4. 图片的大模型嵌入。
> 在ImageQuery类中实现基于大模型的相似性计算方法，即利用相关API(具体见Demo ali_image_embed.py或者ark_image_embed.py)首先将图片嵌入为向量，继而通过向量的余弦相似度等给出相似性大小(cos_simi.py)。注意，选一个大模型实现即可，ali和字节均提供一定的免费token额度。

在my_ali_model模块中储存API_KEY,MODEL，以及调用Model的方法get_embeddings
```python

def get_embeddings(image_path):
    with open(image_path, "rb") as image_file:
    # 读取文件并转换为Base64
        base64_image = base64.b64encode(image_file.read()).decode('utf-8')
    image_format = 'png' # 根据实际情况修改，比如png, jpg、bmp 等
    image_data = f"data:image/{image_format};base64,{base64_image}"
    #输入数据
    inputs = [{'image': image_data}]
    # 调用模型接口
    resp = dashscope.MultiModalEmbedding.call(
        api_key = KEY,
        model = MODEL,
        input = inputs
        )
    if resp.status_code == HTTPStatus.OK:

        return resp.output['embeddings'][0]['embedding']#1024维向量
    #print(json.dumps(resp.output, ensure_ascii=False, indent=4))   
```
在主文件中import相关内容
```python
from my_ali_model import KEY, MODEL, get_embeddings  #get_embeddings 调用API的方法
```

在ImageQuery类中定义计算余弦相似度的方法
```python

    def cos_simi(self,image1_path,image2_path):
        embedings1 = get_embeddings(image1_path)
        embedings2 = get_embeddings(image2_path)
        #把1024维向量转换为二维数组
        vec1 = np.array(embedings1).reshape(1, -1)
        vec2 = np.array(embedings2).reshape(1, -1)
        
        similarity = cosine_similarity(vec1, vec2)
        #输出是一个矩阵,如果只比较两个向量，结果是 1x1 矩阵，所以取 [0][0]。
        return similarity[0][0]
```

***对以上三种方法进行测试***

test1_image(100*100): 比格多栋

![1](https://gitee.com/aliinali/25_data_analysis_pics/raw/master/w7/test1_100.png)

test2_image(100*100): 比格多栋

![2](https://gitee.com/aliinali/25_data_analysis_pics/raw/master/w7/test2_100.png)

test3_image(97*97): ；领结猫

![3](https://gitee.com/aliinali/25_data_analysis_pics/raw/master/w7/test3_97.png)

test4_image(100*100): 领结猫

![4](https://gitee.com/aliinali/25_data_analysis_pics/raw/master/w7/test4_100.png)
> 我写python作业就像这样

```python

#创建实例
    image_query = ImageQuery()
    #转换为PIL.image
    image1 = image_query._create_an_image(image1_path)
    image2 = image_query._create_an_image(image2_path)
    image3 = image_query._create_an_image(image3_path)
    image4 = image_query._create_an_image(image4_path)
    #测试pixel
    try:
        pixel_12 = image_query.pixel_difference(image1,image2) #同size
        print('test1和test2的逐像素相减: ',pixel_12)
    except ImageQueryShapeNotMatchError as iqsnme:
        print(iqsnme.message)

    try:
        pixel_14 = image_query.pixel_difference(image1,image4) #同size
        print('test1和test4的逐像素相减: ',pixel_14)
    except ImageQueryShapeNotMatchError as iqsnme:
        print(iqsnme.message)
    

    try:
        pixel_13 = image_query.pixel_difference(image2,image3) #不同size
    except ImageQueryShapeNotMatchError as iqsnme:
        print(iqsnme.message)

    #测试直方图
    pearson_12 = image_query.histogram_difference(image1, image2)
    pearson_13 = image_query.histogram_difference(image1, image3)
    print('test1和test2的直方图相似性: ',pearson_12)
    print('test1和test3的直方图相似性: ',pearson_13)

    #测试余弦
    similarity_12 = image_query.cos_simi(image1_path, image2_path)
    similarity_13 = image_query.cos_simi(image1_path, image3_path)
    print('test1和test2的余弦相似性: ',similarity_12)
    print('test1和test3的余弦相似性: ',similarity_13)

    
```

***输出***
```python
图片加载成功！
图片加载成功！
图片加载成功！
图片加载成功！
test1和test2的逐像素相减:  187.90103911381237
test1和test4的逐像素相减:  378.4850259778453
The sizes of images are not matched
test1和test2的直方图相似性:  0.9902254846951382
test1和test3的直方图相似性:  0.2962063668227174
test1和test2的余弦相似性:  0.9725522853151289
test1和test3的余弦相似性:  0.3703323488321294
```

逐个分析：

**逐像素相减的方法**：

很明显：比格多栋-比格多栋（187） < 比格多栋-领结猫（378）

对于size不匹配的比格多栋与领结猫，捕获了错误，输出了报错信息：The sizes of images are not matched

**直方图相似性（Pearson）**

计算Pearson在[-1,1]之间，正负号代表正相关/负相关，绝对值越大相关性越强。显然 小比和小比的相关性（0.99）>> 小比和领结猫的相关性（0.29），所以验证算法还是不错滴（虽然我忧心0.99是否过高，或许可以进一步验证）

**余弦相似性**

与Pearson相似，同样是在[-1,1]间。似乎余弦比Pearson更“温和”一点


## 5. （附加）hash
> 安装imagehash库，利用其提供的一些hash算法（如average_hash)等，来计算两张图片间的相似性，即其hash值的差异。

```python
from imagehash import average_hash
```

```python
    def hash_simi(self,image1,image2):
        hash_value1 = average_hash(image1)
        hash_value2 = average_hash(image2)
        dis = abs(hash_value1-hash_value2)
        return dis
```
***测试***
```python

    #测试哈希
    dis1 = image_query.hash_simi(image1,image2)
    dis2 = image_query.hash_simi(image1, image4)
    print('test1和test2的哈希距离：',dis1)
    print('test1和test4的哈希距离：',dis2)

```
***输出***
```python
test1和test2的哈希距离： 23
test1和test4的哈希距离： 31
```









    





