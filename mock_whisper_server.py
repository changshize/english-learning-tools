#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
模拟Whisper服务器 - 用于测试前端连接
返回示例字幕数据，确保整个流程正常工作
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import time
import random

app = Flask(__name__)
CORS(app)

@app.route('/health', methods=['GET'])
def health_check():
    """健康检查"""
    return jsonify({
        'status': 'ok',
        'model_loaded': True,
        'version': 'mock'
    })

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    """模拟转录，返回示例字幕"""
    try:
        if 'audio' not in request.files:
            return jsonify({'error': '没有音频文件'}), 400
        
        audio_file = request.files['audio']
        if audio_file.filename == '':
            return jsonify({'error': '文件名为空'}), 400
        
        print(f"收到音频文件: {audio_file.filename}, 大小: {len(audio_file.read())} bytes")
        
        # 模拟处理时间
        print("模拟AI处理中...")
        time.sleep(2)
        
        # 生成示例字幕数据
        sample_segments = [
            {
                'start': 0.0,
                'end': 3.5,
                'text': "Hello everyone and welcome back to English with Lucy."
            },
            {
                'start': 3.5,
                'end': 7.0,
                'text': "Today I have a very interesting grammar question for you."
            },
            {
                'start': 7.0,
                'end': 10.5,
                'text': "I borrowed my guitar to my brother."
            },
            {
                'start': 10.5,
                'end': 13.0,
                'text': "Can you spot the mistake in this sentence?"
            },
            {
                'start': 13.0,
                'end': 16.5,
                'text': "The correct way to say this is: I lent my guitar to my brother."
            },
            {
                'start': 16.5,
                'end': 20.0,
                'text': "We use 'lend' when we give something temporarily."
            },
            {
                'start': 20.0,
                'end': 23.5,
                'text': "And we use 'borrow' when we receive something temporarily."
            },
            {
                'start': 23.5,
                'end': 27.0,
                'text': "So remember: you lend TO someone, and you borrow FROM someone."
            },
            {
                'start': 27.0,
                'end': 30.0,
                'text': "Thanks for watching, and I'll see you in the next lesson!"
            }
        ]
        
        # 随机化一些时间，让它看起来更真实
        for segment in sample_segments:
            segment['start'] += random.uniform(-0.2, 0.2)
            segment['end'] += random.uniform(-0.2, 0.2)
        
        result = {
            'text': ' '.join([seg['text'] for seg in sample_segments]),
            'language': 'en',
            'segments': sample_segments
        }
        
        print(f"返回 {len(sample_segments)} 个字幕片段")
        
        return jsonify({
            'success': True,
            'result': result
        })
        
    except Exception as e:
        print(f"处理出错: {e}")
        return jsonify({'error': f'服务器错误: {str(e)}'}), 500

@app.route('/', methods=['GET'])
def index():
    """首页"""
    return """
    <h1>🎤 模拟Whisper服务器</h1>
    <p>✅ 服务器正在运行</p>
    <p>📡 健康检查: <a href="/health">/health</a></p>
    <p>🔧 这是一个测试服务器，返回示例字幕数据</p>
    """

if __name__ == '__main__':
    print("🎤 模拟Whisper字幕生成服务器")
    print("=" * 50)
    print("📋 返回示例字幕数据，用于测试前端连接")
    print("✅ 无需安装Whisper，直接可用")
    print("📡 API地址: http://localhost:5000")
    print("🔗 健康检查: http://localhost:5000/health")
    print("=" * 50)
    
    print("🚀 服务器启动中...")
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        threaded=True
    )
