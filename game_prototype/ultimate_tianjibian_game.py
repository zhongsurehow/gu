"""
天机变 - 终极版本
集成所有深度改进系统的完整游戏体验
"""

import random
import time
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field

# 导入所有新系统
from advanced_ui_system import advanced_ui, MessageType, DisplaySection
from tianshi_system import tianshi_system, TianShiType, activate_tianshi
from faction_system import faction_system, FactionType, SecretRole, assign_faction_identities
from alliance_system import alliance_system, AllianceType, propose_alliance
from yaoci_aura_system import yaoci_aura_system, AuraType, ZonePosition
from evolving_cards_system import evolving_cards_system, initialize_player_deck, record_card_use
from ai_divination_system import ai_divination_system, DivinationType, GameState, perform_divination

@dataclass
class UltimatePlayer:
    """终极版玩家"""
    name: str
    avatar: str = "帝王"
    
    # 基础资源
    ap: int = 3
    qi: int = 5
    dao_xing: int = 0
    cheng_yi: int = 3
    
    # 位置和状态
    zone: str = "地"
    hand: List[str] = field(default_factory=list)
    influence_markers: Dict[str, int] = field(default_factory=dict)
    
    # 新系统相关
    secret_identity: Optional[str] = None
    faction: Optional[str] = None
    active_auras: List[str] = field(default_factory=list)
    alliance_ids: List[str] = field(default_factory=list)
    reputation: float = 50.0
    
    # 易学文化深度增强
    yin_energy: int = 5  # 阴气
    yang_energy: int = 5  # 阳气
    wuxing_mastery: Dict[str, int] = field(default_factory=lambda: {
        "木": 0, "火": 0, "土": 0, "金": 0, "水": 0
    })
    bagua_affinity: Dict[str, int] = field(default_factory=lambda: {
        "乾": 0, "坤": 0, "震": 0, "巽": 0, 
        "坎": 0, "离": 0, "艮": 0, "兑": 0
    })
    spiritual_realm: str = "凡人"  # 凡人 -> 修士 -> 真人 -> 仙人 -> 圣人
    
    # 游戏统计
    turns_played: int = 0
    successful_actions: int = 0
    failed_actions: int = 0
    
    def get_yin_yang_balance(self) -> float:
        """获取阴阳平衡度"""
        total = self.yin_energy + self.yang_energy
        if total == 0:
            return 0.5
        return min(self.yin_energy, self.yang_energy) / max(self.yin_energy, self.yang_energy)
    
    def get_wuxing_total(self) -> int:
        """获取五行总掌握度"""
        return sum(self.wuxing_mastery.values())
    
    def get_bagua_total(self) -> int:
        """获取八卦总亲和度"""
        return sum(self.bagua_affinity.values())
    
    def advance_spiritual_realm(self):
        """提升修为境界"""
        realms = ["凡人", "修士", "真人", "仙人", "圣人"]
        current_index = realms.index(self.spiritual_realm)
        if current_index < len(realms) - 1:
            self.spiritual_realm = realms[current_index + 1]
            return True
        return False
    
    def get_cultural_power(self) -> int:
        """获取文化力量值"""
        balance_bonus = int(self.get_yin_yang_balance() * 10)
        wuxing_bonus = self.get_wuxing_total()
        bagua_bonus = self.get_bagua_total()
        realm_bonus = ["凡人", "修士", "真人", "仙人", "圣人"].index(self.spiritual_realm) * 5
        
        return balance_bonus + wuxing_bonus + bagua_bonus + realm_bonus

    def get_resource_dict(self) -> Dict[str, int]:
        """获取资源字典"""
        return {
            "ap": self.ap,
            "qi": self.qi,
            "dao_xing": self.dao_xing,
            "cheng_yi": self.cheng_yi
        }
    
    def modify_resource(self, resource: str, amount: int):
        """修改资源"""
        if resource == "ap":
            self.ap = max(0, self.ap + amount)
        elif resource == "qi":
            self.qi = max(0, self.qi + amount)
        elif resource == "dao_xing":
            self.dao_xing = max(0, self.dao_xing + amount)
        elif resource == "cheng_yi":
            self.cheng_yi = max(0, self.cheng_yi + amount)
    
    def can_afford(self, cost: Dict[str, int]) -> bool:
        """检查是否能承担成本"""
        for resource, amount in cost.items():
            if resource == "ap" and self.ap < amount:
                return False
            elif resource == "qi" and self.qi < amount:
                return False
            elif resource == "dao_xing" and self.dao_xing < amount:
                return False
            elif resource == "cheng_yi" and self.cheng_yi < amount:
                return False
        return True
    
    def pay_cost(self, cost: Dict[str, int]) -> bool:
        """支付成本"""
        if not self.can_afford(cost):
            return False
        
        for resource, amount in cost.items():
            self.modify_resource(resource, -amount)
        
        return True

