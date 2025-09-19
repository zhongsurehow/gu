"""
势力根基系统 - Influence Foundation System
支持三十六计中需要建立根基、扩张影响力的计谋
"""

from dataclasses import dataclass, field
from typing import Dict, List, Set, Optional, Tuple
from enum import Enum
import random
from datetime import datetime, timedelta

class FoundationType(Enum):
    """根基类型"""
    ECONOMIC = "economic"           # 经济根基
    MILITARY = "military"          # 军事根基
    CULTURAL = "cultural"          # 文化根基
    SPIRITUAL = "spiritual"        # 精神根基（易经修行）
    DIPLOMATIC = "diplomatic"      # 外交根基
    INFORMATION = "information"    # 信息根基

class InfluenceLevel(Enum):
    """影响力等级"""
    NONE = 0        # 无影响
    MINIMAL = 1     # 微弱影响
    WEAK = 2        # 弱影响
    MODERATE = 3    # 中等影响
    STRONG = 4      # 强影响
    DOMINANT = 5    # 主导影响

class FoundationStability(Enum):
    """根基稳定性"""
    FRAGILE = 1     # 脆弱
    UNSTABLE = 2    # 不稳定
    STABLE = 3      # 稳定
    SOLID = 4       # 坚固
    UNSHAKEABLE = 5 # 不可撼动

@dataclass
class InfluenceNode:
    """影响力节点"""
    node_id: str
    location: Tuple[int, int]  # 位置坐标
    foundation_type: FoundationType
    influence_level: InfluenceLevel
    stability: FoundationStability
    owner_id: str
    established_time: datetime = field(default_factory=datetime.now)
    last_reinforced: datetime = field(default_factory=datetime.now)
    connected_nodes: Set[str] = field(default_factory=set)
    resources_invested: Dict[str, int] = field(default_factory=dict)
    
    def get_influence_radius(self) -> int:
        """获取影响力半径"""
        base_radius = {
            InfluenceLevel.NONE: 0,
            InfluenceLevel.MINIMAL: 1,
            InfluenceLevel.WEAK: 2,
            InfluenceLevel.MODERATE: 3,
            InfluenceLevel.STRONG: 4,
            InfluenceLevel.DOMINANT: 5
        }
        return base_radius.get(self.influence_level, 0)
    
    def get_defense_strength(self) -> int:
        """获取防御强度"""
        return self.stability.value * self.influence_level.value
    
    def is_vulnerable(self) -> bool:
        """检查是否脆弱"""
        # 新建立的根基更脆弱
        age_hours = (datetime.now() - self.established_time).total_seconds() / 3600
        if age_hours < 2:
            return True
        
        # 长时间未加强的根基也脆弱
        since_reinforced = (datetime.now() - self.last_reinforced).total_seconds() / 3600
        if since_reinforced > 12:
            return True
        
        return self.stability.value <= 2

@dataclass
class InfluenceNetwork:
    """影响力网络"""
    owner_id: str
    nodes: Dict[str, InfluenceNode] = field(default_factory=dict)
    network_cohesion: float = 0.0  # 网络凝聚力
    total_influence_points: int = 0
    
    def add_node(self, node: InfluenceNode):
        """添加节点"""
        self.nodes[node.node_id] = node
        self._update_network_metrics()
    
    def remove_node(self, node_id: str):
        """移除节点"""
        if node_id in self.nodes:
            # 断开连接
            node = self.nodes[node_id]
            for connected_id in node.connected_nodes:
                if connected_id in self.nodes:
                    self.nodes[connected_id].connected_nodes.discard(node_id)
            
            del self.nodes[node_id]
            self._update_network_metrics()
    
    def connect_nodes(self, node1_id: str, node2_id: str) -> bool:
        """连接两个节点"""
        if node1_id in self.nodes and node2_id in self.nodes:
            self.nodes[node1_id].connected_nodes.add(node2_id)
            self.nodes[node2_id].connected_nodes.add(node1_id)
            self._update_network_metrics()
            return True
        return False
    
    def get_network_strength(self) -> float:
        """获取网络整体强度"""
        if not self.nodes:
            return 0.0
        
        total_strength = sum(node.get_defense_strength() for node in self.nodes.values())
        return total_strength * self.network_cohesion
    
    def get_vulnerable_nodes(self) -> List[InfluenceNode]:
        """获取脆弱节点"""
        return [node for node in self.nodes.values() if node.is_vulnerable()]
    
    def _update_network_metrics(self):
        """更新网络指标"""
        if not self.nodes:
            self.network_cohesion = 0.0
            self.total_influence_points = 0
            return
        
        # 计算连接密度
        total_possible_connections = len(self.nodes) * (len(self.nodes) - 1) / 2
        actual_connections = sum(len(node.connected_nodes) for node in self.nodes.values()) / 2
        
        if total_possible_connections > 0:
            connection_density = actual_connections / total_possible_connections
        else:
            connection_density = 0
        
        # 计算稳定性平均值
        avg_stability = sum(node.stability.value for node in self.nodes.values()) / len(self.nodes)
        
        # 网络凝聚力 = 连接密度 * 稳定性
        self.network_cohesion = min(1.0, connection_density * (avg_stability / 5))
        
        # 总影响力点数
        self.total_influence_points = sum(node.influence_level.value for node in self.nodes.values())

