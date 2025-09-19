"""
天机变游戏验证工具
提供数据验证和检查功能
"""

from typing import Dict, List, Tuple, Optional, Any, Union, Callable
import re
from dataclasses import dataclass
from enum import Enum

from ..core.base_types import *
from ..core.constants import *
from ..core.exceptions import *

# ==================== 验证结果类 ====================

@dataclass
class ValidationResult:
    """验证结果"""
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    
    def add_error(self, message: str) -> None:
        """添加错误"""
        self.errors.append(message)
        self.is_valid = False
    
    def add_warning(self, message: str) -> None:
        """添加警告"""
        self.warnings.append(message)
    
    def merge(self, other: 'ValidationResult') -> None:
        """合并验证结果"""
        if not other.is_valid:
            self.is_valid = False
        self.errors.extend(other.errors)
        self.warnings.extend(other.warnings)

def create_validation_result(is_valid: bool = True) -> ValidationResult:
    """创建验证结果"""
    return ValidationResult(is_valid=is_valid, errors=[], warnings=[])

# ==================== 基础验证器 ====================

class BaseValidator:
    """基础验证器"""
    
    def __init__(self, name: str):
        self.name = name
    
    def validate(self, value: Any) -> ValidationResult:
        """验证值"""
        raise NotImplementedError
    
    def __call__(self, value: Any) -> ValidationResult:
        return self.validate(value)

class RangeValidator(BaseValidator):
    """范围验证器"""
    
    def __init__(self, name: str, min_val: Union[int, float], max_val: Union[int, float]):
        super().__init__(name)
        self.min_val = min_val
        self.max_val = max_val
    
    def validate(self, value: Union[int, float]) -> ValidationResult:
        result = create_validation_result()
        
        if not isinstance(value, (int, float)):
            result.add_error(f"{self.name}必须是数字")
            return result
        
        if value < self.min_val:
            result.add_error(f"{self.name}不能小于{self.min_val}")
        elif value > self.max_val:
            result.add_error(f"{self.name}不能大于{self.max_val}")
        
        return result

class LengthValidator(BaseValidator):
    """长度验证器"""
    
    def __init__(self, name: str, min_length: int = 0, max_length: int = 100):
        super().__init__(name)
        self.min_length = min_length
        self.max_length = max_length
    
    def validate(self, value: str) -> ValidationResult:
        result = create_validation_result()
        
        if not isinstance(value, str):
            result.add_error(f"{self.name}必须是字符串")
            return result
        
        length = len(value)
        if length < self.min_length:
            result.add_error(f"{self.name}长度不能少于{self.min_length}个字符")
        elif length > self.max_length:
            result.add_error(f"{self.name}长度不能超过{self.max_length}个字符")
        
        return result

class PatternValidator(BaseValidator):
    """模式验证器"""
    
    def __init__(self, name: str, pattern: str, error_message: str = None):
        super().__init__(name)
        self.pattern = re.compile(pattern)
        self.error_message = error_message or f"{name}格式不正确"
    
    def validate(self, value: str) -> ValidationResult:
        result = create_validation_result()
        
        if not isinstance(value, str):
            result.add_error(f"{self.name}必须是字符串")
            return result
        
        if not self.pattern.match(value):
            result.add_error(self.error_message)
        
        return result

class ChoiceValidator(BaseValidator):
    """选择验证器"""
    
    def __init__(self, name: str, choices: List[Any]):
        super().__init__(name)
        self.choices = choices
    
    def validate(self, value: Any) -> ValidationResult:
        result = create_validation_result()
        
        if value not in self.choices:
            result.add_error(f"{self.name}必须是以下值之一: {self.choices}")
        
        return result

class TypeValidator(BaseValidator):
    """类型验证器"""
    
    def __init__(self, name: str, expected_type: type):
        super().__init__(name)
        self.expected_type = expected_type
    
    def validate(self, value: Any) -> ValidationResult:
        result = create_validation_result()
        
        if not isinstance(value, self.expected_type):
            result.add_error(f"{self.name}必须是{self.expected_type.__name__}类型")
        
        return result

# ==================== 游戏特定验证器 ====================