@dataclass
class UltimateGameState:
    """终极游戏状态"""
    players: Dict[str, UltimatePlayer] = field(default_factory=dict)
    current_turn: int = 0
    current_player_index: int = 0
    player_order: List[str] = field(default_factory=list)
    
    # 棋盘状态
    zones: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    
    # 游戏历史
    action_history: List[Dict[str, Any]] = field(default_factory=list)
    
    # 全局状态
    active_tianshi: List[str] = field(default_factory=list)
    global_events: List[Dict[str, Any]] = field(default_factory=list)
    
    def get_current_player(self) -> UltimatePlayer:
        """获取当前玩家"""
        current_player_name = self.player_order[self.current_player_index]
        return self.players[current_player_name]
    
    def next_player(self):
        """切换到下一个玩家"""
        self.current_player_index = (self.current_player_index + 1) % len(self.player_order)
        if self.current_player_index == 0:
            self.current_turn += 1
    
    def record_action(self, player_name: str, action: str, success: bool, details: Dict[str, Any]):
        """记录行动"""
        self.action_history.append({
            "turn": self.current_turn,
            "player": player_name,
            "action": action,
            "success": success,
            "details": details,
            "timestamp": time.time()
        })
    
    def get_game_state_for_ai(self) -> GameState:
        """为AI系统获取游戏状态"""
        players_data = {}
        for name, player in self.players.items():
            players_data[name] = {
                "resources": player.get_resource_dict(),
                "zone": player.zone,
                "hand_size": len(player.hand),
                "influence": player.influence_markers,
                "reputation": player.reputation
            }
        
        return GameState(
            current_turn=self.current_turn,
            players=players_data,
            board_state={"zones": self.zones},
            remaining_cards=[],  # 简化处理
            recent_actions=self.action_history[-10:],
            global_events=self.global_events
        )

