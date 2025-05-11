import whisper
import zipfile
from multiprocessing import Process
import os


#解压文件
def unzip(file_path):
    folder_name = os.path.splitext(os.path.basename(file_path))[0]
    extract_path = os.path.join(os.getcwd(), folder_name)
    
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)
    
    print('解压完成')
    return extract_path

#语音转文本
def w2t(audiofile):
    whisper_md = whisper.load_model('base')  #内存不够了 
    result = whisper_md.transcribe(audiofile)
    return result['text']

#写文件
def save_text_file(text, filename):
    with open(filename, 'w') as file:
        file.write(text)

def write_text(start,end,file_list):
    for i in range(start, end):
        text = w2t(file_list[i])
        print(f'正在处理第{i+1}个文件')
        #print(text)
        save_text_file(text, f'audio{i}.txt')

class TASK(Process):
    def __init__(self, start, end, file_list):
        super().__init__()
        self._start = start
        self._end = end
        self._file_list = file_list

    def run(self):
        write_text(self._start, self._end, self._file_list)

def main1():
    #读取声音文件
    #zip_file = r'C:\Users\Huawei\Desktop\好一个大学\课内学习\大二下\ppppp数据分析\w11\live_voice.zip'
    #folder_list = os.listdir(unzip(zip_file))
    folder_list = os.scandir(r'C:\Users\Huawei\Desktop\好一个大学\课内学习\大二下\ppppp数据分析\w11\voice')
    file_list = []
    for folder in folder_list:
        for file in os.scandir(folder):
            file_list.append(file.path)
    #num = len(file_list)
    #print('文件数量为{}'.format(num))

    #文件数量为20
    #进程数取5 则chunk_size = 4
    chunk_size = 4
    #1.直接使用process类构建紫禁城
    processes = []
    for i in range(0, 20, chunk_size):
        start = i
        end = i+chunk_size
        p = Process(target=write_text, args = (start, end, file_list))
        processes.append(p)

    for p in processes:
        p.start()
        pass
    for p in processes:
        p.join()
        pass
    print('文件已全部处理完毕')

def main2():
    #读取声音文件
    #zip_file = r'C:\Users\Huawei\Desktop\好一个大学\课内学习\大二下\ppppp数据分析\w11\live_voice.zip'
    #folder_list = os.listdir(unzip(zip_file))
    folder_list = os.scandir(r'C:\Users\Huawei\Desktop\好一个大学\课内学习\大二下\ppppp数据分析\w11\voice')
    file_list = []
    for folder in folder_list:
        for file in os.scandir(folder):
            file_list.append(file.path)
    #num = len(file_list)
    #print('文件数量为{}'.format(num))

    #文件数量为20
    #进程数取5 则chunk_size = 4
    chunk_size = 4
    processes = []
    for i in range(0, 20, chunk_size):
        start = i
        end = i+chunk_size
        p = TASK(start, end, file_list)
        processes.append(p)

    for p in processes:
        p.start()
        pass
    for p in processes:
        p.join()
        pass
    print('文件已全部处理完毕')

if __name__ == "__main__":
    main2()
