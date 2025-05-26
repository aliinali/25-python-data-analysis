import gevent
from gevent import monkey,pool
#monkey.patch_all()
import aiofiles
import aiohttp
import asyncio

import requests
import json
import os
from ffmpy import FFmpeg
import subprocess
import matplotlib.pyplot as plt

from dashscope import MultiModalConversation
from openai import OpenAI
from ali_key import ALI_KEY
from ds_key import DS_KEY
import time
from datetime import datetime, timedelta


#读取视频文件列表
file_path = r'C:\Users\Huawei\Desktop\好一个大学\课内学习\大二下\ppppp数据分析\w13\bh_videos_links.txt'
with open (file_path,'r') as f:
    urls = [line.strip() for line in f.readlines()]

#检查状态
async def fetch(session, url, save_path):
    print(f'begin to download {url}')
    try:
        async with session.get(url) as response:
            async with aiofiles.open(save_path, 'wb') as f:
                async for chunk in response.content.iter_chunked(1024*1024):  # 1MB分块写入
                    await f.write(chunk)
            return url, response.status
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return url, None


#使用aiofiles下载文件
def save_videos(url,save_path):
    try:
        response = requests.get(url)
        response.raise_for_status()  # 检查请求是否成功
        with open(save_path, 'wb') as f:
            f.write(response.content)
        print(f"视频已保存至：{save_path}")
    except Exception as e:
        print(f"视频{save_path}下载失败：{str(e)}")

#使用gevent+aiofiles实现视频文件下载
def main1():
    p = pool.Pool(10)
    save_paths = [r'F:\gevent_videos\{}.mp4'.format(i) for i in range(1,len(urls)+1)]
    jobs=[p.spawn(save_videos,url,save_path) for url,save_path in zip(urls,save_paths)]
    gevent.joinall(jobs,timeout=10)

    
#使用aiohttp+aiofiles实现视频文件下载
async def download_urls(urls, limit = 10):
    save_paths = [r'F:\aiohttp_videos\{}.mp4'.format(i) for i in range(1,len(urls)+1)]
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url, save_path in zip(urls, save_paths):
            task = asyncio.create_task(fetch(session, url, save_path))
            tasks.append(task)
            # 控制每组最多limit个并发任务
            if len(tasks) >= limit:
                results = await asyncio.gather(*tasks)
                for result in results:
                    print(f"URL: {result[0]}, Status: {result[1]}")
                tasks.clear()
        
        # 处理剩余的任务
        if tasks:
            results = await asyncio.gather(*tasks)
            for result in results:
                print(f"URL: {result[0]}, Status: {result[1]}")

def main2(urls,limit):
    asyncio.run(download_urls(urls,limit = limit))

#计算视频时长
def get_video_duration(file_path):
    """
    获取视频基本信息，包括时长、分辨率等。
    依赖 ffprobe 工具。
    """
    cmd = [
        'ffprobe',
        '-v', 'error',
        '-print_format', 'json',
        '-show_format',
        '-show_streams',
        file_path
    ]

    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        info = json.loads(result.stdout)
    
        # 尝试获取所有可能的时长信息
        format_duration = float(info['format']['duration'])
        video_duration = None
        for stream in info.get('streams', []):
            if stream.get('codec_type') == 'video' and 'duration' in stream:
                video_duration = float(stream['duration'])
                break
        
        final_duration = video_duration if video_duration is not None else format_duration

        return final_duration
        
    except subprocess.CalledProcessError as e:
        print("ffprobe 执行出错:", e.stderr)
        return None
    except (KeyError, ValueError) as e:
        print("解析视频信息出错:", e)
        return None

def vis(file_paths):
    global durations
    durations = []
    dir_path = r'F:\aiohttp_videos'
    i = 0
    #file_paths中的文件顺序和durations对应文件顺序不一样
    for file_path in file_paths:
        video_path = os.path.join(dir_path, file_path)
        duration = get_video_duration(video_path)
        durations.append(duration)
        i += 1
        if i%100 == 0:
            print(f'mark-{i}')
    
    with open ('durations.json', 'w') as f:
        json.dump(durations, f)


    print('时长已全部计算完毕，开始画图')
    plt.scatter(list(range(1,len(durations)+1)), durations, linewidths= 0.3)
    plt.ylabel('time')
    plt.xlabel('videos')
    plt.grid()
    plt.title('video time')
    #plt.show()

