#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UI界面优化模块
提供更美观、更直观的用户界面和交互体验
"""

import os
import sys
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
from game_state import Player, GameState
from config_manager import ConfigManager

class UITheme(Enum):
    """UI主题"""
    CLASSIC = "经典"
    MODERN = "现代"
    ELEGANT = "雅致"

class ColorCode:
    """颜色代码"""
    # 基础颜色
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    
    # 前景色
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    # 亮色
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'
    
    # 背景色
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'

@dataclass
class UIConfig:
    """UI配置"""
    theme: UITheme = UITheme.ELEGANT
    use_colors: bool = True
    use_unicode: bool = True
    screen_width: int = 80
    animation_speed: float = 0.5
    show_tips: bool = True

class UIEnhancement:
    """UI增强类"""
    
    def __init__(self):
        self.config = UIConfig()
        self.config_manager = ConfigManager()
        self._load_ui_settings()
    
    def _load_ui_settings(self):
        """加载UI设置"""
        try:
            ui_settings = self.config_manager.get("ui_settings", {})
            if "use_colors" in ui_settings:
                self.config.use_colors = ui_settings["use_colors"]
            if "use_unicode" in ui_settings:
                self.config.use_unicode = ui_settings["use_unicode"]
            if "screen_width" in ui_settings:
                self.config.screen_width = ui_settings["screen_width"]
        except:
            pass  # 使用默认设置
    
    def clear_screen(self):
        """清屏"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def colorize(self, text: str, color: str = ColorCode.RESET) -> str:
        """给文本添加颜色"""
        if not self.config.use_colors:
            return text
        return f"{color}{text}{ColorCode.RESET}"
    
    def create_border(self, text: str, style: str = "=", width: Optional[int] = None) -> str:
        """创建边框"""
        if width is None:
            width = self.config.screen_width
        
        if self.config.use_unicode:
            borders = {
                "=": "═",
                "-": "─",
                "*": "✦",
                "~": "～"
            }
            border_char = borders.get(style, style)
        else:
            border_char = style
        
        return border_char * width
    
    def create_title(self, title: str, subtitle: str = "") -> str:
        """创建标题"""
        lines = []
        
        # 主标题
        if self.config.use_unicode:
            title_decorated = f"✦ {title} ✦"
        else:
            title_decorated = f"* {title} *"
        
        lines.append(self.colorize(self.create_border("="), ColorCode.CYAN))
        lines.append(self.colorize(title_decorated.center(self.config.screen_width), 
                                 ColorCode.BRIGHT_CYAN + ColorCode.BOLD))
        
        if subtitle:
            lines.append(self.colorize(subtitle.center(self.config.screen_width), 
                                     ColorCode.YELLOW))
        
        lines.append(self.colorize(self.create_border("="), ColorCode.CYAN))
        
        return "\n".join(lines)
    
    def create_section_header(self, title: str) -> str:
        """创建章节标题"""
        if self.config.use_unicode:
            icon = "◆"
        else:
            icon = ">"
        
        header = f"{icon} {title}"
        return self.colorize(header, ColorCode.BRIGHT_BLUE + ColorCode.BOLD)
    
    def create_menu(self, title: str, options: List[str], 
                   descriptions: Optional[List[str]] = None) -> str:
        """创建菜单"""
        lines = []
        
        # 菜单标题
        lines.append(self.create_section_header(title))
        lines.append(self.colorize(self.create_border("-", width=len(title) + 10), ColorCode.BLUE))
        
        # 菜单选项
        for i, option in enumerate(options, 1):
            if self.config.use_unicode:
                bullet = "▶"
            else:
                bullet = ">"
            
            option_text = f"{bullet} {i}. {option}"
            lines.append(self.colorize(option_text, ColorCode.WHITE))
            
            # 添加描述
            if descriptions and i-1 < len(descriptions):
                desc_text = f"   {descriptions[i-1]}"
                lines.append(self.colorize(desc_text, ColorCode.DIM + ColorCode.CYAN))
        
        return "\n".join(lines)
    
    def create_player_status(self, player: Player) -> str:
        """创建玩家状态显示"""
        lines = []
        
        # 玩家名称和头像
        if self.config.use_unicode:
            avatar_icon = "[玩家]" if player.avatar.name.value == "EMPEROR" else "[法师]"
        else:
            avatar_icon = "[E]" if player.avatar.name.value == "EMPEROR" else "[H]"
        
        name_line = f"{avatar_icon} {player.name} ({player.avatar.name.value})"
        lines.append(self.colorize(name_line, ColorCode.BRIGHT_YELLOW + ColorCode.BOLD))
        
        # 资源状态
        if self.config.use_unicode:
            qi_icon = "[电]"
            dao_icon = "[星]"
            cheng_icon = "[钻]"
        else:
            qi_icon = "Qi:"
            dao_icon = "Dao:"
            cheng_icon = "Cheng:"
        
        resources = [
            f"{qi_icon} {player.qi}",
            f"{dao_icon} {player.dao_xing}",
            f"{cheng_icon} {player.cheng_yi}"
        ]
        
        resource_line = " | ".join(resources)
        lines.append(self.colorize(resource_line, ColorCode.GREEN))
        
        # 手牌数量
        if self.config.use_unicode:
            hand_icon = "[卡牌]"
        else:
            hand_icon = "Cards:"
        
        hand_line = f"{hand_icon} {len(player.hand)} 张手牌"
        lines.append(self.colorize(hand_line, ColorCode.CYAN))
        
        return "\n".join(lines)
    
    def create_progress_bar(self, current: int, maximum: int, width: int = 20, 
                          label: str = "") -> str:
        """创建进度条"""
        if maximum == 0:
            percentage = 0
        else:
            percentage = min(current / maximum, 1.0)
        
        filled = int(width * percentage)
        
        if self.config.use_unicode:
            fill_char = "█"
            empty_char = "░"
        else:
            fill_char = "#"
            empty_char = "-"
        
        bar = fill_char * filled + empty_char * (width - filled)
        
        if label:
            return f"{label}: [{bar}] {current}/{maximum}"
        else:
            return f"[{bar}] {current}/{maximum}"
    
    def create_notification(self, message: str, type: str = "info") -> str:
        """创建通知消息"""
        if self.config.use_unicode:
            icons = {
                "info": "[信息]",
                "success": "[完成]",
                "warning": "[警告]",
                "error": "[错误]",
                "achievement": "🏆"
            }
            icon = icons.get(type, "[信息]")
        else:
            icons = {
                "info": "[i]",
                "success": "[✓]",
                "warning": "[!]",
                "error": "[X]",
                "achievement": "[*]"
            }
            icon = icons.get(type, "[i]")
        
        colors = {
            "info": ColorCode.BLUE,
            "success": ColorCode.GREEN,
            "warning": ColorCode.YELLOW,
            "error": ColorCode.RED,
            "achievement": ColorCode.MAGENTA
        }
        color = colors.get(type, ColorCode.RESET)
        
        notification = f"{icon} {message}"
        return self.colorize(notification, color + ColorCode.BOLD)
    
    def create_table(self, headers: List[str], rows: List[List[str]], 
                    title: str = "") -> str:
        """创建表格"""
        lines = []
        
        if title:
            lines.append(self.create_section_header(title))
            lines.append("")
        
        # 计算列宽
        col_widths = [len(header) for header in headers]
        for row in rows:
            for i, cell in enumerate(row):
                if i < len(col_widths):
                    col_widths[i] = max(col_widths[i], len(str(cell)))
        
        # 创建分隔线
        if self.config.use_unicode:
            separator = "─"
            corner = "┼"
        else:
            separator = "-"
            corner = "+"
        
        sep_line = corner.join(separator * (width + 2) for width in col_widths)
        
        # 表头
        header_cells = []
        for i, header in enumerate(headers):
            cell = f" {header:<{col_widths[i]}} "
            header_cells.append(self.colorize(cell, ColorCode.BRIGHT_WHITE + ColorCode.BOLD))
        
        lines.append("|".join(header_cells))
        lines.append(self.colorize(sep_line, ColorCode.DIM))
        
        # 数据行
        for row in rows:
            row_cells = []
            for i, cell in enumerate(row):
                if i < len(col_widths):
                    formatted_cell = f" {str(cell):<{col_widths[i]}} "
                    row_cells.append(formatted_cell)
            lines.append("|".join(row_cells))
        
        return "\n".join(lines)
    
    def create_yijing_status(self, player: Player) -> str:
        """创建易经修行状态显示"""
        lines = []
        
        # 标题
        lines.append(self.create_section_header("易经修行状态"))
        
        # 阴阳平衡
        if hasattr(player, 'yin_yang_balance'):
            balance = getattr(player, 'yin_yang_balance', 0.5)
            if self.config.use_unicode:
                yin_icon = "☯"
                yang_icon = "☯"
            else:
                yin_icon = "Yin"
                yang_icon = "Yang"
            
            balance_text = f"{yin_icon} 阴阳平衡: {balance:.2f}"
            lines.append(self.colorize(balance_text, ColorCode.MAGENTA))
        
        # 五行亲和力
        if hasattr(player, 'wuxing_affinity'):
            affinity = getattr(player, 'wuxing_affinity', {})
            if affinity:
                wuxing_icons = {
                    "金": "🔸" if self.config.use_unicode else "[金]",
                    "木": "🌿" if self.config.use_unicode else "[木]",
                    "水": "💧" if self.config.use_unicode else "[水]",
                    "火": "[火]" if self.config.use_unicode else "[火]",
                    "土": "🌍" if self.config.use_unicode else "[土]"
                }
                
                wuxing_text = "五行亲和: " + " ".join([
                    f"{wuxing_icons.get(element, element)}{value}"
                    for element, value in affinity.items()
                ])
                lines.append(self.colorize(wuxing_text, ColorCode.GREEN))
        
        return "\n".join(lines)
    
    def display_welcome_screen(self):
        """显示欢迎界面"""
        self.clear_screen()
        
        welcome_text = """
天机变 - 易经主题策略游戏

"易有太极，是生两仪，两仪生四象，四象生八卦"

在这个游戏中，您将体验到：
• 深邃的易经哲学智慧
• 策略性的卡牌对战
• 阴阳平衡的修行之道
• 五行相生相克的奥秘
        """
        
        print(self.create_title("天机变", "易经主题策略游戏"))
        print()
        print(self.colorize(welcome_text.strip(), ColorCode.CYAN))
        print()
        print(self.create_border("~"))
    
    def display_game_menu(self) -> str:
        """显示游戏主菜单"""
        options = [
            "单人修行模式 (与AI对弈)",
            "多人游戏模式 (2-8人)",
            "教学系统",
            "成就系统",
            "设置选项",
            "退出游戏"
        ]
        
        descriptions = [
            "与智能AI对手切磋，提升修行境界",
            "邀请朋友一起体验易经智慧",
            "学习易经知识和游戏策略",
            "查看解锁的成就和进度",
            "调整游戏设置和界面选项",
            "愿易经智慧伴您前行"
        ]
        
        menu = self.create_menu("游戏主菜单", options, descriptions)
        print(menu)
        print()
        
        if self.config.show_tips:
            tip = self.create_notification("提示: 输入对应数字选择菜单项", "info")
            print(tip)
        
        return input(self.colorize("请选择 (1-6): ", ColorCode.BRIGHT_WHITE))
    
    def display_action_menu(self, player: Player, actions_menu: Dict[int, Dict[str, Any]], 
                          ap: int) -> str:
        """显示行动菜单"""
        print(f"\n{self.create_section_header(f'{player.name} 的回合')}")
        print(f"剩余行动点: {self.colorize(str(ap), ColorCode.BRIGHT_YELLOW)}")
        print()
        
        # 显示可用行动
        options = []
        descriptions = []
        
        for key, action_data in actions_menu.items():
            action_name = action_data.get('description', '未知行动')
            action_cost = action_data.get('cost', 0)
            
            option_text = f"{action_name} (消耗 {action_cost} AP)"
            options.append(option_text)
            
            # 添加行动描述
            action_desc = action_data.get('help', '执行此行动')
            descriptions.append(action_desc)
        
        menu = self.create_menu("可用行动", options, descriptions)
        print(menu)
        print()
        
        return input(self.colorize("选择行动: ", ColorCode.BRIGHT_WHITE))

