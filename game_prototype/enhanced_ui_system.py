#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强用户界面系统
提供更好的游戏体验和易经文化展示
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import random

from game_state import GameState, Player, Zone
from yijing_mechanics import YinYang, WuXing
from card_base import GuaCard

class UITheme(Enum):
    """界面主题"""
    CLASSIC = "经典"
    MODERN = "现代"
    TRADITIONAL = "传统"

@dataclass
class UIConfig:
    """界面配置"""
    theme: UITheme = UITheme.CLASSIC
    show_animations: bool = True
    show_tooltips: bool = True
    auto_save: bool = True
    sound_enabled: bool = True

class EnhancedUISystem:
    """增强用户界面系统"""
    
    def __init__(self, config: UIConfig = None):
        self.config = config or UIConfig()
        self.symbols = self._init_symbols()
        self.colors = self._init_colors()
        
    def _init_symbols(self) -> Dict[str, str]:
        """初始化符号系统"""
        return {
            # 基础符号
            "yin": "⚋",
            "yang": "⚊",
            "taiji": "☯",
            
            # 八卦符号
            "qian": "☰",
            "kun": "☷", 
            "zhen": "☳",
            "xun": "☴",
            "kan": "☵",
            "li": "☲",
            "gen": "☶",
            "dui": "☱",
            
            # 五行符号
            "jin": "⚪",
            "mu": "🌳",
            "shui": "💧",
            "huo": "🔥",
            "tu": "🏔️",
            
            # 游戏符号
            "qi": "⚡",
            "dao": "🌟",
            "cheng": "💎",
            "wisdom": "📚",
            "action": "⚔️",
            "meditation": "🧘",
            "study": "📖",
            "divination": "🔮",
            
            # 状态符号
            "up": "↑",
            "down": "↓",
            "balance": "⚖️",
            "warning": "⚠️",
            "success": "✅",
            "fail": "❌",
            "info": "ℹ️"
        }
    
    def _init_colors(self) -> Dict[str, str]:
        """初始化颜色系统（ANSI颜色代码）"""
        return {
            "reset": "\033[0m",
            "bold": "\033[1m",
            "dim": "\033[2m",
            
            # 基础颜色
            "red": "\033[31m",
            "green": "\033[32m",
            "yellow": "\033[33m",
            "blue": "\033[34m",
            "magenta": "\033[35m",
            "cyan": "\033[36m",
            "white": "\033[37m",
            
            # 背景颜色
            "bg_red": "\033[41m",
            "bg_green": "\033[42m",
            "bg_yellow": "\033[43m",
            "bg_blue": "\033[44m",
            
            # 易经主题颜色
            "yin_color": "\033[36m",      # 青色代表阴
            "yang_color": "\033[33m",     # 黄色代表阳
            "balance_color": "\033[35m",  # 紫色代表平衡
            "qi_color": "\033[32m",       # 绿色代表气
            "dao_color": "\033[34m",      # 蓝色代表道
            "wisdom_color": "\033[37m"    # 白色代表智慧
        }
    
    def colorize(self, text: str, color: str) -> str:
        """给文本添加颜色"""
        if color in self.colors:
            return f"{self.colors[color]}{text}{self.colors['reset']}"
        return text
    
    def display_game_header(self, game_state: GameState):
        """显示游戏标题"""
        print("\n" + "=" * 60)
        title = f"{self.symbols['taiji']} 天机变 - 易经主题策略游戏 {self.symbols['taiji']}"
        print(self.colorize(title.center(60), "bold"))
        print("=" * 60)
        
        # 显示回合信息
        turn_info = f"第 {game_state.turn} 回合"
        current_player = game_state.get_current_player()
        player_info = f"当前玩家: {current_player.name}"
        
        print(f"{turn_info:<30} {player_info:>30}")
        print("-" * 60)
    
    def display_player_status_enhanced(self, player: Player) -> str:
        """增强的玩家状态显示"""
        status_lines = []
        
        # 标题
        title = f"{self.symbols['taiji']} 修行者状态 {self.symbols['taiji']}"
        status_lines.append(self.colorize(title, 'cyan'))
        status_lines.append("=" * 50)
        
        # 基础属性 - 使用进度条显示
        qi_bar = self._create_progress_bar(player.qi, 20, "⚡")
        dao_bar = self._create_progress_bar(player.dao_xing, 20, "🌟")
        cheng_bar = self._create_progress_bar(player.cheng_yi, 20, "💎")
        
        status_lines.append(f"{self.symbols['qi']} 气: {qi_bar} ({player.qi}/20)")
        status_lines.append(f"{self.symbols['dao']} 道行: {dao_bar} ({player.dao_xing}/20)")
        status_lines.append(f"{self.symbols['cheng']} 诚意: {cheng_bar} ({player.cheng_yi}/20)")
        status_lines.append("")
        
        # 阴阳平衡 - 可视化显示
        if hasattr(player, 'yin_yang_balance'):
            balance_visual = self._create_balance_visual(player.yin_yang_balance)
            status_lines.append(f"阴阳平衡: {balance_visual}")
            status_lines.append("")
        
        # 五行状态 - 彩色显示
        if hasattr(player, 'wuxing_balance'):
            status_lines.append("五行状态:")
            wuxing_display = self._create_wuxing_display(player.wuxing_balance)
            status_lines.extend(wuxing_display)
            status_lines.append("")
        
        # 手牌信息
        hand_count = len(player.hand) if hasattr(player, 'hand') else 0
        status_lines.append(f"手牌数量: {hand_count} 张")
        
        # 行动点数
        if hasattr(player, 'action_points'):
            action_bar = self._create_progress_bar(player.action_points, 5, "⚔️")
            status_lines.append(f"行动点: {action_bar} ({player.action_points}/5)")
        
        return "\n".join(status_lines)
    
    def _create_progress_bar(self, current: int, maximum: int, symbol: str = "█") -> str:
        """创建进度条"""
        if maximum <= 0:
            return "N/A"
        
        percentage = min(current / maximum, 1.0)
        filled_length = int(20 * percentage)
        
        # 根据百分比选择颜色
        if percentage >= 0.8:
            color = 'green'
        elif percentage >= 0.5:
            color = 'yellow'
        elif percentage >= 0.3:
            color = 'orange'
        else:
            color = 'red'
        
        bar = "█" * filled_length + "░" * (20 - filled_length)
        return self.colorize(bar, color)
    
    def _create_balance_visual(self, balance: float) -> str:
        """创建阴阳平衡可视化"""
        # balance范围 -1.0 到 1.0，0为完美平衡
        abs_balance = abs(balance)
        
        if abs_balance <= 0.1:
            return f"{self.colorize('☯ 完美平衡', 'green')} ({balance:.2f})"
        elif abs_balance <= 0.3:
            return f"{self.colorize('⚖️ 基本平衡', 'yellow')} ({balance:.2f})"
        elif balance > 0:
            return f"{self.colorize('☰ 阳盛', 'orange')} ({balance:.2f})"
        else:
            return f"{self.colorize('☷ 阴盛', 'blue')} ({balance:.2f})"
    
    def _create_wuxing_display(self, wuxing_balance: Dict) -> List[str]:
        """创建五行显示"""
        wuxing_lines = []
        wuxing_colors = {
            '金': 'white',
            '木': 'green', 
            '水': 'blue',
            '火': 'red',
            '土': 'yellow'
        }
        
        for element, value in wuxing_balance.items():
            color = wuxing_colors.get(element, 'white')
            bar = self._create_progress_bar(value, 10, "●")
            symbol = self.symbols.get(element.lower(), "●")
            wuxing_lines.append(f"  {symbol} {element}: {bar} ({value})")
        
        return wuxing_lines
    
    def display_action_feedback(self, action_name: str, result: Dict, animated: bool = True):
        """显示行动反馈"""
        if animated:
            self._animate_action_start(action_name)
        
        # 显示行动结果
        print(f"\n{self.symbols['action']} {self.colorize(f'执行: {action_name}', 'cyan')}")
        
        # 显示资源变化
        if 'resource_changes' in result:
            self._display_resource_changes(result['resource_changes'])
        
        # 显示特殊效果
        if 'special_effects' in result:
            self._display_special_effects(result['special_effects'])
        
        # 显示触发的智慧格言
        if 'wisdom_quotes' in result:
            self._display_wisdom_quotes(result['wisdom_quotes'])
        
        if animated:
            self._animate_action_end()
    
    def _animate_action_start(self, action_name: str):
        """行动开始动画"""
        import time
        symbols = ["⚡", "✨", "🌟", "💫"]
        for symbol in symbols:
            print(f"\r{symbol} 正在{action_name}...", end="", flush=True)
            time.sleep(0.2)
        print()
    
    def _animate_action_end(self):
        """行动结束动画"""
        import time
        print(f"{self.colorize('✅ 完成!', 'green')}")
        time.sleep(0.5)
    
    def _display_resource_changes(self, changes: Dict):
        """显示资源变化"""
        if not changes:
            return
        
        print(f"\n{self.symbols['info']} 资源变化:")
        for resource, change in changes.items():
            if change > 0:
                color = 'green'
                symbol = self.symbols['up']
            elif change < 0:
                color = 'red'
                symbol = self.symbols['down']
            else:
                continue
            
            resource_symbol = self.symbols.get(resource.lower(), "●")
            print(f"  {resource_symbol} {resource}: {self.colorize(f'{symbol}{abs(change)}', color)}")
    
    def _display_special_effects(self, effects: List[str]):
        """显示特殊效果"""
        if not effects:
            return
        
        print(f"\n{self.symbols['success']} 特殊效果:")
        for effect in effects:
            print(f"  ✨ {self.colorize(effect, 'magenta')}")
    
    def _display_wisdom_quotes(self, quotes: List):
        """显示智慧格言"""
        if not quotes:
            return
        
        print(f"\n{self.symbols['wisdom']} 智慧启发:")
        for quote in quotes:
            if hasattr(quote, 'title') and hasattr(quote, 'content'):
                print(f"  📜 {self.colorize(quote.title, 'yellow')}")
                print(f"     {self.colorize(quote.content, 'cyan')}")
                if hasattr(quote, 'effect_description'):
                    print(f"     💡 {self.colorize(quote.effect_description, 'green')}")
    
    def display_game_phase(self, phase_name: str, description: str = ""):
        """显示游戏阶段"""
        print("\n" + "="*60)
        title = f"🎯 {phase_name}"
        if description:
            title += f" - {description}"
        print(self.colorize(title, 'cyan'))
        print("="*60)
    
    def display_victory_progress(self, victory_conditions: Dict):
        """显示胜利进度"""
        print(f"\n{self.symbols['success']} 胜利进度:")
        print("-" * 40)
        
        for condition_name, progress in victory_conditions.items():
            if isinstance(progress, dict):
                current = progress.get('current', 0)
                required = progress.get('required', 1)
                percentage = min(current / required, 1.0) if required > 0 else 0
                
                progress_bar = self._create_progress_bar(current, required, "●")
                print(f"🏆 {condition_name}: {progress_bar} ({current}/{required})")
            else:
                status = "✅ 已达成" if progress else "⏳ 进行中"
                color = 'green' if progress else 'yellow'
                print(f"🏆 {condition_name}: {self.colorize(status, color)}")
    
    def display_enhanced_menu(self, title: str, options: List[str], descriptions: List[str] = None) -> str:
        """显示增强菜单"""
        self.display_game_phase(title)
        
        print(f"\n{self.symbols['info']} 可选行动:")
        for i, option in enumerate(options, 1):
            option_text = f"{i}. {option}"
            if descriptions and i-1 < len(descriptions):
                option_text += f" - {self.colorize(descriptions[i-1], 'dim')}"
            print(f"  {option_text}")
        
        print(f"\n{self.symbols['info']} 输入 'help' 查看详细说明")
        print(f"{self.symbols['info']} 输入 'status' 查看当前状态")
        
        while True:
            choice = input(f"\n{self.colorize('请选择 (1-' + str(len(options)) + '): ', 'yellow')}").strip()
            
            if choice.lower() == 'help':
                self._display_help(options, descriptions)
                continue
            elif choice.lower() == 'status':
                return 'status'
            
            try:
                choice_num = int(choice)
                if 1 <= choice_num <= len(options):
                    return str(choice_num)
                else:
                    self.display_error(f"请输入 1-{len(options)} 之间的数字")
            except ValueError:
                self.display_error("请输入有效的数字")
    
    def _display_help(self, options: List[str], descriptions: List[str] = None):
        """显示帮助信息"""
        print(f"\n{self.symbols['info']} 详细说明:")
        for i, option in enumerate(options):
            desc = descriptions[i] if descriptions and i < len(descriptions) else "暂无详细说明"
            print(f"  {i+1}. {self.colorize(option, 'cyan')}")
            print(f"     {desc}")
    
    def display_tutorial_tip(self, tip: str, category: str = "提示"):
        """显示教程提示"""
        print(f"\n💡 {self.colorize(f'[{category}]', 'yellow')} {tip}")
    
    def display_achievement_unlock(self, achievement_name: str, description: str):
        """显示成就解锁"""
        print(f"\n🎉 {self.colorize('成就解锁!', 'green')}")
        print(f"🏆 {self.colorize(achievement_name, 'yellow')}")
        print(f"📝 {description}")
        print("="*50)