class VideoPlayer {
    constructor() {
        this.video = document.getElementById('videoPlayer');
        this.subtitles = [];
        this.currentSubtitleIndex = -1;
        this.isSubtitleVisible = false;
        this.autoScroll = true;
        
        this.initializeElements();
        this.bindEvents();
    }

    initializeElements() {
        this.videoFile = document.getElementById('videoFile');
        this.subtitleFile = document.getElementById('subtitleFile');
        this.subtitleList = document.getElementById('subtitleList');
        this.currentSubtitle = document.getElementById('currentSubtitle');
        this.progressBar = document.getElementById('progressBar');
        this.progressFill = document.getElementById('progressFill');
        this.currentTime = document.getElementById('currentTime');
        this.totalTime = document.getElementById('totalTime');
        this.fileInfo = document.getElementById('fileInfo');
        this.videoInfo = document.getElementById('videoInfo');
        this.subtitleInfo = document.getElementById('subtitleInfo');
        
        // 控制按钮
        this.toggleSubtitleBtn = document.getElementById('toggleSubtitle');
        this.repeatBtn = document.getElementById('repeatBtn');
        this.prevBtn = document.getElementById('prevBtn');
        this.nextBtn = document.getElementById('nextBtn');
        this.autoScrollBtn = document.getElementById('autoScrollBtn');
        this.clearHighlightBtn = document.getElementById('clearHighlightBtn');
        
        // 浮动控制按钮
        this.floatingControls = document.getElementById('floatingControls');
        this.floatRepeat = document.getElementById('floatRepeat');
        this.floatPrev = document.getElementById('floatPrev');
        this.floatNext = document.getElementById('floatNext');
        this.floatToggle = document.getElementById('floatToggle');
    }

    bindEvents() {
        // 文件选择事件
        this.videoFile.addEventListener('change', (e) => this.loadVideo(e.target.files[0]));
        this.subtitleFile.addEventListener('change', (e) => this.loadSubtitle(e.target.files[0]));
        
        // 视频事件
        this.video.addEventListener('timeupdate', () => this.updateProgress());
        this.video.addEventListener('loadedmetadata', () => this.updateVideoInfo());
        
        // 控制按钮事件
        this.toggleSubtitleBtn.addEventListener('click', () => this.toggleSubtitleDisplay());
        this.repeatBtn.addEventListener('click', () => this.repeatCurrentSubtitle());
        this.prevBtn.addEventListener('click', () => this.goToPreviousSubtitle());
        this.nextBtn.addEventListener('click', () => this.goToNextSubtitle());
        this.autoScrollBtn.addEventListener('click', () => this.toggleAutoScroll());
        this.clearHighlightBtn.addEventListener('click', () => this.clearHighlight());
        
        // 浮动控制按钮事件
        this.floatRepeat.addEventListener('click', () => this.repeatCurrentSubtitle());
        this.floatPrev.addEventListener('click', () => this.goToPreviousSubtitle());
        this.floatNext.addEventListener('click', () => this.goToNextSubtitle());
        this.floatToggle.addEventListener('click', () => this.toggleSubtitleDisplay());
        
        // 播放速度控制
        document.querySelectorAll('.speed-btn').forEach(btn => {
            btn.addEventListener('click', (e) => this.setPlaybackSpeed(e.target.dataset.speed));
        });
        
        // 进度条点击
        this.progressBar.addEventListener('click', (e) => this.seekTo(e));
        
        // 键盘快捷键
        document.addEventListener('keydown', (e) => this.handleKeyboard(e));
    }

    loadVideo(file) {
        if (file) {
            const url = URL.createObjectURL(file);
            this.video.src = url;
            this.videoInfo.textContent = `视频: ${file.name} (${this.formatFileSize(file.size)})`;
            this.fileInfo.style.display = 'block';
            this.floatingControls.style.display = 'flex';
            console.log('视频加载成功:', file.name);
        }
    }

