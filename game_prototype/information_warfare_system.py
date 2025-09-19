"""
信息层级系统 - Information Warfare System
支持三十六计中的信息战计谋，包括情报收集、传播、欺骗等
"""

from dataclasses import dataclass, field
from typing import Dict, List, Set, Optional, Tuple
from enum import Enum
import random
from datetime import datetime, timedelta

class InformationType(Enum):
    """信息类型"""
    PLAYER_POSITION = "player_position"      # 玩家位置
    PLAYER_RESOURCES = "player_resources"    # 玩家资源
    PLAYER_CARDS = "player_cards"           # 玩家手牌
    PLAYER_STRATEGY = "player_strategy"      # 玩家策略意图
    ZONE_CONTROL = "zone_control"           # 区域控制情况
    ALLIANCE_STATUS = "alliance_status"      # 联盟状态
    WEAKNESS = "weakness"                   # 弱点信息
    FUTURE_PLAN = "future_plan"             # 未来计划
    FALSE_INFO = "false_info"               # 虚假信息

class InformationLevel(Enum):
    """信息层级"""
    PUBLIC = 1      # 公开信息 - 所有人可见
    OBSERVED = 2    # 观察信息 - 需要观察获得
    PRIVATE = 3     # 私密信息 - 需要特殊手段获得
    SECRET = 4      # 机密信息 - 极难获得
    TOP_SECRET = 5  # 绝密信息 - 几乎不可能获得

class InformationReliability(Enum):
    """信息可靠性"""
    CONFIRMED = 1.0     # 确认无误
    RELIABLE = 0.8      # 可靠
    UNCERTAIN = 0.6     # 不确定
    DOUBTFUL = 0.4      # 可疑
    FALSE = 0.0         # 虚假

@dataclass
class InformationPiece:
    """信息片段"""
    info_type: InformationType
    level: InformationLevel
    content: Dict
    reliability: InformationReliability
    source_player: Optional[str] = None
    target_player: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)
    expiry_time: Optional[datetime] = None
    is_false: bool = False
    
    def is_expired(self) -> bool:
        """检查信息是否过期"""
        if self.expiry_time is None:
            return False
        return datetime.now() > self.expiry_time
    
    def get_effective_reliability(self) -> float:
        """获取有效可靠性（考虑时间衰减）"""
        base_reliability = self.reliability.value
        
        # 时间衰减
        if self.expiry_time:
            time_factor = max(0.1, (self.expiry_time - datetime.now()).total_seconds() / 
                            (self.expiry_time - self.timestamp).total_seconds())
            return base_reliability * time_factor
        
        return base_reliability

@dataclass
class PlayerIntelligence:
    """玩家情报状态"""
    player_id: str
    known_information: Dict[str, List[InformationPiece]] = field(default_factory=dict)
    intelligence_network: Set[str] = field(default_factory=set)  # 情报网络
    counter_intelligence: int = 0  # 反情报能力
    information_gathering_skill: int = 0  # 情报收集技能
    deception_skill: int = 0  # 欺骗技能
    
    def add_information(self, info: InformationPiece):
        """添加情报"""
        target = info.target_player or "general"
        if target not in self.known_information:
            self.known_information[target] = []
        self.known_information[target].append(info)
    
    def get_information_about(self, target_player: str, info_type: InformationType) -> List[InformationPiece]:
        """获取关于特定玩家的特定类型信息"""
        if target_player not in self.known_information:
            return []
        
        return [info for info in self.known_information[target_player] 
                if info.info_type == info_type and not info.is_expired()]
    
    def get_reliability_about(self, target_player: str) -> float:
        """获取关于特定玩家的信息可靠性"""
        infos = self.known_information.get(target_player, [])
        if not infos:
            return 0.0
        
        valid_infos = [info for info in infos if not info.is_expired()]
        if not valid_infos:
            return 0.0
        
        total_reliability = sum(info.get_effective_reliability() for info in valid_infos)
        return min(1.0, total_reliability / len(valid_infos))

