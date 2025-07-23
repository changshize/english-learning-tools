#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Faster-Whisper字幕生成服务器
使用faster-whisper库，更稳定，依赖更少
"""

try:
    from faster_whisper import WhisperModel
    FASTER_WHISPER_AVAILABLE = True
except ImportError:
    FASTER_WHISPER_AVAILABLE = False

import tempfile
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# 全局变量存储模型
model = None

def load_faster_whisper_model(model_size="small"):
    """加载Faster-Whisper模型"""
    global model
    try:
        logger.info(f"Loading Faster-Whisper model: {model_size}")
        model = WhisperModel(model_size, device="cpu", compute_type="int8")
        logger.info("Faster-Whisper model loaded successfully")
        return True
    except Exception as e:
        logger.error(f"Failed to load model: {e}")
        return False

@app.route('/health', methods=['GET'])
def health_check():
    """健康检查接口"""
    return jsonify({
        'status': 'ok',
        'model_loaded': model is not None,
        'version': 'faster_whisper',
        'available': FASTER_WHISPER_AVAILABLE
    })

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    """音频转录接口"""
    try:
        if not FASTER_WHISPER_AVAILABLE:
            return jsonify({'error': 'faster-whisper not installed'}), 500
            
        # 检查模型是否已加载
        if model is None:
            return jsonify({'error': 'Whisper model not loaded'}), 500
        
        # 检查是否有音频文件
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file provided'}), 400
        
        audio_file = request.files['audio']
        if audio_file.filename == '':
            return jsonify({'error': 'Empty filename'}), 400
        
        # 获取参数
        language = request.form.get('language', 'en')
        
        logger.info(f"Starting transcription: {audio_file.filename}")
        
        # 保存临时文件
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_file:
            audio_file.save(tmp_file.name)
            tmp_filename = tmp_file.name
        
        try:
            # 使用Faster-Whisper转录
            logger.info("Running Faster-Whisper transcription...")
            segments, info = model.transcribe(tmp_filename, language=language)
            
            # 处理结果
            processed_segments = []
            full_text = ""
            
            for segment in segments:
                text = segment.text.strip()
                if text:
                    processed_segments.append({
                        'start': segment.start,
                        'end': segment.end,
                        'text': text
                    })
                    full_text += text + " "
            
            logger.info(f"Transcription completed, found {len(processed_segments)} segments")
            
            result = {
                'text': full_text.strip(),
                'language': info.language,
                'segments': processed_segments
            }
            
            return jsonify({
                'success': True,
                'result': result
            })
            
        except Exception as e:
            logger.error(f"Transcription error: {e}")
            return jsonify({'error': f'Transcription failed: {str(e)}'}), 500
            
        finally:
            # 清理临时文件
            try:
                os.unlink(tmp_filename)
            except:
                pass
    
    except Exception as e:
        logger.error(f"Request processing error: {e}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500

if __name__ == '__main__':
    print("🚀 Faster-Whisper AI Server")
    print("=" * 50)
    
    if not FASTER_WHISPER_AVAILABLE:
        print("❌ faster-whisper not installed")
        print("Please run: pip install faster-whisper")
        exit(1)
    
    # 启动时加载默认模型
    print("Loading Faster-Whisper model...")
    if load_faster_whisper_model("small"):
        print("✅ Faster-Whisper model loaded successfully")
    else:
        print("❌ Failed to load Faster-Whisper model")
        exit(1)
    
    print("🚀 Starting server...")
    print("📡 API URL: http://localhost:5000")
    print("=" * 50)
    
    # 启动Flask服务器
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=False,
        threaded=True
    )