def validate_player_name(name: str) -> ValidationResult:
    """验证玩家名称"""
    result = create_validation_result()
    
    # 长度验证
    length_validator = LengthValidator("玩家名称", 1, 20)
    result.merge(length_validator.validate(name))
    
    if not result.is_valid:
        return result
    
    # 字符验证
    if not re.match(r'^[\u4e00-\u9fa5a-zA-Z0-9_\-]+$', name):
        result.add_error("玩家名称只能包含中文、英文、数字、下划线和连字符")
    
    # 敏感词检查
    sensitive_words = ["管理员", "系统", "GM", "admin", "system"]
    for word in sensitive_words:
        if word.lower() in name.lower():
            result.add_error(f"玩家名称不能包含敏感词: {word}")
    
    return result

def validate_position(pos: Position, board_size: int = 19) -> ValidationResult:
    """验证位置"""
    result = create_validation_result()
    
    if not isinstance(pos, Position):
        result.add_error("位置必须是Position类型")
        return result
    
    if pos.x < 0 or pos.x >= board_size:
        result.add_error(f"X坐标必须在0-{board_size-1}之间")
    
    if pos.y < 0 or pos.y >= board_size:
        result.add_error(f"Y坐标必须在0-{board_size-1}之间")
    
    return result

def validate_resources(resources: Dict[ResourceType, int]) -> ValidationResult:
    """验证资源"""
    result = create_validation_result()
    
    if not isinstance(resources, dict):
        result.add_error("资源必须是字典类型")
        return result
    
    for resource_type, amount in resources.items():
        if not isinstance(resource_type, ResourceType):
            result.add_error(f"资源类型{resource_type}无效")
            continue
        
        if not isinstance(amount, int):
            result.add_error(f"资源{resource_type.value}数量必须是整数")
            continue
        
        if amount < 0:
            result.add_error(f"资源{resource_type.value}数量不能为负数")
        
        # 检查资源上限
        max_amount = MAX_RESOURCE_AMOUNT.get(resource_type, 999999)
        if amount > max_amount:
            result.add_warning(f"资源{resource_type.value}数量{amount}超过建议上限{max_amount}")
    
    return result

def validate_wuxing_mastery(mastery: Dict[WuxingElement, int]) -> ValidationResult:
    """验证五行掌握度"""
    result = create_validation_result()
    
    if not isinstance(mastery, dict):
        result.add_error("五行掌握度必须是字典类型")
        return result
    
    # 检查是否包含所有五行元素
    required_elements = set(WuxingElement)
    provided_elements = set(mastery.keys())
    
    missing_elements = required_elements - provided_elements
    if missing_elements:
        result.add_error(f"缺少五行元素: {[elem.value for elem in missing_elements]}")
    
    extra_elements = provided_elements - required_elements
    if extra_elements:
        result.add_error(f"包含无效五行元素: {[elem.value for elem in extra_elements]}")
    
    # 验证每个元素的掌握度
    for element, value in mastery.items():
        if not isinstance(value, int):
            result.add_error(f"五行{element.value}掌握度必须是整数")
            continue
        
        if value < 0:
            result.add_error(f"五行{element.value}掌握度不能为负数")
        elif value > MAX_WUXING_MASTERY:
            result.add_error(f"五行{element.value}掌握度不能超过{MAX_WUXING_MASTERY}")
    
    return result

def validate_bagua_affinity(affinity: Dict[BaguaType, int]) -> ValidationResult:
    """验证八卦亲和度"""
    result = create_validation_result()
    
    if not isinstance(affinity, dict):
        result.add_error("八卦亲和度必须是字典类型")
        return result
    
    # 检查是否包含所有八卦
    required_bagua = set(BaguaType)
    provided_bagua = set(affinity.keys())
    
    missing_bagua = required_bagua - provided_bagua
    if missing_bagua:
        result.add_error(f"缺少八卦: {[bagua.value for bagua in missing_bagua]}")
    
    extra_bagua = provided_bagua - required_bagua
    if extra_bagua:
        result.add_error(f"包含无效八卦: {[bagua.value for bagua in extra_bagua]}")
    
    # 验证每个八卦的亲和度
    for bagua, value in affinity.items():
        if not isinstance(value, int):
            result.add_error(f"八卦{bagua.value}亲和度必须是整数")
            continue
        
        if value < 0:
            result.add_error(f"八卦{bagua.value}亲和度不能为负数")
        elif value > MAX_BAGUA_AFFINITY:
            result.add_error(f"八卦{bagua.value}亲和度不能超过{MAX_BAGUA_AFFINITY}")
    
    return result

