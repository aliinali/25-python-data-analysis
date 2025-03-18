import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict
import os
from pylab import mpl

mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False

# 获取脚本所在目录
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path_data = os.path.join(script_dir, "week3.csv")
EMOTION_LEXICON_DIR = r'C:\Users\Huawei\Desktop\好一个大学\课内学习\大二下\ppppp数据分析\w3\emotions'

# 加载情绪字典
def load_emotion_lexicon(directory):
    emotion_dict = defaultdict(set)
    for emotion in ['anger', 'disgust', 'fear', 'sadness', 'joy']:
        file_path = os.path.join(directory, f'{emotion}.txt')
        with open(file_path, 'r', encoding='utf-8') as f:
            words = {line.strip() for line in f.readlines()}
            emotion_dict[emotion] = words
    return emotion_dict

# 创建情绪分析器
def create_emotion_analyzer():
    EMOTION_DIC = load_emotion_lexicon(EMOTION_LEXICON_DIR)

    def emotion_analysis(text, mode='mixed'):
        emotion_count = {emotion: 0 for emotion in EMOTION_DIC.keys()}
        total_emotion_words = 0

        for word in text:
            for emotion, words in EMOTION_DIC.items():
                if word in words:
                    emotion_count[emotion] += 1
                    total_emotion_words += 1

        if total_emotion_words == 0:
            return "No emotion words"

        emotion_freq_dic = {emotion: emotion_count[emotion] / total_emotion_words for emotion in EMOTION_DIC.keys()}
        sorted_emotion_freq_list = sorted(emotion_freq_dic.items(), key=lambda x: x[1], reverse=True)

        if mode == 'mixed':
            return sorted_emotion_freq_list
        elif mode == 'single':
            if sorted_emotion_freq_list[0][1] > sorted_emotion_freq_list[1][1]:
                return sorted_emotion_freq_list[0][0]
            else:
                return "Multiple emotions"
        else:
            raise ValueError("Invalid mode. Choose 'mixed' or 'single'.")

    return emotion_analysis

# 创建情绪分析器
emotion_analyzer = create_emotion_analyzer()

# 测试情绪分析函数
df = pd.read_csv(file_path_data, encoding='gbk')
text = df.loc[0, 'cus_comment'].split()
print(emotion_analyzer(text, mode='mixed'))
print(emotion_analyzer(text, mode='single'))

# 时间模式分析函数
def time_analysis(df, shopid, emotion, timeMode, emotion_dic):
    '''timeMode == 'month', 'weekday', 'hour'
       emotion == '积极', '消极' '''
    if timeMode not in df.columns:
        raise ValueError(f"Invalid timeMode: {timeMode}. Must be one of {df.columns}")

    # 筛选子表
    sub_df = df[df['shopID'] == shopid]
    sub_df = sub_df[['cus_comment', timeMode]]

    # 按 timeMode 分组，并将评论内容合并为分词列表
    text_at_time = sub_df.groupby(timeMode)['cus_comment'].apply(lambda x: ' '.join(x.astype(str)).split()).to_dict()

    # 初始化 time_emotion 字典
    time_emotion = {time: 0 for time in text_at_time.keys()}

    # 计算情绪分布
    for time, words in text_at_time.items():
        for word in words:
            if emotion == '积极':
                if word in emotion_dic['joy']:
                    time_emotion[time] += 1
            elif emotion == '消极':
                if any(word in emotion_dic[key] for key in ('anger', 'disgust', 'sadness', 'fear')):
                    time_emotion[time] += 1

    # 对时间点排序
    sorted_time = sorted(time_emotion.keys())
    sorted_emotion = [time_emotion[time] for time in sorted_time]

    # 可视化
    fig, ax = plt.subplots()
    ax.bar(sorted_time, sorted_emotion, width=0.5, label=f'{emotion}情绪分布')
    ax.set_xlabel(timeMode)
    ax.set_ylabel('情绪词数量')
    ax.set_title(f'店铺 {shopid} 的 {emotion} 情绪分布（按 {timeMode}）')
    ax.legend()
    plt.xticks(rotation=45) 
    plt.tight_layout()  
    plt.show()

# 测试时间模式分析函数
EMOTION_DIC = load_emotion_lexicon(EMOTION_LEXICON_DIR)
#time_analysis(df, shopid=518986, emotion='积极', timeMode='hour', emotion_dic=EMOTION_DIC)
#time_analysis(df, shopid = 520004,emotion = '消极',timeMode='weekday',emotion_dic = EMOTION_DIC)

