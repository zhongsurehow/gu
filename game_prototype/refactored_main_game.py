"""
天机变游戏 - 重构版本
应用新的架构设计，提供更好的代码组织和可维护性
"""

from typing import Dict, List, Optional, Tuple, Any, Union
import asyncio
from dataclasses import dataclass, field
import json
import time

# 导入核心模块
from core.game_engine import GameEngine, GameEngineConfig
from core.event_system import EventBus, GameEvent
from core.logging_system import get_logger
from core.base_types import *
from core.constants import *
from core.exceptions import *
from core.interfaces import *

# 导入系统模块
from systems.config_system import ConfigManager, GameConfigData

# 导入模型
from models.player_model import Player, PlayerStats, PlayerState

# 导入工具
from utils.game_utils import *
from utils.yixue_utils import *
from utils.validation_utils import *

# 设置日志
logger = get_logger(__name__)

@dataclass
class GameSession:
    """游戏会话"""
    session_id: str
    players: List[Player]
    game_engine: GameEngine
    config: GameConfigData
    start_time: float
    end_time: Optional[float] = None
    winner: Optional[Player] = None
    
    def get_duration(self) -> float:
        """获取游戏时长"""
        end = self.end_time or time.time()
        return end - self.start_time
    
    def is_active(self) -> bool:
        """检查游戏是否活跃"""
        return self.end_time is None