# 全局UI增强实例
ui_enhancement = UIEnhancement()

def enhanced_print(message: str, type: str = "info"):
    """增强的打印函数"""
    print(ui_enhancement.create_notification(message, type))

def enhanced_input(prompt: str, color: str = ColorCode.BRIGHT_WHITE) -> str:
    """增强的输入函数"""
    colored_prompt = ui_enhancement.colorize(prompt, color)
    return input(colored_prompt)

def display_player_status_enhanced(player: Player):
    """增强的玩家状态显示"""
    print(ui_enhancement.create_player_status(player))
    
    # 显示易经修行状态
    yijing_status = ui_enhancement.create_yijing_status(player)
    if yijing_status:
        print()
        print(yijing_status)

def display_game_state_summary(game_state: GameState):
    """显示游戏状态摘要"""
    print(ui_enhancement.create_section_header("游戏状态"))
    
    # 玩家状态表格
    headers = ["玩家", "气", "道行", "诚意", "手牌", "控制区域"]
    rows = []
    
    for player in game_state.players:
        controlled_zones = sum(1 for zone_data in game_state.board.gua_zones.values() 
                             if zone_data.get("controller") == player.name)
        
        row = [
            player.name,
            str(player.qi),
            str(player.dao_xing),
            str(player.cheng_yi),
            str(len(player.hand)),
            str(controlled_zones)
        ]
        rows.append(row)
    
    table = ui_enhancement.create_table(headers, rows, "玩家状态一览")
    print(table)