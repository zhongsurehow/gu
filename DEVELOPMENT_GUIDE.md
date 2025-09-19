# 开发者协作指南

## 目录
1. [项目架构](#项目架构)
2. [代码规范](#代码规范)
3. [开发环境设置](#开发环境设置)
4. [功能开发流程](#功能开发流程)
5. [测试指南](#测试指南)
6. [文档维护](#文档维护)
7. [版本管理](#版本管理)

## 项目架构

### 核心模块设计

```
game_prototype/
├── 核心系统
│   ├── main.py              # 游戏主入口
│   ├── game_state.py        # 游戏状态管理
│   ├── game_data.py         # 游戏数据配置
│   └── actions.py           # 基础游戏动作
├── 易经系统
│   ├── yijing_mechanics.py  # 易经哲学机制
│   ├── yijing_actions.py    # 增强的易经动作
│   └── generate_64_guas.py  # 64卦生成器
├── 增强系统 🆕
│   ├── wisdom_system.py     # 智慧系统 🧠
│   ├── tutorial_system.py   # 教学系统 📚
│   ├── achievement_system.py # 成就系统 🏆
│   ├── enhanced_cards.py    # 增强卡牌系统 🃏
│   └── enhanced_victory.py  # 增强胜利条件
├── 卡牌系统
│   └── cards_data/          # 卡牌数据目录
└── 测试演示
    ├── test_systems_integration.py # 系统集成测试
    └── interactive_demo.py  # 交互式演示
```

### 模块职责

#### 核心系统
- **main.py**: 游戏主循环，玩家交互界面，集成所有系统
- **game_state.py**: 游戏状态数据结构，玩家属性管理
- **game_data.py**: 游戏配置，卡组定义，平衡参数
- **actions.py**: 基础游戏动作（打牌、冥想、学习等）

#### 易经系统
- **yijing_mechanics.py**: 阴阳、五行、变卦等核心机制
- **yijing_actions.py**: 集成易经哲学的增强动作系统
- **generate_64_guas.py**: 自动生成64卦卡牌数据

#### 增强系统 🆕
- **wisdom_system.py**: 智慧格言库，触发机制，属性加成
- **tutorial_system.py**: 分类教学，互动课程，进度管理
- **achievement_system.py**: 成就追踪，奖励发放，稀有度分级
- **enhanced_cards.py**: 增强卡牌，特殊效果，易经融合
- **enhanced_victory.py**: 多元胜利条件，平衡机制

#### 卡牌系统
- **card_base.py**: 卡牌基础类定义
- **各卦文件**: 具体卦象的卡牌数据和爻辞任务

### 数据流设计

```
用户输入 → 动作验证 → 状态更新 → 易经机制应用 → 结果反馈
    ↓           ↓           ↓           ↓           ↓
  main.py → actions.py → game_state → yijing_* → 界面显示
```

## 代码规范

### Python编码标准

#### 1. 命名规范
```python
# 类名：大驼峰命名
class GameState:
    pass

class YinYangBalance:
    pass

# 函数名：小写下划线
def apply_yin_yang_effect():
    pass

def get_current_player():
    pass

# 常量：全大写下划线
MAX_HAND_SIZE = 7
DEFAULT_QI = 5

# 变量：小写下划线
current_player = None
yin_yang_balance = YinYangBalance()
```

#### 2. 类型提示
```python
from typing import Optional, List, Dict, Union

def enhanced_play_card(
    game_state: GameState, 
    card_index: int, 
    target_gua: str
) -> GameState:
    """增强的打牌动作"""
    pass

def get_players_by_position(
    players: List[Player], 
    position: Zone
) -> List[Player]:
    """根据位置获取玩家列表"""
    pass
```

#### 3. 文档字符串
```python
def apply_wuxing_effect(player: Player, element: WuXing, points: int = 1) -> Optional[str]:
    """
    应用五行效果到玩家
    
    Args:
        player: 目标玩家
        element: 五行元素
        points: 效果点数，默认为1
    
    Returns:
        如果触发相生效果，返回描述字符串；否则返回None
    
    Example:
        >>> player = Player("张三")
        >>> result = apply_wuxing_effect(player, WuXing.WOOD, 2)
        >>> print(result)  # "木生火"
    """
    pass
```

#### 4. 错误处理
```python
def play_card(game_state: GameState, card_index: int) -> GameState:
    """打牌动作"""
    try:
        current_player = game_state.get_current_player()
        
        if card_index >= len(current_player.hand):
            raise ValueError(f"卡牌索引 {card_index} 超出手牌范围")
        
        if current_player.qi < 1:
            raise ValueError("气不足，无法打牌")
        
        # 执行打牌逻辑
        return execute_play_card(game_state, card_index)
        
    except ValueError as e:
        print(f"打牌失败: {e}")
        return game_state
    except Exception as e:
        print(f"未知错误: {e}")
        return game_state
```

### 代码组织原则

#### 1. 单一职责原则
每个函数只做一件事：
```python
# 好的例子
def calculate_yin_yang_balance(yin_points: int, yang_points: int) -> float:
    """只计算阴阳平衡度"""
    return min(yin_points, yang_points) / max(yin_points, yang_points)

def apply_balance_bonus(player: Player, balance_ratio: float) -> int:
    """只应用平衡奖励"""
    if balance_ratio >= 0.8:
        bonus = 2
    elif balance_ratio >= 0.6:
        bonus = 1
    else:
        bonus = 0
    
    player.qi += bonus
    return bonus
```

#### 2. 开闭原则
对扩展开放，对修改封闭：
```python
# 基础动作接口
class BaseAction:
    def execute(self, game_state: GameState) -> GameState:
        raise NotImplementedError

# 具体动作实现
class PlayCardAction(BaseAction):
    def execute(self, game_state: GameState) -> GameState:
        # 实现具体逻辑
        pass
```

## 新增系统开发指南 🆕

### 智慧系统开发
智慧系统负责管理格言库和触发机制：

#### 核心组件
```python
# wisdom_system.py 结构
class WisdomSystem:
    def __init__(self):
        self.wisdom_quotes = {}  # 格言库
        self.player_progress = {}  # 玩家进度
    
    def trigger_wisdom(self, trigger_type: str, context: dict) -> dict:
        """触发智慧格言"""
        pass
    
    def apply_wisdom_bonus(self, player_name: str, wisdom_data: dict):
        """应用智慧奖励"""
        pass
```

#### 开发要点
- 格言分类管理（修身、治国、处世等）
- 触发条件设计（行动、状态、随机）
- 属性加成平衡（避免过强或过弱）

### 教学系统开发
教学系统提供分层次的学习内容：

#### 核心组件
```python
# tutorial_system.py 结构
class TutorialSystem:
    def __init__(self):
        self.lessons = {}  # 课程内容
        self.player_progress = {}  # 学习进度
    
    def start_lesson(self, player_name: str, lesson_id: str):
        """开始课程"""
        pass
    
    def complete_lesson(self, player_name: str, lesson_id: str):
        """完成课程"""
        pass
```

#### 开发要点
- 课程内容分级（基础→进阶→高级）
- 互动元素设计（问答、演示、实践）
- 学习奖励机制（资源、能力、成就）

### 成就系统开发
成就系统追踪玩家行为并提供奖励：

#### 核心组件
```python
# achievement_system.py 结构
class AchievementSystem:
    def __init__(self):
        self.achievements = {}  # 成就定义
        self.player_achievements = {}  # 玩家成就
    
    def check_achievements(self, player_name: str, action_data: dict):
        """检查成就触发"""
        pass
    
    def unlock_achievement(self, player_name: str, achievement_id: str):
        """解锁成就"""
        pass
```

#### 开发要点
- 成就条件设计（明确、可达成、有挑战性）
- 稀有度平衡（普通→稀有→史诗→传说）
- 奖励价值设计（有意义但不破坏平衡）

### 增强卡牌系统开发
增强卡牌系统提供更丰富的策略选择：

#### 核心组件
```python
# enhanced_cards.py 结构
class EnhancedCardSystem:
    def __init__(self):
        self.card_database = {}  # 卡牌数据库
        self.player_decks = {}  # 玩家卡组
    
    def use_card(self, player_name: str, card_id: str, target=None):
        """使用卡牌"""
        pass
    
    def get_available_cards(self, player_name: str) -> list:
        """获取可用卡牌"""
        pass
```

#### 开发要点
- 卡牌效果设计（简单→复杂→组合）
- 易经元素融合（卦象、阴阳、五行）
- 平衡性测试（避免过强卡牌）

## 系统集成开发流程

### 1. 新系统开发步骤
1. **需求分析**：明确系统功能和目标
2. **接口设计**：定义与其他系统的交互接口
3. **核心实现**：开发系统核心功能
4. **集成测试**：与现有系统集成测试
5. **平衡调整**：根据测试结果调整参数

### 2. 集成注意事项
- **导入顺序**：确保正确的模块导入顺序
- **状态同步**：保持各系统状态一致性
- **错误处理**：添加完善的异常处理机制
- **性能优化**：避免系统间的重复计算

### 3. 测试验证
```python
# 系统集成测试示例
def test_systems_integration():
    """测试所有系统的集成"""
    # 初始化所有系统
    wisdom_system.initialize()
    tutorial_system.initialize()
    achievement_system.initialize()
    enhanced_card_system.initialize()
    
    # 模拟玩家行为
    player_name = "测试玩家"
    
    # 测试系统间交互
    # ...测试逻辑
    
    print("✅ 所有系统集成测试通过")
```
        # 实现打牌逻辑
        pass

class MeditateAction(BaseAction):
    def execute(self, game_state: GameState) -> GameState:
        # 实现冥想逻辑
        pass
```

## 开发环境设置

### 1. 环境要求
```bash
# Python版本
Python 3.7+

# 开发工具（推荐）
VS Code / PyCharm
Git
```

### 2. 项目设置
```bash
# 克隆项目
git clone [项目地址]
cd we-feat-tianjibian-rules-v1

# 创建虚拟环境（可选）
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows

# 安装开发依赖（如果有）
pip install -r requirements-dev.txt
```

### 3. IDE配置

#### VS Code设置
```json
// .vscode/settings.json
{
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.formatting.provider": "black",
    "python.sortImports.args": ["--profile", "black"],
    "editor.formatOnSave": true
}
```

#### PyCharm设置
- 设置Python解释器为项目虚拟环境
- 启用代码检查和格式化
- 配置运行配置

## 功能开发流程

### 1. 需求分析
在开发新功能前，明确：
- 功能目标和用户价值
- 易经文化教育价值
- 与现有系统的集成方式
- 性能和平衡性考虑

### 2. 设计阶段
```python
# 示例：新增"占卜"功能设计

# 1. 定义数据结构
@dataclass
class DivinationResult:
    primary_gua: str      # 本卦
    changing_lines: List[int]  # 变爻
    transformed_gua: str  # 变卦
    interpretation: str   # 解释

# 2. 定义接口
def perform_divination(
    player: Player, 
    question: str
) -> DivinationResult:
    """执行占卜"""
    pass

# 3. 集成到游戏状态
class Player:
    def __init__(self):
        # ... 现有属性
        self.divination_history: List[DivinationResult] = []
```

### 3. 实现阶段

#### 步骤1：核心逻辑
```python
def perform_divination(player: Player, question: str) -> DivinationResult:
    """占卜功能核心实现"""
    # 消耗资源
    if player.cheng_yi < 2:
        raise ValueError("诚意不足，无法占卜")
    
    player.cheng_yi -= 2
    
    # 生成卦象
    primary_gua = generate_random_gua()
    changing_lines = generate_changing_lines()
    transformed_gua = apply_changes(primary_gua, changing_lines)
    
    # 生成解释
    interpretation = generate_interpretation(primary_gua, transformed_gua, question)
    
    result = DivinationResult(
        primary_gua=primary_gua,
        changing_lines=changing_lines,
        transformed_gua=transformed_gua,
        interpretation=interpretation
    )
    
    player.divination_history.append(result)
    return result
```

#### 步骤2：集成到动作系统
```python
def enhanced_divination(game_state: GameState, question: str) -> GameState:
    """集成易经哲学的占卜动作"""
    new_state = copy.deepcopy(game_state)
    current_player = new_state.get_current_player()
    
    try:
        result = perform_divination(current_player, question)
        
        # 应用易经机制
        apply_divination_effects(current_player, result)
        
        # 显示结果
        display_divination_result(result)
        
        return new_state
        
    except ValueError as e:
        print(f"占卜失败: {e}")
        return game_state
```

#### 步骤3：用户界面集成
```python
def handle_divination_command(game_state: GameState) -> GameState:
    """处理占卜命令"""
    question = input("请输入您要占卜的问题: ")
    
    if not question.strip():
        print("请输入有效的问题")
        return game_state
    
    return enhanced_divination(game_state, question)
```

### 4. 测试阶段

#### 单元测试
```python
def test_perform_divination():
    """测试占卜功能"""
    player = Player("测试玩家")
    player.cheng_yi = 5
    
    result = perform_divination(player, "今日运势如何？")
    
    assert result.primary_gua in ALL_64_GUAS
    assert result.transformed_gua in ALL_64_GUAS
    assert len(result.interpretation) > 0
    assert player.cheng_yi == 3  # 消耗了2点诚意

def test_divination_insufficient_resources():
    """测试资源不足的情况"""
    player = Player("测试玩家")
    player.cheng_yi = 1
    
    with pytest.raises(ValueError):
        perform_divination(player, "测试问题")
```

#### 集成测试
```python
def test_divination_integration():
    """测试占卜功能集成"""
    game_state = create_test_game_state()
    initial_cheng_yi = game_state.get_current_player().cheng_yi
    
    new_state = enhanced_divination(game_state, "测试问题")
    
    assert new_state.get_current_player().cheng_yi == initial_cheng_yi - 2
    assert len(new_state.get_current_player().divination_history) == 1
```

## 测试指南

### 测试策略

#### 1. 单元测试
测试单个函数或方法：
```python
import unittest
from game_prototype.yijing_mechanics import YinYangBalance

class TestYinYangBalance(unittest.TestCase):
    def setUp(self):
        self.balance = YinYangBalance()
    
    def test_initial_state(self):
        """测试初始状态"""
        self.assertEqual(self.balance.yin_points, 0)
        self.assertEqual(self.balance.yang_points, 0)
        self.assertEqual(self.balance.balance_ratio, 1.0)
    
    def test_add_yin_points(self):
        """测试添加阴点"""
        self.balance.yin_points = 3
        self.balance.yang_points = 2
        self.assertAlmostEqual(self.balance.balance_ratio, 2/3, places=2)
    
    def test_balance_bonus(self):
        """测试平衡奖励"""
        self.balance.yin_points = 4
        self.balance.yang_points = 5
        bonus = self.balance.get_balance_bonus()
        self.assertEqual(bonus, 1)  # 平衡度0.8，应该获得1点奖励
```

#### 2. 集成测试
测试模块间的交互：
```python
def test_play_card_with_yijing_effects():
    """测试打牌的易经效果"""
    game_state = create_test_game_state()
    player = game_state.get_current_player()
    
    # 给玩家一张乾卦卡牌
    qian_card = create_qian_card()
    player.hand.append(qian_card)
    
    # 打出卡牌
    new_state = enhanced_play_card(game_state, 0, "乾为天")
    
    # 验证易经效果
    new_player = new_state.get_current_player()
    assert new_player.yin_yang_balance.yang_points > player.yin_yang_balance.yang_points
    assert new_player.wuxing_affinities[WuXing.METAL] > player.wuxing_affinities[WuXing.METAL]
```

#### 3. 游戏流程测试
测试完整的游戏流程：
```python
def test_complete_game_flow():
    """测试完整游戏流程"""
    game_state = setup_game(["玩家1", "玩家2"])
    
    # 模拟多轮游戏
    for turn in range(20):
        # 执行随机动作
        action = random.choice(["play", "meditate", "study"])
        game_state = execute_action(game_state, action)
        
        # 检查胜利条件
        winner = check_victory_conditions_enhanced(game_state)
        if winner:
            break
    
    # 验证游戏状态的一致性
    assert_game_state_valid(game_state)
```

### 测试数据管理

#### 创建测试数据
```python
def create_test_game_state() -> GameState:
    """创建测试用游戏状态"""
    players = [
        Player("测试玩家1"),
        Player("测试玩家2")
    ]
    
    # 设置测试用的初始状态
    for player in players:
        player.qi = 10
        player.dao_xing = 5
        player.cheng_yi = 3
        player.hand = create_test_hand()
    
    return GameState(players=players, current_player_index=0)

def create_test_hand() -> List[GuaCard]:
    """创建测试用手牌"""
    return [
        create_qian_card(),
        create_kun_card(),
        create_zhen_card()
    ]
```

## 文档维护

### 文档类型

#### 1. API文档
使用docstring自动生成：
```python
def apply_yin_yang_effect(player: Player, yin_yang: YinYang, points: int = 1):
    """
    应用阴阳效果到玩家
    
    这个函数会根据指定的阴阳属性，为玩家增加相应的阴阳点数。
    当阴阳达到平衡时，玩家会获得额外的奖励。
    
    Args:
        player (Player): 目标玩家对象
        yin_yang (YinYang): 阴阳属性，YinYang.YIN 或 YinYang.YANG
        points (int, optional): 要增加的点数，默认为1
    
    Returns:
        None: 该函数直接修改玩家对象，不返回值
    
    Raises:
        ValueError: 当points为负数时抛出
    
    Example:
        >>> player = Player("张三")
        >>> apply_yin_yang_effect(player, YinYang.YANG, 2)
        >>> print(player.yin_yang_balance.yang_points)
        2
    
    Note:
        - 阴阳平衡会影响玩家的气值奖励
        - 建议在每次应用效果后检查平衡状态
    
    See Also:
        - YinYangBalance.get_balance_bonus(): 获取平衡奖励
        - TaijiMechanism.apply_transformation(): 应用太极转化
    """
    pass
```

#### 2. 用户文档
- README.md: 项目概述和快速开始
- YIJING_GUIDE.md: 易经知识详解
- GAME_RULES.md: 详细游戏规则

#### 3. 开发文档
- DEVELOPMENT_GUIDE.md: 开发指南（本文档）
- API_REFERENCE.md: API参考
- CHANGELOG.md: 版本更新日志

### 文档更新流程

#### 1. 代码变更时
- 更新相关的docstring
- 更新API文档
- 更新示例代码

#### 2. 功能添加时
- 在README中添加功能说明
- 更新游戏规则文档
- 添加使用示例

#### 3. 版本发布时
- 更新CHANGELOG
- 检查所有文档的一致性
- 生成API文档

## 版本管理

### Git工作流

#### 1. 分支策略
```bash
main        # 主分支，稳定版本
develop     # 开发分支，集成新功能
feature/*   # 功能分支，开发具体功能
hotfix/*    # 热修复分支，紧急修复
```

#### 2. 提交规范
```bash
# 提交消息格式
<type>(<scope>): <subject>

<body>

<footer>

# 示例
feat(yijing): 添加变卦机制

- 实现变卦转化逻辑
- 添加变卦历史记录
- 集成到游戏动作系统

Closes #123
```

#### 3. 提交类型
- `feat`: 新功能
- `fix`: 修复bug
- `docs`: 文档更新
- `style`: 代码格式调整
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建过程或辅助工具的变动

### 发布流程

#### 1. 功能开发
```bash
# 创建功能分支
git checkout -b feature/divination-system

# 开发和提交
git add .
git commit -m "feat(divination): 实现占卜系统核心逻辑"

# 推送分支
git push origin feature/divination-system
```

#### 2. 代码审查
- 创建Pull Request
- 代码审查和讨论
- 修改和完善

#### 3. 合并和发布
```bash
# 合并到develop分支
git checkout develop
git merge feature/divination-system

# 测试和验证
python -m pytest

# 合并到main分支
git checkout main
git merge develop

# 创建版本标签
git tag -a v1.2.0 -m "Release version 1.2.0"
git push origin v1.2.0
```

### 版本号规范

使用语义化版本号：`MAJOR.MINOR.PATCH`

- **MAJOR**: 不兼容的API修改
- **MINOR**: 向后兼容的功能性新增
- **PATCH**: 向后兼容的问题修正

示例：
- `1.0.0`: 初始版本
- `1.1.0`: 添加占卜功能
- `1.1.1`: 修复占卜bug
- `2.0.0`: 重构游戏引擎

## 协作最佳实践

### 1. 沟通协作
- 使用GitHub Issues跟踪任务和bug
- 定期进行代码审查
- 保持文档同步更新
- 及时响应Pull Request

### 2. 代码质量
- 编写清晰的代码和注释
- 保持测试覆盖率
- 遵循项目编码规范
- 定期重构和优化

### 3. 知识分享
- 记录设计决策和原因
- 分享易经文化知识
- 维护开发日志
- 组织技术讨论

---

通过遵循这些指南，我们可以确保项目的高质量开发和团队协作的顺畅进行。