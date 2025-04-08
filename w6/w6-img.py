from PIL import ImageFilter
from PIL import Image
import os
from w6_ark import print_response
import matplotlib.pyplot as plt
import numpy as np

script_name = os.path.dirname(os.path.abspath(__file__))
filepath = os.path.join(script_name,'test.jpg')

#base class
class ImageProcessor:
    def __init__(self,im,*args):
        #self.image_path = image_path
        self.im = im
        self.params = ()
    def process(self):
        pass

#sub class
#灰度化处理
class GRAY_PROCESSOR(ImageProcessor):
    def process(self):
        return self.im.convert("L")
    
#裁剪或调整大小
class CHANGE_SIZE_PROCESSOR(ImageProcessor):
    
    def process(self):
        #裁剪
        if len(self.params) == 4:
            return self.im.crop(self.params)
        #放缩
        elif len(self.params) == 2:
            return self.im.resize(self.params)
    
#模糊
class BLUR_PROCESSOR(ImageProcessor):
    def process(self):
        return self.im.filter(ImageFilter.BLUR)
    
#边缘提取
class EDGE_PROCESSOR(ImageProcessor):
    def process(self):
        return self.im.filter(ImageFilter.EDGE_ENHANCE_MORE)
    
#调用api
'''
class ImageTextExtractor(ImageProcessor):
    def process(self):
        print_response(self.image_path)

'''

#批量图片处理类
class ImageShop:
    def __init__(self,im_format, im_dir):
        self.im_format = im_format
        self.im_dir = im_dir
        self.im_list = [] #图片实例的列表
        self.processed_ims = [] #处理好的图片
    
    def load_images(self):
        '''
        从路径加载统一格式的图片，返回图片实例的列表
        '''
        for file_name in os.listdir(self.im_dir):
            im_path = os.path.join(self.im_dir,file_name)
            im = Image.open(im_path)
            self.im_list.append(im)

        print(f"{len(self.im_list)}张图片成功加载")
        #检查一下
        #for im in self.im_list:
            #im.show()

    def __batch_ps(self,Processor,args):
        '''
        Processor选择处理方法 返回处理好的图片列表
        '''
        print(args)
        if args == None:
            for im in self.im_list:
                processed_im = Processor(im).process()
                self.processed_ims.append(processed_im)
        else:
            
            for im in self.im_list:
                change_size_processor = CHANGE_SIZE_PROCESSOR(im)
                change_size_processor.params = args
                processed_im = change_size_processor.process()
                self.processed_ims.append(processed_im)
        
        #检查一下
        for processed_im in self.processed_ims:
            processed_im.show()

        return self.processed_ims
        

    def batch_ps(self,*args):
        '''
        输入操作名，参数，调用__batch_ps 返回处理好的图片列表
        '''
        op_name = args[0]
        if len(args) > 1:
            op_params = args[1:]

        if op_name == '灰度化':
            self.__batch_ps(GRAY_PROCESSOR)
        elif op_name == '模糊':
            self.__batch_ps(BLUR_PROCESSOR)
        elif op_name == '边缘提取':
            self.__batch_ps(EDGE_PROCESSOR)
        elif (op_name == '放缩')or (op_name =='裁剪'):
            #CHANGE_SIZE_PROCESSOR.params = op_params
            self.__batch_ps(CHANGE_SIZE_PROCESSOR,op_params)
        
        else:
            ValueError('不合法的操作')


    
    def save(self):
        '''
        图片保存
        '''
        for i in range(len(self.processed_ims)):
            self.processed_ims[i].save(f'处理好的图片{i}.jpg')

        print(f'{i}张图片已成功保存')

    def display(self,rows = None,cols = None, im_size = (10,10),max_show = None):
        '''
        图片展示 params：
        行rows、列cols、图片大小im_size、最多展示数max_show
        '''
        
        #参数默认值除了im_size都是None 如果是默认值就开始计算合适的参数
        if max_show == None:
            max_show = len(self.processed_ims)
        
        im_num = min(len(self.processed_ims),max_show)

        if (rows == None) & (cols == None):
            cols = int(np.ceil(np.sqrt(im_num)))
            rows = int(np.ceil(im_num / cols))
        elif rows == None:
            rows = int(np.ceil(im_num / cols))
        elif cols == None:
            cols = int(np.ceil(im_num / rows))

        #创建图
        fig,ax = plt.subplots(rows,cols,figsize = im_size)
        axes_flat = fig.axes  # 获取所有子图对象的列表
    
        # 遍历所有子图并显示图片或关闭轴
        for i, ax in enumerate(axes_flat):
            if i < im_num:
                ax.imshow(self.processed_ims[i])
            ax.axis('off')  # 关闭所有子图的坐标轴
    
        plt.tight_layout()  # 自动调整子图间距
        plt.show()
    



if __name__ == '__main__':
    image_path = filepath
    im = Image.open(image_path)

    #灰
    gray_processor = GRAY_PROCESSOR(im)
    grayed_img = gray_processor.process()
    #grayed_img.show()
    #grayed_img.save(r'C:\Users\Huawei\Desktop\好一个大学\课内学习\大二下\ppppp数据分析\w6\灰度化.png')

    #裁剪
    change_size_processor = CHANGE_SIZE_PROCESSOR(im)
    change_size_processor.params = (10,10,500,500)
    changed_size_img = change_size_processor.process()
    #changed_size_img.show()
    #changed_size_img.save(r'C:\Users\Huawei\Desktop\好一个大学\课内学习\大二下\ppppp数据分析\w6\裁剪.png')

    #缩小
    change_size_processor.params = (300,300)
    changed_size_img1 = change_size_processor.process()
    #changed_size_img1.show()
    #changed_size_img1.save(r'C:\Users\Huawei\Desktop\好一个大学\课内学习\大二下\ppppp数据分析\w6\缩小.png')

    #放大
    change_size_processor.params = (2000,2000)
    changed_size_img2 = change_size_processor.process()
    #changed_size_img2.show()
    #changed_size_img2.save(r'C:\Users\Huawei\Desktop\好一个大学\课内学习\大二下\ppppp数据分析\w6\放大.png')

    #模糊
    blur_processor = BLUR_PROCESSOR(im)
    blurred_image = blur_processor.process()
    #blurred_image.show()
    #blurred_image.save(r'C:\Users\Huawei\Desktop\好一个大学\课内学习\大二下\ppppp数据分析\w6\模糊.png')

    #边缘提取
    edge_processor = EDGE_PROCESSOR(im)
    edged_image = edge_processor.process()
    #edged_image.show()
    #edged_image.save(r'C:\Users\Huawei\Desktop\好一个大学\课内学习\大二下\ppppp数据分析\w6\边缘提取.png')

    '''
    image_text_extractor = ImageTextExtractor(image_path)
    image_text_extractor.process()
    '''

    #test imageshop
    im_format = 'jpg'
    im_dir = r'C:\Users\Huawei\Desktop\好一个大学\课内学习\大二下\ppppp数据分析\w6\immage'
    imageshop = ImageShop(im_format,im_dir)

    imageshop.load_images()
    #imageshop.batch_ps('模糊')
    imageshop.batch_ps('放缩',100,100)
    imageshop.display(rows = 3)#rows = 2,cols = 3)







