"""
天机变游戏通用工具
提供游戏逻辑相关的工具函数
"""

from typing import Dict, List, Tuple, Optional, Any, Union
import random
import math
from dataclasses import dataclass
from enum import Enum

from ..core.base_types import *
from ..core.constants import *

# ==================== 位置和移动相关 ====================

def calculate_distance(pos1: Position, pos2: Position) -> float:
    """
    计算两个位置之间的距离
    
    Args:
        pos1: 第一个位置
        pos2: 第二个位置
        
    Returns:
        距离值
    """
    return math.sqrt((pos1.x - pos2.x) ** 2 + (pos1.y - pos2.y) ** 2)

def get_adjacent_positions(pos: Position, board_size: int = 19) -> List[Position]:
    """
    获取相邻位置
    
    Args:
        pos: 当前位置
        board_size: 棋盘大小
        
    Returns:
        相邻位置列表
    """
    adjacent = []
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # 上右下左
    
    for dx, dy in directions:
        new_x, new_y = pos.x + dx, pos.y + dy
        if 0 <= new_x < board_size and 0 <= new_y < board_size:
            adjacent.append(Position(new_x, new_y))
    
    return adjacent

def is_valid_position(pos: Position, board_size: int = 19) -> bool:
    """
    检查位置是否有效
    
    Args:
        pos: 位置
        board_size: 棋盘大小
        
    Returns:
        是否有效
    """
    return 0 <= pos.x < board_size and 0 <= pos.y < board_size

def get_positions_in_range(center: Position, range_val: int, board_size: int = 19) -> List[Position]:
    """
    获取范围内的所有位置
    
    Args:
        center: 中心位置
        range_val: 范围
        board_size: 棋盘大小
        
    Returns:
        范围内位置列表
    """
    positions = []
    
    for x in range(max(0, center.x - range_val), min(board_size, center.x + range_val + 1)):
        for y in range(max(0, center.y - range_val), min(board_size, center.y + range_val + 1)):
            pos = Position(x, y)
            if calculate_distance(center, pos) <= range_val:
                positions.append(pos)
    
    return positions

def get_line_positions(start: Position, end: Position) -> List[Position]:
    """
    获取两点之间直线上的所有位置
    
    Args:
        start: 起始位置
        end: 结束位置
        
    Returns:
        直线上的位置列表
    """
    positions = []
    
    dx = abs(end.x - start.x)
    dy = abs(end.y - start.y)
    
    x, y = start.x, start.y
    
    x_inc = 1 if end.x > start.x else -1
    y_inc = 1 if end.y > start.y else -1
    
    error = dx - dy
    
    while True:
        positions.append(Position(x, y))
        
        if x == end.x and y == end.y:
            break
        
        error2 = 2 * error
        
        if error2 > -dy:
            error -= dy
            x += x_inc
        
        if error2 < dx:
            error += dx
            y += y_inc
    
    return positions

# ==================== 资源相关计算 ====================

def calculate_resource_cost(
    base_cost: Dict[ResourceType, int], 
    multiplier: float = 1.0,
    discounts: Optional[Dict[ResourceType, float]] = None
) -> Dict[ResourceType, int]:
    """
    计算资源消耗
    
    Args:
        base_cost: 基础消耗
        multiplier: 倍数
        discounts: 折扣字典
        
    Returns:
        实际消耗
    """
    actual_cost = {}
    discounts = discounts or {}
    
    for resource, amount in base_cost.items():
        discount = discounts.get(resource, 0.0)
        final_amount = int(amount * multiplier * (1.0 - discount))
        actual_cost[resource] = max(0, final_amount)
    
    return actual_cost

def can_afford_cost(
    resources: Dict[ResourceType, int], 
    cost: Dict[ResourceType, int]
) -> bool:
    """
    检查是否能承担消耗
    
    Args:
        resources: 当前资源
        cost: 需要消耗的资源
        
    Returns:
        是否能承担
    """
    for resource, amount in cost.items():
        if resources.get(resource, 0) < amount:
            return False
    return True

def apply_resource_cost(
    resources: Dict[ResourceType, int], 
    cost: Dict[ResourceType, int]
) -> Dict[ResourceType, int]:
    """
    应用资源消耗
    
    Args:
        resources: 当前资源
        cost: 消耗的资源
        
    Returns:
        消耗后的资源
    """
    new_resources = resources.copy()
    
    for resource, amount in cost.items():
        new_resources[resource] = max(0, new_resources.get(resource, 0) - amount)
    
    return new_resources

def calculate_resource_efficiency(
    input_resources: Dict[ResourceType, int],
    output_resources: Dict[ResourceType, int],
    weights: Optional[Dict[ResourceType, float]] = None
) -> float:
    """
    计算资源效率
    
    Args:
        input_resources: 输入资源
        output_resources: 输出资源
        weights: 资源权重
        
    Returns:
        效率值
    """
    weights = weights or {resource: 1.0 for resource in ResourceType}
    
    input_value = sum(amount * weights.get(resource, 1.0) 
                     for resource, amount in input_resources.items())
    output_value = sum(amount * weights.get(resource, 1.0) 
                      for resource, amount in output_resources.items())
    
    return output_value / input_value if input_value > 0 else 0.0

