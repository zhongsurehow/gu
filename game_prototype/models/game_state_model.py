"""
游戏状态模型
管理整个游戏的状态、棋盘、回合等信息
"""

from typing import Dict, List, Optional, Any, Tuple, Set
from dataclasses import dataclass, field
from enum import Enum
import time
import json
from copy import deepcopy

from core.base_types import *
from core.interfaces import IGameState
from models.player_model import Player
from models.action_model import BaseGameAction
from utils.game_utils import *

class GamePhase(Enum):
    """游戏阶段"""
    SETUP = "setup"           # 设置阶段
    PLAYING = "playing"       # 游戏进行中
    PAUSED = "paused"         # 暂停
    ENDED = "ended"           # 游戏结束

class TurnPhase(Enum):
    """回合阶段"""
    START = "start"           # 回合开始
    ACTION = "action"         # 行动阶段
    RESOLUTION = "resolution" # 结算阶段
    END = "end"              # 回合结束

@dataclass
class BoardCell:
    """棋盘格子"""
    position: Position
    terrain_type: str = "平地"
    piece: Optional[str] = None
    owner: Optional[str] = None
    special_effects: List[str] = field(default_factory=list)
    wuxing_element: Optional[WuxingElement] = None
    bagua_type: Optional[BaguaType] = None
    
    def is_empty(self) -> bool:
        """检查格子是否为空"""
        return self.piece is None
    
    def can_place_piece(self, player_id: str) -> bool:
        """检查是否可以放置棋子"""
        return self.is_empty() or self.owner == player_id
    
    def get_terrain_bonus(self) -> Dict[str, float]:
        """获取地形加成"""
        terrain_bonuses = {
            "平地": {"movement": 1.0, "defense": 1.0},
            "山地": {"movement": 0.8, "defense": 1.5},
            "水域": {"movement": 1.2, "defense": 0.8},
            "森林": {"movement": 0.9, "defense": 1.2},
            "沙漠": {"movement": 0.7, "defense": 0.9}
        }
        return terrain_bonuses.get(self.terrain_type, {"movement": 1.0, "defense": 1.0})

