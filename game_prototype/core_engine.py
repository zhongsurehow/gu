"""
天机变游戏核心引擎
整合游戏状态管理、规则验证、回合控制等核心功能
"""

from typing import Dict, List, Optional, Tuple, Any
from enum import Enum
import logging
from dataclasses import dataclass

from game_state import GameState, Player, Zone, BonusType, Modifiers
from card_base import GuaCard, YaoCiTask
from yijing_mechanics import YinYangBalance, WuXing, WuXingCycle, YinYang
from config_manager import get_config

class ActionType(Enum):
    """游戏动作类型"""
    PLAY_CARD = "play_card"
    MOVE = "move"
    STUDY = "study"
    MEDITATE = "meditate"
    TASK = "task"
    PASS = "pass"
    DIVINE = "divine"
    TRANSFORM = "transform"

class GamePhase(Enum):
    """游戏阶段"""
    SETUP = "setup"
    MAIN_GAME = "main_game"
    END_GAME = "end_game"
    FINISHED = "finished"

@dataclass
class ActionResult:
    """动作执行结果"""
    success: bool
    message: str
    effects: Dict[str, Any] = None
    next_phase: Optional[GamePhase] = None

class CoreGameEngine:
    """核心游戏引擎"""
    
    def __init__(self, game_state: GameState):
        self.game_state = game_state
        self.current_phase = GamePhase.SETUP
        self.action_history: List[Dict] = []
        self.logger = logging.getLogger(__name__)
        
        # 游戏配置
        self.max_turns = get_config("game_rules.max_turns", 20)
        self.victory_conditions = get_config("game_rules.victory_conditions", {})
        
    def get_current_player(self) -> Player:
        """获取当前玩家"""
        return self.game_state.players[self.game_state.current_player_index]
    
    def validate_action(self, action_type: ActionType, **kwargs) -> Tuple[bool, str]:
        """验证动作是否合法"""
        player = self.get_current_player()
        
        if action_type == ActionType.PLAY_CARD:
            return self._validate_play_card(player, kwargs.get('card_index'), kwargs.get('zone'))
        elif action_type == ActionType.MOVE:
            return self._validate_move(player, kwargs.get('target_zone'))
        elif action_type == ActionType.STUDY:
            return self._validate_study(player)
        elif action_type == ActionType.MEDITATE:
            return self._validate_meditate(player)
        elif action_type == ActionType.TASK:
            return self._validate_task(player, kwargs.get('task_index'))
        elif action_type == ActionType.DIVINE:
            return self._validate_divine(player)
        elif action_type == ActionType.TRANSFORM:
            return self._validate_transform(player, kwargs.get('source'), kwargs.get('target'))
        else:
            return True, "动作有效"
    
    def execute_action(self, action_type: ActionType, **kwargs) -> ActionResult:
        """执行游戏动作"""
        # 验证动作
        is_valid, message = self.validate_action(action_type, **kwargs)
        if not is_valid:
            return ActionResult(False, message)
        
        # 记录动作
        self._record_action(action_type, kwargs)
        
        # 执行动作
        try:
            if action_type == ActionType.PLAY_CARD:
                return self._execute_play_card(**kwargs)
            elif action_type == ActionType.MOVE:
                return self._execute_move(**kwargs)
            elif action_type == ActionType.STUDY:
                return self._execute_study(**kwargs)
            elif action_type == ActionType.MEDITATE:
                return self._execute_meditate(**kwargs)
            elif action_type == ActionType.TASK:
                return self._execute_task(**kwargs)
            elif action_type == ActionType.PASS:
                return self._execute_pass(**kwargs)
            elif action_type == ActionType.DIVINE:
                return self._execute_divine(**kwargs)
            elif action_type == ActionType.TRANSFORM:
                return self._execute_transform(**kwargs)
            else:
                return ActionResult(False, "未知动作类型")
                
        except Exception as e:
            self.logger.error(f"执行动作时发生错误: {e}")
            return ActionResult(False, f"执行失败: {str(e)}")
    
    def advance_turn(self) -> ActionResult:
        """推进回合"""
        # 检查胜利条件
        winner = self.check_victory_conditions()
        if winner:
            self.current_phase = GamePhase.FINISHED
            return ActionResult(True, f"游戏结束！{winner.name} 获胜！", 
                              next_phase=GamePhase.FINISHED)
        
        # 检查最大回合数
        if self.game_state.turn >= self.max_turns:
            self.current_phase = GamePhase.END_GAME
            return ActionResult(True, "达到最大回合数，进入结算阶段", 
                              next_phase=GamePhase.END_GAME)
        
        # 切换到下一个玩家
        self.game_state.current_player_index = (
            self.game_state.current_player_index + 1
        ) % len(self.game_state.players)
        
        # 如果回到第一个玩家，增加回合数
        if self.game_state.current_player_index == 0:
            self.game_state.turn += 1
            self._process_turn_effects()
        
        # 处理玩家回合开始效果
        self._process_player_turn_start()
        
        return ActionResult(True, f"轮到 {self.get_current_player().name}")
    
    def check_victory_conditions(self) -> Optional[Player]:
        """检查胜利条件"""
        for player in self.game_state.players:
            # 道行胜利
            if player.dao_xing >= self.victory_conditions.get("dao_xing_threshold", 20):
                return player
            
            # 诚意胜利
            if player.cheng_yi >= self.victory_conditions.get("cheng_yi_threshold", 15):
                return player
            
            # 控制区域胜利
            controlled_zones = self._count_controlled_zones(player)
            if controlled_zones >= self.victory_conditions.get("zone_control_threshold", 5):
                return player
        
        return None
    
    def get_game_status(self) -> Dict[str, Any]:
        """获取游戏状态摘要"""
        current_player = self.get_current_player()
        
        return {
            "phase": self.current_phase.value,
            "turn": self.game_state.turn,
            "current_player": current_player.name,
            "players": [
                {
                    "name": p.name,
                    "dao_xing": p.dao_xing,
                    "cheng_yi": p.cheng_yi,
                    "qi": p.qi,
                    "position": p.position.value,
                    "hand_size": len(p.hand),
                    "yin_yang_balance": p.yin_yang_balance.balance_ratio,
                    "controlled_zones": self._count_controlled_zones(p)
                }
                for p in self.game_state.players
            ],
            "board_state": self._get_board_summary()
        }
    
    # 私有方法 - 动作验证
    def _validate_play_card(self, player: Player, card_index: int, zone: str) -> Tuple[bool, str]:
        """验证打牌动作"""
        if card_index is None or card_index < 0 or card_index >= len(player.hand):
            return False, "无效的卡牌索引"
        
        if zone not in self.game_state.board.gua_zones:
            return False, "无效的区域"
        
        card = player.hand[card_index]
        if zone not in card.associated_guas:
            return False, f"卡牌 {card.name} 不能放置在 {zone} 区域"
        
        return True, "可以打牌"
    
    def _validate_move(self, player: Player, target_zone: str) -> Tuple[bool, str]:
        """验证移动动作"""
        try:
            target = Zone(target_zone)
        except ValueError:
            return False, "无效的目标位置"
        
        if player.position == target:
            return False, "已经在目标位置"
        
        return True, "可以移动"
    
    def _validate_study(self, player: Player) -> Tuple[bool, str]:
        """验证学习动作"""
        if player.qi < 2:
            return False, "气不足，无法学习"
        
        return True, "可以学习"
    
    def _validate_meditate(self, player: Player) -> Tuple[bool, str]:
        """验证冥想动作"""
        return True, "可以冥想"
    
    def _validate_task(self, player: Player, task_index: int) -> Tuple[bool, str]:
        """验证任务动作"""
        if not player.current_task_card:
            return False, "没有当前任务卡"
        
        if task_index < 0 or task_index >= 6:
            return False, "无效的任务索引"
        
        return True, "可以执行任务"
    
    def _validate_divine(self, player: Player) -> Tuple[bool, str]:
        """验证占卜动作"""
        if player.qi < 3:
            return False, "气不足，无法占卜"
        
        return True, "可以占卜"
    
    def _validate_transform(self, player: Player, source: str, target: str) -> Tuple[bool, str]:
        """验证变卦动作"""
        if player.dao_xing < 5:
            return False, "道行不足，无法变卦"
        
        return True, "可以变卦"
    
    # 私有方法 - 动作执行
    def _execute_play_card(self, card_index: int, zone: str, **kwargs) -> ActionResult:
        """执行打牌动作"""
        player = self.get_current_player()
        card = player.hand.pop(card_index)
        
        # 放置卡牌到区域
        zone_data = self.game_state.board.gua_zones[zone]
        if player.name not in zone_data["markers"]:
            zone_data["markers"][player.name] = 0
        zone_data["markers"][player.name] += 1
        
        # 检查区域控制
        if zone_data["markers"][player.name] > self.game_state.board.base_limit // 2:
            zone_data["controller"] = player.name
        
        # 设置当前任务卡
        player.current_task_card = card
        
        # 易经效果
        self._apply_yijing_effects(player, card, zone)
        
        return ActionResult(True, f"在 {zone} 区域打出了 {card.name}")
    
    def _execute_move(self, target_zone: str, **kwargs) -> ActionResult:
        """执行移动动作"""
        player = self.get_current_player()
        old_position = player.position
        player.position = Zone(target_zone)
        
        # 更新棋盘位置
        self.game_state.board.player_positions[player.name] = player.position
        
        # 位置效果
        self._apply_position_effects(player, old_position, player.position)
        
        return ActionResult(True, f"从 {old_position.value} 移动到 {target_zone}")
    
    def _execute_study(self, **kwargs) -> ActionResult:
        """执行学习动作"""
        player = self.get_current_player()
        
        # 消耗气
        player.qi -= 2
        
        # 增加道行
        dao_gain = 1 + player.yin_yang_balance.get_balance_bonus()
        player.dao_xing += dao_gain
        
        # 抽卡
        cards_to_draw = 2  # 基础抽卡数
        # TODO: 实现抽卡逻辑
        
        return ActionResult(True, f"学习获得 {dao_gain} 点道行")
    
    def _execute_meditate(self, **kwargs) -> ActionResult:
        """执行冥想动作"""
        player = self.get_current_player()
        
        # 调节阴阳平衡
        if player.yin_yang_balance.yin_points > player.yin_yang_balance.yang_points:
            player.yin_yang_balance.yang_points += 1
            balance_type = "阳"
        else:
            player.yin_yang_balance.yin_points += 1
            balance_type = "阴"
        
        # 恢复气
        qi_gain = 2
        player.qi += qi_gain
        
        return ActionResult(True, f"冥想增加了 {balance_type} 属性，恢复 {qi_gain} 点气")
    
    def _execute_task(self, task_index: int, **kwargs) -> ActionResult:
        """执行任务动作"""
        player = self.get_current_player()
        task = player.current_task_card.tasks[task_index]
        
        # 获得奖励
        player.dao_xing += task.reward_dao_xing
        player.cheng_yi += task.reward_cheng_yi
        
        return ActionResult(True, f"完成任务 {task.name}，获得奖励")
    
    def _execute_pass(self, **kwargs) -> ActionResult:
        """执行跳过动作"""
        return ActionResult(True, "跳过回合")
    
    def _execute_divine(self, **kwargs) -> ActionResult:
        """执行占卜动作"""
        player = self.get_current_player()
        player.qi -= 3
        
        # TODO: 实现占卜逻辑
        
        return ActionResult(True, "进行了占卜")
    
    def _execute_transform(self, source: str, target: str, **kwargs) -> ActionResult:
        """执行变卦动作"""
        player = self.get_current_player()
        player.dao_xing -= 2  # 消耗道行
        
        # TODO: 实现变卦逻辑
        player.transformation_history.append(f"{source} -> {target}")
        
        return ActionResult(True, f"成功变卦：{source} -> {target}")
    
    # 私有方法 - 辅助功能
    def _record_action(self, action_type: ActionType, kwargs: Dict):
        """记录动作历史"""
        self.action_history.append({
            "turn": self.game_state.turn,
            "player": self.get_current_player().name,
            "action": action_type.value,
            "params": kwargs
        })
    
    def _apply_yijing_effects(self, player: Player, card: GuaCard, zone: str):
        """应用易经效果"""
        # 根据卦象和位置应用效果
        # TODO: 实现具体的易经效果逻辑
        pass
    
    def _apply_position_effects(self, player: Player, old_pos: Zone, new_pos: Zone):
        """应用位置效果"""
        # 根据三才位置应用效果
        if new_pos == Zone.TIAN:
            player.qi += 1  # 天位增加气
        elif new_pos == Zone.REN:
            player.cheng_yi += 1  # 人位增加诚意
        elif new_pos == Zone.DI:
            player.dao_xing += 1  # 地位增加道行
    
    def _process_turn_effects(self):
        """处理回合效果"""
        # 处理全局回合效果
        for player in self.game_state.players:
            # 自然恢复
            player.qi = min(player.qi + 1, 10)  # 最大气值限制
    
    def _process_player_turn_start(self):
        """处理玩家回合开始效果"""
        player = self.get_current_player()
        # 重置回合状态
        player.placed_influence_this_turn = False
    
    def _count_controlled_zones(self, player: Player) -> int:
        """计算玩家控制的区域数量"""
        count = 0
        for zone_data in self.game_state.board.gua_zones.values():
            if zone_data["controller"] == player.name:
                count += 1
        return count
    
    def _get_board_summary(self) -> Dict[str, Any]:
        """获取棋盘状态摘要"""
        return {
            zone: {
                "controller": data["controller"],
                "markers": dict(data["markers"])
            }
            for zone, data in self.game_state.board.gua_zones.items()
        }