class TianJiBianGame(IGameSystem):
    """
    天机变游戏主类
    重构后的游戏系统，采用事件驱动架构
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        初始化游戏
        
        Args:
            config_path: 配置文件路径
        """
        self.logger = get_logger(self.__class__.__name__)
        self.config_manager = ConfigManager()
        self.event_bus = EventBus()
        
        # 加载配置
        if config_path:
            self.config_manager.load_from_file(config_path)
        
        self.config = self.config_manager.get_config()
        
        # 初始化游戏引擎
        engine_config = GameEngineConfig(
            max_players=self.config.basic.max_players,
            turn_time_limit=self.config.basic.turn_time_limit,
            board_size=self.config.basic.board_size,
            enable_ai=self.config.ai.enabled,
            debug_mode=self.config.basic.debug_mode
        )
        
        self.game_engine = GameEngine(engine_config, self.event_bus)
        
        # 游戏状态
        self.current_session: Optional[GameSession] = None
        self.sessions_history: List[GameSession] = []
        
        # 注册事件处理器
        self._register_event_handlers()
        
        self.logger.info("天机变游戏系统初始化完成")
    
    def _register_event_handlers(self) -> None:
        """注册事件处理器"""
        self.event_bus.subscribe(GameEventType.GAME_STARTED, self._on_game_started)
        self.event_bus.subscribe(GameEventType.GAME_ENDED, self._on_game_ended)
        self.event_bus.subscribe(GameEventType.PLAYER_JOINED, self._on_player_joined)
        self.event_bus.subscribe(GameEventType.PLAYER_LEFT, self._on_player_left)
        self.event_bus.subscribe(GameEventType.TURN_STARTED, self._on_turn_started)
        self.event_bus.subscribe(GameEventType.TURN_ENDED, self._on_turn_ended)
        self.event_bus.subscribe(GameEventType.ACTION_PERFORMED, self._on_action_performed)
        self.event_bus.subscribe(GameEventType.ERROR_OCCURRED, self._on_error_occurred)
    
    async def create_game_session(
        self, 
        session_id: str,
        player_configs: List[Dict[str, Any]]
    ) -> GameSession:
        """
        创建游戏会话
        
        Args:
            session_id: 会话ID
            player_configs: 玩家配置列表
            
        Returns:
            游戏会话
            
        Raises:
            GameException: 创建失败时
        """
        try:
            self.logger.info(f"创建游戏会话: {session_id}")
            
            # 验证玩家配置
            if len(player_configs) < 2:
                raise GameLogicException("至少需要2个玩家")
            
            if len(player_configs) > self.config.basic.max_players:
                raise GameLogicException(f"玩家数量不能超过{self.config.basic.max_players}")
            
            # 创建玩家
            players = []
            for i, player_config in enumerate(player_configs):
                player = self._create_player(player_config, i)
                players.append(player)
            
            # 创建游戏会话
            session = GameSession(
                session_id=session_id,
                players=players,
                game_engine=self.game_engine,
                config=self.config,
                start_time=time.time()
            )
            
            self.current_session = session
            self.sessions_history.append(session)
            
            # 初始化游戏引擎
            await self.game_engine.initialize_game(players)
            
            self.logger.info(f"游戏会话创建成功: {session_id}")
            return session
            
        except Exception as e:
            self.logger.error(f"创建游戏会话失败: {e}")
            raise GameException(f"创建游戏会话失败: {e}")
    
    def _create_player(self, player_config: Dict[str, Any], index: int) -> Player:
        """
        创建玩家
        
        Args:
            player_config: 玩家配置
            index: 玩家索引
            
        Returns:
            玩家对象
        """
        # 验证玩家配置
        validation_result = validate_player_data(player_config)
        if not validation_result.is_valid:
            raise ValidationException(f"玩家配置无效: {', '.join(validation_result.errors)}")
        
        # 创建玩家统计
        stats = PlayerStats(
            games_played=0,
            games_won=0,
            total_actions=0,
            successful_actions=0,
            average_game_duration=0.0
        )
        
        # 创建玩家状态
        state = PlayerState(
            is_online=True,
            is_active=True,
            current_position=Position(index, index),  # 初始位置
            last_action_time=time.time()
        )
        
        # 获取初始资源
        initial_resources = self.config.basic.initial_resources.copy()
        
        # 创建玩家
        player = Player(
            player_id=f"player_{index}",
            name=player_config.get("name", f"玩家{index + 1}"),
            player_type=PlayerType(player_config.get("type", "human")),
            avatar=player_config.get("avatar", "默认"),
            resources=initial_resources,
            cultivation_realm=CultivationRealm.MORTAL,
            yin=self.config.yixue.initial_yin,
            yang=self.config.yixue.initial_yang,
            wuxing_mastery={elem: 1 for elem in WuxingElement},
            bagua_affinity={bagua: 1 for bagua in BaguaType},
            stats=stats,
            state=state
        )
        
        return player
    
    async def start_game(self) -> None:
        """开始游戏"""
        if not self.current_session:
            raise GameStateException("没有活跃的游戏会话")
        
        try:
            self.logger.info("开始游戏")
            await self.game_engine.start_game()
            
        except Exception as e:
            self.logger.error(f"开始游戏失败: {e}")
            raise GameException(f"开始游戏失败: {e}")
    
    async def end_game(self, winner: Optional[Player] = None) -> None:
        """结束游戏"""
        if not self.current_session:
            return
        
        try:
            self.logger.info("结束游戏")
            
            self.current_session.end_time = time.time()
            self.current_session.winner = winner
            
            await self.game_engine.end_game()
            
            # 更新玩家统计
            for player in self.current_session.players:
                player.stats.games_played += 1
                if player == winner:
                    player.stats.games_won += 1
                
                duration = self.current_session.get_duration()
                player.stats.average_game_duration = (
                    (player.stats.average_game_duration * (player.stats.games_played - 1) + duration) 
                    / player.stats.games_played
                )
            
            self.current_session = None
            
        except Exception as e:
            self.logger.error(f"结束游戏失败: {e}")
            raise GameException(f"结束游戏失败: {e}")
    
    async def perform_player_action(
        self, 
        player: Player, 
        action: IGameAction
    ) -> ActionResult:
        """
        执行玩家行动
        
        Args:
            player: 玩家
            action: 行动
            
        Returns:
            行动结果
        """
        if not self.current_session:
            raise GameStateException("没有活跃的游戏会话")
        
        try:
            self.logger.debug(f"玩家 {player.name} 执行行动: {action.action_type}")
            
            # 验证行动
            validation_result = self._validate_action(player, action)
            if not validation_result.is_valid:
                return ActionResult(
                    success=False,
                    message=f"行动验证失败: {', '.join(validation_result.errors)}",
                    data={}
                )
            
            # 执行行动
            result = await self.game_engine.execute_action(player, action)
            
            # 更新玩家统计
            player.stats.total_actions += 1
            if result.success:
                player.stats.successful_actions += 1
            
            player.state.last_action_time = time.time()
            
            return result
            
        except Exception as e:
            self.logger.error(f"执行玩家行动失败: {e}")
            return ActionResult(
                success=False,
                message=f"执行行动失败: {e}",
                data={}
            )
    
    def _validate_action(self, player: Player, action: IGameAction) -> ValidationResult:
        """验证玩家行动"""
        result = create_validation_result()
        
        # 检查玩家状态
        if not player.state.is_active:
            result.add_error("玩家未激活")
        
        # 检查资源
        if hasattr(action, 'cost') and action.cost:
            cost_result = validate_resource_cost(player.resources, action.cost)
            result.merge(cost_result)
        
        # 检查位置（如果是移动行动）
        if action.action_type == ActionType.MOVE:
            if hasattr(action, 'target_position'):
                move_result = validate_move_action(
                    player.state.current_position,
                    action.target_position,
                    self.config.basic.board_size
                )
                result.merge(move_result)
        
        return result
    
    def get_game_state(self) -> Optional[Dict[str, Any]]:
        """获取游戏状态"""
        if not self.current_session:
            return None
        
        return {
            "session_id": self.current_session.session_id,
            "players": [self._serialize_player(player) for player in self.current_session.players],
            "game_phase": self.game_engine.get_current_phase(),
            "current_turn": self.game_engine.get_current_turn(),
            "board_state": self.game_engine.get_board_state(),
            "start_time": self.current_session.start_time,
            "duration": self.current_session.get_duration()
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
            "yin": player.yin,
            "yang": player.yang,
            "wuxing_mastery": {elem.value: value for elem, value in player.wuxing_mastery.items()},
            "bagua_affinity": {bagua.value: value for bagua, value in player.bagua_affinity.items()},
            "position": {
                "x": player.state.current_position.x,
                "y": player.state.current_position.y
            },
            "is_active": player.state.is_active,
            "stats": {
                "games_played": player.stats.games_played,
                "games_won": player.stats.games_won,
                "win_rate": player.get_win_rate(),
                "total_actions": player.stats.total_actions,
                "success_rate": player.get_success_rate()
            }
        }
    
    def get_player_recommendations(self, player: Player) -> List[str]:
        """获取玩家建议"""
        recommendations = []
        
        # 易学建议
        yixue_recommendations = get_yixue_recommendations(
            player.yin, player.yang,
            player.wuxing_mastery,
            player.bagua_affinity
        )
        recommendations.extend(yixue_recommendations)
        
        # 资源建议
        if player.resources.get(ResourceType.CULTURE, 0) < 50:
            recommendations.append("建议增加文化资源，提升修为境界")
        
        if player.resources.get(ResourceType.WISDOM, 0) < 20:
            recommendations.append("建议积累智慧资源，用于高级行动")
        
        # 修为建议
        progress = calculate_cultivation_progress(
            player.cultivation_realm,
            player.yin, player.yang,
            player.wuxing_mastery,
            player.bagua_affinity,
            player.resources.get(ResourceType.CULTURE, 0)
        )
        
        if progress > 0.8:
            recommendations.append("修为进度良好，可尝试突破境界")
        elif progress < 0.3:
            recommendations.append("建议加强修炼，提升各项指标")
        
        return recommendations
    
    def save_game_state(self, file_path: str) -> None:
        """保存游戏状态"""
        if not self.current_session:
            raise GameStateException("没有活跃的游戏会话")
        
        try:
            game_state = self.get_game_state()
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(game_state, f, ensure_ascii=False, indent=2)
            
            self.logger.info(f"游戏状态已保存到: {file_path}")
            
        except Exception as e:
            self.logger.error(f"保存游戏状态失败: {e}")
            raise GameException(f"保存游戏状态失败: {e}")
    
    def load_game_state(self, file_path: str) -> None:
        """加载游戏状态"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                game_state = json.load(f)
            
            # 这里需要实现状态恢复逻辑
            # 由于复杂性，这里只是一个框架
            self.logger.info(f"游戏状态已从 {file_path} 加载")
            
        except Exception as e:
            self.logger.error(f"加载游戏状态失败: {e}")
            raise GameException(f"加载游戏状态失败: {e}")
    
    # 事件处理器
    async def _on_game_started(self, event: GameEvent) -> None:
        """游戏开始事件处理"""
        self.logger.info("游戏开始")
    
    async def _on_game_ended(self, event: GameEvent) -> None:
        """游戏结束事件处理"""
        self.logger.info("游戏结束")
    
    async def _on_player_joined(self, event: GameEvent) -> None:
        """玩家加入事件处理"""
        player_name = event.data.get("player_name", "未知玩家")
        self.logger.info(f"玩家加入: {player_name}")
    
    async def _on_player_left(self, event: GameEvent) -> None:
        """玩家离开事件处理"""
        player_name = event.data.get("player_name", "未知玩家")
        self.logger.info(f"玩家离开: {player_name}")
    
    async def _on_turn_started(self, event: GameEvent) -> None:
        """回合开始事件处理"""
        turn_number = event.data.get("turn_number", 0)
        current_player = event.data.get("current_player", "未知玩家")
        self.logger.debug(f"回合 {turn_number} 开始，当前玩家: {current_player}")
    
    async def _on_turn_ended(self, event: GameEvent) -> None:
        """回合结束事件处理"""
        turn_number = event.data.get("turn_number", 0)
        self.logger.debug(f"回合 {turn_number} 结束")
    
    async def _on_action_performed(self, event: GameEvent) -> None:
        """行动执行事件处理"""
        player_name = event.data.get("player_name", "未知玩家")
        action_type = event.data.get("action_type", "未知行动")
        success = event.data.get("success", False)
        
        self.logger.debug(f"玩家 {player_name} 执行 {action_type}，结果: {'成功' if success else '失败'}")
    
    async def _on_error_occurred(self, event: GameEvent) -> None:
        """错误发生事件处理"""
        error_message = event.data.get("error_message", "未知错误")
        self.logger.error(f"游戏错误: {error_message}")
    
    # 系统接口实现
    def initialize(self) -> None:
        """初始化系统"""
        self.logger.info("天机变游戏系统初始化")
    
    def shutdown(self) -> None:
        """关闭系统"""
        if self.current_session and self.current_session.is_active():
            asyncio.create_task(self.end_game())
        
        self.logger.info("天机变游戏系统关闭")
    
    def get_status(self) -> Dict[str, Any]:
        """获取系统状态"""
        return {
            "system_name": "天机变游戏系统",
            "version": "2.0.0",
            "active_session": self.current_session.session_id if self.current_session else None,
            "total_sessions": len(self.sessions_history),
            "config_loaded": self.config_manager.is_loaded(),
            "engine_status": self.game_engine.get_status()
        }

# ==================== 便捷函数 ====================

def create_default_game(config_path: Optional[str] = None) -> TianJiBianGame:
    """
    创建默认游戏实例
    
    Args:
        config_path: 配置文件路径
        
    Returns:
        游戏实例
    """
    return TianJiBianGame(config_path)

async def quick_start_game(
    player_names: List[str],
    config_path: Optional[str] = None
) -> TianJiBianGame:
    """
    快速开始游戏
    
    Args:
        player_names: 玩家名称列表
        config_path: 配置文件路径
        
    Returns:
        游戏实例
    """
    game = create_default_game(config_path)
    
    # 创建玩家配置
    player_configs = []
    for i, name in enumerate(player_names):
        player_configs.append({
            "name": name,
            "type": "human",
            "avatar": f"avatar_{i}"
        })
    
    # 创建游戏会话
    session_id = f"session_{int(time.time())}"
    await game.create_game_session(session_id, player_configs)
    
    # 开始游戏
    await game.start_game()
    
    return game

def create_test_game() -> TianJiBianGame:
    """
    创建测试游戏
    
    Returns:
        测试游戏实例
    """
    game = create_default_game()
    
    # 设置测试配置
    test_config = game.config_manager.get_config()
    test_config.basic.debug_mode = True
    test_config.basic.turn_time_limit = 10  # 短时间限制用于测试
    
    return game

# ==================== 主程序入口 ====================

async def main():
    """主程序入口"""
    try:
        # 创建游戏
        game = await quick_start_game(["玩家1", "玩家2"])
        
        print("天机变游戏已启动！")
        print("游戏状态:", game.get_game_state())
        
        # 这里可以添加游戏循环逻辑
        
    except Exception as e:
        print(f"游戏启动失败: {e}")

if __name__ == "__main__":
    asyncio.run(main())