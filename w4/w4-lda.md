# LDA主题模型
## 文档预处理

> 一般来讲，LDA在评论等短文本上的效果并不理想，且多数情况下，我们希望给话题赋予时间含义，以讨论其“波动性”。因此，往往先需要按时间进行文档的生成，比如，将某一店铺的评论按年进行合并，即将某店铺某年发布的所有评论视为一个文档。请实现一个模块，其中包含一个或多个函数，其能够读取该数据集并将之分店铺（共8家店铺，可根据shopID进行区分）处理以天（或其他时间单位）为单位的文档集合。

### 思路
新建python文件dfcut.py,保存在主文件同一文件夹中。定义函数id_time_cut(file_path, shopid, TimeMode),读取文件，根据店铺ID和TimeMode筛选子表，合并同一时间文本，返回一个字典。其中key为时间值，value为字符串列表。

### 代码
```Python
import pandas as pd
#import os

def id_time_cut(file_path, shopid, TimeMode) -> dict:
    '''将某一店铺的评论按{TimeMode}进行合并
    返回字典{时间：list文档}'''
    
    df = pd.read_csv(file_path, encoding='gbk')
    sub_df = df[df['shopID'] == shopid]
    sub_df = sub_df[['cus_comment', TimeMode]]
    text_at_time_dic = {}
    
    #遍历每行
    for index,row in sub_df.iterrows():
        time = row[TimeMode]
        comment = row['cus_comment']
        if pd.isnull(comment):  #去除空白词
            continue
        
        if time not in text_at_time_dic:
            text_at_time_dic[time] = []

        text_at_time_dic[time].append(comment)


    return text_at_time_dic
```

### 输出
```Python
['双皮奶 好味 比仁信 大碗 云吞面 好 大碗 抵食 不过 太多人 阿姨 都 吾 多理 人', '双皮奶 很 好吃 的 不过 环境 太 吵 杂 了 要 和 人 拼桌 的 说', '雙皮奶 是 我 的 至 愛必 吃  这 裹 價錢 可以 雙皮奶 做 的 比仁信 好', '双皮奶 比仁信  好 很多 就是 太挤 了 服务 就 有点 跟不上 咯 总体 食物 水 平 不错', '挤得 一塌糊涂 只能 拼桌 服务员 大喊大叫 跑来跑去 完全 丧失 了 品位 美食 的 兴致 印象 打 了 大大的 折扣 主食 品种 比 甜点 还 多 虽然 价格 更加 的 便宜 名气 也 很 响亮 但 双皮奶 和 其他 甜水 从 外表 来说 就 不及 仁信 一尝 更是 甜 的 发腻 特别 是 奶糊 绝对 肥', '十甫路 的 店  生意 真的 爆好 平心而论 这里 的 双皮奶 还 不错 曾经 是 印象 中 的 第一名 直到 在 香港 吃 到益 顺人 的 嘴 真实 刁  啊', '最 搞笑 的 是 我 把 单子 弄 丢 了 差点 就 把 端 到 我 面前 的 双皮奶 给 端 回去 可能 是 先入为主 吧 而且 到 这里 要 的 是 纯 的 双皮奶 没加 红豆 表面 的 裂痕 就 不可 遮掩 地露 了 出来 感觉 整体 上 比仁信 的 再 冻 一点 但是 皮 就 没有 厚出 凤凰 奶糊 好 甜 啊 就是 奶粉 冲 的 感觉 第十 甫 的 小吃 太多 了 感觉 胃口 完全 装不下 呀 每次 想 吃 云吞面 都 没 地方 放 了', '非常 好吃 每次 去 广州 都  要 想 办法 去 尝尝 尤其 是 凤凰 奶糊 一级 棒', '也 是 个 老字号 点 了 招牌 的 双皮奶 想 尝尝 正宗 的 味道 如何 可 能 是 天生 不 喜欢 这种 味道 的 吧 吃 了 几口 就 浪费 了', '最 喜欢 这里 的 姜 埋奶 其他 主食 也 很 不错 如牛 三星 个人 认为 是 广州 最 好吃 的 云吞面 也 很 好 块钱 就 有 大大的 虾 在 里面']
```
> 翻不到最开始print出来的东西了（👉🏻👈🏻）...字符串列表大概长这样

## 文本的特征表示
> 实现一个模块，通过一个或多个函数，将每个文档转变为词频特征表示，以形成文档-词语的词频矩阵，可以选择使用sklearn中的CountVectorizer和TfidfVectorizer两种方式。也可以使用gensim中的dictionary.doc2bow等。