#计算视频时长并画图
def main3():
    file_paths = os.listdir(r'F:\aiohttp_videos')
    vis(file_paths)

#视频按时长排序
def sort_videos(durations):
    '''
    对视频长度进行排序，返回最短的10个视频名称（i）
    '''
    video_time = [(video, time) for video,time in zip(list(range(1,len(durations)+1)), durations)]
    sorted_video_time = sorted(video_time, key= lambda x:x[1], reverse = False)
    #print(sorted_video_time)
    smallest_videos = [sorted_video_time[x][0] for x in range(10)]
    #print('smallest videos',smallest_videos)
    return smallest_videos

#内容理解

#总结视频主题
def get_video_topic():
    with open ('infos.json', 'r') as f:
        infos = json.load(f)

    client = OpenAI(api_key=DS_KEY, base_url="https://api.deepseek.com")
    
    topics = []
    for info in infos:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "你是一个视频内容总结助手，请用5-10个字概括视频主题"},
                {"role": "user", "content": f"请总结以下视频内容的主题：{info}"}
            ],
            temperature=0.3,
            max_tokens=10
        )
        topics.append(response.choices[0].message.content.strip())
    
    return topics

def get_video_info(durations):
    '''
    对最短的10个视频应用ali大模型进行内容理解，返回10个info的list infos
    增加了精确的请求频率控制，确保不超过15 QPM
    '''
    smallest_videos = sort_videos(durations)
    infos = []
    file_paths = os.listdir(r'F:\aiohttp_videos')
    dir_path = r'F:\aiohttp_videos'
    
    # 请求计数器和时间记录
    request_times = []
    
    for video in smallest_videos:
        file_path = file_paths[video-1]
        video_path = os.path.join(dir_path,file_path)
        
        # 获取视频文件大小(MB)
        file_size = os.path.getsize(video_path) / (1024 * 1024)
        
        print(f'开始处理视频，大小: {file_size:.2f}MB)')
        # 精确控制请求频率
        current_time = datetime.now()
        # 移除一分钟前的请求记录
        request_times = [t for t in request_times if (current_time - t) <= timedelta(minutes=1)]
        
        # 如果一分钟内请求数达到15，等待足够时间
        if len(request_times) >= 15:
            oldest_request = request_times[0]
            wait_seconds = 60 - (current_time - oldest_request).total_seconds() + 1
            print(f"已达到QPM限制，等待 {wait_seconds:.1f} 秒...")
            time.sleep(wait_seconds)
        
        # 记录当前请求时间
        request_times.append(datetime.now())
        
        # 准备API请求
        messages = [
            {'role': 'system', 'content': [{'text': 'You are a helpful assistant.'}]},
            {'role': 'user', 'content': [
                {'video': video_path, "fps": 2},
                {'text': '详细描述视频内容。'}
            ]}
        ]
        
        try:
            # 调用API
            response = MultiModalConversation.call(
                api_key=ALI_KEY,
                model='qwen-vl-max-latest',
                messages=messages
            )
            
            # 详细的响应检查
            if response is None:
                error_msg = f"API调用返回None，视频: {video_path}"
                print(f"警告: {error_msg}")
                continue
                
            if "output" not in response or "choices" not in response.get("output", {}):
                error_msg = f"API响应格式异常，视频: {video_path}"
                print(f"警告: {error_msg}")
                print(f"响应内容: {response}")
                continue
                
            # 提取信息
            info = response["output"]["choices"][0]["message"].content[0]["text"]
            infos.append(info)
            print("成功获取视频信息")
            
        except Exception as e:
            error_msg = f"处理视频 {video_path} 时发生异常: {str(e)}"
            print(f"错误: {error_msg}")

    with open ('infos.json','w') as f:
        json.dump(infos, f)

    return infos

def main4():
    with open ('durations.json', 'r') as f:
        durations = json.load(f)
    #print(durations)
    for i in range(len(durations)):
        if durations[i] == None:
            durations[i] = 100000000000

    infos = get_video_info(durations)
    topics = get_video_topic()
    
    for info, topic in zip(infos, topics):
        print('视频内容:')
        print(info)
        print('视频主题')
        print(topic)
        print('-'*50)


#main1()
#main2(urls, limit= 3)
#main3()
#vis(file_paths = os.listdir(r'F:\aiohttp_videos'))
main4()

#file_paths = os.listdir(r'F:\aiohttp_videos')
#print(file_paths)


