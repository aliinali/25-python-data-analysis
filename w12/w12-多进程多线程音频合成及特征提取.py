from multiprocessing import Process, Pool, Lock
import multiprocessing
from threading import Thread

from my_ali_model import KEY
import dashscopea
import requests
import librosa
import numpy as np
import sys
import os

api_key = KEY

#text = ['test','test','test']

#将文件转为文本
def get_text(file_name):
    text = []
    with open (file_name,'r',encoding='utf-8') as f:
        text = f.readlines()
    return [line.strip() for line in text]

#通过大模型将文本转换为音频并保存
def t2v_save(part_text, i, voice_name):
    response = dashscope.audio.qwen_tts.SpeechSynthesizer.call(
    model = "qwen-tts",
    api_key = KEY,
    text = part_text,
    voice = voice_name,
    )
    
    audio_url = response.output.audio["url"]
    save_path = r'C:\Users\Huawei\Desktop\好一个大学\课内学习\大二下\ppppp数据分析\w12\test_audios\text_{}_{}.wav'.format(voice_name,i)  

    #通过网络下载文件
    try:
        response = requests.get(audio_url)
        response.raise_for_status()  # 检查请求是否成功
        with open(save_path, 'wb') as f:
            f.write(response.content)
        print(f"音频文件已保存至：{save_path}")
    except Exception as e:
        print(f"下载失败：{str(e)}")

#多线程转换文本->音频
class MultiThreadASR(Thread):
    def __init__(self, text, i, voice_name):
        super().__init__()
        self.text = text #text是字符串列表
        self.i = i
        self.voice_name = voice_name ##Chelsie（女）Cherry（女） Ethan（男）Serena（女）

    def run(self):
        print(f'正在处理第{self.i + 1}句')
        t2v_save(self.text[self.i],self.i, self.voice_name)

#多进程计算音频特征
class MultiProcessVoiceFeature():
    def __init__(self, workers = None):
        self.workers = workers

    @staticmethod
    def calculate_feature(audio_file):
        '''
        计算单个音频的特征，返回平均值和连续时间'''
        y, sr = librosa.load(audio_file, sr = None)
        #音高
        pitch = librosa.yin(y,fmin = librosa.note_to_hz('C1'),fmax = librosa.note_to_hz('C7'))  
        avg_pitch = np.mean(pitch)
        #声强
        sdb = librosa.amplitude_to_db(librosa.feature.rms(y=y), ref=0.00002)
        avg_sdb = np.mean(sdb)
        #语速
        onsets = librosa.onset.onset_detect(y=y,sr=sr,units="time",hop_length=128,backtrack=False) 
        number_of_words = len(onsets)
        duration = len(y)/sr
        words_per_second = number_of_words/duration

        #以元组形式返回
        return (avg_pitch, avg_sdb, words_per_second, duration)

    def get_feature(self, audio_files):
        '''
        所有音频文件的加权平均
        '''
        with Pool(processes=self.workers) as pool:
            results = pool.map(self.calculate_feature, audio_files)

        # 提取各特征和持续时间
        pitches = [r[0] for r in results]
        sdbs = [r[1] for r in results]
        wpss = [r[2] for r in results]
        durations = [r[3] for r in results]
        total_duration = sum(durations)
        weights = np.array(durations)/total_duration

        # 加权平均（按 duration 加权）
        avg_pitch = np.average(pitches, weights=weights)
        avg_sdb = np.average(sdbs, weights=weights)
        avg_words_per_second = np.average(wpss,weights=weights)

        return (avg_pitch, avg_sdb, avg_words_per_second)
        
        

if __name__ == "__main__":
    #测试文本
    file_path = r'C:\Users\Huawei\Desktop\好一个大学\课内学习\大二下\ppppp数据分析\w12\test.txt'
    text = get_text(file_path)
    #print(text)
    num_len = len(text)
    voice_names = ['Chelsie','Cherry','Ethan','Serena']

    '''
    #测试MultiProcessVoiceFeature
    #每种声音都转成音频
    for voice_name in voice_names:
        threads = []
        for i in range(num_len):
            thread = MultiThreadASR(text, i, voice_name)
            threads.append(thread)
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
            '''
    
    #用字典记录音频文件、音频特征
    voice_file_dic = {voice_name:[] for voice_name in voice_names}
    voice_feature_dic = {voice_name:None for voice_name in voice_names}

    dir_path = r'C:\Users\Huawei\Desktop\好一个大学\课内学习\大二下\ppppp数据分析\w12\test_audios'

    # 初始化特征处理器
    feature_processor = MultiProcessVoiceFeature(workers=4)
    
    # 计算特征
    for voice_name in voice_names:
        audio_files = [os.path.join(dir_path, f'text_{voice_name}_{i}.wav') for i in range(num_len)]
        features = feature_processor.get_feature(audio_files)
        voice_feature_dic[voice_name] = features
        print(f"{voice_name} 特征: 平均音高={features[0]:.2f}Hz, "
              f"平均声强={features[1]:.2f}dB, 平均语速={features[2]:.2f}词/秒")


'''
    #测试MultiThreadASR
    voice_name = input() #Chelsie（女）Cherry（女） Ethan（男）Serena（女）
    if voice_name not in ['Chelsie','Cherry','Ethan','Serena']:
        print('名称无效')
        sys.exit()

    for i in range(num_len):
        thread = MultiThreadASR(text, i, voice_name)
        threads.append(thread)

    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
'''
    

    
