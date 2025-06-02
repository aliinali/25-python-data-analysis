# 网络分发视频数据
> 根据视频数据传输的演示例子（campost.py, camrecive.py），实现一个简单的监控服务程序。

## 1. CampostServer
> 实现一个支持多线程的服务器类CampostServer，当客户端连入时启动一个新的线程为其传输视频。

```python

class CampostServer:
    def __init__(self, host='0.0.0.0', port=9999):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.clients = {}  # 存储客户端信息: {客户端地址: 线程对象}
        self.log_file = "server_log.txt" 
        self.rsize = 65000 
        self.server_socket.bind((self.host, self.port))
        
    def log(self, message):
        '''
        日志记录
        '''
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        print(log_entry)
        with open(self.log_file, 'a') as f:
            f.write(log_entry + '\n')

    def handle_client(self, client_address):
        #打开摄像头
        camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        camera.set(cv2.CAP_PROP_FPS, 25) 
        self.log(f"客户端 {client_address} 已连接")

        try:
            while True:
                ret, frame = camera.read()
                if not ret or frame is None:
                    self.log("无效帧")
                    time.sleep(1)
                    continue
                self.send_frame(frame, client_address)
                time.sleep(0.04)  # 帧率为25fps

        except Exception as e:
            self.log(f"客户端 {client_address} 错误: {str(e)}")
        finally:
            if client_address in self.clients:
                del self.clients[client_address]
            camera.release()  
            self.log(f"客户端 {client_address} 已断开连接")
            
    def send_frame(self, frame, client_address):
        '''
        发送帧到客户端
        '''
        try:
            if len(frame.shape) == 2:
                frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
            img_encode = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 85])[1]
            data_encode = np.array(img_encode)
            data = data_encode.tobytes()
            start = 0
            while start < len(data):
                end = min(start + self.rsize, len(data))
                packet = data[start:end]
                self.server_socket.sendto(packet, client_address)
                start = end
        except Exception as e:
            self.log(f"发送帧到 {client_address} 失败: {str(e)}")

    def start(self):
        self.log('-'*50)
        self.log("服务器已启动，等待客户端连接...")
        try:
            while True:
                data, client_address = self.server_socket.recvfrom(1024)
                if client_address not in self.clients:
                    client_thread = threading.Thread(
                        target=self.handle_client, 
                        args=(client_address,), 
                        daemon=True
                    )
                    self.clients[client_address] = client_thread
                    client_thread.start()
        except KeyboardInterrupt:
            self.log("服务器正在关闭...")
        finally:
            self.server_socket.close()
            self.log("服务器已关闭")
```


## 2.CamreiveClient
> 实现一个客户端类CamreiveClient，连接服务器并获取视频流。注意，测试时要建立多个客户端以测试服务器类的并发能力。
```python

class CamreiveClient:
    def __init__(self, server_host, server_port, save_dir='recordings'):
        self.server_host = server_host
        self.server_port = server_port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.rsize = 65000
        self.save_dir = save_dir
        self.video_writer = None
        self.start_time = None
        self.duration = 60  # 为方便测试改成1min
        self.frame_width = 640
        self.frame_height = 480
        self.fps = 25  # 与服务器帧率一致
        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # MP4编码
        os.makedirs(save_dir, exist_ok=True)
        
    def get_new_filename(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return os.path.join(self.save_dir, f"recording_{timestamp}.mp4") 
        
    def init_video_writer(self):
        filename = self.get_new_filename()
        try:
            self.video_writer = cv2.VideoWriter(
                filename, 
                self.fourcc, 
                self.fps, 
                (self.frame_width, self.frame_height),
                isColor=True
            )
            self.start_time = time.time()
            self.log(f"新建视频文件：{filename}")
        except Exception as e:
            print(f"创建视频写入器失败: {str(e)}")
            
    def log(self, message):
        print(f"[CLIENT] {message}")

    def save_frame(self, frame):
        if frame is None:
            return
        if self.video_writer is None:
            self.init_video_writer()
            if self.video_writer is None:  # 防止初始化失败
                return
            
        try:
            self.video_writer.write(frame)
        except Exception as e:
            print(f"写入帧失败: {str(e)}")
        
        # 检查是否需要切换文件
        if time.time() - self.start_time >= self.duration:
            try:
                self.video_writer.release()
                self.video_writer = None  # 触发重新初始化
            except Exception as e:
                print(f"关闭视频文件失败: {str(e)}")

    def receive_stream(self):
        self.client_socket.sendto(b'CONNECT', (self.server_host, self.server_port))
        self.log(f"连接到服务器 {self.server_host}:{self.server_port}")
        try:
            while True:
                data, addr = self.client_socket.recvfrom(self.rsize)
                if not data:
                    break
                    
                nparr = np.frombuffer(data, np.uint8)
                frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                
                if frame is None:
                    print("空帧，跳过写入")
                    continue
                
                self.save_frame(frame)
                cv2.imshow('Remote Camera', frame)
                
                #esc键
                if cv2.waitKey(1) & 0xFF == 27:
                    self.log("用户按下ESC键，准备退出")
                    break
        except Exception as e:
            print(f"接收视频流时出错: {str(e)}")
        finally:
            if self.video_writer:
                try:
                    self.video_writer.release()
                except:
                    pass
            self.client_socket.close()
            cv2.destroyAllWindows()
            self.log("客户端已退出")


```
## 3. 日志记录
> 服务器类CampostServer中应有一个方法来记录客户端接入的日志（哪个客户端，何时接入或何时离开）；客户端类CamreceiveClient应有一个方法，其能够按一定时长存储视频流（比如每10分钟存储一个文件）。

见上面两个类，实际为了方便测试，设置1分钟存储一个文件


## 测试
```python

if __name__ == "__main__":
    if sys.argv[1] == 'server':
        server = CampostServer()
        server.start()
        
    elif sys.argv[1] == 'client':
        client = CamreiveClient(
            server_host=sys.argv[2],
            server_port=int(sys.argv[3])
        )
        client.receive_stream()
```

#### ps

截止目前（25-6-2-19:05）没找到合适的人和我一起运行多线程（包括但不限于：网不通等），所以先把目前的测试结果写一下

## 输出
![client终端](https://gitee.com/aliinali/25_data_analysis_pics/raw/master/w14/client.png)

log文件：
![log文件](https://gitee.com/aliinali/25_data_analysis_pics/raw/master/w14/日志.jpg)

保存的视频： 可以正常播放
![视频](https://gitee.com/aliinali/25_data_analysis_pics/raw/master/w14/视频.png)

感谢hzh同学
![视频](https://gitee.com/aliinali/25_data_analysis_pics/raw/master/w14/视频2.png)

#### 更新（25-6-2-23:12）
运行了多线程

再次感谢hzh同学
![hzh](https://gitee.com/aliinali/25_data_analysis_pics/raw/master/w14/hzh3.png)