    loadSubtitle(file) {
        if (file) {
            console.log('开始加载字幕文件:', file.name, '大小:', file.size, '类型:', file.type);

            const reader = new FileReader();
            reader.onload = (e) => {
                const content = e.target.result;
                console.log('字幕文件内容长度:', content.length);
                console.log('文件开头内容:', content.substring(0, 100));

                // 检查文件是否为空
                if (!content || content.trim().length === 0) {
                    alert('字幕文件为空，请检查文件内容');
                    return;
                }

                // 检查是否包含VTT标识
                if (!content.includes('WEBVTT') && !content.includes('-->')) {
                    alert('这不是有效的VTT字幕文件，请检查文件格式');
                    return;
                }

                this.parseSubtitle(content);
                this.subtitleInfo.textContent = `字幕: ${file.name} (${this.subtitles.length} 条字幕)`;
                this.fileInfo.style.display = 'block';

                if (this.subtitles.length === 0) {
                    alert('字幕解析失败，请检查文件格式是否正确\n\n调试信息请查看浏览器控制台（按F12）');
                } else {
                    console.log('字幕解析成功，共', this.subtitles.length, '条字幕');
                    console.log('前3条字幕:', this.subtitles.slice(0, 3));
                    this.enableSubtitleControls();
                }
            };

            reader.onerror = (e) => {
                console.error('文件读取失败:', e);
                alert('文件读取失败，请重试');
            };

            reader.readAsText(file, 'utf-8');
        }
    }

    parseSubtitle(content) {
        this.subtitles = [];

        if (content.includes('WEBVTT')) {
            // 解析VTT格式
            this.parseVTTSimple(content);
        } else {
            // 解析SRT格式
            this.parseSRT(content);
        }

        this.renderSubtitleList();
        console.log('字幕解析完成:', this.subtitles.length, '条');
    }

    parseVTTSimple(content) {
        console.log('开始解析VTT内容，长度:', content.length);
        console.log('前200个字符:', content.substring(0, 200));

        const lines = content.split(/\r?\n/); // 支持不同的换行符
        const seenTexts = new Set(); // 用于去重
        let subtitleCount = 0;

        for (let i = 0; i < lines.length; i++) {
            const line = lines[i].trim();

            // 检查是否是时间行
            if (line.includes('-->')) {
                console.log(`找到时间行 ${i}: ${line}`);

                try {
                    const times = line.split('-->');
                    if (times.length !== 2) {
                        console.log('时间格式错误:', line);
                        continue;
                    }

                    const startTime = this.parseTime(times[0].trim());
                    const endTime = this.parseTime(times[1].trim());

                    // 检查时间是否有效
                    if (startTime < 0 || endTime <= 0 || endTime <= startTime) {
                        console.log('无效时间范围:', { startTime, endTime, line });
                        continue;
                    }

                    console.log(`解析时间: ${startTime} -> ${endTime}`);

                    // 收集字幕文本
                    let text = '';
                    i++;
                    while (i < lines.length && lines[i].trim() && !lines[i].includes('-->')) {
                        const textLine = lines[i].trim();
                        // console.log(`文本行 ${i}: ${textLine}`);

                        // 清理时间戳标记和其他VTT标记
                        let cleanText = textLine
                            .replace(/<\d{2}:\d{2}:\d{2}\.\d{3}>/g, '') // 清理 <00:00:00.480>
                            .replace(/<c[^>]*>/g, '') // 清理 <c> 标记
                            .replace(/<\/c>/g, '') // 清理 </c> 标记
                            .replace(/<[^>]*>/g, '') // 清理其他HTML标记
                            .replace(/&lt;/g, '<') // 解码HTML实体
                            .replace(/&gt;/g, '>')
                            .replace(/&amp;/g, '&')
                            .trim();

                        if (cleanText) {
                            text += (text ? ' ' : '') + cleanText;
                        }
                        i++;
                    }
                    i--; // 回退一行，因为外层循环会自动+1

                    // 只添加非重复且有效的字幕
                    if (text && !seenTexts.has(text) && startTime >= 0 && endTime > startTime) {
                        seenTexts.add(text);
                        this.subtitles.push({
                            start: startTime,
                            end: endTime,
                            text: text
                        });
                        subtitleCount++;
                        console.log(`添加字幕 ${subtitleCount}: ${text}`);
                    } else {
                        console.log('跳过字幕:', { text, duplicate: seenTexts.has(text), startTime, endTime });
                    }
                } catch (error) {
                    console.error('解析时间行出错:', line, error);
                }
            }
        }

        // 按时间排序
        this.subtitles.sort((a, b) => a.start - b.start);
        console.log(`VTT解析完成，共 ${this.subtitles.length} 条字幕`);
    }



    parseSRT(content) {
        const blocks = content.split('\n\n');
        
        blocks.forEach(block => {
            const lines = block.trim().split('\n');
            if (lines.length >= 3) {
                const timeLine = lines[1];
                if (timeLine.includes('-->')) {
                    const times = timeLine.split('-->');
                    const text = lines.slice(2).join(' ');
                    
                    this.subtitles.push({
                        start: this.parseTime(times[0].trim()),
                        end: this.parseTime(times[1].trim()),
                        text: text
                    });
                }
            }
        });
    }