class InfluenceFoundationSystem:
    """势力根基系统"""
    
    def __init__(self):
        self.player_networks: Dict[str, InfluenceNetwork] = {}
        self.global_influence_map: Dict[Tuple[int, int], List[str]] = {}  # 位置 -> 影响此位置的节点列表
        self.foundation_costs: Dict[FoundationType, Dict[str, int]] = {}
        
        self._initialize_foundation_costs()
    
    def _initialize_foundation_costs(self):
        """初始化建立根基的成本"""
        self.foundation_costs = {
            FoundationType.ECONOMIC: {"gold": 50, "qi": 10},
            FoundationType.MILITARY: {"qi": 30, "dao_xing": 10},
            FoundationType.CULTURAL: {"dao_xing": 20, "cheng_yi": 15},
            FoundationType.SPIRITUAL: {"dao_xing": 40, "cheng_yi": 20},
            FoundationType.DIPLOMATIC: {"cheng_yi": 30, "gold": 20},
            FoundationType.INFORMATION: {"qi": 20, "dao_xing": 15, "gold": 10}
        }
    
    def register_player(self, player_id: str):
        """注册玩家"""
        if player_id not in self.player_networks:
            self.player_networks[player_id] = InfluenceNetwork(player_id)
    
    def establish_foundation(self, player_id: str, location: Tuple[int, int], 
                           foundation_type: FoundationType, 
                           initial_investment: Dict[str, int]) -> Optional[InfluenceNode]:
        """建立根基"""
        if player_id not in self.player_networks:
            self.register_player(player_id)
        
        # 检查成本
        required_costs = self.foundation_costs.get(foundation_type, {})
        if not self._check_sufficient_resources(initial_investment, required_costs):
            return None
        
        # 检查位置是否已被强势力控制
        if self._is_location_dominated(location, player_id):
            return None
        
        # 创建新节点
        node_id = f"{player_id}_{foundation_type.value}_{location[0]}_{location[1]}"
        
        # 根据投资确定初始等级和稳定性
        influence_level = self._calculate_initial_influence_level(initial_investment, required_costs)
        stability = self._calculate_initial_stability(initial_investment, required_costs)
        
        node = InfluenceNode(
            node_id=node_id,
            location=location,
            foundation_type=foundation_type,
            influence_level=influence_level,
            stability=stability,
            owner_id=player_id,
            resources_invested=initial_investment.copy()
        )
        
        # 添加到网络
        self.player_networks[player_id].add_node(node)
        
        # 更新全局影响力地图
        self._update_global_influence_map(node)
        
        return node
    
    def reinforce_foundation(self, player_id: str, node_id: str, 
                           additional_investment: Dict[str, int]) -> bool:
        """加强根基"""
        network = self.player_networks.get(player_id)
        if not network or node_id not in network.nodes:
            return False
        
        node = network.nodes[node_id]
        
        # 更新投资
        for resource, amount in additional_investment.items():
            node.resources_invested[resource] = node.resources_invested.get(resource, 0) + amount
        
        # 重新计算等级和稳定性
        total_investment = node.resources_invested
        required_costs = self.foundation_costs.get(node.foundation_type, {})
        
        new_influence_level = self._calculate_initial_influence_level(total_investment, required_costs)
        new_stability = self._calculate_initial_stability(total_investment, required_costs)
        
        # 更新节点
        node.influence_level = new_influence_level
        node.stability = new_stability
        node.last_reinforced = datetime.now()
        
        # 更新网络指标
        network._update_network_metrics()
        
        # 更新全局影响力地图
        self._update_global_influence_map(node)
        
        return True
    
    def attack_foundation(self, attacker_id: str, target_node_id: str, 
                         attack_type: str, attack_strength: int) -> Dict:
        """攻击根基"""
        # 找到目标节点
        target_node = None
        target_network = None
        
        for network in self.player_networks.values():
            if target_node_id in network.nodes:
                target_node = network.nodes[target_node_id]
                target_network = network
                break
        
        if not target_node:
            return {"success": False, "message": "目标根基不存在"}
        
        # 计算攻击成功率
        defense_strength = target_node.get_defense_strength()
        success_rate = self._calculate_attack_success_rate(
            attack_strength, defense_strength, attack_type, target_node
        )
        
        result = {"success": False, "damage": 0, "destroyed": False}
        
        if random.random() < success_rate:
            # 攻击成功
            damage = self._calculate_damage(attack_strength, defense_strength, attack_type)
            result["success"] = True
            result["damage"] = damage
            
            # 应用伤害
            if self._apply_damage_to_node(target_node, damage):
                # 节点被摧毁
                target_network.remove_node(target_node_id)
                self._remove_from_global_influence_map(target_node)
                result["destroyed"] = True
                result["message"] = "根基被完全摧毁"
            else:
                result["message"] = f"根基受到{damage}点伤害"
        else:
            result["message"] = "攻击失败"
        
        return result
    
    def expand_influence(self, player_id: str, source_node_id: str, 
                        target_location: Tuple[int, int]) -> bool:
        """扩张影响力"""
        network = self.player_networks.get(player_id)
        if not network or source_node_id not in network.nodes:
            return False
        
        source_node = network.nodes[source_node_id]
        
        # 检查距离
        distance = self._calculate_distance(source_node.location, target_location)
        if distance > source_node.get_influence_radius():
            return False
        
        # 检查是否有足够的影响力
        if source_node.influence_level.value < 3:
            return False
        
        # 在目标位置建立影响力
        expansion_node_id = f"{player_id}_expansion_{target_location[0]}_{target_location[1]}"
        
        expansion_node = InfluenceNode(
            node_id=expansion_node_id,
            location=target_location,
            foundation_type=source_node.foundation_type,
            influence_level=InfluenceLevel.MINIMAL,
            stability=FoundationStability.FRAGILE,
            owner_id=player_id
        )
        
        # 连接到源节点
        network.add_node(expansion_node)
        network.connect_nodes(source_node_id, expansion_node_id)
        
        # 更新全局影响力地图
        self._update_global_influence_map(expansion_node)
        
        return True
    
    def get_influence_at_location(self, location: Tuple[int, int]) -> Dict[str, int]:
        """获取特定位置的影响力分布"""
        influences = {}
        
        for network in self.player_networks.values():
            player_influence = 0
            for node in network.nodes.values():
                distance = self._calculate_distance(node.location, location)
                if distance <= node.get_influence_radius():
                    # 影响力随距离衰减
                    influence_strength = node.influence_level.value * (1 - distance / (node.get_influence_radius() + 1))
                    player_influence += influence_strength
            
            if player_influence > 0:
                influences[network.owner_id] = int(player_influence)
        
        return influences
    
    def get_dominant_influence(self, location: Tuple[int, int]) -> Optional[str]:
        """获取特定位置的主导影响力"""
        influences = self.get_influence_at_location(location)
        if not influences:
            return None
        
        max_influence = max(influences.values())
        dominant_players = [player for player, influence in influences.items() if influence == max_influence]
        
        # 如果有多个玩家影响力相等，返回None（争议区域）
        if len(dominant_players) > 1:
            return None
        
        return dominant_players[0]
    
    def execute_foundation_strategy(self, strategy_name: str, executor_id: str, 
                                  target_id: str, **kwargs) -> Dict:
        """执行根基相关策略"""
        strategies = {
            "釜底抽薪": self._execute_remove_firewood_from_cauldron,
            "抛砖引玉": self._execute_throw_brick_attract_jade,
            "借刀杀人": self._execute_kill_with_borrowed_knife,
            "以逸待劳": self._execute_wait_at_ease,
            "趁火打劫": self._execute_loot_burning_house,
            "李代桃僵": self._execute_sacrifice_plum_for_peach,
        }
        
        strategy_func = strategies.get(strategy_name)
        if strategy_func:
            return strategy_func(executor_id, target_id, **kwargs)
        
        return {"success": False, "message": f"未知策略: {strategy_name}"}
    
    def _check_sufficient_resources(self, available: Dict[str, int], required: Dict[str, int]) -> bool:
        """检查资源是否充足"""
        for resource, amount in required.items():
            if available.get(resource, 0) < amount:
                return False
        return True
    
    def _is_location_dominated(self, location: Tuple[int, int], player_id: str) -> bool:
        """检查位置是否被其他强势力主导"""
        dominant_player = self.get_dominant_influence(location)
        if dominant_player and dominant_player != player_id:
            influences = self.get_influence_at_location(location)
            if influences.get(dominant_player, 0) >= 4:  # 强影响力阈值
                return True
        return False
    
    def _calculate_initial_influence_level(self, investment: Dict[str, int], 
                                         required: Dict[str, int]) -> InfluenceLevel:
        """计算初始影响力等级"""
        investment_ratio = 0
        for resource, required_amount in required.items():
            if required_amount > 0:
                ratio = investment.get(resource, 0) / required_amount
                investment_ratio += ratio
        
        avg_ratio = investment_ratio / len(required) if required else 0
        
        if avg_ratio >= 3:
            return InfluenceLevel.DOMINANT
        elif avg_ratio >= 2:
            return InfluenceLevel.STRONG
        elif avg_ratio >= 1.5:
            return InfluenceLevel.MODERATE
        elif avg_ratio >= 1:
            return InfluenceLevel.WEAK
        else:
            return InfluenceLevel.MINIMAL
    
    def _calculate_initial_stability(self, investment: Dict[str, int], 
                                   required: Dict[str, int]) -> FoundationStability:
        """计算初始稳定性"""
        investment_ratio = 0
        for resource, required_amount in required.items():
            if required_amount > 0:
                ratio = investment.get(resource, 0) / required_amount
                investment_ratio += ratio
        
        avg_ratio = investment_ratio / len(required) if required else 0
        
        if avg_ratio >= 2.5:
            return FoundationStability.UNSHAKEABLE
        elif avg_ratio >= 2:
            return FoundationStability.SOLID
        elif avg_ratio >= 1.5:
            return FoundationStability.STABLE
        elif avg_ratio >= 1:
            return FoundationStability.UNSTABLE
        else:
            return FoundationStability.FRAGILE
    
    def _update_global_influence_map(self, node: InfluenceNode):
        """更新全局影响力地图"""
        radius = node.get_influence_radius()
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                if dx * dx + dy * dy <= radius * radius:
                    location = (node.location[0] + dx, node.location[1] + dy)
                    if location not in self.global_influence_map:
                        self.global_influence_map[location] = []
                    if node.node_id not in self.global_influence_map[location]:
                        self.global_influence_map[location].append(node.node_id)
    
    def _remove_from_global_influence_map(self, node: InfluenceNode):
        """从全局影响力地图移除节点"""
        radius = node.get_influence_radius()
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                if dx * dx + dy * dy <= radius * radius:
                    location = (node.location[0] + dx, node.location[1] + dy)
                    if location in self.global_influence_map:
                        if node.node_id in self.global_influence_map[location]:
                            self.global_influence_map[location].remove(node.node_id)
                        if not self.global_influence_map[location]:
                            del self.global_influence_map[location]
    
    def _calculate_distance(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> float:
        """计算两点距离"""
        return ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2) ** 0.5
    
    def _calculate_attack_success_rate(self, attack_strength: int, defense_strength: int, 
                                     attack_type: str, target_node: InfluenceNode) -> float:
        """计算攻击成功率"""
        base_rate = 0.5
        
        # 攻防比影响
        if defense_strength > 0:
            ratio = attack_strength / defense_strength
            base_rate = min(0.9, max(0.1, 0.3 + ratio * 0.2))
        
        # 攻击类型修正
        type_modifiers = {
            "direct_assault": 0.0,      # 直接攻击
            "economic_warfare": 0.1,    # 经济战
            "cultural_erosion": 0.15,   # 文化侵蚀
            "spiritual_challenge": 0.2, # 精神挑战
            "diplomatic_isolation": 0.1, # 外交孤立
            "information_warfare": 0.25  # 信息战
        }
        base_rate += type_modifiers.get(attack_type, 0)
        
        # 目标脆弱性
        if target_node.is_vulnerable():
            base_rate += 0.2
        
        return max(0.05, min(0.95, base_rate))
    
    def _calculate_damage(self, attack_strength: int, defense_strength: int, attack_type: str) -> int:
        """计算伤害"""
        base_damage = max(1, attack_strength - defense_strength // 2)
        
        # 攻击类型影响伤害
        type_multipliers = {
            "direct_assault": 1.5,
            "economic_warfare": 1.0,
            "cultural_erosion": 0.8,
            "spiritual_challenge": 1.2,
            "diplomatic_isolation": 0.9,
            "information_warfare": 0.7
        }
        
        multiplier = type_multipliers.get(attack_type, 1.0)
        return int(base_damage * multiplier)
    
    def _apply_damage_to_node(self, node: InfluenceNode, damage: int) -> bool:
        """对节点应用伤害，返回是否被摧毁"""
        # 伤害影响稳定性和影响力
        stability_damage = damage // 2
        influence_damage = damage // 3
        
        # 降低稳定性
        new_stability_value = max(1, node.stability.value - stability_damage)
        node.stability = FoundationStability(new_stability_value)
        
        # 降低影响力
        new_influence_value = max(0, node.influence_level.value - influence_damage)
        if new_influence_value == 0:
            return True  # 节点被摧毁
        
        node.influence_level = InfluenceLevel(new_influence_value)
        return False
    
    def _execute_remove_firewood_from_cauldron(self, executor_id: str, target_id: str, **kwargs) -> Dict:
        """执行釜底抽薪策略"""
        # 攻击敌人的经济根基
        target_network = self.player_networks.get(target_id)
        if not target_network:
            return {"success": False, "message": "目标玩家无根基"}
        
        # 找到经济根基
        economic_nodes = [node for node in target_network.nodes.values() 
                         if node.foundation_type == FoundationType.ECONOMIC]
        
        if not economic_nodes:
            return {"success": False, "message": "目标无经济根基"}
        
        # 攻击最脆弱的经济根基
        target_node = min(economic_nodes, key=lambda n: n.get_defense_strength())
        
        attack_result = self.attack_foundation(
            executor_id, target_node.node_id, "economic_warfare", 
            kwargs.get("attack_strength", 5)
        )
        
        if attack_result["success"]:
            return {
                "success": True,
                "message": "釜底抽薪成功，削弱敌人经济根基",
                "effect": f"对{target_node.node_id}造成{attack_result['damage']}点伤害"
            }
        
        return {"success": False, "message": "釜底抽薪失败"}
    
    def _execute_throw_brick_attract_jade(self, executor_id: str, target_id: str, **kwargs) -> Dict:
        """执行抛砖引玉策略"""
        # 故意暴露一个弱根基来引诱敌人攻击，然后反击
        executor_network = self.player_networks.get(executor_id)
        if not executor_network:
            return {"success": False, "message": "执行者无根基"}
        
        # 选择一个根基作为"砖"
        bait_node = kwargs.get("bait_node")
        if not bait_node or bait_node not in executor_network.nodes:
            # 自动选择最弱的根基
            if not executor_network.nodes:
                return {"success": False, "message": "无可用根基"}
            bait_node = min(executor_network.nodes.values(), 
                          key=lambda n: n.get_defense_strength()).node_id
        
        # 临时降低根基防御，引诱攻击
        node = executor_network.nodes[bait_node]
        original_stability = node.stability
        node.stability = FoundationStability.FRAGILE
        
        return {
            "success": True,
            "message": "抛砖引玉设置完成",
            "effect": f"根基{bait_node}暂时变得脆弱，引诱敌人攻击",
            "bait_node": bait_node,
            "original_stability": original_stability
        }
    
    def _execute_kill_with_borrowed_knife(self, executor_id: str, target_id: str, **kwargs) -> Dict:
        """执行借刀杀人策略"""
        # 利用第三方力量攻击目标
        third_party = kwargs.get("third_party")
        if not third_party:
            return {"success": False, "message": "需要指定第三方"}
        
        # 检查第三方是否有能力攻击目标
        third_party_network = self.player_networks.get(third_party)
        target_network = self.player_networks.get(target_id)
        
        if not third_party_network or not target_network:
            return {"success": False, "message": "第三方或目标无根基"}
        
        # 模拟第三方攻击
        target_nodes = list(target_network.nodes.values())
        if not target_nodes:
            return {"success": False, "message": "目标无可攻击根基"}
        
        target_node = random.choice(target_nodes)
        
        # 第三方攻击强度基于其网络强度
        attack_strength = int(third_party_network.get_network_strength())
        
        attack_result = self.attack_foundation(
            third_party, target_node.node_id, "direct_assault", attack_strength
        )
        
        if attack_result["success"]:
            return {
                "success": True,
                "message": f"借刀杀人成功，{third_party}攻击了{target_id}",
                "effect": f"{target_node.node_id}受到{attack_result['damage']}点伤害"
            }
        
        return {"success": False, "message": "借刀杀人失败"}
    
    def _execute_wait_at_ease(self, executor_id: str, target_id: str, **kwargs) -> Dict:
        """执行以逸待劳策略"""
        # 加强自己的防御，等待敌人疲惫后反击
        executor_network = self.player_networks.get(executor_id)
        if not executor_network:
            return {"success": False, "message": "执行者无根基"}
        
        # 加强所有根基的稳定性
        reinforcement_investment = kwargs.get("investment", {"qi": 20, "dao_xing": 10})
        
        reinforced_count = 0
        for node_id in executor_network.nodes:
            if self.reinforce_foundation(executor_id, node_id, reinforcement_investment):
                reinforced_count += 1
        
        if reinforced_count > 0:
            return {
                "success": True,
                "message": f"以逸待劳成功，加强了{reinforced_count}个根基",
                "effect": "所有根基防御力提升，等待反击时机"
            }
        
        return {"success": False, "message": "以逸待劳失败"}
    
    def _execute_loot_burning_house(self, executor_id: str, target_id: str, **kwargs) -> Dict:
        """执行趁火打劫策略"""
        # 趁敌人根基脆弱时攻击
        target_network = self.player_networks.get(target_id)
        if not target_network:
            return {"success": False, "message": "目标无根基"}
        
        # 找到脆弱的根基
        vulnerable_nodes = target_network.get_vulnerable_nodes()
        if not vulnerable_nodes:
            return {"success": False, "message": "目标无脆弱根基"}
        
        # 攻击最脆弱的根基
        target_node = min(vulnerable_nodes, key=lambda n: n.get_defense_strength())
        
        # 趁火打劫有额外攻击加成
        attack_strength = kwargs.get("attack_strength", 5) + 3
        
        attack_result = self.attack_foundation(
            executor_id, target_node.node_id, "direct_assault", attack_strength
        )
        
        if attack_result["success"]:
            return {
                "success": True,
                "message": "趁火打劫成功",
                "effect": f"对脆弱根基{target_node.node_id}造成{attack_result['damage']}点伤害"
            }
        
        return {"success": False, "message": "趁火打劫失败"}
    
    def _execute_sacrifice_plum_for_peach(self, executor_id: str, target_id: str, **kwargs) -> Dict:
        """执行李代桃僵策略"""
        # 牺牲一个次要根基来保护重要根基
        executor_network = self.player_networks.get(executor_id)
        if not executor_network:
            return {"success": False, "message": "执行者无根基"}
        
        sacrifice_node_id = kwargs.get("sacrifice_node")
        protect_node_id = kwargs.get("protect_node")
        
        if not sacrifice_node_id or not protect_node_id:
            return {"success": False, "message": "需要指定牺牲和保护的根基"}
        
        if (sacrifice_node_id not in executor_network.nodes or 
            protect_node_id not in executor_network.nodes):
            return {"success": False, "message": "指定的根基不存在"}
        
        sacrifice_node = executor_network.nodes[sacrifice_node_id]
        protect_node = executor_network.nodes[protect_node_id]
        
        # 将牺牲根基的资源转移到保护根基
        transferred_resources = sacrifice_node.resources_invested.copy()
        
        # 移除牺牲根基
        executor_network.remove_node(sacrifice_node_id)
        self._remove_from_global_influence_map(sacrifice_node)
        
        # 加强保护根基
        self.reinforce_foundation(executor_id, protect_node_id, transferred_resources)
        
        return {
            "success": True,
            "message": "李代桃僵成功",
            "effect": f"牺牲{sacrifice_node_id}，大幅加强{protect_node_id}"
        }