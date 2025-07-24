#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量视频字幕预处理系统
自动为所有视频生成双语字幕文件
"""

import os
import json
import asyncio
import aiohttp
from pathlib import Path
import time
from datetime import datetime

class BatchSubtitleProcessor:
    def __init__(self, downloads_path, output_path):
        self.downloads_path = Path(downloads_path)
        self.output_path = Path(output_path)
        self.whisper_api_url = "http://localhost:5000"
        self.processed_count = 0
        self.failed_count = 0
        self.skipped_count = 0
        
        # 创建输出目录
        self.output_path.mkdir(exist_ok=True)
        
    def scan_video_files(self):
        """扫描所有视频文件"""
        video_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.webm'}
        video_files = []
        
        for channel_dir in self.downloads_path.iterdir():
            if channel_dir.is_dir():
                print(f"📁 扫描频道: {channel_dir.name}")
                
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
                            print(f"⏭️  跳过已处理: {file_path.name}")
                            self.skipped_count += 1
        
        return video_files
    
    def get_subtitle_path(self, video_path):
        """获取字幕文件路径"""
        channel_name = video_path.parent.name
        safe_filename = self.sanitize_filename(video_path.stem)
        return self.output_path / channel_name / f"{safe_filename}.json"
    
    def sanitize_filename(self, filename):
        """清理文件名，移除特殊字符"""
        import re
        # 移除或替换特殊字符
        filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
        filename = re.sub(r'[：｜？]', '_', filename)
        return filename[:100]  # 限制长度
    
    async def check_whisper_service(self):
        """检查Whisper服务是否可用"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.whisper_api_url}/health") as response:
                    if response.status == 200:
                        data = await response.json()
                        print(f"✅ Whisper服务正常: {data.get('version', 'unknown')}")
                        return True
        except Exception as e:
            print(f"❌ Whisper服务不可用: {e}")
            return False
        
        return False
    
    async def process_video(self, video_info, session):
        """处理单个视频"""
        video_path = video_info['path']
        print(f"\n🎬 处理视频: {video_info['name']}")
        print(f"📁 频道: {video_info['channel']}")
        print(f"📏 大小: {video_info['size_mb']:.1f}MB")
        
        try:
            # 1. 生成英文字幕
            print("🤖 开始AI转录...")
            english_subtitles = await self.transcribe_video(video_path, session)
            
            if not english_subtitles:
                raise Exception("AI转录失败")
            
            print(f"✅ 英文字幕生成完成: {len(english_subtitles)} 条")
            
            # 2. 翻译为中文
            print("🌐 开始翻译...")
            bilingual_subtitles = await self.translate_subtitles(english_subtitles, session)
            
            print(f"✅ 中文翻译完成: {len(bilingual_subtitles)} 条")
            
            # 3. 保存字幕文件
            subtitle_path = self.get_subtitle_path(video_path)
            subtitle_path.parent.mkdir(parents=True, exist_ok=True)
            
            subtitle_data = {
                'video_info': {
                    'filename': video_path.name,
                    'channel': video_info['channel'],
                    'processed_at': datetime.now().isoformat(),
                    'duration': self.calculate_duration(bilingual_subtitles)
                },
                'subtitles': bilingual_subtitles
            }
            
            with open(subtitle_path, 'w', encoding='utf-8') as f:
                json.dump(subtitle_data, f, ensure_ascii=False, indent=2)
            
            print(f"💾 字幕文件已保存: {subtitle_path}")
            self.processed_count += 1
            
        except Exception as e:
            print(f"❌ 处理失败: {e}")
            self.failed_count += 1
    
    async def transcribe_video(self, video_path, session):
        """调用Whisper API转录视频"""
        try:
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
                
                raise Exception(f"API返回错误: {response.status}")
                
        except Exception as e:
            print(f"转录API调用失败: {e}")
            return None
    
    async def translate_subtitles(self, subtitles, session):
        """翻译字幕"""
        bilingual_subtitles = []
        
        for i, subtitle in enumerate(subtitles):
            try:
                # 调用翻译API
                translation = await self.translate_text(subtitle['text'], session)
                
                bilingual_subtitles.append({
                    'start': subtitle['start'],
                    'end': subtitle['end'],
                    'text': subtitle['text'],
                    'chinese': translation
                })
                
                # 避免API限制
                if i % 5 == 0:
                    await asyncio.sleep(0.5)
                    
            except Exception as e:
                print(f"翻译失败 {i+1}: {e}")
                bilingual_subtitles.append({
                    'start': subtitle['start'],
                    'end': subtitle['end'],
                    'text': subtitle['text'],
                    'chinese': f"[翻译失败] {subtitle['text']}"
                })
        
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
                        if translation and not 'MYMEMORY WARNING' in translation:
                            return translation
            
            # 降级方案
            return f"[中文] {text}"
            
        except Exception:
            return f"[翻译失败] {text}"
    
    def calculate_duration(self, subtitles):
        """计算视频总时长"""
        if not subtitles:
            return 0
        return max(sub['end'] for sub in subtitles)
    
    async def run(self):
        """运行批量处理"""
        print("🚀 批量视频字幕预处理系统")
        print("=" * 50)
        
        # 检查Whisper服务
        if not await self.check_whisper_service():
            print("❌ 请先启动Whisper服务器")
            return
        
        # 扫描视频文件
        print("\n📁 扫描视频文件...")
        video_files = self.scan_video_files()
        
        if not video_files:
            print("✅ 所有视频都已处理完成！")
            return
        
        print(f"\n📊 扫描结果:")
        print(f"   待处理视频: {len(video_files)} 个")
        print(f"   已跳过视频: {self.skipped_count} 个")
        
        total_size = sum(v['size_mb'] for v in video_files)
        print(f"   总大小: {total_size:.1f}MB")
        
        # 确认处理
        response = input(f"\n是否开始处理这 {len(video_files)} 个视频？ (y/n): ")
        if response.lower() != 'y':
            print("❌ 用户取消处理")
            return
        
        # 开始批量处理
        print(f"\n🚀 开始批量处理...")
        start_time = time.time()
        
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=3600)) as session:
            for i, video_info in enumerate(video_files, 1):
                print(f"\n📈 进度: {i}/{len(video_files)}")
                await self.process_video(video_info, session)
        
        # 处理完成统计
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"\n🎉 批量处理完成！")
        print(f"⏱️  总耗时: {duration/60:.1f} 分钟")
        print(f"✅ 成功处理: {self.processed_count} 个")
        print(f"❌ 处理失败: {self.failed_count} 个")
        print(f"⏭️  跳过文件: {self.skipped_count} 个")

if __name__ == "__main__":
    # 配置路径
    downloads_path = "../youtube-downloader/downloads"
    output_path = "./subtitles"
    
    # 创建处理器
    processor = BatchSubtitleProcessor(downloads_path, output_path)
    
    # 运行处理
    asyncio.run(processor.run())