class InformationWarfareSystem:
    """信息战系统"""
    
    def __init__(self):
        self.player_intelligence: Dict[str, PlayerIntelligence] = {}
        self.global_information: List[InformationPiece] = []
        self.information_market: Dict[InformationType, int] = {}  # 信息价值市场
        
        # 初始化信息价值
        self._initialize_information_values()
    
    def _initialize_information_values(self):
        """初始化信息价值"""
        self.information_market = {
            InformationType.PLAYER_POSITION: 1,
            InformationType.PLAYER_RESOURCES: 2,
            InformationType.PLAYER_CARDS: 3,
            InformationType.PLAYER_STRATEGY: 4,
            InformationType.ZONE_CONTROL: 2,
            InformationType.ALLIANCE_STATUS: 3,
            InformationType.WEAKNESS: 5,
            InformationType.FUTURE_PLAN: 4,
            InformationType.FALSE_INFO: 1,
        }
    
    def register_player(self, player_id: str):
        """注册玩家"""
        if player_id not in self.player_intelligence:
            self.player_intelligence[player_id] = PlayerIntelligence(player_id)
    
    def gather_information(self, gatherer_id: str, target_id: str, 
                          info_type: InformationType, method: str = "observation") -> Optional[InformationPiece]:
        """收集信息"""
        gatherer = self.player_intelligence.get(gatherer_id)
        if not gatherer:
            return None
        
        # 计算成功率
        success_rate = self._calculate_gathering_success_rate(
            gatherer, target_id, info_type, method
        )
        
        if random.random() > success_rate:
            return None
        
        # 生成信息
        info_content = self._generate_information_content(target_id, info_type)
        reliability = self._determine_reliability(gatherer, info_type, method)
        level = self._determine_information_level(info_type, method)
        
        info = InformationPiece(
            info_type=info_type,
            level=level,
            content=info_content,
            reliability=reliability,
            source_player=gatherer_id,
            target_player=target_id,
            expiry_time=datetime.now() + timedelta(hours=self._get_info_lifetime(info_type))
        )
        
        gatherer.add_information(info)
        return info
    
    def spread_information(self, spreader_id: str, receiver_id: str, 
                          info: InformationPiece, modify_reliability: bool = False) -> bool:
        """传播信息"""
        spreader = self.player_intelligence.get(spreader_id)
        receiver = self.player_intelligence.get(receiver_id)
        
        if not spreader or not receiver:
            return False
        
        # 创建信息副本
        new_info = InformationPiece(
            info_type=info.info_type,
            level=info.level,
            content=info.content.copy(),
            reliability=info.reliability,
            source_player=spreader_id,  # 更新来源
            target_player=info.target_player,
            timestamp=datetime.now(),
            expiry_time=info.expiry_time,
            is_false=info.is_false
        )
        
        # 可能修改可靠性（传播过程中的失真）
        if modify_reliability:
            new_info.reliability = self._modify_reliability_during_spread(
                info.reliability, spreader.deception_skill
            )
        
        receiver.add_information(new_info)
        return True
    
    def plant_false_information(self, planter_id: str, target_id: str, 
                               info_type: InformationType, false_content: Dict) -> Optional[InformationPiece]:
        """植入虚假信息"""
        planter = self.player_intelligence.get(planter_id)
        if not planter:
            return None
        
        # 虚假信息看起来很可靠
        fake_reliability = InformationReliability.RELIABLE
        
        # 根据欺骗技能调整可靠性
        if planter.deception_skill > 3:
            fake_reliability = InformationReliability.CONFIRMED
        elif planter.deception_skill < 2:
            fake_reliability = InformationReliability.UNCERTAIN
        
        false_info = InformationPiece(
            info_type=info_type,
            level=InformationLevel.PRIVATE,
            content=false_content,
            reliability=fake_reliability,
            source_player=planter_id,
            target_player=target_id,
            is_false=True,
            expiry_time=datetime.now() + timedelta(hours=6)  # 虚假信息持续时间较短
        )
        
        # 将虚假信息添加到全局信息池，等待其他玩家"发现"
        self.global_information.append(false_info)
        return false_info
    
    def detect_false_information(self, detector_id: str, info: InformationPiece) -> bool:
        """检测虚假信息"""
        detector = self.player_intelligence.get(detector_id)
        if not detector:
            return False
        
        # 计算检测成功率
        detection_rate = (detector.counter_intelligence * 0.2 + 
                         detector.information_gathering_skill * 0.1)
        
        # 虚假信息越不可靠越容易被发现
        if info.reliability == InformationReliability.DOUBTFUL:
            detection_rate += 0.3
        elif info.reliability == InformationReliability.UNCERTAIN:
            detection_rate += 0.2
        
        return random.random() < detection_rate
    
    def _calculate_gathering_success_rate(self, gatherer: PlayerIntelligence, 
                                        target_id: str, info_type: InformationType, 
                                        method: str) -> float:
        """计算信息收集成功率"""
        base_rate = 0.3
        
        # 技能加成
        base_rate += gatherer.information_gathering_skill * 0.1
        
        # 情报网络加成
        if target_id in gatherer.intelligence_network:
            base_rate += 0.3
        
        # 信息类型难度
        difficulty_modifier = {
            InformationType.PLAYER_POSITION: 0.4,
            InformationType.PLAYER_RESOURCES: 0.2,
            InformationType.PLAYER_CARDS: -0.1,
            InformationType.PLAYER_STRATEGY: -0.2,
            InformationType.WEAKNESS: -0.3,
            InformationType.FUTURE_PLAN: -0.4,
        }
        base_rate += difficulty_modifier.get(info_type, 0)
        
        # 方法加成
        method_modifier = {
            "observation": 0.1,
            "infiltration": 0.3,
            "bribery": 0.2,
            "deception": 0.25,
            "divination": 0.15,  # 易经占卜
        }
        base_rate += method_modifier.get(method, 0)
        
        return max(0.05, min(0.95, base_rate))
    
    def _generate_information_content(self, target_id: str, info_type: InformationType) -> Dict:
        """生成信息内容（这里是模拟，实际应该从游戏状态获取）"""
        # 这里应该从实际游戏状态获取信息
        # 现在只是返回模拟数据
        return {
            "target": target_id,
            "type": info_type.value,
            "data": f"模拟的{info_type.value}信息",
            "confidence": random.uniform(0.6, 1.0)
        }
    
    def _determine_reliability(self, gatherer: PlayerIntelligence, 
                             info_type: InformationType, method: str) -> InformationReliability:
        """确定信息可靠性"""
        base_reliability = 0.6
        
        # 技能影响
        base_reliability += gatherer.information_gathering_skill * 0.05
        
        # 方法影响
        method_reliability = {
            "observation": 0.8,
            "infiltration": 0.7,
            "bribery": 0.6,
            "deception": 0.5,
            "divination": 0.75,
        }
        base_reliability *= method_reliability.get(method, 0.6)
        
        # 转换为枚举
        if base_reliability >= 0.9:
            return InformationReliability.CONFIRMED
        elif base_reliability >= 0.7:
            return InformationReliability.RELIABLE
        elif base_reliability >= 0.5:
            return InformationReliability.UNCERTAIN
        else:
            return InformationReliability.DOUBTFUL
    
    def _determine_information_level(self, info_type: InformationType, method: str) -> InformationLevel:
        """确定信息层级"""
        type_levels = {
            InformationType.PLAYER_POSITION: InformationLevel.OBSERVED,
            InformationType.PLAYER_RESOURCES: InformationLevel.PRIVATE,
            InformationType.PLAYER_CARDS: InformationLevel.SECRET,
            InformationType.PLAYER_STRATEGY: InformationLevel.SECRET,
            InformationType.ZONE_CONTROL: InformationLevel.PUBLIC,
            InformationType.ALLIANCE_STATUS: InformationLevel.OBSERVED,
            InformationType.WEAKNESS: InformationLevel.TOP_SECRET,
            InformationType.FUTURE_PLAN: InformationLevel.TOP_SECRET,
            InformationType.FALSE_INFO: InformationLevel.PRIVATE,
        }
        
        base_level = type_levels.get(info_type, InformationLevel.PRIVATE)
        
        # 某些方法可以获得更高级别的信息
        if method in ["infiltration", "divination"] and base_level.value < InformationLevel.SECRET.value:
            return InformationLevel(base_level.value + 1)
        
        return base_level
    
    def _get_info_lifetime(self, info_type: InformationType) -> int:
        """获取信息生命周期（小时）"""
        lifetimes = {
            InformationType.PLAYER_POSITION: 2,
            InformationType.PLAYER_RESOURCES: 4,
            InformationType.PLAYER_CARDS: 6,
            InformationType.PLAYER_STRATEGY: 8,
            InformationType.ZONE_CONTROL: 3,
            InformationType.ALLIANCE_STATUS: 12,
            InformationType.WEAKNESS: 24,
            InformationType.FUTURE_PLAN: 6,
            InformationType.FALSE_INFO: 4,
        }
        return lifetimes.get(info_type, 6)
    
    def _modify_reliability_during_spread(self, original: InformationReliability, 
                                        spreader_skill: int) -> InformationReliability:
        """传播过程中修改可靠性"""
        # 高技能的传播者可能提高可靠性（通过添加细节）
        # 低技能的传播者可能降低可靠性（传播失真）
        
        if spreader_skill >= 4:
            # 可能提高可靠性
            if original.value < 1.0 and random.random() < 0.3:
                new_value = min(1.0, original.value + 0.2)
                for reliability in InformationReliability:
                    if abs(reliability.value - new_value) < 0.1:
                        return reliability
        elif spreader_skill <= 1:
            # 可能降低可靠性
            if random.random() < 0.4:
                new_value = max(0.0, original.value - 0.2)
                for reliability in InformationReliability:
                    if abs(reliability.value - new_value) < 0.1:
                        return reliability
        
        return original
    
    def get_player_information_summary(self, player_id: str) -> Dict:
        """获取玩家信息摘要"""
        intelligence = self.player_intelligence.get(player_id)
        if not intelligence:
            return {}
        
        summary = {
            "total_information_pieces": sum(len(infos) for infos in intelligence.known_information.values()),
            "network_size": len(intelligence.intelligence_network),
            "skills": {
                "gathering": intelligence.information_gathering_skill,
                "counter_intelligence": intelligence.counter_intelligence,
                "deception": intelligence.deception_skill
            },
            "information_by_target": {}
        }
        
        for target, infos in intelligence.known_information.items():
            valid_infos = [info for info in infos if not info.is_expired()]
            summary["information_by_target"][target] = {
                "count": len(valid_infos),
                "reliability": intelligence.get_reliability_about(target),
                "types": list(set(info.info_type.value for info in valid_infos))
            }
        
        return summary
    
    def execute_information_strategy(self, strategy_name: str, executor_id: str, 
                                   target_id: str, **kwargs) -> Dict:
        """执行信息战策略"""
        strategies = {
            "无中生有": self._execute_create_something_from_nothing,
            "暗度陈仓": self._execute_secretly_cross_chencang,
            "反间计": self._execute_sow_discord,
            "苦肉计": self._execute_self_torture,
            "连环计": self._execute_chain_stratagem,
            "声东击西": self._execute_make_noise_east_attack_west,
        }
        
        strategy_func = strategies.get(strategy_name)
        if strategy_func:
            return strategy_func(executor_id, target_id, **kwargs)
        
        return {"success": False, "message": f"未知策略: {strategy_name}"}
    
    def _execute_create_something_from_nothing(self, executor_id: str, target_id: str, **kwargs) -> Dict:
        """执行无中生有策略"""
        false_content = kwargs.get("false_content", {"fake_weakness": "资源不足"})
        
        false_info = self.plant_false_information(
            executor_id, target_id, InformationType.WEAKNESS, false_content
        )
        
        if false_info:
            return {
                "success": True,
                "message": "成功植入虚假信息",
                "effect": "目标可能基于错误信息做出决策"
            }
        
        return {"success": False, "message": "植入虚假信息失败"}
    
    def _execute_secretly_cross_chencang(self, executor_id: str, target_id: str, **kwargs) -> Dict:
        """执行暗度陈仓策略"""
        # 公开一个假计划，暗中执行真计划
        fake_plan = kwargs.get("fake_plan", {"action": "攻击东方"})
        real_plan = kwargs.get("real_plan", {"action": "攻击西方"})
        
        # 故意让对方获得假计划信息
        fake_info = self.plant_false_information(
            executor_id, target_id, InformationType.FUTURE_PLAN, fake_plan
        )
        
        if fake_info:
            return {
                "success": True,
                "message": "成功实施暗度陈仓",
                "effect": "敌人将准备错误的防御",
                "real_plan": real_plan
            }
        
        return {"success": False, "message": "暗度陈仓失败"}
    
    def _execute_sow_discord(self, executor_id: str, target_id: str, **kwargs) -> Dict:
        """执行反间计策略"""
        # 在敌人内部制造不信任
        discord_info = kwargs.get("discord_info", {"betrayal": "盟友计划背叛"})
        
        false_info = self.plant_false_information(
            executor_id, target_id, InformationType.ALLIANCE_STATUS, discord_info
        )
        
        if false_info:
            return {
                "success": True,
                "message": "成功挑拨离间",
                "effect": "目标与盟友关系可能恶化"
            }
        
        return {"success": False, "message": "反间计失败"}
    
    def _execute_self_torture(self, executor_id: str, target_id: str, **kwargs) -> Dict:
        """执行苦肉计策略（重新诠释为舍身求道）"""
        # 故意暴露自己的"弱点"来获得对方信任
        sacrifice_info = kwargs.get("sacrifice_info", {"weakness": "修行遇到瓶颈"})
        
        # 降低自己的反情报能力，但获得对方信任
        executor = self.player_intelligence.get(executor_id)
        if executor:
            executor.counter_intelligence = max(0, executor.counter_intelligence - 1)
            
            # 获得对方的情报网络接入
            executor.intelligence_network.add(target_id)
            
            return {
                "success": True,
                "message": "舍身求道成功",
                "effect": "获得目标信任，可获得更多情报",
                "cost": "反情报能力暂时降低"
            }
        
        return {"success": False, "message": "舍身求道失败"}
    
    def _execute_chain_stratagem(self, executor_id: str, target_id: str, **kwargs) -> Dict:
        """执行连环计策略"""
        # 连续植入多个相关的虚假信息
        chain_infos = kwargs.get("chain_infos", [
            {"type": InformationType.PLAYER_RESOURCES, "content": {"gold": 100}},
            {"type": InformationType.FUTURE_PLAN, "content": {"plan": "大举进攻"}},
            {"type": InformationType.WEAKNESS, "content": {"weakness": "防御薄弱"}}
        ])
        
        success_count = 0
        for info_data in chain_infos:
            false_info = self.plant_false_information(
                executor_id, target_id, info_data["type"], info_data["content"]
            )
            if false_info:
                success_count += 1
        
        if success_count > 0:
            return {
                "success": True,
                "message": f"连环计成功，植入{success_count}个相关虚假信息",
                "effect": "目标将基于一系列错误信息做出重大决策"
            }
        
        return {"success": False, "message": "连环计失败"}
    
    def _execute_make_noise_east_attack_west(self, executor_id: str, target_id: str, **kwargs) -> Dict:
        """执行声东击西策略"""
        # 在东方制造假象，实际攻击西方
        fake_target = kwargs.get("fake_target", "东方区域")
        real_target = kwargs.get("real_target", "西方区域")
        
        # 故意泄露假的攻击计划
        fake_plan = {"target": fake_target, "time": "下回合"}
        false_info = self.plant_false_information(
            executor_id, target_id, InformationType.FUTURE_PLAN, fake_plan
        )
        
        if false_info:
            return {
                "success": True,
                "message": "声东击西成功",
                "effect": f"敌人将防守{fake_target}，{real_target}防御薄弱",
                "real_target": real_target
            }
        
        return {"success": False, "message": "声东击西失败"}