def validate_cultivation_realm(realm: CultivationRealm) -> ValidationResult:
    """验证修为境界"""
    result = create_validation_result()
    
    if not isinstance(realm, CultivationRealm):
        result.add_error("修为境界必须是CultivationRealm类型")
    
    return result

def validate_yinyang_balance(yin: int, yang: int) -> ValidationResult:
    """验证阴阳平衡"""
    result = create_validation_result()
    
    if not isinstance(yin, int):
        result.add_error("阴能量必须是整数")
    elif yin < 0:
        result.add_error("阴能量不能为负数")
    elif yin > MAX_YINYANG_ENERGY:
        result.add_error(f"阴能量不能超过{MAX_YINYANG_ENERGY}")
    
    if not isinstance(yang, int):
        result.add_error("阳能量必须是整数")
    elif yang < 0:
        result.add_error("阳能量不能为负数")
    elif yang > MAX_YINYANG_ENERGY:
        result.add_error(f"阳能量不能超过{MAX_YINYANG_ENERGY}")
    
    # 检查平衡度
    if yin > 0 or yang > 0:
        total = yin + yang
        balance = min(yin, yang) / max(yin, yang) if max(yin, yang) > 0 else 1.0
        
        if balance < 0.1:
            result.add_warning("阴阳严重失衡，建议调整")
        elif balance < 0.3:
            result.add_warning("阴阳失衡，建议适当调整")
    
    return result

# ==================== 游戏行动验证 ====================

def validate_move_action(
    player_pos: Position, 
    target_pos: Position, 
    board_size: int = 19
) -> ValidationResult:
    """验证移动行动"""
    result = create_validation_result()
    
    # 验证位置
    result.merge(validate_position(player_pos, board_size))
    result.merge(validate_position(target_pos, board_size))
    
    if not result.is_valid:
        return result
    
    # 检查移动距离
    from ..utils.game_utils import calculate_distance
    distance = calculate_distance(player_pos, target_pos)
    
    if distance > MAX_MOVE_DISTANCE:
        result.add_error(f"移动距离{distance:.1f}超过最大限制{MAX_MOVE_DISTANCE}")
    
    if distance == 0:
        result.add_error("不能移动到当前位置")
    
    return result

def validate_place_stone_action(
    pos: Position, 
    board_state: Dict[Position, Any],
    board_size: int = 19
) -> ValidationResult:
    """验证放置棋子行动"""
    result = create_validation_result()
    
    # 验证位置
    result.merge(validate_position(pos, board_size))
    
    if not result.is_valid:
        return result
    
    # 检查位置是否已被占用
    if pos in board_state:
        result.add_error(f"位置{pos}已被占用")
    
    return result

def validate_resource_cost(
    available_resources: Dict[ResourceType, int],
    required_cost: Dict[ResourceType, int]
) -> ValidationResult:
    """验证资源消耗"""
    result = create_validation_result()
    
    # 验证资源格式
    result.merge(validate_resources(available_resources))
    result.merge(validate_resources(required_cost))
    
    if not result.is_valid:
        return result
    
    # 检查资源是否足够
    for resource_type, cost in required_cost.items():
        available = available_resources.get(resource_type, 0)
        if available < cost:
            result.add_error(f"资源{resource_type.value}不足，需要{cost}，当前{available}")
    
    return result

# ==================== 配置验证 ====================

def validate_game_config(config: Dict[str, Any]) -> ValidationResult:
    """验证游戏配置"""
    result = create_validation_result()
    
    # 必需的配置项
    required_keys = [
        "board_size", "max_players", "turn_time_limit",
        "initial_resources", "cultivation_enabled"
    ]
    
    for key in required_keys:
        if key not in config:
            result.add_error(f"缺少必需的配置项: {key}")
    
    if not result.is_valid:
        return result
    
    # 验证具体配置值
    board_size = config.get("board_size", 19)
    if not isinstance(board_size, int) or board_size < 9 or board_size > 25:
        result.add_error("棋盘大小必须是9-25之间的整数")
    
    max_players = config.get("max_players", 2)
    if not isinstance(max_players, int) or max_players < 2 or max_players > 8:
        result.add_error("最大玩家数必须是2-8之间的整数")
    
    turn_time_limit = config.get("turn_time_limit", 60)
    if not isinstance(turn_time_limit, int) or turn_time_limit < 10 or turn_time_limit > 300:
        result.add_error("回合时间限制必须是10-300秒之间的整数")
    
    # 验证初始资源
    initial_resources = config.get("initial_resources", {})
    if initial_resources:
        result.merge(validate_resources(initial_resources))
    
    return result