class UltimateTianJiBianGame:
    """终极版天机变游戏"""
    
    def __init__(self):
        self.game_state = UltimateGameState()
        self.game_running = False
        self.tutorial_mode = False
        
        # 初始化所有系统
        self._initialize_systems()
    
    def _initialize_systems(self):
        """初始化所有系统"""
        # 初始化棋盘
        self.game_state.zones = {
            "乾": {"controller": None, "influence": {}, "special_effects": []},
            "坤": {"controller": None, "influence": {}, "special_effects": []},
            "震": {"controller": None, "influence": {}, "special_effects": []},
            "巽": {"controller": None, "influence": {}, "special_effects": []},
            "坎": {"controller": None, "influence": {}, "special_effects": []},
            "离": {"controller": None, "influence": {}, "special_effects": []},
            "艮": {"controller": None, "influence": {}, "special_effects": []},
            "兑": {"controller": None, "influence": {}, "special_effects": []}
        }
    
    def start_game(self, player_names: List[str], tutorial: bool = False):
        """开始游戏"""
        self.tutorial_mode = tutorial
        
        advanced_ui.clear_screen()
        advanced_ui.display_title("天机变 - 终极版本")
        
        if tutorial:
            self._show_tutorial_intro()
        
        # 初始化玩家
        self._initialize_players(player_names)
        
        # 分配秘密身份
        self._assign_secret_identities()
        
        # 初始化牌库
        self._initialize_player_decks()
        
        # 触发开局天时事件
        self._trigger_opening_tianshi()
        
        # 显示游戏开始信息
        self._display_game_start_info()
        
        self.game_running = True
        
        # 开始游戏循环
        self._game_loop()
    
    def _show_tutorial_intro(self):
        """显示教程介绍"""
        advanced_ui.display_mystical_message(
            "欢迎来到天机变的世界！\n\n"
            "在这个充满智慧与策略的游戏中，你将：\n"
            "• 运用易经智慧，掌控八卦之力\n"
            "• 体验动态的天时变化\n"
            "• 建立盟约或策划背叛\n"
            "• 让你的卡牌在战斗中成长\n"
            "• 通过AI占卜洞察先机\n\n"
            "准备好开始你的修行之旅了吗？",
            "游戏介绍",
            MessageType.MYSTICAL
        )
        input("\n按回车键继续...")
    
    def _initialize_players(self, player_names: List[str]):
        """初始化玩家"""
        self.game_state.player_order = player_names.copy()
        
        avatars = ["帝王", "隐士", "学者", "武者"]
        
        for i, name in enumerate(player_names):
            avatar = avatars[i % len(avatars)]
            player = UltimatePlayer(name=name, avatar=avatar)
            
            # 根据化身调整初始资源
            if avatar == "帝王":
                player.cheng_yi += 2
                player.ap += 1
            elif avatar == "隐士":
                player.qi += 3
                player.dao_xing += 1
            elif avatar == "学者":
                player.qi += 2
                player.dao_xing += 2
            elif avatar == "武者":
                player.ap += 2
                player.cheng_yi += 1
            
            # 初始手牌
            starting_cards = ["乾为天", "坤为地", "水雷屯", "山水蒙"]
            player.hand = starting_cards.copy()
            
            self.game_state.players[name] = player
    
    def _assign_secret_identities(self):
        """分配秘密身份"""
        # 为所有玩家分配身份
        assign_faction_identities(self.game_state.player_order)
        
        # 显示每个玩家的秘密身份
        for player_name in self.game_state.player_order:
            identity = faction_system.player_identities[player_name]
            player = self.game_state.players[player_name]
            player.secret_identity = identity.role.value
            player.faction = identity.faction.value
            
            # 获取秘密任务
            missions = identity.secret_missions
            mission_text = "\n".join([f"• {mission.description}" for mission in missions])
            
            advanced_ui.display_mystical_message(
                f"你的秘密身份：{identity.role.value}\n"
                f"所属阵营：{identity.faction.value}\n"
                f"秘密任务：\n{mission_text}",
                f"{player_name} 的天命",
                MessageType.MYSTICAL
            )
            input("按回车键继续...")
    
    def _initialize_player_decks(self):
        """初始化玩家牌库"""
        for player_name, player in self.game_state.players.items():
            initialize_player_deck(player_name, player.hand)
    
    def _trigger_opening_tianshi(self):
        """触发开局天时事件"""
        event = tianshi_system.draw_tianshi()
        if event:
            tianshi_system.activate_tianshi(self.game_state)
            self.game_state.active_tianshi.append(event.name)
            self.game_state.global_events.append({
                "type": "tianshi",
                "name": event.name,
                "description": event.flavor_text,
                "turn": self.game_state.current_turn
            })
    
    def _display_game_start_info(self):
        """显示游戏开始信息"""
        advanced_ui.clear_screen()
        advanced_ui.display_title("游戏开始")
        
        advanced_ui.print_colored("玩家信息：", MessageType.HIGHLIGHT)
        for player_name, player in self.game_state.players.items():
            advanced_ui.print_colored(
                f"• {player_name} ({player.avatar}) - "
                f"AP:{player.ap} 气:{player.qi} 道行:{player.dao_xing} 诚意:{player.cheng_yi}",
                MessageType.INFO
            )
        
        if self.game_state.active_tianshi:
            advanced_ui.print_colored("当前天时：", MessageType.MYSTICAL)
            for tianshi in self.game_state.active_tianshi:
                advanced_ui.print_colored(f"• {tianshi}", MessageType.INFO)
        
        input("\n按回车键开始第一回合...")
    
    def _game_loop(self):
        """游戏主循环"""
        while self.game_running:
            current_player = self.game_state.get_current_player()
            
            # 回合开始处理
            self._start_turn(current_player)
            
            # 玩家行动阶段
            self._player_turn(current_player)
            
            # 回合结束处理
            self._end_turn(current_player)
            
            # 检查胜利条件
            if self._check_victory_conditions():
                break
            
            # 切换到下一个玩家
            self.game_state.next_player()
            
            # 每轮结束时的处理
            if self.game_state.current_player_index == 0:
                self._end_round()
    
    def _start_turn(self, player: UltimatePlayer):
        """回合开始"""
        player.turns_played += 1
        
        # 恢复AP
        player.ap = min(5, player.ap + 2)
        
        # 应用光环效果
        yaoci_aura_system.apply_turn_start_effects(player.name)
        
        # 应用天时效果
        for tianshi_name in self.game_state.active_tianshi:
            tianshi_system.apply_tianshi_effects(tianshi_name, player.name)
        
        # 显示回合开始信息
        self._display_turn_start(player)
    
    def _display_turn_start(self, player: UltimatePlayer):
        """显示回合开始信息"""
        advanced_ui.clear_screen()
        
        # 显示核心状态
        core_status = DisplaySection(
            title=f"{player.name} 的回合 (第{self.game_state.current_turn + 1}回合)",
            content=[
                f"化身：{player.avatar}",
                f"位置：{player.zone}",
                f"AP: {player.ap}  气: {player.qi}  道行: {player.dao_xing}  诚意: {player.cheng_yi}"
            ],
            priority=1
        )
        
        advanced_ui.display_section(core_status)
        
        # 显示活跃效果
        if player.active_auras or self.game_state.active_tianshi:
            effects_content = []
            if player.active_auras:
                effects_content.append("活跃光环：" + ", ".join(player.active_auras))
            if self.game_state.active_tianshi:
                effects_content.append("当前天时：" + ", ".join(self.game_state.active_tianshi))
            
            effects_section = DisplaySection(
                title="当前效果",
                content=effects_content,
                priority=2
            )
            advanced_ui.display_section(effects_section)
    
    def _player_turn(self, player: UltimatePlayer):
        """玩家回合"""
        while player.ap > 0:
            # 显示行动菜单
            action = self._display_action_menu(player)
            
            if action == "结束回合":
                break
            elif action == "查看状态":
                self._display_detailed_status(player)
            elif action == "查看棋盘":
                self._display_board_status()
            elif action == "演卦":
                self._action_play_card(player)
            elif action == "移动":
                self._action_move(player)
            elif action == "冥想":
                self._action_meditate(player)
            elif action == "学习":
                self._action_study(player)
            elif action == "占卜":
                self._action_divination(player)
            elif action == "盟约":
                self._action_alliance(player)
            elif action == "进化卡牌":
                self._action_evolve_card(player)
            elif action == "查看牌库":
                self._display_deck_status(player)
            else:
                advanced_ui.print_colored("无效的行动选择", MessageType.ERROR)
    
    def _display_action_menu(self, player: UltimatePlayer) -> str:
        """显示行动菜单"""
        menu_items = [
            f"演卦 (1 AP) - 打出卦象牌",
            f"移动 (1 AP) - 改变位置",
            f"冥想 (1 AP) - 获得气",
            f"学习 (2 AP) - 获得道行",
            f"占卜 (1 AP) - AI智能占卜",
            f"盟约 (2 AP) - 建立或管理盟约",
            f"进化卡牌 - 升级你的卡牌",
            "查看状态 - 详细状态信息",
            "查看棋盘 - 棋盘控制情况",
            "查看牌库 - 牌库进化状态",
            "结束回合"
        ]
        
        menu_section = DisplaySection(
            title=f"行动选择 (剩余AP: {player.ap})",
            content=menu_items,
            priority=1
        )
        
        advanced_ui.display_section(menu_section)
        
        while True:
            choice = input("\n请选择行动: ").strip()
            
            action_map = {
                "1": "演卦", "演卦": "演卦",
                "2": "移动", "移动": "移动",
                "3": "冥想", "冥想": "冥想",
                "4": "学习", "学习": "学习",
                "5": "占卜", "占卜": "占卜",
                "6": "盟约", "盟约": "盟约",
                "7": "进化卡牌", "进化": "进化卡牌", "进化卡牌": "进化卡牌",
                "8": "查看状态", "状态": "查看状态",
                "9": "查看棋盘", "棋盘": "查看棋盘",
                "10": "查看牌库", "牌库": "查看牌库",
                "0": "结束回合", "结束": "结束回合", "结束回合": "结束回合"
            }
            
            if choice in action_map:
                return action_map[choice]
            else:
                advanced_ui.print_colored("请输入有效的选择", MessageType.ERROR)
    
    def _action_play_card(self, player: UltimatePlayer):
        """演卦行动"""
        if player.ap < 1:
            advanced_ui.print_colored("AP不足", MessageType.ERROR)
            return
        
        if not player.hand:
            advanced_ui.print_colored("手牌为空", MessageType.ERROR)
            return
        
        # 显示手牌
        advanced_ui.print_colored("你的手牌：", MessageType.INFO)
        for i, card in enumerate(player.hand):
            advanced_ui.print_colored(f"{i + 1}. {card}", MessageType.INFO)
        
        try:
            choice = int(input("选择要打出的卡牌 (输入数字): ")) - 1
            if 0 <= choice < len(player.hand):
                card_name = player.hand[choice]
                
                # 选择目标区域
                zone = self._select_target_zone()
                if zone:
                    success = self._play_card(player, card_name, zone)
                    if success:
                        player.hand.remove(card_name)
                        player.ap -= 1
                        
                        # 记录卡牌使用
                        record_card_use(player.name, card_name, self.game_state.current_turn, zone, success)
                        
                        # 激活爻辞光环
                        yaoci_aura_system.set_player_gua(player.name, card_name)
                        zone_position = ZonePosition.DI if zone == "地" else ZonePosition.REN if zone == "人" else ZonePosition.TIAN
                        yaoci_aura_system.update_player_zone(player.name, zone_position)
                        
                        advanced_ui.print_colored(f"成功打出 {card_name}", MessageType.SUCCESS)
                    else:
                        advanced_ui.print_colored("打出卡牌失败", MessageType.ERROR)
            else:
                advanced_ui.print_colored("无效的卡牌选择", MessageType.ERROR)
        except ValueError:
            advanced_ui.print_colored("请输入有效的数字", MessageType.ERROR)
    
    def _select_target_zone(self) -> Optional[str]:
        """选择目标区域"""
        zones = list(self.game_state.zones.keys())
        
        advanced_ui.print_colored("选择目标区域：", MessageType.INFO)
        for i, zone in enumerate(zones):
            controller = self.game_state.zones[zone]["controller"]
            controller_text = f" (控制者: {controller})" if controller else " (无人控制)"
            advanced_ui.print_colored(f"{i + 1}. {zone}{controller_text}", MessageType.INFO)
        
        try:
            choice = int(input("选择区域 (输入数字): ")) - 1
            if 0 <= choice < len(zones):
                return zones[choice]
        except ValueError:
            pass
        
        advanced_ui.print_colored("无效的区域选择", MessageType.ERROR)
        return None
    
    def _play_card(self, player: UltimatePlayer, card_name: str, zone: str) -> bool:
        """打出卡牌的具体逻辑"""
        # 简化的卡牌效果处理
        zone_data = self.game_state.zones[zone]
        
        # 增加影响力
        if player.name not in zone_data["influence"]:
            zone_data["influence"][player.name] = 0
        
        zone_data["influence"][player.name] += 2
        
        # 检查是否获得控制权
        max_influence = max(zone_data["influence"].values())
        if zone_data["influence"][player.name] == max_influence:
            old_controller = zone_data["controller"]
            zone_data["controller"] = player.name
            
            if old_controller != player.name:
                advanced_ui.print_colored(f"获得了 {zone} 的控制权！", MessageType.SUCCESS)
                player.dao_xing += 2  # 获得控制权奖励
        
        # 记录行动
        self.game_state.record_action(
            player.name, "演卦", True,
            {"card": card_name, "zone": zone, "influence_gained": 2}
        )
        
        player.successful_actions += 1
        return True
    
    def _action_move(self, player: UltimatePlayer):
        """移动行动"""
        if player.ap < 1:
            advanced_ui.print_colored("AP不足", MessageType.ERROR)
            return
        
        zones = ["地", "人", "天"]
        current_index = zones.index(player.zone)
        
        advanced_ui.print_colored(f"当前位置：{player.zone}", MessageType.INFO)
        advanced_ui.print_colored("可移动到：", MessageType.INFO)
        
        available_zones = []
        for i, zone in enumerate(zones):
            if zone != player.zone:
                available_zones.append(zone)
                advanced_ui.print_colored(f"{len(available_zones)}. {zone}", MessageType.INFO)
        
        try:
            choice = int(input("选择目标位置: ")) - 1
            if 0 <= choice < len(available_zones):
                new_zone = available_zones[choice]
                player.zone = new_zone
                player.ap -= 1
                
                advanced_ui.print_colored(f"移动到 {new_zone}", MessageType.SUCCESS)
                
                # 记录行动
                self.game_state.record_action(
                    player.name, "移动", True,
                    {"from": zones[current_index], "to": new_zone}
                )
                
                player.successful_actions += 1
            else:
                advanced_ui.print_colored("无效的位置选择", MessageType.ERROR)
        except ValueError:
            advanced_ui.print_colored("请输入有效的数字", MessageType.ERROR)
    
    def _action_meditate(self, player: UltimatePlayer):
        """冥想行动 - 增强易学文化内涵"""
        if player.ap < 1:
            advanced_ui.print_colored("AP不足", MessageType.ERROR)
            return
        
        # 选择冥想类型
        meditation_types = [
            ("阴阳调和", "平衡阴阳之气"),
            ("五行修炼", "提升五行掌握"),
            ("八卦感悟", "增强八卦亲和"),
            ("境界突破", "尝试提升修为境界")
        ]
        
        advanced_ui.print_colored("选择冥想类型：", MessageType.MYSTICAL)
        for i, (name, desc) in enumerate(meditation_types):
            advanced_ui.print_colored(f"{i + 1}. {name} - {desc}", MessageType.INFO)
        
        try:
            choice = int(input("选择冥想类型: ")) - 1
            if 0 <= choice < len(meditation_types):
                meditation_type, _ = meditation_types[choice]
                self._perform_meditation(player, meditation_type)
            else:
                advanced_ui.print_colored("无效的冥想类型", MessageType.ERROR)
        except ValueError:
            advanced_ui.print_colored("请输入有效的数字", MessageType.ERROR)
    
    def _perform_meditation(self, player: UltimatePlayer, meditation_type: str):
        """执行冥想"""
        qi_gain = 3
        
        # 位置加成
        if player.zone == "地":
            qi_gain += 1
        
        if meditation_type == "阴阳调和":
            # 平衡阴阳之气
            total_energy = player.yin_energy + player.yang_energy
            target_balance = total_energy // 2
            
            if abs(player.yin_energy - player.yang_energy) > 2:
                player.yin_energy = target_balance
                player.yang_energy = total_energy - target_balance
                advanced_ui.print_colored("阴阳之气得到平衡！", MessageType.SUCCESS)
                qi_gain += 2
            else:
                player.yin_energy += 1
                player.yang_energy += 1
                advanced_ui.print_colored("阴阳之气同时增长", MessageType.SUCCESS)
        
        elif meditation_type == "五行修炼":
            # 选择要修炼的五行
            wuxing_elements = ["木", "火", "土", "金", "水"]
            advanced_ui.print_colored("选择要修炼的五行：", MessageType.INFO)
            for i, element in enumerate(wuxing_elements):
                current_level = player.wuxing_mastery[element]
                advanced_ui.print_colored(f"{i + 1}. {element} (当前等级: {current_level})", MessageType.INFO)
            
            try:
                element_choice = int(input("选择五行: ")) - 1
                if 0 <= element_choice < len(wuxing_elements):
                    element = wuxing_elements[element_choice]
                    player.wuxing_mastery[element] += 1
                    
                    # 五行相生加成
                    sheng_cycle = {"木": "火", "火": "土", "土": "金", "金": "水", "水": "木"}
                    if element in sheng_cycle:
                        next_element = sheng_cycle[element]
                        player.wuxing_mastery[next_element] += 1
                        advanced_ui.print_colored(f"{element}生{next_element}，{next_element}也得到提升！", MessageType.SUCCESS)
                    
                    advanced_ui.print_colored(f"{element}修炼成功！", MessageType.SUCCESS)
                    qi_gain += 1
            except ValueError:
                advanced_ui.print_colored("请输入有效的数字", MessageType.ERROR)
                return
        
        elif meditation_type == "八卦感悟":
            # 根据当前位置和时间增强对应八卦
            zone_bagua_map = {
                "乾": "乾", "坤": "坤", "震": "震", "巽": "巽",
                "坎": "坎", "离": "离", "艮": "艮", "兑": "兑"
            }
            
            # 如果在八卦区域，增强对应八卦
            for zone, bagua in zone_bagua_map.items():
                if zone in self.game_state.zones and self.game_state.zones[zone]["controller"] == player.name:
                    player.bagua_affinity[bagua] += 2
                    advanced_ui.print_colored(f"在{zone}区域的感悟让你对{bagua}卦的理解更深！", MessageType.SUCCESS)
                    qi_gain += 1
            
            # 随机增强一个八卦
            import random
            random_bagua = random.choice(list(player.bagua_affinity.keys()))
            player.bagua_affinity[random_bagua] += 1
            advanced_ui.print_colored(f"对{random_bagua}卦有了新的感悟", MessageType.SUCCESS)
        
        elif meditation_type == "境界突破":
            # 尝试提升修为境界
            cultural_power = player.get_cultural_power()
            realm_requirements = {"凡人": 10, "修士": 25, "真人": 50, "仙人": 80, "圣人": 120}
            
            current_realm = player.spiritual_realm
            if current_realm in realm_requirements:
                required_power = realm_requirements[current_realm]
                
                if cultural_power >= required_power:
                    if player.advance_spiritual_realm():
                        advanced_ui.print_colored(f"恭喜！修为境界提升至{player.spiritual_realm}！", MessageType.HIGHLIGHT)
                        qi_gain += 5
                        player.dao_xing += 3
                    else:
                        advanced_ui.print_colored("已达到最高境界", MessageType.INFO)
                else:
                    advanced_ui.print_colored(f"文化力量不足，需要{required_power}点，当前{cultural_power}点", MessageType.WARNING)
                    qi_gain += 1
        
        player.qi += qi_gain
        player.ap -= 1
        
        advanced_ui.print_colored(f"冥想获得 {qi_gain} 点气", MessageType.SUCCESS)
        
        # 显示当前文化状态
        self._display_cultural_status(player)
        
        # 记录行动
        self.game_state.record_action(
            player.name, "冥想", True,
            {"type": meditation_type, "qi_gained": qi_gain}
        )
        
        player.successful_actions += 1
    
    def _display_cultural_status(self, player: UltimatePlayer):
        """显示文化状态"""
        advanced_ui.print_colored("当前修行状态：", MessageType.MYSTICAL)
        
        # 阴阳状态
        balance = player.get_yin_yang_balance()
        balance_desc = "完美平衡" if balance > 0.8 else "基本平衡" if balance > 0.6 else "略有失衡" if balance > 0.4 else "严重失衡"
        advanced_ui.print_colored(f"阴阳平衡: {balance:.2f} ({balance_desc})", MessageType.INFO)
        
        # 五行状态
        wuxing_total = player.get_wuxing_total()
        advanced_ui.print_colored(f"五行总掌握: {wuxing_total}点", MessageType.INFO)
        
        # 八卦状态
        bagua_total = player.get_bagua_total()
        advanced_ui.print_colored(f"八卦总亲和: {bagua_total}点", MessageType.INFO)
        
        # 修为境界
        cultural_power = player.get_cultural_power()
        advanced_ui.print_colored(f"修为境界: {player.spiritual_realm} (文化力量: {cultural_power})", MessageType.HIGHLIGHT)

    def _action_study(self, player: UltimatePlayer):
        """学习行动"""
        if player.ap < 2:
            advanced_ui.print_colored("AP不足 (需要2点)", MessageType.ERROR)
            return
        
        if player.qi < 3:
            advanced_ui.print_colored("气不足 (需要3点)", MessageType.ERROR)
            return
        
        dao_xing_gain = 2
        
        # 位置加成
        if player.zone == "天":
            dao_xing_gain += 1
        
        player.dao_xing += dao_xing_gain
        player.qi -= 3
        player.ap -= 2
        
        advanced_ui.print_colored(f"学习获得 {dao_xing_gain} 点道行", MessageType.SUCCESS)
        
        # 记录行动
        self.game_state.record_action(
            player.name, "学习", True,
            {"dao_xing_gained": dao_xing_gain, "qi_spent": 3}
        )
        
        player.successful_actions += 1
    
    def _action_divination(self, player: UltimatePlayer):
        """占卜行动"""
        if player.ap < 1:
            advanced_ui.print_colored("AP不足", MessageType.ERROR)
            return
        
        # 选择占卜类型
        divination_types = [
            (DivinationType.FORTUNE, "运势占卜"),
            (DivinationType.ACTION, "行动占卜"),
            (DivinationType.STRATEGY, "策略占卜"),
            (DivinationType.TIMING, "时机占卜"),
            (DivinationType.RELATIONSHIP, "关系占卜")
        ]
        
        advanced_ui.print_colored("选择占卜类型：", MessageType.MYSTICAL)
        for i, (div_type, name) in enumerate(divination_types):
            advanced_ui.print_colored(f"{i + 1}. {name}", MessageType.INFO)
        
        try:
            choice = int(input("选择占卜类型: ")) - 1
            if 0 <= choice < len(divination_types):
                div_type, _ = divination_types[choice]
                
                # 执行占卜
                game_state = self.game_state.get_game_state_for_ai()
                result = perform_divination(player.name, div_type, game_state)
                
                # 显示占卜结果
                ai_divination_system.display_divination_result(result)
                
                player.ap -= 1
                
                # 记录行动
                self.game_state.record_action(
                    player.name, "占卜", True,
                    {"type": div_type.value, "accuracy": result.accuracy}
                )
                
                player.successful_actions += 1
                
                input("\n按回车键继续...")
            else:
                advanced_ui.print_colored("无效的占卜类型", MessageType.ERROR)
        except ValueError:
            advanced_ui.print_colored("请输入有效的数字", MessageType.ERROR)
    
    def _action_alliance(self, player: UltimatePlayer):
        """盟约行动"""
        if player.ap < 2:
            advanced_ui.print_colored("AP不足 (需要2点)", MessageType.ERROR)
            return
        
        # 显示盟约选项
        advanced_ui.print_colored("盟约选项：", MessageType.INFO)
        advanced_ui.print_colored("1. 提议新盟约", MessageType.INFO)
        advanced_ui.print_colored("2. 查看现有盟约", MessageType.INFO)
        advanced_ui.print_colored("3. 背叛盟约", MessageType.INFO)
        
        choice = input("选择操作: ").strip()
        
        if choice == "1":
            self._propose_new_alliance(player)
        elif choice == "2":
            alliance_system.display_player_alliances(player.name)
        elif choice == "3":
            self._betray_alliance(player)
        else:
            advanced_ui.print_colored("无效的选择", MessageType.ERROR)
            return
        
        player.ap -= 2
    
    def _propose_new_alliance(self, player: UltimatePlayer):
        """提议新盟约"""
        # 选择目标玩家
        other_players = [name for name in self.game_state.player_order if name != player.name]
        
        if not other_players:
            advanced_ui.print_colored("没有其他玩家可以结盟", MessageType.ERROR)
            return
        
        advanced_ui.print_colored("选择结盟对象：", MessageType.INFO)
        for i, name in enumerate(other_players):
            advanced_ui.print_colored(f"{i + 1}. {name}", MessageType.INFO)
        
        try:
            choice = int(input("选择玩家: ")) - 1
            if 0 <= choice < len(other_players):
                target_player = other_players[choice]
                
                # 选择盟约类型
                alliance_types = [
                    (AllianceType.TRADE, "通商协议"),
                    (AllianceType.NON_AGGRESSION, "互不侵犯"),
                    (AllianceType.MUTUAL_DEFENSE, "共同防御")
                ]
                
                advanced_ui.print_colored("选择盟约类型：", MessageType.INFO)
                for i, (a_type, name) in enumerate(alliance_types):
                    advanced_ui.print_colored(f"{i + 1}. {name}", MessageType.INFO)
                
                type_choice = int(input("选择类型: ")) - 1
                if 0 <= type_choice < len(alliance_types):
                    alliance_type, _ = alliance_types[type_choice]
                    
                    # 提议盟约
                    success = propose_alliance(player.name, target_player, alliance_type, 5)  # 5回合期限
                    
                    if success:
                        advanced_ui.print_colored(f"向 {target_player} 提议了盟约", MessageType.SUCCESS)
                        player.successful_actions += 1
                    else:
                        advanced_ui.print_colored("盟约提议失败", MessageType.ERROR)
                        player.failed_actions += 1
                else:
                    advanced_ui.print_colored("无效的盟约类型", MessageType.ERROR)
            else:
                advanced_ui.print_colored("无效的玩家选择", MessageType.ERROR)
        except ValueError:
            advanced_ui.print_colored("请输入有效的数字", MessageType.ERROR)
    
    def _betray_alliance(self, player: UltimatePlayer):
        """背叛盟约"""
        # 获取玩家的盟约
        alliances = alliance_system.get_player_alliances(player.name)
        
        if not alliances:
            advanced_ui.print_colored("你没有任何盟约可以背叛", MessageType.INFO)
            return
        
        advanced_ui.print_colored("选择要背叛的盟约：", MessageType.WARNING)
        for i, alliance in enumerate(alliances):
            other_party = alliance.party_b if alliance.party_a == player.name else alliance.party_a
            advanced_ui.print_colored(f"{i + 1}. 与 {other_party} 的 {alliance.alliance_type.value}", MessageType.INFO)
        
        try:
            choice = int(input("选择盟约: ")) - 1
            if 0 <= choice < len(alliances):
                alliance = alliances[choice]
                
                # 确认背叛
                confirm = input(f"确认背叛与 {alliance.party_b if alliance.party_a == player.name else alliance.party_a} 的盟约？(y/n): ")
                
                if confirm.lower() == 'y':
                    success = alliance_system.betray_alliance(player.name, alliance.alliance_id)
                    
                    if success:
                        advanced_ui.print_colored("背叛成功！但你的声誉受损", MessageType.WARNING)
                        player.reputation -= 20
                        player.successful_actions += 1
                    else:
                        advanced_ui.print_colored("背叛失败", MessageType.ERROR)
                        player.failed_actions += 1
            else:
                advanced_ui.print_colored("无效的盟约选择", MessageType.ERROR)
        except ValueError:
            advanced_ui.print_colored("请输入有效的数字", MessageType.ERROR)
    
    def _action_evolve_card(self, player: UltimatePlayer):
        """进化卡牌行动"""
        opportunities = evolving_cards_system.get_evolution_opportunities(player.name)
        
        if not opportunities:
            advanced_ui.print_colored("当前没有可进化的卡牌", MessageType.INFO)
            return
        
        advanced_ui.print_colored("可进化的卡牌：", MessageType.MYSTICAL)
        for i, (card_name, condition) in enumerate(opportunities):
            advanced_ui.print_colored(f"{i + 1}. {card_name} - {condition}", MessageType.INFO)
        
        try:
            choice = int(input("选择要进化的卡牌: ")) - 1
            if 0 <= choice < len(opportunities):
                card_name, _ = opportunities[choice]
                
                success = evolving_cards_system.trigger_evolution(player.name, card_name)
                
                if success:
                    advanced_ui.print_colored(f"{card_name} 进化成功！", MessageType.SUCCESS)
                    player.successful_actions += 1
                else:
                    advanced_ui.print_colored("进化失败", MessageType.ERROR)
                    player.failed_actions += 1
                
                input("按回车键继续...")
            else:
                advanced_ui.print_colored("无效的卡牌选择", MessageType.ERROR)
        except ValueError:
            advanced_ui.print_colored("请输入有效的数字", MessageType.ERROR)
    
    def _display_detailed_status(self, player: UltimatePlayer):
        """显示详细状态"""
        advanced_ui.clear_screen()
        
        # 基础信息
        basic_info = DisplaySection(
            title=f"{player.name} 的详细状态",
            content=[
                f"化身：{player.avatar}",
                f"位置：{player.zone}",
                f"AP: {player.ap}  气: {player.qi}  道行: {player.dao_xing}  诚意: {player.cheng_yi}",
                f"声誉: {player.reputation:.1f}",
                f"手牌数量: {len(player.hand)}"
            ],
            priority=1
        )
        advanced_ui.display_section(basic_info)
        
        # 秘密身份
        if player.secret_identity:
            identity_info = DisplaySection(
                title="秘密身份",
                content=[
                    f"身份：{player.secret_identity}",
                    f"阵营：{player.faction}"
                ],
                priority=2
            )
            advanced_ui.display_section(identity_info)
        
        # 游戏统计
        stats_info = DisplaySection(
            title="游戏统计",
            content=[
                f"已进行回合：{player.turns_played}",
                f"成功行动：{player.successful_actions}",
                f"失败行动：{player.failed_actions}",
                f"成功率：{player.successful_actions / max(1, player.successful_actions + player.failed_actions):.1%}"
            ],
            priority=3
        )
        advanced_ui.display_section(stats_info)
        
        input("\n按回车键返回...")
    
    def _display_board_status(self):
        """显示棋盘状态"""
        advanced_ui.clear_screen()
        
        board_content = []
        for zone_name, zone_data in self.game_state.zones.items():
            controller = zone_data["controller"] or "无人控制"
            influence_text = ", ".join([f"{player}:{inf}" for player, inf in zone_data["influence"].items()])
            
            board_content.append(f"{zone_name}: 控制者={controller}")
            if influence_text:
                board_content.append(f"  影响力: {influence_text}")
        
        board_section = DisplaySection(
            title="棋盘状态",
            content=board_content,
            priority=1
        )
        advanced_ui.display_section(board_section)
        
        input("\n按回车键返回...")
    
    def _display_deck_status(self, player: UltimatePlayer):
        """显示牌库状态"""
        advanced_ui.clear_screen()
        evolving_cards_system.display_deck_status(player.name)
        input("\n按回车键返回...")
    
    def _end_turn(self, player: UltimatePlayer):
        """回合结束"""
        # 应用回合结束效果
        yaoci_aura_system.update_turn(player.name)
        
        # 更新盟约
        alliance_system.update_turn()
        
        # 显示回合结束信息
        if player.ap > 0:
            advanced_ui.print_colored(f"回合结束，剩余 {player.ap} AP", MessageType.INFO)
    
    def _end_round(self):
        """轮次结束"""
        # 触发天时事件
        if tianshi_system.should_draw_tianshi():
            event = tianshi_system.draw_tianshi()
            if event:
                tianshi_system.activate_tianshi(self.game_state)
                self.game_state.active_tianshi.append(event.name)
                self.game_state.global_events.append({
                    "type": "tianshi",
                    "name": event.name,
                    "description": event.flavor_text,
                    "turn": self.game_state.current_turn
                })
        
        # 清理过期的天时事件
        tianshi_system.tick_turn()
        
        # 触发全局进化事件
        if random.random() < 0.2:  # 20%概率
            evolving_cards_system.trigger_global_evolution_event()
        
        advanced_ui.print_colored(f"第 {self.game_state.current_turn + 1} 轮结束", MessageType.HIGHLIGHT)
        input("按回车键继续下一轮...")
    
    def _check_victory_conditions(self) -> bool:
        """检查胜利条件"""
        # 简化的胜利条件：道行达到20点或控制5个区域
        for player_name, player in self.game_state.players.items():
            if player.dao_xing >= 20:
                self._declare_victory(player_name, "道行胜利")
                return True
            
            controlled_zones = sum(1 for zone_data in self.game_state.zones.values() 
                                 if zone_data["controller"] == player_name)
            if controlled_zones >= 5:
                self._declare_victory(player_name, "区域控制胜利")
                return True
        
        # 检查阵营胜利条件
        faction_victory = faction_system.check_victory_conditions()
        if faction_victory:
            self._declare_victory(faction_victory, "阵营胜利")
            return True
        
        return False
    
    def _declare_victory(self, winner: str, victory_type: str):
        """宣布胜利"""
        advanced_ui.clear_screen()
        advanced_ui.display_mystical_message(
            f"游戏结束！\n\n"
            f"胜利者：{winner}\n"
            f"胜利方式：{victory_type}\n\n"
            f"恭喜获得最终胜利！",
            "游戏结束",
            MessageType.HIGHLIGHT
        )
        
        # 显示最终统计
        self._display_final_statistics()
        
        self.game_running = False
    
    def _display_final_statistics(self):
        """显示最终统计"""
        advanced_ui.print_colored("最终统计：", MessageType.HIGHLIGHT)
        
        for player_name, player in self.game_state.players.items():
            controlled_zones = sum(1 for zone_data in self.game_state.zones.values() 
                                 if zone_data["controller"] == player_name)
            
            advanced_ui.print_colored(
                f"{player_name}: 道行={player.dao_xing}, 控制区域={controlled_zones}, "
                f"声誉={player.reputation:.1f}, 成功率={player.successful_actions / max(1, player.successful_actions + player.failed_actions):.1%}",
                MessageType.INFO
            )
        
        # 显示牌库进化统计
        for player_name in self.game_state.player_order:
            stats = evolving_cards_system.player_decks[player_name].get_deck_statistics()
            advanced_ui.print_colored(
                f"{player_name} 牌库: 进化率={stats['evolution_rate']:.1%}, 进化次数={stats['deck_memory']['evolution_count']}",
                MessageType.MYSTICAL
            )

