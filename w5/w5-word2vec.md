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
 #文本预处理
 ```python
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
### 输出
![文本预处理](