# ==================== 批量验证 ====================

def validate_player_data(player_data: Dict[str, Any]) -> ValidationResult:
    """验证玩家数据"""
    result = create_validation_result()
    
    # 验证玩家名称
    if "name" in player_data:
        result.merge(validate_player_name(player_data["name"]))
    
    # 验证资源
    if "resources" in player_data:
        result.merge(validate_resources(player_data["resources"]))
    
    # 验证五行掌握度
    if "wuxing_mastery" in player_data:
        result.merge(validate_wuxing_mastery(player_data["wuxing_mastery"]))
    
    # 验证八卦亲和度
    if "bagua_affinity" in player_data:
        result.merge(validate_bagua_affinity(player_data["bagua_affinity"]))
    
    # 验证修为境界
    if "cultivation_realm" in player_data:
        result.merge(validate_cultivation_realm(player_data["cultivation_realm"]))
    
    # 验证阴阳平衡
    if "yin" in player_data and "yang" in player_data:
        result.merge(validate_yinyang_balance(player_data["yin"], player_data["yang"]))
    
    return result

def validate_game_state(game_state: Dict[str, Any]) -> ValidationResult:
    """验证游戏状态"""
    result = create_validation_result()
    
    # 验证基本字段
    required_fields = ["players", "current_turn", "board_state", "game_phase"]
    for field in required_fields:
        if field not in game_state:
            result.add_error(f"游戏状态缺少必需字段: {field}")
    
    if not result.is_valid:
        return result
    
    # 验证玩家数据
    players = game_state.get("players", [])
    if not isinstance(players, list):
        result.add_error("玩家列表必须是数组类型")
    else:
        for i, player in enumerate(players):
            player_result = validate_player_data(player)
            if not player_result.is_valid:
                for error in player_result.errors:
                    result.add_error(f"玩家{i+1}: {error}")
    
    # 验证当前回合
    current_turn = game_state.get("current_turn", 0)
    if not isinstance(current_turn, int) or current_turn < 0:
        result.add_error("当前回合必须是非负整数")
    
    # 验证游戏阶段
    game_phase = game_state.get("game_phase")
    if game_phase and not isinstance(game_phase, GamePhase):
        result.add_error("游戏阶段必须是GamePhase类型")
    
    return result

# ==================== 验证装饰器 ====================

def validate_input(validator: Callable[[Any], ValidationResult]):
    """输入验证装饰器"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            # 假设第一个参数是需要验证的输入
            if args:
                validation_result = validator(args[0])
                if not validation_result.is_valid:
                    raise ValidationException(
                        f"输入验证失败: {', '.join(validation_result.errors)}"
                    )
            return func(*args, **kwargs)
        return wrapper
    return decorator

def validate_output(validator: Callable[[Any], ValidationResult]):
    """输出验证装饰器"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            validation_result = validator(result)
            if not validation_result.is_valid:
                raise ValidationException(
                    f"输出验证失败: {', '.join(validation_result.errors)}"
                )
            return result
        return wrapper
    return decorator

# ==================== 便捷验证函数 ====================

def quick_validate(value: Any, validators: List[BaseValidator]) -> bool:
    """快速验证（只返回是否通过）"""
    for validator in validators:
        result = validator.validate(value)
        if not result.is_valid:
            return False
    return True

def validate_and_raise(value: Any, validators: List[BaseValidator], context: str = ""):
    """验证并在失败时抛出异常"""
    errors = []
    for validator in validators:
        result = validator.validate(value)
        if not result.is_valid:
            errors.extend(result.errors)
    
    if errors:
        error_message = f"{context}: {', '.join(errors)}" if context else ', '.join(errors)
        raise ValidationException(error_message)

def create_validator_chain(*validators: BaseValidator) -> Callable[[Any], ValidationResult]:
    """创建验证器链"""
    def validate(value: Any) -> ValidationResult:
        result = create_validation_result()
        for validator in validators:
            validator_result = validator.validate(value)
            result.merge(validator_result)
        return result
    return validate