"""
天机变游戏异常定义
提供统一的错误处理机制
"""

from typing import Optional, Dict, Any

class GameException(Exception):
    """游戏基础异常类"""
    
    def __init__(self, message: str, error_code: Optional[str] = None, context: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code or self.__class__.__name__
        self.context = context or {}
    
    def __str__(self) -> str:
        if self.context:
            context_str = ", ".join(f"{k}={v}" for k, v in self.context.items())
            return f"{self.message} (错误代码: {self.error_code}, 上下文: {context_str})"
        return f"{self.message} (错误代码: {self.error_code})"

# ==================== 游戏逻辑异常 ====================

class InvalidActionException(GameException):
    """无效行动异常"""
    
    def __init__(self, action_type: str, reason: str, **context):
        message = f"无效的行动 '{action_type}': {reason}"
        super().__init__(message, "INVALID_ACTION", context)

class InsufficientResourcesException(GameException):
    """资源不足异常"""
    
    def __init__(self, required_resources: Dict[str, int], available_resources: Dict[str, int]):
        message = "资源不足以执行此操作"
        context = {
            "required": required_resources,
            "available": available_resources
        }
        super().__init__(message, "INSUFFICIENT_RESOURCES", context)

class GameStateException(GameException):
    """游戏状态异常"""
    
    def __init__(self, message: str, current_state: str, **context):
        context["current_state"] = current_state
        super().__init__(message, "GAME_STATE_ERROR", context)

class PlayerNotFoundException(GameException):
    """玩家未找到异常"""
    
    def __init__(self, player_id: str):
        message = f"未找到玩家: {player_id}"
        super().__init__(message, "PLAYER_NOT_FOUND", {"player_id": player_id})

# ==================== 配置异常 ====================

class ConfigurationException(GameException):
    """配置异常"""
    
    def __init__(self, config_key: str, reason: str):
        message = f"配置错误 '{config_key}': {reason}"
        super().__init__(message, "CONFIG_ERROR", {"config_key": config_key})

class InvalidConfigValueException(ConfigurationException):
    """无效配置值异常"""
    
    def __init__(self, config_key: str, value: Any, expected_type: str):
        reason = f"期望类型 {expected_type}，但得到 {type(value).__name__}: {value}"
        super().__init__(config_key, reason)

# ==================== 系统异常 ====================

class SystemException(GameException):
    """系统异常"""
    
    def __init__(self, system_name: str, message: str, **context):
        full_message = f"系统 '{system_name}' 错误: {message}"
        context["system_name"] = system_name
        super().__init__(full_message, "SYSTEM_ERROR", context)

class SystemNotInitializedException(SystemException):
    """系统未初始化异常"""
    
    def __init__(self, system_name: str):
        super().__init__(system_name, "系统尚未初始化")

class SystemAlreadyInitializedException(SystemException):
    """系统已初始化异常"""
    
    def __init__(self, system_name: str):
        super().__init__(system_name, "系统已经初始化")

# ==================== AI异常 ====================

class AIException(GameException):
    """AI异常"""
    
    def __init__(self, ai_name: str, message: str, **context):
        full_message = f"AI '{ai_name}' 错误: {message}"
        context["ai_name"] = ai_name
        super().__init__(full_message, "AI_ERROR", context)

class AIDecisionException(AIException):
    """AI决策异常"""
    
    def __init__(self, ai_name: str, decision_context: Dict[str, Any]):
        super().__init__(ai_name, "AI决策失败", **decision_context)

# ==================== 易学系统异常 ====================

class YijingException(GameException):
    """易经系统异常"""
    
    def __init__(self, message: str, **context):
        super().__init__(message, "YIJING_ERROR", context)

class InvalidHexagramException(YijingException):
    """无效卦象异常"""
    
    def __init__(self, hexagram_id: str):
        message = f"无效的卦象ID: {hexagram_id}"
        super().__init__(message, hexagram_id=hexagram_id)

class DivinationException(YijingException):
    """占卜异常"""
    
    def __init__(self, method: str, reason: str):
        message = f"占卜方法 '{method}' 失败: {reason}"
        super().__init__(message, method=method, reason=reason)

# ==================== UI异常 ====================

class UIException(GameException):
    """UI异常"""
    
    def __init__(self, message: str, **context):
        super().__init__(message, "UI_ERROR", context)

class InvalidInputException(UIException):
    """无效输入异常"""
    
    def __init__(self, input_value: str, expected_format: str):
        message = f"无效输入 '{input_value}'，期望格式: {expected_format}"
        super().__init__(message, input_value=input_value, expected_format=expected_format)

# ==================== 数据异常 ====================

class DataException(GameException):
    """数据异常"""
    
    def __init__(self, message: str, **context):
        super().__init__(message, "DATA_ERROR", context)

class DataCorruptionException(DataException):
    """数据损坏异常"""
    
    def __init__(self, data_type: str, details: str):
        message = f"数据损坏: {data_type} - {details}"
        super().__init__(message, data_type=data_type, details=details)

class DataNotFoundException(DataException):
    """数据未找到异常"""
    
    def __init__(self, data_key: str, data_type: str = "数据"):
        message = f"未找到{data_type}: {data_key}"
        super().__init__(message, data_key=data_key, data_type=data_type)

# ==================== 异常处理工具 ====================

def handle_exception(exception: Exception, context: Optional[Dict[str, Any]] = None) -> str:
    """
    统一异常处理函数
    
    Args:
        exception: 异常对象
        context: 额外上下文信息
    
    Returns:
        格式化的错误消息
    """
    if isinstance(exception, GameException):
        return str(exception)
    
    # 处理标准异常
    error_message = f"未预期的错误: {str(exception)}"
    if context:
        context_str = ", ".join(f"{k}={v}" for k, v in context.items())
        error_message += f" (上下文: {context_str})"
    
    return error_message

def create_error_response(exception: Exception, include_traceback: bool = False) -> Dict[str, Any]:
    """
    创建标准化的错误响应
    
    Args:
        exception: 异常对象
        include_traceback: 是否包含堆栈跟踪
    
    Returns:
        错误响应字典
    """
    response = {
        "success": False,
        "error": {
            "type": exception.__class__.__name__,
            "message": str(exception)
        }
    }
    
    if isinstance(exception, GameException):
        response["error"]["code"] = exception.error_code
        response["error"]["context"] = exception.context
    
    if include_traceback:
        import traceback
        response["error"]["traceback"] = traceback.format_exc()
    
    return response