### 思路
这里使用了sklearn库的CountVectorizer。新建DocToBow.py文件，保存在主文件同一文件夹下。定义Doc2Bow函数,输入id_time_cut返回的{时间：字符串列表}字典，返回{时间：矩阵}字典

### 代码
 ```Python
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd

def Doc2Bow(text_at_time_dic) -> dict:
    '''return {time:词频矩阵} '''
    matrix_at_time_dic = {}
    for time, doc in text_at_time_dic.items():
        vectorizer = CountVectorizer()
        matrix = vectorizer.fit_transform(doc)
        matrix_at_time_dic[time] = matrix
    return matrix_at_time_dic
```
### 输出
```python
{2018: <Compressed Sparse Row sparse matrix of dtype 'int64'
        with 90191 stored elements and shape (2624, 11936)>, 2017: <Compressed Sparse Row sparse matrix of dtype 'int64'
        with 69990 stored elements and shape (2108, 10416)>, 2016: <Compressed Sparse Row sparse matrix of dtype 'int64'
        with 49613 stored elements and shape (1737, 8563)
```
可以看见2018对应的矩阵是最大的，说明2018的文档具有最丰富的词汇表，当然，也有可能是停用词过滤不充分

## 3.文本的话题分析
> 实现一个模块，通过一个或多个函数，借助sklearn.decomposition中的LatentDirichletAllocation构建主题模型（话题数目可以自主指定），并对发现的主题进行分析（每个主题对应的词语可利用model.components_来查看，每篇文档的主题概率分布可通过model.transform来查看）。也可以参考demo里的ldav.py，用gensim进行LDA分析，并进行可视化.

### 思路
新建python文件find_feature.py,保存在主文件同一文件夹中。定义函数lda_analysis(doc,n_topics,n_words),将文档转换为词频矩阵，获取主题关键词及文档-主题分布

### 代码
```python

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

def lda_analysis(documents, n_topics=5, n_words=10):

    # 将文档转换为词频矩阵
    vectorizer = CountVectorizer(stop_words='english')
    X = vectorizer.fit_transform(documents)
    
    # 构建 LDA 模型
    lda = LatentDirichletAllocation(n_components=n_topics, random_state=42)
    lda.fit(X)
    
    # 获取主题关键词
    feature_names = vectorizer.get_feature_names_out()
    topic_keywords = {}
    for topic_idx, topic in enumerate(lda.components_):
        top_features_ind = topic.argsort()[:-n_words - 1:-1]
        topic_keywords[topic_idx] = [feature_names[i] for i in top_features_ind]
    
    # 获取文档-主题分布
    doc_topic_distr = lda.transform(X)
    
    return topic_keywords, doc_topic_distr
```
主文件中：对所有文档依次调用函数，打印主题关键词及文档主题分布，选择主题数为5
```python

combined_documents = {time: " ".join(doc) for time, doc in doc_at_time_dic.items()}
documents = list(combined_documents.values())
times = list(combined_documents.keys())

# 对所有文档进行 LDA 分析
topic_keywords, doc_topic_distr = lda_analysis(documents, n_topics=k, n_words=5)

# 打印每个时间点的主题关键词和文档-主题分布
for time, doc_topic in zip(times, doc_topic_distr):
    print(f"时间: {time}")
    print("主题关键词:")
    for topic_idx, keywords in topic_keywords.items():
        print(f"  主题 {topic_idx}: {' '.join(keywords)}")
    print("文档-主题分布:")
    print(f"  主题分布: {doc_topic}")
    print("-" * 50)
```
### 输出（部分）
```python
--------------------------------------------------
时间: 2005
主题关键词:
  主题 0: 双皮奶 不错 好吃 味道 甜品
  主题 1: 龟零膏 就晤 小新则 小桌 小碗
  主题 2: 龟零膏 就晤 小新则 小桌 小碗
文档-主题分布:
  文档 0: [9.99882024e-01 5.89877741e-05 5.89877741e-05]   
--------------------------------------------------
时间: 2004
主题关键词:
  主题 0: 双皮奶 比仁信 好吃 奶糊 云吞面
  主题 1: 香港 太多 品种 响亮 回去
  主题 2: 香港 太多 品种 响亮 回去
文档-主题分布:
  文档 0: [0.99597329 0.00201336 0.00201336]
--------------------------------------------------

时间: 2011
主题关键词:
  主题 0: 或是 旧时 早饭 早门 早要
  主题 1: 或是 旧时 早饭 早门 早要
  主题 2: 双皮奶 好吃 三星 味道 不过
文档-主题分布:
  文档 0: [2.11024051e-05 2.11024051e-05 9.99957795e-01]   
--------------------------------------------------
时间: 2010
主题关键词:
  主题 0: 龟苓膏 差南信 布置 市区 差远了
  主题 1: 双皮奶 三星 好吃 不过 味道
  主题 2: 龟苓膏 差南信 布置 市区 差远了
文档-主题分布:
  文档 0: [2.43922121e-05 9.99951216e-01 2.43922121e-05]   
--------------------------------------------------
```
总的来说，当采用主题数为3时会出现有两个主题非常相似的情况。但如果设置主题数为2，就会出现两个主题对应关键词完全相同，主题概率分布不同的情况，比如：
```python
--------------------------------------------------
时间: 2006
主题关键词:
  主题 0: 双皮奶 三星 不过 喜欢 味道
  主题 1: 双皮奶 三星 不过 喜欢 味道
文档-主题分布:
  文档 0: [2.17919040e-04 9.99782081e-01]
--------------------------------------------------
时间: 2005
主题关键词:
  主题 0: 双皮奶 不错 好吃 味道 甜品
  主题 1: 双皮奶 不错 好吃 味道 甜品
文档-主题分布:
  文档 0: [9.99903493e-01 9.65072885e-05]
--------------------------------------------------
```
显然能够得到的信息更少了，因此采用主题数为3

