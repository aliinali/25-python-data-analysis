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
> 定义一个类TextAnalyzer，其属性包括待分析的文本文件路径，等加载的预训练模型文件路径，训练word2vec的一些简单参数（如向量长度，窗口大小）等，初始化的时候需要对这些属性进行定义。

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

> 在上述类加入一个预处理方法_pre_process，如将待分析的weibo.txt加载到内存（请先解压提供的weibo.txt.zip)，进行基本的文本预处理，如对所有微博内容进行去重，进行分词、去除停用词、标点等，最终建立一个以微博为单位进行分词的二维列表。注意，weibo.txt一行为一条微博的属性，用\t分隔后，第二个元素为微博内容。（提供的weibo.txt包含大量重复和标点等，需要仔细预处理，否则会影响后面的嵌入模型训练。）

***思路***

把几个停用词表合起来之后，还是没有完全覆盖非中文字符，于是再去除停用词的同时筛选掉非中文字符('\u4e00'<= w <= '\u9fa5')

对于去重：考虑转为set去重，但是报错list unhashable 原因是原来的sentences是一个二维列表，而set去重操作是通过哈希表完成的。于是先把sentences中的元素转为tuple，去重后再转回list.把处理完的文本存储起来，主程序中首先检查是否存在处理好的文件，有则使用，没有则预处理



***代码***

 ```python
    #文本预处理
    def _pre_process(self):
        sentences = []
        with open(file_path,'r',encoding = 'utf-8') as f:
            for line in f:
                cnt+=1
                #去除掉停用词和所有非中文字符
                sen = [w for w in jieba.cut(line.strip().split('\t')[1]) if ((w not in stopwords) & ('\u4e00'<= w <= '\u9fa5'))]
                #print(sen)
                #去重
                sen = tuple(sen)
                sentences.append(sen)
            sentences = set(sentences) 
            sentences = [list(sen) for sen in sentences] 
        self.sentences = sentences
        with open('processed_weibo.pkl',"wb") as f:
            pickle.dump(self.sentences,f)
        print('文件处理完毕')
        print('文件时间：',time.time())
```
主程序中：
```python

if __name__ == "__main__":
    # 检查预处理文本是否存在
    processed_text_path = 'processed_weibo.pkl'
    if not os.path.exists(processed_text_path):
        text = TextAnalyzer(file_path, 300, 5, 1)
        text._pre_process()
        text._get_word2vec_model()
    else:
        # 加载预处理文本
        with open(processed_text_path, 'rb') as f:
            sentences = pickle.load(f)
        text = TextAnalyzer(file_path, 300, 5, 1)
        text.sentences = sentences
        text._get_word2vec_model()

```
***输出***
> sentences中的部分sen
```python
['当今', '国庆节', '说', '中华人民共和国', '成立', '纪念 日', '说', '祖国', '母亲', '生日', '泱泱', '五千年', '历 史', '那去', '中国', '统一', '民族团结', '国家', '历史', '记载', '纪元', '数千年', '岁', '五千年', '文化', '文明']
['只想', '找', '合适', '做', '女朋友', '谈', '一场', '无 止尽', '恋爱', '全身心', '投入', '未来', '打拼', '中', ' 背后', '有个', '理解', '支持', '我要', '仅此而已']       
['男孩儿', '居然', '分钟', '寺开', '一家', '类似', '茶油', '鸭', '小店', '配料', '味道', '鲜美', '顾客', '闻香', '大姐', '自愧不如', '小兄弟', '姐祝', '生意兴隆', '加油'] 
['气垫', '运动鞋', '敌不住', '北京', '正规', '导游', '快 节奏', '泪', '木兰', '清香']

```

### 3.3 w2v训练
> 在上述类加入一个方法_get_word2vec_model来利用2中构建的微博二维列表来训练Word2Vec模型，可参照demo使用gensim完成Word2Vec模型的建立。

***代码***

```python
#训练Word2Vec模型 保存
    def _get_word2vec_model(self):  
        model_path = 'word2vec.model'
        if os.path.exists(model_path):
            self.model = Word2Vec.load(model_path)

        else:
            model = Word2Vec(self.sentences, vector_size=self.vector_size, window=self.window, min_count = self.min_count)
            model.save(model_path)
            self.model = model
        print('模型加载完毕，当前时间:',time.time())
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
text._get_similar_words('生活',10)
```

***输出***
```python
#花朵
[('盛开', 0.930207371711731), ('凋零', 0.9229941368103027), ('种子', 0.921674907207489), ('一朵', 0.9181733131408691), ('浅浅', 0.9167525172233582), ('深邃', 0.9148210883140564), ('洁白', 0.9146103262901306), ('温润', 0.9120347499847412), ('心田', 0.9106951951980591), ('凋落', 0.9092465043067932)]

#生活
[('安逸', 0.7551324963569641), ('平淡', 0.7032443881034851), ('乐趣', 0.6984530091285706), ('一成不变', 0.6653362512588501), ('当下', 0.661339521408081), ('向往', 0.6610845923423767), ('平凡', 0.6597033739089966), ('活着', 0.6556937098503113), ('活', 0.6552977561950684), ('会活', 0.6513950824737549)]
```


***分析***

总的来说，与“花朵”相似的词语相似度在0.9以上。找到的词确实是与“花朵”一词紧密相关的。如“盛开”、“凋零”、“凋落”等是花朵的直接行为，“一朵”、“浅浅”、“洁白”，“温润”等是对花朵的修饰，“种子”是花朵的衍生物，“心田”应与花朵的引申义相关：“花朵开在心田”引申为人类安详幸福的状态。“深邃”在语义上与常见意象的花朵相距较远，应结合文本检查是否有较多将“花朵”与“深邃”连接紧密的文本。