    parseTime(timeStr) {
        try {
            // 清理时间字符串，移除VTT格式参数
            timeStr = timeStr.trim()
                .replace(',', '.')
                .replace(/\s+align:start.*$/i, '')  // 移除 align:start position:0%
                .replace(/\s+position:.*$/i, '')   // 移除 position:0%
                .replace(/\s+line:.*$/i, '')       // 移除 line:参数
                .replace(/\s+size:.*$/i, '')       // 移除 size:参数
                .trim();

            // console.log('清理后的时间字符串:', timeStr);

            // 支持多种时间格式: HH:MM:SS.mmm 或 MM:SS.mmm 或 SS.mmm
            const parts = timeStr.split(':');
            let hours = 0, minutes = 0, seconds = 0;

            if (parts.length === 3) {
                // HH:MM:SS.mmm 格式
                hours = parseInt(parts[0]) || 0;
                minutes = parseInt(parts[1]) || 0;
                seconds = parseFloat(parts[2]) || 0;
            } else if (parts.length === 2) {
                // MM:SS.mmm 格式
                minutes = parseInt(parts[0]) || 0;
                seconds = parseFloat(parts[1]) || 0;
            } else if (parts.length === 1) {
                // SS.mmm 格式
                seconds = parseFloat(parts[0]) || 0;
            } else {
                console.error('无法解析时间格式:', timeStr);
                return 0;
            }

            const totalSeconds = hours * 3600 + minutes * 60 + seconds;
            // console.log(`时间解析结果: ${timeStr} -> ${totalSeconds}秒`);
            return totalSeconds;
        } catch (error) {
            console.error('时间解析出错:', timeStr, error);
            return 0;
        }
    }

    renderSubtitleList() {
        this.subtitleList.innerHTML = '';
        
        this.subtitles.forEach((subtitle, index) => {
            const item = document.createElement('div');
            item.className = 'subtitle-item';
            item.dataset.index = index;
            
            item.innerHTML = `
                <div class="subtitle-time">${this.formatTime(subtitle.start)} - ${this.formatTime(subtitle.end)}</div>
                <div class="subtitle-text">${subtitle.text}</div>
            `;
            
            item.addEventListener('click', () => this.jumpToSubtitle(index));
            this.subtitleList.appendChild(item);
        });
    }

    updateProgress() {
        const currentTime = this.video.currentTime;
        const duration = this.video.duration;
        
        // 更新进度条
        if (duration) {
            const progress = (currentTime / duration) * 100;
            this.progressFill.style.width = progress + '%';
        }
        
        // 更新时间显示
        this.currentTime.textContent = this.formatTime(currentTime);
        this.totalTime.textContent = this.formatTime(duration || 0);
        
        // 更新当前字幕
        this.updateCurrentSubtitle(currentTime);
    }

    updateCurrentSubtitle(currentTime) {
        let newIndex = -1;
        
        for (let i = 0; i < this.subtitles.length; i++) {
            if (currentTime >= this.subtitles[i].start && currentTime <= this.subtitles[i].end) {
                newIndex = i;
                break;
            }
        }
        
        if (newIndex !== this.currentSubtitleIndex) {
            // 移除之前的高亮
            if (this.currentSubtitleIndex >= 0) {
                const prevItem = this.subtitleList.children[this.currentSubtitleIndex];
                if (prevItem) prevItem.classList.remove('active');
            }
            
            this.currentSubtitleIndex = newIndex;
            
            if (newIndex >= 0) {
                const currentItem = this.subtitleList.children[newIndex];
                if (currentItem) {
                    currentItem.classList.add('active');
                    
                    // 自动滚动到当前字幕
                    if (this.autoScroll) {
                        currentItem.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    }
                }
                
                // 显示当前字幕
                if (this.isSubtitleVisible) {
                    this.currentSubtitle.textContent = this.subtitles[newIndex].text;
                    this.currentSubtitle.style.display = 'block';
                }
            } else {
                this.currentSubtitle.style.display = 'none';
            }
        }
    }

    jumpToSubtitle(index) {
        if (index >= 0 && index < this.subtitles.length) {
            const subtitle = this.subtitles[index];
            this.video.currentTime = subtitle.start;

            // 更新当前字幕索引
            this.currentSubtitleIndex = index;

            // 立即更新UI显示
            this.updateSubtitleHighlight(index);

            console.log(`跳转到字幕 ${index + 1}/${this.subtitles.length}: ${subtitle.text}`);
        }
    }