@dataclass
class GameBoard:
    """游戏棋盘"""
    size: int
    cells: Dict[Tuple[int, int], BoardCell] = field(default_factory=dict)
    
    def __post_init__(self):
        """初始化棋盘"""
        if not self.cells:
            self._initialize_board()
    
    def _initialize_board(self) -> None:
        """初始化棋盘格子"""
        for x in range(self.size):
            for y in range(self.size):
                position = Position(x, y)
                cell = BoardCell(
                    position=position,
                    terrain_type=self._get_terrain_type(x, y),
                    wuxing_element=self._get_wuxing_element(x, y),
                    bagua_type=self._get_bagua_type(x, y)
                )
                self.cells[(x, y)] = cell
    
    def _get_terrain_type(self, x: int, y: int) -> str:
        """根据位置确定地形类型"""
        # 简单的地形生成逻辑
        center_x, center_y = self.size // 2, self.size // 2
        distance_from_center = ((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5
        
        if distance_from_center < self.size * 0.2:
            return "平地"
        elif distance_from_center < self.size * 0.4:
            return "森林" if (x + y) % 3 == 0 else "平地"
        elif distance_from_center < self.size * 0.6:
            return "山地" if (x + y) % 4 == 0 else "森林"
        else:
            return "沙漠" if (x + y) % 5 == 0 else "山地"
    
    def _get_wuxing_element(self, x: int, y: int) -> Optional[WuxingElement]:
        """根据位置确定五行元素"""
        # 基于位置的五行分布
        element_map = {
            0: WuxingElement.WOOD,
            1: WuxingElement.FIRE,
            2: WuxingElement.EARTH,
            3: WuxingElement.METAL,
            4: WuxingElement.WATER
        }
        return element_map.get((x + y) % 5)
    
    def _get_bagua_type(self, x: int, y: int) -> Optional[BaguaType]:
        """根据位置确定八卦类型"""
        # 基于位置的八卦分布
        bagua_list = list(BaguaType)
        return bagua_list[(x * self.size + y) % len(bagua_list)]
    
    def get_cell(self, x: int, y: int) -> Optional[BoardCell]:
        """获取指定位置的格子"""
        return self.cells.get((x, y))
    
    def get_cell_by_position(self, position: Position) -> Optional[BoardCell]:
        """根据位置对象获取格子"""
        return self.get_cell(position.x, position.y)
    
    def is_valid_position(self, x: int, y: int) -> bool:
        """检查位置是否有效"""
        return 0 <= x < self.size and 0 <= y < self.size
    
    def is_valid_position_obj(self, position: Position) -> bool:
        """检查位置对象是否有效"""
        return self.is_valid_position(position.x, position.y)
    
    def get_adjacent_cells(self, x: int, y: int) -> List[BoardCell]:
        """获取相邻格子"""
        adjacent = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                
                new_x, new_y = x + dx, y + dy
                if self.is_valid_position(new_x, new_y):
                    cell = self.get_cell(new_x, new_y)
                    if cell:
                        adjacent.append(cell)
        
        return adjacent
    
    def get_cells_in_range(self, center_x: int, center_y: int, range_val: int) -> List[BoardCell]:
        """获取指定范围内的格子"""
        cells = []
        for x in range(max(0, center_x - range_val), min(self.size, center_x + range_val + 1)):
            for y in range(max(0, center_y - range_val), min(self.size, center_y + range_val + 1)):
                if calculate_distance(Position(center_x, center_y), Position(x, y)) <= range_val:
                    cell = self.get_cell(x, y)
                    if cell:
                        cells.append(cell)
        
        return cells
    
    def place_piece(self, x: int, y: int, piece: str, owner: str) -> bool:
        """在指定位置放置棋子"""
        cell = self.get_cell(x, y)
        if not cell or not cell.can_place_piece(owner):
            return False
        
        cell.piece = piece
        cell.owner = owner
        return True
    
    def remove_piece(self, x: int, y: int) -> bool:
        """移除指定位置的棋子"""
        cell = self.get_cell(x, y)
        if not cell:
            return False
        
        cell.piece = None
        cell.owner = None
        return True
    
    def get_player_pieces(self, player_id: str) -> List[Tuple[Position, str]]:
        """获取玩家的所有棋子"""
        pieces = []
        for (x, y), cell in self.cells.items():
            if cell.owner == player_id and cell.piece:
                pieces.append((Position(x, y), cell.piece))
        
        return pieces
    
    def count_player_pieces(self, player_id: str) -> int:
        """统计玩家棋子数量"""
        return len(self.get_player_pieces(player_id))
    
    def get_control_areas(self) -> Dict[str, int]:
        """获取各玩家控制区域"""
        control_areas = {}
        for cell in self.cells.values():
            if cell.owner:
                control_areas[cell.owner] = control_areas.get(cell.owner, 0) + 1
        
        return control_areas
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "size": self.size,
            "cells": {
                f"{x},{y}": {
                    "position": {"x": cell.position.x, "y": cell.position.y},
                    "terrain_type": cell.terrain_type,
                    "piece": cell.piece,
                    "owner": cell.owner,
                    "special_effects": cell.special_effects,
                    "wuxing_element": cell.wuxing_element.value if cell.wuxing_element else None,
                    "bagua_type": cell.bagua_type.value if cell.bagua_type else None
                }
                for (x, y), cell in self.cells.items()
            }
        }

@dataclass
class TurnInfo:
    """回合信息"""
    turn_number: int
    current_player_id: str
    phase: TurnPhase
    start_time: float
    time_limit: float
    actions_performed: List[str] = field(default_factory=list)
    
    def get_remaining_time(self) -> float:
        """获取剩余时间"""
        elapsed = time.time() - self.start_time
        return max(0, self.time_limit - elapsed)
    
    def is_time_up(self) -> bool:
        """检查时间是否用完"""
        return self.get_remaining_time() <= 0
    
    def add_action(self, action_id: str) -> None:
        """添加行动记录"""
        self.actions_performed.append(action_id)

@dataclass
class GameHistory:
    """游戏历史"""
    actions: List[Dict[str, Any]] = field(default_factory=list)
    turns: List[TurnInfo] = field(default_factory=list)
    events: List[Dict[str, Any]] = field(default_factory=list)
    
    def add_action(self, action: BaseGameAction, result: ActionResult) -> None:
        """添加行动记录"""
        self.actions.append({
            "timestamp": time.time(),
            "action_id": action.get_action_id(),
            "player_id": action.get_player_id(),
            "action_type": action.action_type.value,
            "description": action.description,
            "success": result.success,
            "message": result.message,
            "data": result.data
        })
    
    def add_turn(self, turn_info: TurnInfo) -> None:
        """添加回合记录"""
        self.turns.append(deepcopy(turn_info))
    
    def add_event(self, event_type: str, description: str, data: Optional[Dict[str, Any]] = None) -> None:
        """添加事件记录"""
        self.events.append({
            "timestamp": time.time(),
            "event_type": event_type,
            "description": description,
            "data": data or {}
        })
    
    def get_player_actions(self, player_id: str) -> List[Dict[str, Any]]:
        """获取指定玩家的行动历史"""
        return [action for action in self.actions if action["player_id"] == player_id]
    
    def get_recent_actions(self, count: int = 10) -> List[Dict[str, Any]]:
        """获取最近的行动"""
        return self.actions[-count:] if len(self.actions) >= count else self.actions
    
    def get_turn_count(self) -> int:
        """获取回合数"""
        return len(self.turns)

class UltimateGameState(IGameState):
    """
    天机变游戏状态
    管理整个游戏的状态信息
    """
    
    def __init__(
        self,
        players: List[Player],
        board_size: int = 15,
        turn_time_limit: float = 60.0
    ):
        self.players: Dict[str, Player] = {player.player_id: player for player in players}
        self.board = GameBoard(board_size)
        self.game_phase = GamePhase.SETUP
        self.turn_time_limit = turn_time_limit
        
        # 回合信息
        self.current_turn: Optional[TurnInfo] = None
        self.turn_order: List[str] = [player.player_id for player in players]
        self.current_player_index = 0
        
        # 游戏历史
        self.history = GameHistory()
        
        # 游戏统计
        self.start_time = time.time()
        self.end_time: Optional[float] = None
        self.winner: Optional[str] = None
        
        # 游戏配置
        self.config = {
            "max_turns": 100,
            "victory_conditions": ["control_majority", "cultivation_mastery", "elimination"],
            "special_rules": []
        }
        
        # 初始化
        self._initialize_player_positions()
    
    def _initialize_player_positions(self) -> None:
        """初始化玩家位置"""
        player_count = len(self.players)
        board_size = self.board.size
        
        # 将玩家分布在棋盘边缘
        positions = []
        if player_count == 2:
            positions = [
                Position(0, board_size // 2),
                Position(board_size - 1, board_size // 2)
            ]
        elif player_count == 3:
            positions = [
                Position(0, 0),
                Position(board_size - 1, 0),
                Position(board_size // 2, board_size - 1)
            ]
        elif player_count == 4:
            positions = [
                Position(0, 0),
                Position(board_size - 1, 0),
                Position(0, board_size - 1),
                Position(board_size - 1, board_size - 1)
            ]
        else:
            # 更多玩家的情况，均匀分布在边缘
            for i, player_id in enumerate(self.turn_order):
                angle = 2 * 3.14159 * i / player_count
                x = int(board_size // 2 + (board_size // 3) * math.cos(angle))
                y = int(board_size // 2 + (board_size // 3) * math.sin(angle))
                x = max(0, min(board_size - 1, x))
                y = max(0, min(board_size - 1, y))
                positions.append(Position(x, y))
        
        # 设置玩家初始位置
        for i, player_id in enumerate(self.turn_order):
            if i < len(positions):
                self.players[player_id].state.current_position = positions[i]
    
    def start_game(self) -> None:
        """开始游戏"""
        if self.game_phase != GamePhase.SETUP:
            raise GameStateException("游戏已经开始")
        
        self.game_phase = GamePhase.PLAYING
        self.start_time = time.time()
        
        # 开始第一回合
        self.start_new_turn()
        
        self.history.add_event("game_started", "游戏开始", {
            "players": list(self.players.keys()),
            "board_size": self.board.size
        })
    
    def start_new_turn(self) -> None:
        """开始新回合"""
        if self.game_phase != GamePhase.PLAYING:
            return
        
        # 结束当前回合
        if self.current_turn:
            self.current_turn.phase = TurnPhase.END
            self.history.add_turn(self.current_turn)
        
        # 切换到下一个玩家
        self.current_player_index = (self.current_player_index + 1) % len(self.turn_order)
        current_player_id = self.turn_order[self.current_player_index]
        
        # 创建新回合
        turn_number = self.history.get_turn_count() + 1
        self.current_turn = TurnInfo(
            turn_number=turn_number,
            current_player_id=current_player_id,
            phase=TurnPhase.START,
            start_time=time.time(),
            time_limit=self.turn_time_limit
        )
        
        self.history.add_event("turn_started", f"回合 {turn_number} 开始", {
            "turn_number": turn_number,
            "current_player": current_player_id
        })
    
    def end_turn(self) -> None:
        """结束当前回合"""
        if not self.current_turn:
            return
        
        self.current_turn.phase = TurnPhase.END
        
        # 检查胜利条件
        winner = self.check_victory_conditions()
        if winner:
            self.end_game(winner)
        else:
            # 检查是否达到最大回合数
            if self.history.get_turn_count() >= self.config["max_turns"]:
                self.end_game()  # 平局
            else:
                self.start_new_turn()
    
    def end_game(self, winner: Optional[str] = None) -> None:
        """结束游戏"""
        self.game_phase = GamePhase.ENDED
        self.end_time = time.time()
        self.winner = winner
        
        if self.current_turn:
            self.current_turn.phase = TurnPhase.END
            self.history.add_turn(self.current_turn)
        
        self.history.add_event("game_ended", "游戏结束", {
            "winner": winner,
            "duration": self.get_game_duration()
        })
    
    def pause_game(self) -> None:
        """暂停游戏"""
        if self.game_phase == GamePhase.PLAYING:
            self.game_phase = GamePhase.PAUSED
            self.history.add_event("game_paused", "游戏暂停")
    
    def resume_game(self) -> None:
        """恢复游戏"""
        if self.game_phase == GamePhase.PAUSED:
            self.game_phase = GamePhase.PLAYING
            self.history.add_event("game_resumed", "游戏恢复")
    
    def get_current_player(self) -> Optional[Player]:
        """获取当前玩家"""
        if not self.current_turn:
            return None
        return self.players.get(self.current_turn.current_player_id)
    
    def get_player(self, player_id: str) -> Optional[Player]:
        """获取指定玩家"""
        return self.players.get(player_id)
    
    def get_all_players(self) -> List[Player]:
        """获取所有玩家"""
        return list(self.players.values())
    
    def get_board_state(self) -> Dict[str, Any]:
        """获取棋盘状态"""
        return self.board.to_dict()
    
    def get_game_duration(self) -> float:
        """获取游戏时长"""
        end_time = self.end_time or time.time()
        return end_time - self.start_time
    
    def check_victory_conditions(self) -> Optional[str]:
        """检查胜利条件"""
        for condition in self.config["victory_conditions"]:
            winner = self._check_specific_victory_condition(condition)
            if winner:
                return winner
        
        return None
    
    def _check_specific_victory_condition(self, condition: str) -> Optional[str]:
        """检查特定胜利条件"""
        if condition == "control_majority":
            return self._check_control_majority()
        elif condition == "cultivation_mastery":
            return self._check_cultivation_mastery()
        elif condition == "elimination":
            return self._check_elimination()
        
        return None
    
    def _check_control_majority(self) -> Optional[str]:
        """检查控制区域胜利条件"""
        control_areas = self.board.get_control_areas()
        total_cells = self.board.size * self.board.size
        
        for player_id, controlled in control_areas.items():
            if controlled > total_cells * 0.6:  # 控制60%以上区域
                return player_id
        
        return None
    
    def _check_cultivation_mastery(self) -> Optional[str]:
        """检查修为胜利条件"""
        for player in self.players.values():
            if player.cultivation_realm.value >= 8:  # 达到最高境界
                return player.player_id
        
        return None
    
    def _check_elimination(self) -> Optional[str]:
        """检查淘汰胜利条件"""
        active_players = [p for p in self.players.values() if p.state.is_active]
        if len(active_players) == 1:
            return active_players[0].player_id
        
        return None
    
    def get_game_statistics(self) -> Dict[str, Any]:
        """获取游戏统计信息"""
        stats = {
            "game_duration": self.get_game_duration(),
            "total_turns": self.history.get_turn_count(),
            "total_actions": len(self.history.actions),
            "player_stats": {}
        }
        
        for player in self.players.values():
            player_actions = self.history.get_player_actions(player.player_id)
            stats["player_stats"][player.player_id] = {
                "name": player.name,
                "total_actions": len(player_actions),
                "successful_actions": sum(1 for a in player_actions if a["success"]),
                "controlled_cells": self.board.count_player_pieces(player.player_id),
                "cultivation_realm": player.cultivation_realm.value,
                "resources": {rt.value: amount for rt, amount in player.resources.items()}
            }
        
        return stats
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "players": {pid: self._serialize_player(player) for pid, player in self.players.items()},
            "board": self.board.to_dict(),
            "game_phase": self.game_phase.value,
            "current_turn": {
                "turn_number": self.current_turn.turn_number,
                "current_player_id": self.current_turn.current_player_id,
                "phase": self.current_turn.phase.value,
                "remaining_time": self.current_turn.get_remaining_time()
            } if self.current_turn else None,
            "turn_order": self.turn_order,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "winner": self.winner,
            "statistics": self.get_game_statistics()
        }
    
    def _serialize_player(self, player: Player) -> Dict[str, Any]:
        """序列化玩家数据"""
        return {
            "id": player.player_id,
            "name": player.name,
            "type": player.player_type.value,
            "avatar": player.avatar,
            "resources": {rt.value: amount for rt, amount in player.resources.items()},
            "cultivation_realm": player.cultivation_realm.value,
            "position": {
                "x": player.state.current_position.x,
                "y": player.state.current_position.y
            },
            "is_active": player.state.is_active,
            "yin": player.yin,
            "yang": player.yang,
            "wuxing_mastery": {elem.value: value for elem, value in player.wuxing_mastery.items()},
            "bagua_affinity": {bagua.value: value for bagua, value in player.bagua_affinity.items()}
        }
    
    # IGameState 接口实现
    def get_current_phase(self) -> str:
        """获取当前游戏阶段"""
        return self.game_phase.value
    
    def get_current_turn(self) -> int:
        """获取当前回合数"""
        return self.current_turn.turn_number if self.current_turn else 0
    
    def is_game_over(self) -> bool:
        """检查游戏是否结束"""
        return self.game_phase == GamePhase.ENDED
    
    def get_winner(self) -> Optional[str]:
        """获取获胜者"""
        return self.winner

# ==================== 便捷函数 ====================

def create_game_state(
    players: List[Player],
    board_size: int = 15,
    turn_time_limit: float = 60.0,
    config: Optional[Dict[str, Any]] = None
) -> UltimateGameState:
    """
    创建游戏状态
    
    Args:
        players: 玩家列表
        board_size: 棋盘大小
        turn_time_limit: 回合时间限制
        config: 游戏配置
        
    Returns:
        游戏状态对象
    """
    game_state = UltimateGameState(players, board_size, turn_time_limit)
    
    if config:
        game_state.config.update(config)
    
    return game_state

def load_game_state_from_dict(data: Dict[str, Any]) -> UltimateGameState:
    """
    从字典加载游戏状态
    
    Args:
        data: 游戏状态数据
        
    Returns:
        游戏状态对象
    """
    # 这里需要实现完整的反序列化逻辑
    # 由于复杂性，这里只是一个框架
    pass

def save_game_state_to_file(game_state: UltimateGameState, file_path: str) -> None:
    """
    保存游戏状态到文件
    
    Args:
        game_state: 游戏状态
        file_path: 文件路径
    """
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(game_state.to_dict(), f, ensure_ascii=False, indent=2)

def load_game_state_from_file(file_path: str) -> UltimateGameState:
    """
    从文件加载游戏状态
    
    Args:
        file_path: 文件路径
        
    Returns:
        游戏状态对象
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    return load_game_state_from_dict(data)