而“生活”的近义词的相似度总体较低，在0.65-0.76区间。分析可能原因有：

1.花朵是具象事物，语义较单一；生活是抽象概念，语义更丰富

2.语义的多样性决定了语境（上下文文本）的丰富程度，生活的上下文文本更多样，覆盖的词语也更分散


## 扩展情绪词典
> 这些相似词可否用来扩展我们之前使用过的情感词典？请在类中再增加一个方法expand_emotion_lexicion，对情感词典进行扩充，如对于情感词典中已有的人工标定的词，找到与其相似的词（如top 5)，标记为同样的情感标签，并加入到词典，观察其对情绪分类是否有提升作用（比如增加了覆盖率等）。

***思路***

分别读取情绪词典，对前100个词找最相近的5个词（文本就是微博文本），将找到的5个词写在txt文件最末。通过查看文件末尾的词，以及重新运行w3情绪分析的程序，判断情绪词典的覆盖是否上升。

***代码***

```python
def expand_emotion_lexicion(self):
        print("开始执行字典扩建,当前时间:",time.time())
        for emotion in ['anger', 'disgust', 'fear', 'sadness', 'joy']:
            file_path = os.path.join(EMOTION_DIR, f'{emotion}.txt')
            with open(file_path, 'r', encoding='utf-8') as f:
            #扩展每个字典前100个词语的近义词
                words = [line.strip() for line in f.readlines()]
            with open(file_path, 'a', encoding='utf-8') as f:
                for word in words[:100]:  # 只扩展前100个词
                    if word and word in self.model.wv:
                        similar_words = self._get_similar_words(word, 5)
                        for similar_word, similarity in similar_words:
                            f.write('\n' + similar_word)
```

***运行结果***

情绪词典扩展前的结果：

![更新前](https://gitee.com/aliinali/25_data_analysis_pics/raw/master/w5/emotion更新前w3问题3的图片.jpg)

情绪词典扩展后的结果：

![更新后](https://gitee.com/aliinali/25_data_analysis_pics/raw/master/w5/emotion更新后w3问题3的图片.png)

根据图片，很容易看出，从比例上来说，更新后消极情绪的比例增加了，可能原因是训练文本中消极情绪的词语比较多样（不愧是微博）。

更新前情绪.txt最末几个词：

anger

![更新后](https://gitee.com/aliinali/25_data_analysis_pics/raw/master/w5/anger前.png)

disgust

![更新后](https://gitee.com/aliinali/25_data_analysis_pics/raw/master/w5/disgust前.png)

fear

![更新后](https://gitee.com/aliinali/25_data_analysis_pics/raw/master/w5/fear前.png)

sadness

![更新后](https://gitee.com/aliinali/25_data_analysis_pics/raw/master/w5/sadness前.png)

joy

![更新后](https://gitee.com/aliinali/25_data_analysis_pics/raw/master/w5/joy前.png)


更新后，情绪词典最末几个词变为：

anger

![更新后](https://gitee.com/aliinali/25_data_analysis_pics/raw/master/w5/anger后.png)

从这个结果来看，从文本中挖掘相似词找“近义词”来扩展情绪词典确实会找到一些非常“人性化”的词语

disgust

![更新后](https://gitee.com/aliinali/25_data_analysis_pics/raw/master/w5/disgust后.png)
> 好心酸的普通人

fear

![更新后](https://gitee.com/aliinali/25_data_analysis_pics/raw/master/w5/fear后.png)

但有时的效果也不太好，出现了一些似是而非的词，比如“本田”，“铜壶”，“伸手”，“仰头”等，可能与文本量过小或者表达内容多样有关

sadness

![更新后](https://gitee.com/aliinali/25_data_analysis_pics/raw/master/w5/sadness后.png)
> 很sad了

joy

![更新后](https://gitee.com/aliinali/25_data_analysis_pics/raw/master/w5/joy后.png)
> 喜欢这个 爱意是人类快乐之源

## TSNE可视化

***设置字体***

```python
#设置字体
from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False
```
***思路***

分别找到输入词的most_similar词和least_similar词，合成一个数组后用tsne降维，再可视化

***代码***
```python
def vis_word_tsne(self,word,num):
        most_similar = self._get_similar_words(word,num)
        least_similar = self._get_least_similar_words(word,num)
        vectors = np.array([self.model.wv[word] for word, similarity in most_similar + least_similar])
        #print(vectors.shape)
        words = [word for word, similarity in most_similar + least_similar]

        # 使用t-SNE算法对词向量进行降维
        tsne = TSNE(n_components=2, perplexity=15)
        #print(vectors)
        vectors_tsne = tsne.fit_transform(vectors)

        # 可视化降维后的词向量
        fig, ax = plt.subplots()
        ax.set_title('花朵')
        # t-SNE降维至2维
        ax.scatter(vectors_tsne[:10, 0], vectors_tsne[:10, 1], color='blue',label = 'most_simi')
        ax.scatter(vectors_tsne[10:, 0], vectors_tsne[10:, 1], color='red', label = 'least_simi')
        ax.legend()
        # 打印词
        for i, word in enumerate(words):
            ax.annotate(word, (vectors_tsne[i, 0], vectors_tsne[i, 1]))

        plt.show()

```

***输出***

![更新后](https://gitee.com/aliinali/25_data_analysis_pics/raw/master/w5/近义词_反义词.png)

非常糟糕的是反义词很没有规章，可能是分词结果有问题，而min_count设置的比较小所以留下了这些“分词意外”,因为这些意外实在和”花朵“相隔甚远，于是被当做了least_similar.