    updateSubtitleHighlight(index) {
        // 移除所有高亮
        document.querySelectorAll('.subtitle-item.active').forEach(item => {
            item.classList.remove('active');
        });

        // 添加新的高亮
        if (index >= 0 && index < this.subtitleList.children.length) {
            const currentItem = this.subtitleList.children[index];
            currentItem.classList.add('active');

            // 滚动到当前字幕
            if (this.autoScroll) {
                currentItem.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }

            // 显示当前字幕
            if (this.isSubtitleVisible && this.subtitles[index]) {
                this.currentSubtitle.textContent = this.subtitles[index].text;
                this.currentSubtitle.style.display = 'block';
            }
        }
    }

    repeatCurrentSubtitle() {
        if (this.currentSubtitleIndex >= 0) {
            const subtitle = this.subtitles[this.currentSubtitleIndex];
            this.video.currentTime = subtitle.start;
            this.video.play();
        } else if (this.subtitles.length > 0) {
            // 如果没有当前字幕，播放第一句
            this.jumpToSubtitle(0);
            this.video.play();
        }
    }

    goToPreviousSubtitle() {
        if (this.currentSubtitleIndex > 0) {
            this.jumpToSubtitle(this.currentSubtitleIndex - 1);
        } else if (this.subtitles.length > 0) {
            this.jumpToSubtitle(0);
        }
    }

    goToNextSubtitle() {
        if (this.currentSubtitleIndex < this.subtitles.length - 1) {
            this.jumpToSubtitle(this.currentSubtitleIndex + 1);
        } else if (this.currentSubtitleIndex === -1 && this.subtitles.length > 0) {
            this.jumpToSubtitle(0);
        }
    }

    toggleSubtitleDisplay() {
        this.isSubtitleVisible = !this.isSubtitleVisible;
        this.toggleSubtitleBtn.textContent = this.isSubtitleVisible ? '隐藏字幕' : '显示字幕';
        this.currentSubtitle.style.display = this.isSubtitleVisible && this.currentSubtitleIndex >= 0 ? 'block' : 'none';
    }

    toggleAutoScroll() {
        this.autoScroll = !this.autoScroll;
        this.autoScrollBtn.textContent = this.autoScroll ? '关闭自动滚动' : '开启自动滚动';
        this.autoScrollBtn.style.background = this.autoScroll ? '#4CAF50' : '#FF9800';
    }

    clearHighlight() {
        document.querySelectorAll('.subtitle-item.active').forEach(item => {
            item.classList.remove('active');
        });
        this.currentSubtitleIndex = -1;
        this.currentSubtitle.style.display = 'none';
    }

    setPlaybackSpeed(speed) {
        this.video.playbackRate = parseFloat(speed);
        
        // 更新按钮状态
        document.querySelectorAll('.speed-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelector(`[data-speed="${speed}"]`).classList.add('active');
    }

    seekTo(e) {
        const rect = this.progressBar.getBoundingClientRect();
        const pos = (e.clientX - rect.left) / rect.width;
        this.video.currentTime = pos * this.video.duration;
    }

    enableSubtitleControls() {
        this.repeatBtn.disabled = false;
        this.prevBtn.disabled = false;
        this.nextBtn.disabled = false;

        // 启用浮动控制按钮
        this.floatRepeat.disabled = false;
        this.floatPrev.disabled = false;
        this.floatNext.disabled = false;

        console.log('字幕控制按钮已启用');
    }

    updateVideoInfo() {
        const duration = this.video.duration;
        this.totalTime.textContent = this.formatTime(duration);
    }

    formatTime(seconds) {
        if (isNaN(seconds)) return '00:00';
        
        const hours = Math.floor(seconds / 3600);
        const minutes = Math.floor((seconds % 3600) / 60);
        const secs = Math.floor(seconds % 60);
        
        if (hours > 0) {
            return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
        } else {
            return `${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
        }
    }

    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    handleKeyboard(e) {
        if (e.target.tagName === 'INPUT') return;
        
        switch(e.key) {
            case ' ':
                e.preventDefault();
                this.video.paused ? this.video.play() : this.video.pause();
                break;
            case 'r':
            case 'R':
                this.repeatCurrentSubtitle();
                break;
            case 'ArrowLeft':
                this.goToPreviousSubtitle();
                break;
            case 'ArrowRight':
                this.goToNextSubtitle();
                break;
            case 's':
            case 'S':
                this.toggleSubtitleDisplay();
                break;
        }
    }
}

// 初始化播放器
document.addEventListener('DOMContentLoaded', () => {
    new VideoPlayer();
});