new_emotion_dic = {
    "joy": ["绝绝子", "性价比高", "强烈推荐", "物超所值", "好用", "满意", "惊喜", "赞", "超值", "推荐", "棒", "贴心", "高效", "方便", "耐用", "划算", "喜欢", "好评", "信赖", "愉快"],
    "anger": ["差评", "生气", "无语", "愤怒", "发火", "气炸", "不爽", "恼火", "气愤", "怒", "火大", "气死", "气人", "气炸了", "气疯", "气死", "气人", "气炸了", "气疯", "气死"],
    "disgust": ["恶心", "垃圾", "反感", "厌恶", "恶臭", "恶俗", "恶毒", "恶臭", "恶俗", "恶毒", "恶臭", "恶俗", "恶毒", "恶臭", "恶俗", "恶毒", "恶臭", "恶俗", "恶毒", "恶臭"],
    "fear": ["害怕", "担心", "恐惧", "不安", "恐慌", "心惊", "胆战", "心惊胆战", "恐慌", "心惊", "胆战", "心惊胆战", "恐慌", "心惊", "胆战", "心惊胆战", "恐慌", "心惊", "胆战", "心惊胆战"],
    "sadness": ["失望", "糟糕", "心寒", "难过", "伤心", "沮丧", "郁闷", "失落", "悲伤", "痛苦", "无奈", "心碎", "绝望", "无助", "悲哀", "凄凉", "哀伤", "悲凉", "凄惨", "哀怨"]
}
#合并新旧词典
for emotion, words in new_emotion_dic.items():
    new_words_set = set(words)
    EMOTION_DIC[emotion].update(new_words_set)


#比较评分与情绪
#获得平均分
shop_ids = df['shopID'].unique().tolist()  #店铺列表
stars = df[df['shopID'].isin(shop_ids)].groupby('shopID')['stars'].mean().reset_index()
stars.columns = ['shopID', 'avg_stars']
avg_stars = stars['avg_stars'].tolist()  #平均分列表

#获得评论列表
all_comment_text = []
for id in shop_ids:
    sub_df = df[df['shopID'] == id]
    #text = df.loc[0, 'cus_comment'].split()
    comments_list = [word for comment in sub_df['cus_comment'].dropna() for word in comment.split()]
    single_shop_list = [word for sublist in comments_list for word in sublist]
    all_comment_text.append(single_shop_list)

#用字典储存所有店铺的情绪分布
all_shop_emotion = {'anger':[],  
                    'disgust':[],
                    'fear':[],
                    'sadness':[],
                    'joy':[]}

for single_shop_list in all_comment_text:
    single_shop_emotion = emotion_analyzer(single_shop_list, mode='mixed')
    for emotion,freq in single_shop_emotion:
        all_shop_emotion[emotion].append(freq)

print(all_shop_emotion)
print(shop_ids)

'''
def plot_stacked_bar(width=0.5):
    # shop_ids 和 all_shop_emotion
    fig, ax = plt.subplots()

    # 使用 shop_ids 的索引作为横坐标位置
    x_positions = list(range(len(shop_ids)))
    bottom = [0 for _ in range(len(shop_ids))]

    # 绘制堆叠柱状图
    for emotion, frequencies in all_shop_emotion.items():
        ax.bar(x_positions, frequencies, width, label=emotion, bottom=bottom)
        bottom = [b + f for b, f in zip(bottom, frequencies)]
    ax.legend()
    plt.show()

# 调用函数
plot_stacked_bar()
'''

def plot_stacked_bar_with_line(width=0.5):

    fig, ax1 = plt.subplots()

    # 使用 shop_ids 的索引作为横坐标位置
    x_positions = list(range(len(shop_ids)))
    bottom = [0 for _ in range(len(shop_ids))]

    # 绘制堆叠柱状图
    for emotion, frequencies in all_shop_emotion.items():
        ax1.bar(x_positions, frequencies, width, label=emotion, bottom=bottom)
        bottom = [b + f for b, f in zip(bottom, frequencies)]

    # 设置横轴标号
    ax1.set_xticks(x_positions)
    ax1.set_xticklabels(shop_ids, rotation=45, ha='right')
    ax1.set_xlabel('Shop ID')
    ax1.set_ylabel('Emotion Frequency')
    ax1.legend(loc='upper left')

    # 创建折线图
    ax2 = ax1.twinx()
    ax2.plot(x_positions, avg_stars, label='Average Stars', color='red', marker='o')
    ax2.set_ylabel('Average Stars')
    ax2.legend(loc='upper right')

    plt.show()

plot_stacked_bar_with_line()


