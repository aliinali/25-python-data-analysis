# 词向量表征
> Word2vec是一类用来产生词向量的神经网络模型，通过学习文本语料库中单词之间的语义和上下文关系来表示单词的向量空间。在训练完成后，它可以把每个词映射到一个可以表示词与词之间关系的向量。因此它可以被用来进行文本聚类和相似度计算等任务，也常常被应用在包括文本分类、情感分析、信息检索、机器翻译等场景下。因此，参照wvdemo.py，本次作业将实现一个简单的类，并体会word2vec的各种相关应用。

## 1.文件解压
***代码***
```python
import os
import zipfile

script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir,"weibo.txt.zip")

zip_file_path = file_path
extract_to_folder = 'w5'#解压后的文件存放在这个文件价中

if not os.path.exists(extract_to_folder):
    os.makedirs(extract_to_folder)

with zipfile.ZipFile(zip_file_path,'r') as zip_ref:
    zip_ref.extractall(extract_to_folder)

print('done')
```

## 2.引入停用词表
***代码***
```python

#stopwords路径
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path2 = os.path.join(script_dir,"cn_stopwords.txt")

#引入停用词表 stopwords
with open(file_path2,'r',encoding = 'utf-8') as f:
    con = f.readlines()
    stopwords = set()
    for i in con:
        i = i.replace("\n","")
        stopwords.add(i)
```

## 3.类
### 3.1 初始化
***代码***
```python

class TextAnalyzer:
    def __init__(self,path,vector_size,window,min_count):
        self.path = path
        self.vector_size = vector_size
        self.window = window
        self.min_count = min_count
```

### 3.2文本预处理
***思路***

把几个停用词表合起来之后，还是没有完全覆盖非中文字符，于是再去除停用词的同时筛选掉非中文字符('\u4e00'<= w <= '\u9fa5')
对于去重：考虑转为set去重，但是报错list unhashable 原因是原来的sentences是一个二维列表，而set去重操作是通过哈希表完成的。于是先把sentences中的元素转为tuple，去重后再转回list

***代码***

 ```python
    #文本预处理
    def _pre_process(self):
        sentences = []
        with open(file_path,'r',encoding = 'utf-8') as f:
            for line in f:
                #去除掉停用词和所有非中文字符
                sen = [w for w in jieba.cut(line.strip().split('\t')[1]) if ((w not in stopwords) & ('\u4e00'<= w <= '\u9fa5'))]
                #print(sen)
                #去重
                sen = tuple(sen)
                sentences.append(sen)
            sentences = set(sentences) 
            sentences = [list(sen) for sen in sentences]  # 将 tuple 转换回 list
        self.sentences = sentences
```
***输出***
> sentences中的部分sen
![文本预处理](https://gitee.com/aliinali/25_data_analysis_pics/raw/master/w5/文本预处理.png)

### 3.3 w2v训练
> 在上述类加入一个方法_get_word2vec_model来利用2中构建的微博二维列表来训练Word2Vec模型，可参照demo使用gensim完成Word2Vec模型的建立。
***代码***
```python
#训练Word2Vec模型
    def _get_word2vec_model(self):  
        model = Word2Vec(self.sentences, vector_size=self.vector_size, window=self.window, min_count = self.min_count)
        self.model = model
```
### 3.4 找相似
> 在上述类加入一个方法get_similar_words来利用训练得到的word2vec模型来推断相似词汇。如输入一个任意词，使用model.similarity方法可以来返回与目标词汇相近的一定数目的词。
***代码***
```python
    #得到近义词
    def _get_similar_words(self,word,num):
        most_similar = self.model.wv.most_similar(word,topn = num)
        print(most_similar)
```
创建实例，设置vector_size,window,min_count分别为300/5/1
```python

text = TextAnalyzer(file_path,300,5,1)
text._pre_process()
text._get_word2vec_model()
text._get_similar_words('花朵',10)
```

***输出***
![文本预处理](https://gitee.com/aliinali/25_data_analysis_pics/raw/master/w5/most_similar.png)

***分析***

总的来说，找到的词确实是与“花朵”一词紧密相关的。如“盛开”、“凋零”、“凋落”等是花朵的直接行为，“一朵”、“浅浅”、“洁白”，“温润”等是对花朵的修饰，“心田”应于花朵的引申义相关：“花朵开在心田”引申为人类安详幸福的状态。“深邃”在语义上与常见意象的花朵相距较远，应结合文本检查是否有较多将“花朵”与“深邃”连接紧密的文本。




