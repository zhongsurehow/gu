# 天机变游戏运行指南

## 🚀 快速启动

### 1. 环境检查
```bash
# 检查Python版本（需要3.7+）
python --version
# 或
python3 --version
```

### 2. 下载项目
```bash
# 方式一：Git克隆
git clone [项目地址]
cd we-feat-tianjibian-rules

# 方式二：直接下载ZIP并解压
```

### 3. 运行游戏
```bash
# 进入游戏目录
cd game_prototype

# 启动主游戏
python main.py
```

## 🎮 游戏模式选择

### 标准游戏模式
```bash
# 基础游戏体验
python main.py
```

### 交互式演示（推荐新手）
```bash
# 回到项目根目录
cd ..

# 运行交互式演示
python interactive_demo.py
```

### 完整功能演示
```bash
# 体验所有增强功能
python complete_demo.py

# 易经知识演示
python yijing_demo.py
```

## 🎯 游戏操作指南

### 基础命令
游戏中可以使用以下命令：

| 命令 | 格式 | 示例 | 说明 |
|------|------|------|------|
| 打牌 | `play <牌号> <位置>` | `play 0 乾` | 在乾位打出第0张牌 |
| 移动 | `move <位置>` | `move 人` | 移动到人位 |
| 冥想 | `meditate` | `meditate` | 调节阴阳平衡 |
| 学习 | `study` | `study` | 提升道行 |
| 跳过 | `pass` | `pass` | 跳过当前回合 |
| 帮助 | `help` | `help` | 显示帮助信息 |
| 退出 | `exit` | `exit` | 退出游戏 |

### 高级命令
| 命令 | 格式 | 示例 | 说明 |
|------|------|------|------|
| 变卦 | `biangua <源卦> <目标卦>` | `biangua 乾 坤` | 变卦转换 |
| 占卜 | `divine` | `divine` | 易经占卜 |
| 状态 | `status` | `status` | 查看详细状态 |
| 历史 | `history` | `history` | 查看行动历史 |

### 位置名称
- **八卦位置**：乾、坤、震、巽、坎、离、艮、兑
- **三才位置**：天、人、地

## 🔧 故障排除

### 常见问题

#### 1. Python版本问题
```bash
# 错误：Python版本过低
# 解决：升级Python到3.7+
python --version
```

#### 2. 找不到模块
```bash
# 错误：ModuleNotFoundError
# 解决：确保在正确目录下运行
pwd  # 检查当前目录
cd game_prototype  # 进入游戏目录
```

#### 3. 编码问题
```bash
# 错误：UnicodeDecodeError
# 解决：设置环境变量
export PYTHONIOENCODING=utf-8  # Linux/Mac
set PYTHONIOENCODING=utf-8     # Windows
```

#### 4. 权限问题
```bash
# 错误：Permission denied
# 解决：检查文件权限
chmod +x main.py  # Linux/Mac
```

### 调试模式
```bash
# 启用详细日志
python main.py --debug

# 启用性能监控
python main.py --profile

# 启用测试模式
python main.py --test
```

## 🧪 测试和验证

### 运行测试套件
```bash
# 基础功能测试
python test_game_features.py

# 性能测试
python test_optimized_game.py

# 平衡性测试
python game_prototype/test_enhanced_strategies.py

# 完整测试套件
python game_prototype/comprehensive_test_suite.py
```

### 验证安装
```bash
# 快速验证
python -c "import game_prototype.main; print('安装成功！')"

# 系统检查
python game_prototype/performance_check.py
```

## 📊 性能优化

### 系统要求
- **最低配置**：Python 3.7, 512MB RAM
- **推荐配置**：Python 3.8+, 1GB RAM
- **最佳体验**：Python 3.9+, 2GB RAM

### 性能调优
```bash
# 启用性能优化
python main.py --optimize

# 内存监控
python main.py --memory-monitor

# 缓存启用
python main.py --enable-cache
```

## 🎨 自定义配置

### 配置文件
创建 `config.json` 文件自定义游戏设置：
```json
{
    "game": {
        "difficulty": "normal",
        "language": "zh-CN",
        "auto_save": true
    },
    "ui": {
        "theme": "classic",
        "animations": true,
        "sound": false
    },
    "ai": {
        "level": "medium",
        "personality": "balanced"
    }
}
```

### 命令行参数
```bash
# 指定配置文件
python main.py --config custom_config.json

# 设置难度
python main.py --difficulty hard

# 启用AI对手
python main.py --ai-opponent
```

## 📱 多平台支持

### Windows
```cmd
# PowerShell
cd game_prototype
python main.py

# 命令提示符
cd game_prototype
python.exe main.py
```

### Linux/macOS
```bash
# 终端
cd game_prototype
python3 main.py

# 或使用虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
python main.py
```

## 🆘 获取帮助

### 游戏内帮助
- 输入 `help` 查看命令列表
- 输入 `tutorial` 启动教学模式
- 输入 `guide` 查看策略指南

### 文档资源
- 📖 [快速入门](QUICK_START.md)
- 📚 [完整规则](GAME_RULES.md)
- 🎯 [易经指南](YIJING_GUIDE.md)
- 🔧 [开发指南](DEVELOPMENT_GUIDE.md)

### 社区支持
- 提交 GitHub Issues
- 查看项目 Wiki
- 参与讨论区交流

---

🎉 **准备好开始你的易经修行之旅了吗？运行游戏，探索古老智慧的现代演绎！**
