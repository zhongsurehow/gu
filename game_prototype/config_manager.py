"""
游戏配置管理器
负责加载和管理游戏的所有配置参数
"""

import json
import os
from typing import Dict, Any, Optional
from pathlib import Path

class ConfigManager:
    """游戏配置管理器"""
    
    _instance: Optional['ConfigManager'] = None
    _config: Dict[str, Any] = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_config()
        return cls._instance
    
    def _load_config(self):
        """加载配置文件"""
        config_path = Path(__file__).parent / "game_config.json"
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                self._config = json.load(f)
        except FileNotFoundError:
            print(f"警告：配置文件 {config_path} 未找到，使用默认配置")
            self._config = self._get_default_config()
        except json.JSONDecodeError as e:
            print(f"警告：配置文件格式错误 {e}，使用默认配置")
            self._config = self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """获取默认配置（作为备用）"""
        return {
            "game_balance": {
                "initial_resources": {
                    "qi": 8,
                    "dao_xing": 1,
                    "cheng_yi": 2
                },
                "resource_limits": {
                    "max_qi": 25,
                    "max_dao_xing": 20,
                    "max_cheng_yi": 15
                }
            }
        }
    
    def get(self, key_path: str, default: Any = None) -> Any:
        """
        获取配置值
        
        Args:
            key_path: 配置键路径，用点分隔，如 "game_balance.initial_resources.qi"
            default: 默认值
            
        Returns:
            配置值或默认值
        """
        keys = key_path.split('.')
        value = self._config
        
        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default
    
    def get_balance_config(self) -> Dict[str, Any]:
        """获取游戏平衡配置"""
        return self.get("game_balance", {})
    
    def get_initial_resources(self) -> Dict[str, int]:
        """获取初始资源配置"""
        return self.get("game_balance.initial_resources", {})
    
    def get_resource_limits(self) -> Dict[str, int]:
        """获取资源上限配置"""
        return self.get("game_balance.resource_limits", {})
    
    def get_action_costs(self) -> Dict[str, int]:
        """获取动作消耗配置"""
        return self.get("game_balance.action_costs", {})
    
    def get_yin_yang_config(self) -> Dict[str, Any]:
        """获取阴阳平衡配置"""
        return self.get("game_balance.yin_yang_balance", {})
    
    def get_divination_config(self) -> Dict[str, Any]:
        """获取占卜系统配置"""
        return self.get("game_balance.divination_system", {})
    
    def get_victory_conditions(self) -> Dict[str, Any]:
        """获取胜利条件配置"""
        return self.get("game_balance.victory_conditions", {})
    
    def get_tutorial_config(self) -> Dict[str, Any]:
        """获取教程配置"""
        return self.get("game_balance.tutorial_rewards", {})
    
    def get_game_flow_config(self) -> Dict[str, Any]:
        """获取游戏流程配置"""
        return self.get("game_balance.game_flow", {})
    
    def reload_config(self):
        """重新加载配置文件"""
        self._load_config()
    
    def update_config(self, key_path: str, value: Any):
        """
        更新配置值（仅在内存中，不保存到文件）
        
        Args:
            key_path: 配置键路径
            value: 新值
        """
        keys = key_path.split('.')
        config = self._config
        
        # 导航到父级字典
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]
        
        # 设置值
        config[keys[-1]] = value
    
    def save_config(self, file_path: Optional[str] = None):
        """
        保存配置到文件
        
        Args:
            file_path: 保存路径，默认为原配置文件路径
        """
        if file_path is None:
            file_path = Path(__file__).parent / "game_config.json"
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self._config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存配置文件失败: {e}")

# 全局配置实例
config = ConfigManager()

# 便捷函数
def get_config(key_path: str, default: Any = None) -> Any:
    """获取配置值的便捷函数"""
    return config.get(key_path, default)

def update_config(key_path: str, value: Any):
    """更新配置值的便捷函数"""
    return config.update_config(key_path, value)

def get_initial_qi() -> int:
    """获取初始气值"""
    return config.get("game_balance.initial_resources.qi", 8)

def get_initial_dao_xing() -> int:
    """获取初始道行值"""
    return config.get("game_balance.initial_resources.dao_xing", 1)

def get_initial_cheng_yi() -> int:
    """获取初始诚意值"""
    return config.get("game_balance.initial_resources.cheng_yi", 2)

def get_max_qi() -> int:
    """获取气的上限"""
    return config.get("game_balance.resource_limits.max_qi", 25)

def get_max_dao_xing() -> int:
    """获取道行的上限"""
    return config.get("game_balance.resource_limits.max_dao_xing", 20)

def get_max_cheng_yi() -> int:
    """获取诚意的上限"""
    return config.get("game_balance.resource_limits.max_cheng_yi", 15)

def get_transform_cost() -> int:
    """获取变卦消耗"""
    return config.get("game_balance.action_costs.transform_cheng_yi_cost", 3)

def get_meditate_cost() -> int:
    """获取冥想消耗"""
    return config.get("game_balance.action_costs.meditate_qi_cost", 2)

def get_study_cost() -> int:
    """获取学习消耗"""
    return config.get("game_balance.action_costs.study_dao_xing_cost", 1)