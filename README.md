# 🎬 YT-ENGLISH 智能视频播放器

一个专为英语学习设计的智能视频播放器，支持AI字幕生成、字幕跳转、影子跟读等功能。

[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![HTML5](https://img.shields.io/badge/HTML5-E34F26?logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/HTML)
[![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![Flask](https://img.shields.io/badge/Flask-000000?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)

## ✨ 主要功能

- 🎥 **视频播放**：支持MP4、WebM、AVI等多种视频格式
- 📝 **字幕显示**：支持VTT、SRT格式字幕文件
- 🤖 **AI字幕生成**：集成Python Whisper，自动生成高质量英文字幕
- 🎯 **字幕跳转**：点击字幕直接跳转到对应时间点
- 🔄 **影子跟读**：重复播放当前句子，便于跟读练习
- ⚡ **播放控制**：播放/暂停、进度控制、速度调节(0.5x-1.5x)
- ⌨️ **快捷键支持**：空格键播放/暂停，方向键切换字幕
- 📱 **响应式设计**：完美适配桌面和移动设备
- 🎨 **实时高亮**：当前播放字幕自动高亮显示

## 🚀 快速开始

### 1. 克隆仓库
```bash
git clone https://github.com/changshize/YT-ENGLISH.git
cd YT-ENGLISH
```

### 2. 启动AI字幕服务（可选）
```bash
# 安装Python依赖
pip install flask flask-cors

# 启动Whisper服务器
python mock_whisper_server.py
```

### 3. 打开播放器
直接在浏览器中打开 `index.html` 文件即可开始使用。

### 4. 开始使用
1. 点击"📹 选择视频文件"加载本地视频
2. 点击"🤖 AI生成字幕"自动生成字幕（需要后端服务）
3. 或点击"📝 选择字幕文件"手动加载字幕
4. 点击字幕进行跳转和影子跟读练习

## 📁 项目结构

```
YT-ENGLISH/
├── index.html              # 🏠 主页面 - 播放器界面
├── script.js               # ⚙️ 核心JavaScript逻辑
├── style.css               # 🎨 样式文件 - 响应式设计
├── mock_whisper_server.py  # 🐍 Python后端服务器
├── requirements.txt        # 📦 Python依赖列表
├── test-subtitle.vtt       # 📝 测试字幕文件
├── README.md              # 📖 项目说明文档
├── CHANGELOG.md           # 📋 版本更新日志
├── LICENSE                # ⚖️ MIT开源许可证
└── AI-SUBTITLE-GUIDE.md   # 🤖 AI字幕使用指南
```

## 📋 使用说明

### 基本操作
1. **启动后端**：运行 `python mock_whisper_server.py`
2. **加载视频**：点击"选择视频文件"按钮选择本地视频
3. **AI生成字幕**：点击"🤖 AI生成字幕"按钮自动生成字幕
4. **播放控制**：使用播放器控件控制播放

### 字幕功能
- **字幕跳转**：点击右侧字幕列表中的任意字幕跳转到对应时间
- **当前字幕高亮**：播放时当前字幕会自动高亮显示
- **字幕同步**：字幕与视频播放完全同步
- **手动加载**：也可以点击"选择字幕文件"加载VTT格式字幕

## 🤖 AI字幕生成

本项目使用Python后端 + Whisper AI模型，可以自动为英语视频生成高质量字幕。

### 架构设计
```
前端 (JavaScript)
    ↓ HTTP POST
Python Flask服务器
    ↓
Whisper AI模型处理
    ↓
返回字幕结果
```

### 使用方法
1. 确保Python服务器正在运行
2. 加载视频文件
3. 点击"🤖 AI生成字幕"按钮
4. 等待AI处理完成（通常1-3分钟）
5. 字幕将自动显示在右侧列表中

### 技术特点
- **高准确度**：使用完整版Whisper模型
- **支持长视频**：自动分块处理
- **实时进度**：显示处理进度
- **错误处理**：完善的错误提示和恢复机制

## 🛠️ 技术栈

- **前端**: HTML5, CSS3, JavaScript (ES6+)
- **后端**: Python Flask + OpenAI Whisper
- **AI模型**: Whisper (语音识别)
- **音频处理**: Web Audio API
- **跨域支持**: Flask-CORS
- **依赖管理**: pip + requirements.txt

## 🎯 核心特性

### 🎬 视频播放器
- ✅ 支持多种视频格式 (MP4, WebM, AVI等)
- ✅ 拖拽加载文件，操作简便
- ✅ 播放速度控制 (0.5x - 1.5x)
- ✅ 进度条拖拽跳转
- ✅ 全屏播放支持

### 📝 字幕系统
- ✅ VTT和SRT字幕格式支持
- ✅ 点击字幕精确跳转
- ✅ 实时字幕高亮显示
- ✅ 自动滚动到当前字幕
- ✅ 字幕时间同步

### 🤖 AI字幕生成
- ✅ 集成OpenAI Whisper模型
- ✅ 高精度英文语音识别
- ✅ 自动时间戳对齐
- ✅ 支持长视频处理
- ✅ 实时进度显示

### 🔄 影子跟读功能
- ✅ 一键重复当前句子
- ✅ 上一句/下一句快速切换
- ✅ 浮动控制按钮
- ✅ 键盘快捷键支持
- ✅ 当前句子大字显示

## ⌨️ 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| `空格键` | 播放/暂停视频 |
| `R` | 重复当前句子 |
| `←` | 上一句字幕 |
| `→` | 下一句字幕 |
| `S` | 显示/隐藏字幕 |

## 📋 系统要求

### 基础要求
- **浏览器**: Chrome 80+, Firefox 75+, Safari 13+, Edge 80+
- **操作系统**: Windows 10+, macOS 10.14+, Linux (Ubuntu 18.04+)
- **内存**: 建议4GB以上

### AI字幕功能要求
- **Python**: 3.8 或更高版本
- **内存**: 建议8GB以上 (用于Whisper模型)
- **网络**: 首次使用需下载AI模型

## 🔧 开发说明

### 前端架构
- **VideoPlayer类**: 核心播放器逻辑
- **模块化设计**: 字幕处理、AI集成、UI控制分离
- **响应式布局**: 适配移动端和桌面端

### 后端API
- `GET /health`: 健康检查接口
- `POST /transcribe`: 音频转录接口

### 部署选项
- **开发模式**: 使用 `mock_whisper_server.py` (返回示例字幕)
- **生产模式**: 集成真实Whisper模型
- **Docker部署**: 可容器化部署

## 🎯 使用技巧

### 影子跟读练习
1. 🎬 加载英语学习视频
2. 🤖 使用AI生成字幕或手动加载
3. 🎯 点击字幕句子精确跳转
4. 🔄 使用重复功能反复练习
5. ⚡ 调节播放速度适应语速

### 最佳实践
- **短视频练习**: 建议使用3-10分钟的视频片段
- **循序渐进**: 从0.75x速度开始，逐步提高到1.25x
- **重点突破**: 对难点句子使用重复功能强化练习
- **键盘操作**: 熟练使用快捷键提高练习效率

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

### 贡献流程
1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建Pull Request

### 开发环境
```bash
# 克隆项目
git clone https://github.com/changshize/YT-ENGLISH.git
cd YT-ENGLISH

# 启动开发服务器
python mock_whisper_server.py

# 在浏览器中打开 index.html
```

## 📄 许可证

本项目采用 [MIT许可证](LICENSE) - 详见LICENSE文件。

## 🙏 致谢

- [OpenAI Whisper](https://github.com/openai/whisper) - 优秀的语音识别模型
- [Flask](https://flask.palletsprojects.com/) - 轻量级Web框架
- 所有贡献者和用户的支持与反馈

## 📞 联系方式

- **GitHub Issues**: [提交问题和建议](https://github.com/changshize/YT-ENGLISH/issues)
- **项目主页**: [YT-ENGLISH](https://github.com/changshize/YT-ENGLISH)

---

**开始你的智能英语学习之旅！** 🎉🚀

---

⭐ 如果这个项目对你有帮助，请给个Star支持一下！
