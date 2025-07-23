# 🎬 英语学习工具套件

一套完整的英语学习解决方案，包含YouTube视频下载器和专业的视频播放器，支持字幕显示和影子跟读功能。

[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![HTML5](https://img.shields.io/badge/HTML5-E34F26?logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/HTML)
[![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)

## 🌟 项目特色

### 📥 YouTube下载器
- **批量下载** - 支持下载整个频道的所有视频
- **智能分类** - 按频道名称自动创建文件夹
- **字幕下载** - 自动下载VTT和SRT字幕文件
- **Cookie认证** - 绕过YouTube反机器人检测
- **断点续传** - 自动跳过已下载的视频

### 🎬 视频播放器
- **影子跟读** - 点击字幕句子重复播放，便于跟读练习
- **🆕 智能分句** - 自动将长字幕分割成句子，便于逐句练习
- **智能导航** - 上一句/下一句快速切换
- **速度控制** - 0.5x到1.5x播放速度调节
- **实时高亮** - 当前播放字幕自动高亮显示
- **响应式设计** - 适配桌面和移动设备

## 🚀 快速开始

### 1. 克隆项目
```bash
git clone https://github.com/changshize/english-learning-tools.git
cd english-learning-tools
```

### 2. 使用YouTube下载器
```bash
cd youtube-downloader
pip install -r requirements.txt
python main.py -c "https://www.youtube.com/@BBCLearningEnglish"
```

### 3. 使用视频播放器
```bash
# 直接在浏览器中打开
cd video-player
# 双击 index.html 或在浏览器中打开
```

## 📁 项目结构

```
english-learning-tools/
├── youtube-downloader/          # YouTube视频下载器
│   ├── main.py                 # 主程序入口
│   ├── downloader.py           # 下载器核心逻辑
│   ├── config.py              # 配置管理
│   ├── requirements.txt       # Python依赖
│   └── channels.txt           # 频道列表
├── video-player/               # 视频播放器
│   ├── index.html             # 播放器主页面
│   ├── style.css              # 样式文件
│   ├── script.js              # 功能脚本
│   └── README.md              # 播放器使用说明
├── README.md                   # 项目总说明
└── LICENSE                     # 开源许可证
```

## 🎯 使用场景

### 英语学习完整流程
1. **下载学习材料** - 使用YouTube下载器获取英语教学视频和字幕
2. **影子跟读练习** - 使用视频播放器进行跟读训练
3. **重点句子练习** - 点击字幕重复播放难点句子
4. **语速适应训练** - 调节播放速度逐步提高

### 适用人群
- 🎓 英语学习者
- 👨‍🏫 英语教师
- 🎭 语言爱好者
- 📚 自学者

## ✨ 功能亮点

### YouTube下载器
- ✅ 支持批量下载整个频道
- ✅ 自动下载英文和中文字幕
- ✅ 按频道名称分类存储
- ✅ Cookie认证绕过限制
- ✅ 可配置视频质量和格式

### 视频播放器
- ✅ VTT和SRT字幕格式支持
- ✅ 点击字幕跳转功能
- ✅ 重复播放当前句子
- ✅ **🆕 智能分句模式** - 自动分割长字幕为句子
- ✅ 键盘快捷键支持
- ✅ 自动滚动和高亮显示

#### 🆕 分句功能详解
**智能分句模式**让你的影子跟读练习更加精确：
- 🔍 **自动识别句子边界** - 基于标点符号智能分割
- 📏 **合理时间分配** - 根据句子长度自动分配播放时间
- 🎯 **逐句导航** - 上一句/下一句按钮操作单个句子
- 🎨 **视觉区分** - 分句项目有特殊的橙色标识
- ⚡ **一键切换** - 随时开启或关闭分句模式

## 🛠️ 技术栈

- **后端**: Python 3.7+, yt-dlp
- **前端**: HTML5, CSS3, JavaScript (ES6+)
- **依赖**: 无需额外框架，纯原生实现

## 📋 系统要求

- Python 3.7 或更高版本
- 现代浏览器 (Chrome, Firefox, Safari, Edge)
- 网络连接 (用于下载视频)

## 🔧 配置说明

### YouTube下载器配置
编辑 `youtube-downloader/config.py`:
```python
YT_DLP_OPTIONS = {
    'format': 'best[height<=720]',      # 视频质量
    'writesubtitles': True,             # 下载字幕
    'cookiefile': 'cookies.txt',        # Cookie文件
    # 更多配置选项...
}
```

### Cookie配置 (重要)
为了绕过YouTube限制，需要配置cookies:
1. 安装浏览器扩展 "Get cookies.txt LOCALLY"
2. 登录YouTube后导出cookies.txt
3. 将文件放到youtube-downloader目录

## 📖 详细文档

- [YouTube下载器使用指南](youtube-downloader/README.md)
- [视频播放器使用指南](video-player/README.md)
- [Cookie配置指南](youtube-downloader/COOKIE_SETUP.md)

## 🤝 贡献

欢迎提交Issue和Pull Request！

1. Fork 本项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 📄 许可证

本项目采用 [MIT License](LICENSE) 许可证。

## ⚠️ 免责声明

- 本工具仅供个人学习和研究使用
- 请遵守YouTube的使用条款和版权法律
- 下载的内容请勿用于商业用途
- 使用本工具产生的任何法律责任由用户自行承担

## 🙏 致谢

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - 强大的视频下载工具
- 所有英语学习者和贡献者的支持

## 📞 联系方式

如有问题或建议，请通过以下方式联系：
- 提交 [Issue](https://github.com/changshize/english-learning-tools/issues)
- 发起 [Discussion](https://github.com/changshize/english-learning-tools/discussions)

---

⭐ 如果这个项目对你有帮助，请给个Star支持一下！
