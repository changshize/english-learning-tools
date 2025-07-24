# 🚀 YT-ENGLISH Quick Start Guide

## ⚡ 快速启动

### 1. 启动AI服务器
```bash
# 双击运行
start_real_whisper_isolated.bat
```

### 2. 打开播放器
- 在浏览器中打开 `index.html`

### 3. 使用功能
1. 📹 点击"选择视频文件"加载视频
2. 🤖 点击"AI生成字幕"进行语音识别
3. 🌐 点击"生成中文翻译"获得双语字幕
4. 🎯 点击字幕跳转到对应时间
5. 🔄 使用重复按钮进行影子跟读

## 📁 核心文件

| 文件 | 说明 |
|------|------|
| `index.html` | 🏠 主页面 |
| `script.js` | ⚙️ 前端逻辑 |
| `style.css` | 🎨 样式文件 |
| `faster_whisper_server.py` | 🤖 AI服务器 |
| `start_real_whisper_isolated.bat` | 🚀 启动脚本 |
| `whisper_isolated/` | 🐍 Python环境 |

## ⌨️ 快捷键

- `空格` - 播放/暂停
- `R` - 重复当前句子
- `←/→` - 上一句/下一句

## 🔧 故障排除

### 服务器启动失败
```bash
# 重新创建环境
python -m venv whisper_isolated
whisper_isolated\Scripts\activate.bat
pip install flask flask-cors faster-whisper
```

### AI转录失败
- 检查网络连接（首次需下载模型）
- 确保音频文件格式正确
- 重启服务器

## 🎯 功能特点

- ✅ 真实AI语音识别
- ✅ 智能中英文翻译
- ✅ 双语字幕对照
- ✅ 精确时间戳对齐
- ✅ 点击字幕跳转
- ✅ 影子跟读练习
- ✅ 响应式设计
- ✅ 键盘快捷键

---

**享受智能英语学习！** 🎉