# ==================== 概率和随机相关 ====================

def weighted_random_choice(choices: Dict[Any, float]) -> Any:
    """
    加权随机选择
    
    Args:
        choices: 选择项和权重字典
        
    Returns:
        选中的项
    """
    if not choices:
        return None
    
    total_weight = sum(choices.values())
    if total_weight <= 0:
        return random.choice(list(choices.keys()))
    
    rand_val = random.uniform(0, total_weight)
    current_weight = 0
    
    for choice, weight in choices.items():
        current_weight += weight
        if rand_val <= current_weight:
            return choice
    
    return list(choices.keys())[-1]  # 备选

def calculate_success_probability(
    base_chance: float,
    modifiers: List[float],
    min_chance: float = 0.01,
    max_chance: float = 0.99
) -> float:
    """
    计算成功概率
    
    Args:
        base_chance: 基础概率
        modifiers: 修正值列表
        min_chance: 最小概率
        max_chance: 最大概率
        
    Returns:
        最终概率
    """
    final_chance = base_chance
    
    for modifier in modifiers:
        final_chance += modifier
    
    return max(min_chance, min(max_chance, final_chance))

def roll_dice(sides: int = 6, count: int = 1) -> List[int]:
    """
    掷骰子
    
    Args:
        sides: 骰子面数
        count: 骰子数量
        
    Returns:
        结果列表
    """
    return [random.randint(1, sides) for _ in range(count)]

def check_critical_success(roll: int, threshold: int = 95) -> bool:
    """
    检查是否大成功
    
    Args:
        roll: 掷骰结果 (1-100)
        threshold: 大成功阈值
        
    Returns:
        是否大成功
    """
    return roll >= threshold

def check_critical_failure(roll: int, threshold: int = 5) -> bool:
    """
    检查是否大失败
    
    Args:
        roll: 掷骰结果 (1-100)
        threshold: 大失败阈值
        
    Returns:
        是否大失败
    """
    return roll <= threshold

# ==================== 游戏平衡相关 ====================

def calculate_power_level(
    resources: Dict[ResourceType, int],
    cultivation_realm: CultivationRealm,
    wuxing_total: int,
    bagua_total: int
) -> int:
    """
    计算玩家实力等级
    
    Args:
        resources: 资源字典
        cultivation_realm: 修为境界
        wuxing_total: 五行总掌握度
        bagua_total: 八卦总亲和度
        
    Returns:
        实力等级
    """
    # 基础实力（修为境界）
    realm_power = list(CultivationRealm).index(cultivation_realm) * 100
    
    # 资源实力
    resource_power = sum(resources.values()) // 10
    
    # 易学实力
    yixue_power = (wuxing_total + bagua_total) // 5
    
    return realm_power + resource_power + yixue_power

def calculate_action_difficulty(
    action_type: ActionType,
    player_power: int,
    environmental_factors: Optional[Dict[str, float]] = None
) -> float:
    """
    计算行动难度
    
    Args:
        action_type: 行动类型
        player_power: 玩家实力
        environmental_factors: 环境因素
        
    Returns:
        难度系数 (0.1-2.0)
    """
    base_difficulty = {
        ActionType.MOVE: 0.1,
        ActionType.PLACE_STONE: 0.3,
        ActionType.CULTIVATE: 0.5,
        ActionType.CAST_SPELL: 0.7,
        ActionType.SPECIAL_ABILITY: 0.9,
        ActionType.PASS: 0.0
    }
    
    difficulty = base_difficulty.get(action_type, 0.5)
    
    # 根据玩家实力调整
    power_modifier = max(0.1, 1.0 - (player_power / 1000))
    difficulty *= power_modifier
    
    # 应用环境因素
    if environmental_factors:
        for factor, value in environmental_factors.items():
            difficulty *= (1.0 + value)
    
    return max(0.1, min(2.0, difficulty))

def balance_reward(
    base_reward: Dict[ResourceType, int],
    difficulty: float,
    player_level: int
) -> Dict[ResourceType, int]:
    """
    平衡奖励
    
    Args:
        base_reward: 基础奖励
        difficulty: 难度系数
        player_level: 玩家等级
        
    Returns:
        平衡后的奖励
    """
    balanced_reward = {}
    
    # 难度调整
    difficulty_multiplier = 0.5 + difficulty
    
    # 等级调整（高等级玩家获得更多奖励）
    level_multiplier = 1.0 + (player_level / 100)
    
    for resource, amount in base_reward.items():
        final_amount = int(amount * difficulty_multiplier * level_multiplier)
        balanced_reward[resource] = max(1, final_amount)
    
    return balanced_reward

# ==================== 字符串和格式化工具 ====================

