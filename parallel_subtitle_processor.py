#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
并行视频字幕预处理系统
支持多视频并行转录和翻译，大幅提升处理效率
"""

import os
import json
import asyncio
import aiohttp
from pathlib import Path
import time
from datetime import datetime
import logging
from concurrent.futures import ThreadPoolExecutor
import queue
import threading

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ParallelSubtitleProcessor:
    def __init__(self, downloads_path, output_path, max_transcribe_workers=3, max_translate_workers=5):
        self.downloads_path = Path(downloads_path)
        # output_path现在不再使用，因为字幕文件直接保存在视频同目录
        self.output_path = None
        self.whisper_api_url = "http://localhost:5000"
        
        # 并发控制
        self.max_transcribe_workers = max_transcribe_workers  # 转录并发数
        self.max_translate_workers = max_translate_workers    # 翻译并发数
        
        # 统计信息
        self.processed_count = 0
        self.failed_count = 0
        self.skipped_count = 0
        self.transcribe_queue = asyncio.Queue()
        self.translate_queue = asyncio.Queue()
        
        # 注意：现在字幕文件直接保存在视频同目录，不需要创建额外目录
        
        # 进度跟踪
        self.total_videos = 0
        self.transcribe_completed = 0
        self.translate_completed = 0
        
    def scan_video_files(self):
        """扫描所有视频文件"""
        video_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.webm'}
        video_files = []
        
        for channel_dir in self.downloads_path.iterdir():
            if channel_dir.is_dir():
                logger.info(f"📁 扫描频道: {channel_dir.name}")
                
                for file_path in channel_dir.iterdir():
                    if file_path.suffix.lower() in video_extensions:
                        # 检查是否已有处理过的字幕文件
                        subtitle_file = self.get_subtitle_path(file_path)
                        
                        if not subtitle_file.exists():
                            video_files.append({
                                'path': file_path,
                                'channel': channel_dir.name,
                                'name': file_path.stem,
                                'size_mb': file_path.stat().st_size / (1024 * 1024)
                            })
                        else:
                            logger.info(f"⏭️  跳过已处理: {file_path.name}")
                            self.skipped_count += 1
        
        return video_files
    
    def get_subtitle_path(self, video_path):
        """获取字幕文件路径 - 保存在视频同目录，文件名相同"""
        # 直接保存在视频文件的同一目录，文件名与视频相同
        return video_path.parent / f"{video_path.stem}.json"
    

    
    async def check_whisper_service(self):
        """检查Whisper服务是否可用"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.whisper_api_url}/health") as response:
                    if response.status == 200:
                        data = await response.json()
                        logger.info(f"✅ Whisper服务正常: {data.get('version', 'unknown')}")
                        return True
        except Exception as e:
            logger.error(f"❌ Whisper服务不可用: {e}")
            return False
        
        return False
    
    async def transcribe_worker(self, worker_id):
        """转录工作线程"""
        logger.info(f"🤖 转录工作线程 {worker_id} 启动")
        
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=3600)) as session:
            while True:
                try:
                    # 从队列获取任务
                    video_info = await asyncio.wait_for(self.transcribe_queue.get(), timeout=1.0)
                    
                    logger.info(f"🎬 [转录-{worker_id}] 开始处理: {video_info['name']}")
                    
                    # 执行转录
                    subtitles = await self.transcribe_video(video_info, session)
                    
                    if subtitles:
                        self.transcribe_completed += 1
                        logger.info(f"✅ [转录-{worker_id}] 完成: {video_info['name']} ({len(subtitles)} 条字幕)")
                        
                        # 将结果放入翻译队列
                        await self.translate_queue.put({
                            'video_info': video_info,
                            'subtitles': subtitles
                        })
                    else:
                        self.failed_count += 1
                        logger.error(f"❌ [转录-{worker_id}] 失败: {video_info['name']}")
                    
                    # 标记任务完成
                    self.transcribe_queue.task_done()
                    
                except asyncio.TimeoutError:
                    # 队列为空，继续等待
                    continue
                except Exception as e:
                    logger.error(f"❌ [转录-{worker_id}] 错误: {e}")
                    self.transcribe_queue.task_done()
    
    async def translate_worker(self, worker_id):
        """翻译工作线程"""
        logger.info(f"🌐 翻译工作线程 {worker_id} 启动")
        
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=1800)) as session:
            while True:
                try:
                    # 从队列获取任务
                    task_data = await asyncio.wait_for(self.translate_queue.get(), timeout=1.0)
                    
                    video_info = task_data['video_info']
                    subtitles = task_data['subtitles']
                    
                    logger.info(f"🌐 [翻译-{worker_id}] 开始翻译: {video_info['name']}")
                    
                    # 执行翻译
                    bilingual_subtitles = await self.translate_subtitles(subtitles, session)
                    
                    # 保存结果
                    success = await self.save_subtitle_file(video_info, bilingual_subtitles)
                    
                    if success:
                        self.processed_count += 1
                        self.translate_completed += 1
                        logger.info(f"✅ [翻译-{worker_id}] 完成: {video_info['name']}")
                    else:
                        self.failed_count += 1
                        logger.error(f"❌ [翻译-{worker_id}] 保存失败: {video_info['name']}")
                    
                    # 标记任务完成
                    self.translate_queue.task_done()
                    
                except asyncio.TimeoutError:
                    # 队列为空，继续等待
                    continue
                except Exception as e:
                    logger.error(f"❌ [翻译-{worker_id}] 错误: {e}")
                    self.translate_queue.task_done()
    
    async def progress_monitor(self):
        """进度监控"""
        while True:
            await asyncio.sleep(10)  # 每10秒更新一次
            
            transcribe_pending = self.transcribe_queue.qsize()
            translate_pending = self.translate_queue.qsize()
            
            logger.info(f"📊 进度报告:")
            logger.info(f"   转录: 完成 {self.transcribe_completed}/{self.total_videos}, 队列 {transcribe_pending}")
            logger.info(f"   翻译: 完成 {self.translate_completed}/{self.total_videos}, 队列 {translate_pending}")
            logger.info(f"   总体: 成功 {self.processed_count}, 失败 {self.failed_count}")
            
            # 检查是否全部完成
            if (self.transcribe_completed + self.failed_count >= self.total_videos and 
                translate_pending == 0 and self.translate_queue.empty()):
                logger.info("🎉 所有任务处理完成！")
                break
    
    async def transcribe_video(self, video_info, session):
        """转录单个视频"""
        try:
            video_path = video_info['path']
            
            # 读取视频文件
            with open(video_path, 'rb') as f:
                video_data = f.read()
            
            # 准备表单数据
            data = aiohttp.FormData()
            data.add_field('audio', video_data, filename=video_path.name, content_type='video/mp4')
            data.add_field('language', 'en')
            
            # 调用API
            async with session.post(f"{self.whisper_api_url}/transcribe", data=data) as response:
                if response.status == 200:
                    result = await response.json()
                    if result.get('success'):
                        return result['result']['segments']
                
                logger.error(f"转录API返回错误: {response.status}")
                return None
                
        except Exception as e:
            logger.error(f"转录失败: {e}")
            return None
    
    async def translate_subtitles(self, subtitles, session):
        """翻译字幕"""
        bilingual_subtitles = []
        
        # 批量翻译，提高效率
        batch_size = 5
        for i in range(0, len(subtitles), batch_size):
            batch = subtitles[i:i + batch_size]
            
            # 并行翻译这一批
            tasks = [self.translate_text(sub['text'], session) for sub in batch]
            translations = await asyncio.gather(*tasks, return_exceptions=True)
            
            # 处理结果
            for subtitle, translation in zip(batch, translations):
                if isinstance(translation, Exception):
                    translation = f"[翻译失败] {subtitle['text']}"
                
                bilingual_subtitles.append({
                    'start': subtitle['start'],
                    'end': subtitle['end'],
                    'text': subtitle['text'],
                    'chinese': translation
                })
            
            # 避免API限制
            await asyncio.sleep(0.2)
        
        return bilingual_subtitles
    
    async def translate_text(self, text, session):
        """翻译单条文本"""
        try:
            # 使用MyMemory API
            url = f"https://api.mymemory.translated.net/get?q={text}&langpair=en|zh"
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get('responseStatus') == 200:
                        translation = data['responseData']['translatedText']
                        if translation and 'MYMEMORY WARNING' not in translation:
                            return translation
            
            return f"[中文] {text}"
            
        except Exception:
            return f"[翻译失败] {text}"
    
    async def save_subtitle_file(self, video_info, bilingual_subtitles):
        """保存字幕文件到视频同目录"""
        try:
            subtitle_path = self.get_subtitle_path(video_info['path'])
            # 不需要创建目录，因为保存在视频同目录
            
            subtitle_data = {
                'video_info': {
                    'filename': video_info['path'].name,
                    'channel': video_info['channel'],
                    'processed_at': datetime.now().isoformat(),
                    'duration': self.calculate_duration(bilingual_subtitles)
                },
                'subtitles': bilingual_subtitles
            }
            
            with open(subtitle_path, 'w', encoding='utf-8') as f:
                json.dump(subtitle_data, f, ensure_ascii=False, indent=2)
            
            return True
            
        except Exception as e:
            logger.error(f"保存文件失败: {e}")
            return False
    
    def calculate_duration(self, subtitles):
        """计算视频总时长"""
        if not subtitles:
            return 0
        return max(sub['end'] for sub in subtitles)
    
    async def run(self):
        """运行并行处理"""
        logger.info("🚀 并行视频字幕预处理系统")
        logger.info("=" * 50)
        
        # 检查Whisper服务
        if not await self.check_whisper_service():
            logger.error("❌ 请先启动Whisper服务器")
            return
        
        # 扫描视频文件
        logger.info("📁 扫描视频文件...")
        video_files = self.scan_video_files()
        
        if not video_files:
            logger.info("✅ 所有视频都已处理完成！")
            return
        
        self.total_videos = len(video_files)
        
        logger.info(f"📊 扫描结果:")
        logger.info(f"   待处理视频: {len(video_files)} 个")
        logger.info(f"   已跳过视频: {self.skipped_count} 个")
        
        total_size = sum(v['size_mb'] for v in video_files)
        logger.info(f"   总大小: {total_size:.1f}MB")
        logger.info(f"   转录并发数: {self.max_transcribe_workers}")
        logger.info(f"   翻译并发数: {self.max_translate_workers}")
        
        # 确认处理
        response = input(f"\n是否开始并行处理这 {len(video_files)} 个视频？ (y/n): ")
        if response.lower() != 'y':
            logger.info("❌ 用户取消处理")
            return
        
        # 将所有视频加入转录队列
        for video_info in video_files:
            await self.transcribe_queue.put(video_info)
        
        logger.info(f"🚀 开始并行处理...")
        start_time = time.time()
        
        # 启动工作线程
        tasks = []
        
        # 启动转录工作线程
        for i in range(self.max_transcribe_workers):
            task = asyncio.create_task(self.transcribe_worker(i + 1))
            tasks.append(task)
        
        # 启动翻译工作线程
        for i in range(self.max_translate_workers):
            task = asyncio.create_task(self.translate_worker(i + 1))
            tasks.append(task)
        
        # 启动进度监控
        monitor_task = asyncio.create_task(self.progress_monitor())
        tasks.append(monitor_task)
        
        # 等待所有转录任务完成
        await self.transcribe_queue.join()
        
        # 等待所有翻译任务完成
        await self.translate_queue.join()
        
        # 取消所有任务
        for task in tasks:
            task.cancel()
        
        # 处理完成统计
        end_time = time.time()
        duration = end_time - start_time
        
        logger.info(f"🎉 并行处理完成！")
        logger.info(f"⏱️  总耗时: {duration/60:.1f} 分钟")
        logger.info(f"✅ 成功处理: {self.processed_count} 个")
        logger.info(f"❌ 处理失败: {self.failed_count} 个")
        logger.info(f"⏭️  跳过文件: {self.skipped_count} 个")
        logger.info(f"🚀 平均速度: {self.processed_count/(duration/60):.1f} 个/分钟")

if __name__ == "__main__":
    # 配置路径
    downloads_path = "../youtube-downloader/downloads"

    # 创建处理器 - 可以调整并发数
    # output_path参数不再使用，传入None即可
    processor = ParallelSubtitleProcessor(
        downloads_path,
        None,  # output_path不再使用
        max_transcribe_workers=2,  # 转录并发数：2个视频同时转录（避免资源竞争）
        max_translate_workers=4    # 翻译并发数：4个翻译任务同时进行（平衡效率）
    )
    
    # 运行处理
    asyncio.run(processor.run())
