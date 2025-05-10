import abc
import numpy as np
import matplotlib.pyplot as plt
import librosa
import librosa.display

class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
class Plotter(metaclass = abc.ABCMeta):
    @abc.abstractmethod
    def plot(data, *args, **kwargs):
        pass

class PointPlotter(Plotter):
    def __init__(self):
        pass

    def plot(self,args):
        x = []
        y = []
        for point in args:
            x.append(point.x)
            y.append(point.y)
        plt.scatter(x,y,linewidths=0.1)
        plt.title('pointplotter')
        plt.grid()
        plt.show()

class AudioPlotter(Plotter):
    def plot(self, y, sr):
        #波形图
        fig, ax = plt.subplots(nrows=1)
        librosa.display.waveshow(y[:25000], sr=sr, ax=ax, color = 'blue')
        ax.set(title = 'envelop view')
        ax.label_outer()
        plt.show()
        plt.close()

        #能谱图
        fig, ax = plt.subplots(nrows=1, ncols=1, sharex=True)
        D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
        img = librosa.display.specshow(D, y_axis='linear', x_axis='time', sr=sr, ax=ax)
        ax.set(title='Linear-frequency power spectrogram')
        ax.label_outer()
        fig.colorbar(img, ax=ax, format="%+2.f dB")
        plt.show()
        plt.close()
        

if __name__ == '__main__':
    #test pointplotter
    pointplotter = PointPlotter()
    lis_point = []
    for i in np.linspace(0,10,100):
        lis_point.append(Point(i,i))
    pointplotter.plot(lis_point)

    #test audioplotter
    audioplotter = AudioPlotter()
    sound_path = r'C:\Users\Huawei\Desktop\好一个大学\课内学习\大二下\ppppp数据分析\w10\w10-demo\test.mp3'
    y, sr = librosa.load(sound_path)
    audioplotter.plot(y, sr)


        
