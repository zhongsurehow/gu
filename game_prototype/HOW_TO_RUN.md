# 天机变运行指南

## 快速启动

### 最简单的方式
```bash
# 进入游戏目录
cd game_prototype

# 直接启动游戏
python main.py
```

### 使用启动器（推荐）
```bash
# 启动完整功能启动器
python launcher.py
```

## 系统要求

### 最低要求
- **操作系统**: Windows 7+, macOS 10.12+, Linux (Ubuntu 16.04+)
- **Python版本**: Python 3.8+
- **内存**: 512MB RAM
- **存储空间**: 50MB 可用空间
- **终端**: 支持UTF-8编码的终端

### 推荐配置
- **操作系统**: Windows 10+, macOS 12+, Linux (Ubuntu 20.04+)
- **Python版本**: Python 3.12+
- **内存**: 1GB RAM
- **存储空间**: 100MB 可用空间
- **终端**: 现代终端（Windows Terminal, iTerm2, GNOME Terminal等）

## 安装步骤

### 1. 检查Python环境
```bash
# 检查Python版本
python --version
# 或者
python3 --version

# 应该显示 Python 3.8.0 或更高版本
```

### 2. 下载项目
```bash
# 如果有Git
git clone [项目地址]
cd game_prototype

# 或者直接下载ZIP文件并解压
```

### 3. 验证安装
```bash
# 运行系统检查
python launcher.py check

# 应该显示所有检查项都通过
```

## 启动选项

### 启动器菜单
运行 `python launcher.py` 后会看到以下选项：

```
🎮 启动选项:
1. 🎯 开始游戏          # 启动主游戏
2. 🤖 AI对战演示        # 观看AI对战
3. 📊 开发工具          # 开发者工具
4. 📚 查看文档          # 查看游戏文档
5. 🔧 系统信息          # 查看系统状态
6. 🚪 退出             # 退出程序
```

### 命令行参数
```bash
# 直接启动游戏
python main.py

# 启动AI演示
python launcher.py demo

# 运行系统检查
python launcher.py check

# 查看帮助
python launcher.py --help

# 启动开发模式
python launcher.py dev
```

## 游戏模式

### 1. 单人模式
```bash
# 启动后选择 "1. 🎯 开始游戏"
# 然后选择单人模式
```
- 与AI对战
- 练习模式
- 挑战模式

### 2. AI演示模式
```bash
# 启动后选择 "2. 🤖 AI对战演示"
```
- 观看AI自动对战
- 学习游戏策略
- 了解游戏机制

### 3. 开发模式
```bash
# 启动后选择 "3. 📊 开发工具"
```
- 性能分析
- 平衡测试
- 代码质量检查
- 系统监控

## 配置选项

### 游戏配置
编辑 `main.py` 中的配置：

```python
# 游戏难度设置
DIFFICULTY_LEVELS = {
    'easy': {'ai_thinking_time': 1, 'hint_enabled': True},
    'normal': {'ai_thinking_time': 2, 'hint_enabled': False},
    'hard': {'ai_thinking_time': 3, 'hint_enabled': False},
    'expert': {'ai_thinking_time': 5, 'hint_enabled': False}
}

# 显示设置
DISPLAY_CONFIG = {
    'show_animations': True,      # 显示动画效果
    'color_enabled': True,        # 启用彩色显示
    'sound_enabled': False,       # 启用声音（暂未实现）
    'auto_save': True            # 自动保存游戏
}
```

### AI配置
编辑 `ai_player.py` 中的配置：

```python
# AI行为设置
AI_SETTINGS = {
    'strategy_style': 'balanced',  # aggressive, defensive, balanced
    'learning_rate': 0.1,         # 学习速度
    'exploration_rate': 0.2,      # 探索率
    'memory_size': 1000          # 记忆容量
}
```

## 故障排除

### 常见问题

#### 1. Python版本过低
**问题**: `SyntaxError` 或功能不可用
**解决**: 升级到Python 3.8+
```bash
# 检查版本
python --version

# 如果版本过低，请升级Python
```

#### 2. 编码问题
**问题**: 显示乱码或编码错误
**解决**: 确保终端支持UTF-8
```bash
# Windows
chcp 65001

# Linux/macOS
export LANG=en_US.UTF-8
```