def main():
    """主函数"""
    game = UltimateTianJiBianGame()
    
    advanced_ui.display_title("天机变 - 终极版本")
    advanced_ui.display_mystical_message(
        "欢迎来到天机变的终极体验！\n\n"
        "这个版本包含了所有最新的深度改进：\n"
        "• 分段式彩色UI系统\n"
        "• 动态天时系统\n"
        "• 秘密身份与阵营对抗\n"
        "• 盟约与背叛机制\n"
        "• 爻辞光环系统\n"
        "• 演进卡牌系统\n"
        "• AI智能占卜系统\n\n"
        "准备好体验这场史诗级的策略之旅吗？",
        "游戏介绍"
    )
    
    # 获取玩家数量
    while True:
        try:
            num_players = int(input("\n请输入玩家数量 (2-4): "))
            if 2 <= num_players <= 4:
                break
            else:
                advanced_ui.print_colored("玩家数量必须在2-4之间", MessageType.ERROR)
        except ValueError:
            advanced_ui.print_colored("请输入有效的数字", MessageType.ERROR)
    
    # 获取玩家名称
    player_names = []
    for i in range(num_players):
        while True:
            name = input(f"请输入玩家 {i + 1} 的名称: ").strip()
            if name and name not in player_names:
                player_names.append(name)
                break
            elif name in player_names:
                advanced_ui.print_colored("名称已存在，请选择其他名称", MessageType.ERROR)
            else:
                advanced_ui.print_colored("名称不能为空", MessageType.ERROR)
    
    # 询问是否需要教程
    tutorial = input("\n是否需要教程模式？(y/n): ").lower() == 'y'
    
    # 开始游戏
    game.start_game(player_names, tutorial)

if __name__ == "__main__":
    main()