def format_resources(resources: Dict[ResourceType, int]) -> str:
    """
    格式化资源显示
    
    Args:
        resources: 资源字典
        
    Returns:
        格式化字符串
    """
    if not resources:
        return "无资源"
    
    formatted = []
    for resource, amount in resources.items():
        name = RESOURCE_DISPLAY_NAMES.get(resource, resource.value)
        formatted.append(f"{name}: {amount}")
    
    return ", ".join(formatted)

def format_position(pos: Position) -> str:
    """
    格式化位置显示
    
    Args:
        pos: 位置
        
    Returns:
        格式化字符串
    """
    return f"({pos.x}, {pos.y})"

def format_percentage(value: float, decimal_places: int = 1) -> str:
    """
    格式化百分比显示
    
    Args:
        value: 数值 (0.0-1.0)
        decimal_places: 小数位数
        
    Returns:
        格式化字符串
    """
    percentage = value * 100
    return f"{percentage:.{decimal_places}f}%"

def truncate_text(text: str, max_length: int, suffix: str = "...") -> str:
    """
    截断文本
    
    Args:
        text: 原文本
        max_length: 最大长度
        suffix: 后缀
        
    Returns:
        截断后的文本
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix

# ==================== 验证和检查工具 ====================

def validate_game_state(state: Any) -> List[str]:
    """
    验证游戏状态
    
    Args:
        state: 游戏状态
        
    Returns:
        错误信息列表
    """
    errors = []
    
    # 这里可以添加具体的验证逻辑
    # 例如检查玩家数量、资源合理性等
    
    return errors

def sanitize_input(input_str: str, max_length: int = 100) -> str:
    """
    清理输入字符串
    
    Args:
        input_str: 输入字符串
        max_length: 最大长度
        
    Returns:
        清理后的字符串
    """
    if not isinstance(input_str, str):
        return ""
    
    # 移除危险字符
    sanitized = input_str.strip()
    sanitized = sanitized.replace("<", "&lt;").replace(">", "&gt;")
    
    return truncate_text(sanitized, max_length)

def is_valid_player_name(name: str) -> bool:
    """
    检查玩家名称是否有效
    
    Args:
        name: 玩家名称
        
    Returns:
        是否有效
    """
    if not name or len(name.strip()) == 0:
        return False
    
    if len(name) > 20:
        return False
    
    # 检查是否包含非法字符
    illegal_chars = ["<", ">", "&", "\"", "'", "/", "\\"]
    for char in illegal_chars:
        if char in name:
            return False
    
    return True

# ==================== 性能优化工具 ====================

def batch_process(items: List[Any], batch_size: int = 100) -> List[List[Any]]:
    """
    批量处理数据
    
    Args:
        items: 数据列表
        batch_size: 批次大小
        
    Returns:
        批次列表
    """
    batches = []
    for i in range(0, len(items), batch_size):
        batches.append(items[i:i + batch_size])
    return batches

def memoize(func):
    """
    记忆化装饰器
    """
    cache = {}
    
    def wrapper(*args, **kwargs):
        key = str(args) + str(sorted(kwargs.items()))
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]
    
    return wrapper

# ==================== 调试和测试工具 ====================

def create_test_player(
    name: str = "测试玩家",
    player_type: PlayerType = PlayerType.HUMAN,
    resources: Optional[Dict[ResourceType, int]] = None
) -> Dict[str, Any]:
    """
    创建测试玩家数据
    
    Args:
        name: 玩家名称
        player_type: 玩家类型
        resources: 初始资源
        
    Returns:
        玩家数据字典
    """
    default_resources = {
        ResourceType.WOOD: 10,
        ResourceType.FIRE: 10,
        ResourceType.EARTH: 10,
        ResourceType.METAL: 10,
        ResourceType.WATER: 10,
        ResourceType.CULTURE: 50,
        ResourceType.WISDOM: 20
    }
    
    return {
        "name": name,
        "type": player_type,
        "resources": resources or default_resources,
        "cultivation_realm": CultivationRealm.MORTAL,
        "yin": 5,
        "yang": 5,
        "wuxing_mastery": {elem: 1 for elem in WuxingElement},
        "bagua_affinity": {bagua: 1 for bagua in BaguaType}
    }

def generate_random_position(board_size: int = 19) -> Position:
    """
    生成随机位置
    
    Args:
        board_size: 棋盘大小
        
    Returns:
        随机位置
    """
    return Position(
        random.randint(0, board_size - 1),
        random.randint(0, board_size - 1)
    )

def create_debug_info(data: Any, title: str = "调试信息") -> str:
    """
    创建调试信息字符串
    
    Args:
        data: 数据
        title: 标题
        
    Returns:
        调试信息字符串
    """
    import json
    
    try:
        if hasattr(data, '__dict__'):
            data_dict = data.__dict__
        else:
            data_dict = data
        
        formatted = json.dumps(data_dict, indent=2, ensure_ascii=False, default=str)
        return f"=== {title} ===\n{formatted}\n"
    except Exception as e:
        return f"=== {title} ===\n无法格式化数据: {e}\n"