#### 3. 文件权限问题
**问题**: 无法读取或写入文件
**解决**: 检查文件权限
```bash
# Linux/macOS
chmod +x launcher.py
chmod +r *.py

# Windows: 右键 -> 属性 -> 安全 -> 编辑权限
```

#### 4. 模块导入错误
**问题**: `ModuleNotFoundError`
**解决**: 确保在正确目录运行
```bash
# 确保在game_prototype目录下
pwd  # 或 cd (Windows)
ls   # 或 dir (Windows)

# 应该看到main.py, launcher.py等文件
```

### 性能问题

#### 1. 启动缓慢
**原因**: 系统资源不足或文件过多
**解决**: 
- 关闭其他程序释放内存
- 清理临时文件
- 使用SSD硬盘

#### 2. 游戏卡顿
**原因**: AI计算复杂或系统负载高
**解决**:
- 降低AI难度
- 关闭动画效果
- 减少并发进程

#### 3. 内存占用过高
**原因**: 内存泄漏或数据积累
**解决**:
- 重启游戏
- 清理游戏历史
- 检查系统内存

## 高级用法

### 开发者模式
```bash
# 启用调试模式
python launcher.py --debug

# 运行性能测试
python launcher.py test performance

# 运行平衡性测试
python launcher.py test balance

# 生成分析报告
python launcher.py report
```

### 自定义配置
创建 `config.json` 文件：
```json
{
    "game": {
        "difficulty": "normal",
        "auto_save": true,
        "show_hints": false
    },
    "ai": {
        "thinking_time": 2,
        "strategy": "balanced",
        "learning_enabled": true
    },
    "display": {
        "colors": true,
        "animations": true,
        "sound": false
    }
}
```

### 批处理脚本
创建启动脚本：

**Windows (start_game.bat)**:
```batch
@echo off
cd /d "%~dp0"
python launcher.py
pause
```

**Linux/macOS (start_game.sh)**:
```bash
#!/bin/bash
cd "$(dirname "$0")"
python3 launcher.py
```

## 更新和维护

### 检查更新
```bash
# 检查系统状态
python launcher.py check

# 查看版本信息
python launcher.py --version

# 运行诊断
python launcher.py diagnose
```

### 备份数据
```bash
# 备份游戏数据
cp -r game_prototype game_prototype_backup

# 或者只备份重要文件
cp *.py config.json backup/
```

### 重置游戏
```bash
# 重置配置（保留代码）
rm config.json
rm -rf __pycache__/

# 完全重新安装
rm -rf game_prototype
# 重新下载和安装
```

## 多平台说明

### Windows
- 推荐使用Windows Terminal
- 确保安装了Python 3.8+
- 可能需要安装Visual C++ Redistributable

### macOS
- 使用Terminal或iTerm2
- 可能需要安装Xcode Command Line Tools
- 使用Homebrew安装Python

### Linux
- 大多数发行版都预装Python
- 确保安装了python3-dev包
- 某些发行版可能需要单独安装pip

## 网络和安全

### 网络要求
- 游戏本身不需要网络连接
- 更新检查可能需要网络
- 多人模式（未来版本）需要网络

### 安全注意事项
- 游戏不会收集个人信息
- 不会连接外部服务器
- 所有数据都存储在本地

## 技术支持

### 日志文件
游戏运行时会生成日志文件：
- `game.log`: 游戏运行日志
- `error.log`: 错误日志
- `performance.log`: 性能日志

### 调试信息
```bash
# 启用详细日志
python launcher.py --verbose

# 启用调试模式
python launcher.py --debug

# 生成诊断报告
python launcher.py diagnose > diagnosis.txt
```

### 获取帮助
1. 查看文档：选择菜单中的"📚 查看文档"
2. 运行诊断：`python launcher.py diagnose`
3. 查看日志文件
4. 提交问题报告（如果有GitHub仓库）

## 结语

天机变是一个功能丰富的易经策略游戏，通过本运行指南，你应该能够顺利启动和运行游戏。如果遇到问题，请按照故障排除部分的建议进行解决。

享受游戏，体验易经的智慧！

---

*"工欲善其事，必先利其器。"*

正确的安装和配置是享受游戏的第一步！