## 4.序列化保存
> 利用pickle或json对所得到的lda模型、对应的词频矩阵、以及特征表示等进行序列化保存。

在对应函数（lda_analysis）中保存
```python
import pickle
    # 保存 LDA 模型
    with open('lda_model.pkl', 'wb') as f:
        pickle.dump(lda, f)
         
    # 保存词频矩阵
    with open('matrix.pkl', 'wb') as f:
        pickle.dump(X, f)
    
    # 保存特征表示
    with open('features.pkl', 'wb') as f:
        pickle.dump(vectorizer.get_feature_names_out(),f)
```

## 5.根据困惑度选取最优话题数
> 超参数k（即话题的数目）变化时，评价LDA模型的一个指标即困惑度（lda.perplexity）会随之波动，尝试绘制困惑度随话题数目k变化的曲线，找到较优的k。

### 思路
先从doc_at_time_dic中把所有字符串列表提取出来，合并为docs，绘制困惑度随话题数目变化的曲线，理想的k值应该是：在k前曲线逐渐下降，k后趋于平稳

### 代码
```python
#为找到困惑度 先把所有doc提取出来
docs = []
for time,doc in doc_at_time_dic.items():
    docs += doc


vectorizer = CountVectorizer()
X = vectorizer.fit_transform(docs)

perplexity_scores = []
k_range = range(5,51,5) # k的范围
for k in k_range:
    lda = LatentDirichletAllocation(n_components=k,max_iter= 2000)
    lda.fit(X)
    perplexity_scores.append(lda.perplexity(X))
plt.plot(k_range, perplexity_scores, '-o')
plt.xlabel('Number of topics')
plt.ylabel('Perplexity')
plt.show()
```
### 输出
这一步做了几次调参最后结果还是不好看...截止我写报告的时间（2025年3月24日14:45:14），依旧没有跑出好的结果，先把最后两次结果放出来占个坑......希望助教检查作业的时候我已经跑出来了🥲🥲🥲这两张的迭代次数分别是1000,2000

![pic1](https://gitee.com/aliinali/25_data_analysis_pics/raw/master/w4/困惑度（迭代1000）.png)
![pic2](https://gitee.com/aliinali/25_data_analysis_pics/raw/master/w4/困惑度（迭代2000）.png)

## 6.话题分布的时间趋势分析
> 根据评论文档的时间信息，观察特定话题随着时间的变化趋势，即分析某一话题在不同时间段内的出现频率或权重，以便了解该话题在不同时期内的热度变化。

### 思路
对所有时间序列文档合起来的总文档进行lda分析，找到总文档主题共5个
```python
主题关键词:
  主题 0: 双皮奶 三星 不过 好吃 味道
  主题 1: 挤得 跑来跑去 第一名 丧失 平心而论
  主题 2: 到益 地露 厚出 大喊大叫 顺人
  主题 3: 双皮奶 好吃 味道 甜品 广州
  主题 4: 挤得 跑来跑去 第一名 丧失 平心而论
```
