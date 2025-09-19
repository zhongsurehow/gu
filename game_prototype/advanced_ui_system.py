"""
高级UI系统 - 分段式信息展示和彩色界面
实现用户建议的UI/UX改进
"""

import os
import sys
from enum import Enum
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

# 颜色定义
class Colors:
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

class MessageType(Enum):
    """消息类型枚举"""
    SUCCESS = "success"      # 成功/正面效果 - 绿色
    WARNING = "warning"      # 警告 - 黄色
    ERROR = "error"          # 错误/负面效果 - 红色
    INFO = "info"           # 信息 - 蓝色
    HIGHLIGHT = "highlight"  # 高亮 - 青色
    PLAYER_INPUT = "input"   # 玩家输入 - 黄色
    MYSTICAL = "mystical"    # 神秘/占卜 - 紫色
    RESOURCE = "resource"    # 资源变化 - 绿色/红色

@dataclass
class DisplaySection:
    """显示区段"""
    title: str
    content: List[str]
    visible: bool = True
    color: str = Colors.WHITE

class AdvancedUISystem:
    """高级UI系统"""
    
    def __init__(self):
        self.sections: Dict[str, DisplaySection] = {}
        self.message_colors = {
            MessageType.SUCCESS: Colors.BRIGHT_GREEN,
            MessageType.WARNING: Colors.BRIGHT_YELLOW,
            MessageType.ERROR: Colors.BRIGHT_RED,
            MessageType.INFO: Colors.BRIGHT_BLUE,
            MessageType.HIGHLIGHT: Colors.BRIGHT_CYAN,
            MessageType.PLAYER_INPUT: Colors.YELLOW,
            MessageType.MYSTICAL: Colors.BRIGHT_MAGENTA,
            MessageType.RESOURCE: Colors.GREEN
        }
        self.current_view_mode = "minimal"  # minimal, standard, detailed
        
    def clear_screen(self):
        """清屏"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def colorize(self, text: str, message_type: MessageType) -> str:
        """为文本添加颜色"""
        color = self.message_colors.get(message_type, Colors.WHITE)
        return f"{color}{text}{Colors.RESET}"
    
    def print_colored(self, text: str, message_type: MessageType = MessageType.INFO):
        """打印彩色文本"""
        print(self.colorize(text, message_type))
    
    def create_border(self, text: str, width: int = 80, char: str = "═") -> str:
        """创建边框"""
        if len(text) >= width - 4:
            return f"╔{char * (width-2)}╗\n║ {text[:width-4]} ║\n╚{char * (width-2)}╝"
        
        padding = (width - len(text) - 4) // 2
        line = f"║ {' ' * padding}{text}{' ' * (width - len(text) - 4 - padding)} ║"
        return f"╔{char * (width-2)}╗\n{line}\n╚{char * (width-2)}╝"
    
    def display_title(self, title: str, subtitle: str = ""):
        """显示标题"""
        self.clear_screen()
        title_text = self.create_border(title, 80, "═")
        self.print_colored(title_text, MessageType.HIGHLIGHT)
        
        if subtitle:
            print()
            self.print_colored(f"    {subtitle}", MessageType.INFO)
        print()
    
    def display_core_status(self, player, show_details: bool = False):
        """显示核心状态（简化版）"""
        # 核心资源
        resources = f"[火] AP: {player.action_points} | [电] 气: {player.qi} | [星] 道行: {player.dao_xing} | [钻] 诚意: {player.cheng_yi}"
        self.print_colored(f"【{player.name}】 {resources}", MessageType.RESOURCE)
        
        # 位置信息
        position_text = f"📍 当前位置: {player.position.value}"
        self.print_colored(position_text, MessageType.INFO)
        
        # 手牌数量
        hand_text = f"[卡牌] 手牌: {len(player.hand)}张"
        self.print_colored(hand_text, MessageType.INFO)
        
        if show_details:
            # 显示详细信息
            self.print_colored("─" * 60, MessageType.INFO)
            
    def display_resource_change(self, resource_name: str, old_value: int, new_value: int):
        """显示资源变化"""
        change = new_value - old_value
        if change > 0:
            self.print_colored(f"[完成] {resource_name} +{change} ({old_value} → {new_value})", MessageType.SUCCESS)
        elif change < 0:
            self.print_colored(f"[错误] {resource_name} {change} ({old_value} → {new_value})", MessageType.ERROR)
    
    def display_action_menu(self, actions: List[str], title: str = "可用行动"):
        """显示行动菜单"""
        print()
        self.print_colored(f"═══ {title} ═══", MessageType.HIGHLIGHT)
        
        for i, action in enumerate(actions):
            action_text = f"  {i+1}. {action}"
            self.print_colored(action_text, MessageType.INFO)
        
        print()
        self.print_colored("输入数字选择行动，或输入命令:", MessageType.PLAYER_INPUT)
        self.print_colored("  • status - 查看详细状态", MessageType.INFO)
        self.print_colored("  • board - 查看棋盘状态", MessageType.INFO)
        self.print_colored("  • yinyang - 查看阴阳平衡", MessageType.INFO)
        self.print_colored("  • help - 查看帮助", MessageType.INFO)
        print()
    
    def display_mystical_message(self, message: str, title: str = "神谕"):
        """显示神秘信息（占卜、预言等）"""
        print()
        mystical_border = "✧" * 60
        self.print_colored(mystical_border, MessageType.MYSTICAL)
        self.print_colored(f"    🔮 {title} 🔮", MessageType.MYSTICAL)
        self.print_colored(mystical_border, MessageType.MYSTICAL)
        print()
        
        # 分行显示消息
        for line in message.split('\n'):
            if line.strip():
                self.print_colored(f"    {line.strip()}", MessageType.MYSTICAL)
        
        print()
        self.print_colored(mystical_border, MessageType.MYSTICAL)
        print()
    
    def display_board_status(self, game_state, detailed: bool = False):
        """显示棋盘状态"""
        print()
        self.print_colored("═══ 棋盘状态 ═══", MessageType.HIGHLIGHT)
        
        for zone_name, zone_data in game_state.board.gua_zones.items():
            if zone_data.get('controller'):
                controller_name = zone_data['controller']
                zone_text = f"[区域] 【{zone_name}】: 由 {controller_name} 控制"
                self.print_colored(zone_text, MessageType.SUCCESS)
            else:
                markers = zone_data.get('markers', {})
                if markers:
                    marker_text = ", ".join([f"{name}: {count}" for name, count in markers.items() if count > 0])
                    zone_text = f"[战斗] 【{zone_name}】: {marker_text}"
                    self.print_colored(zone_text, MessageType.WARNING)
                else:
                    zone_text = f"[空白] 【{zone_name}】: 无人控制"
                    self.print_colored(zone_text, MessageType.INFO)
        print()
    
    def display_yinyang_status(self, player):
        """显示阴阳平衡状态"""
        print()
        self.print_colored("═══ 阴阳平衡 ═══", MessageType.HIGHLIGHT)
        
        yin_yang = player.yin_yang_balance
        yin_text = f"[阴阳] 阴: {yin_yang.yin}"
        yang_text = f"[阴阳] 阳: {yin_yang.yang}"
        
        self.print_colored(yin_text, MessageType.INFO)
        self.print_colored(yang_text, MessageType.INFO)
        
        # 显示平衡状态
        balance = yin_yang.get_balance_state()
        if balance == "平衡":
            self.print_colored(f"[平衡] 状态: {balance} (获得额外奖励)", MessageType.SUCCESS)
        elif "偏" in balance:
            self.print_colored(f"[平衡] 状态: {balance}", MessageType.WARNING)
        else:
            self.print_colored(f"[平衡] 状态: {balance}", MessageType.ERROR)
        print()
    
    def display_help(self):
        """显示帮助信息"""
        print()
        self.print_colored("═══ 游戏帮助 ═══", MessageType.HIGHLIGHT)
        
        help_sections = [
            ("基础命令", [
                "status - 查看详细玩家状态",
                "board - 查看棋盘和区域控制情况", 
                "yinyang - 查看阴阳平衡状态",
                "help - 显示此帮助信息"
            ]),
            ("游戏行动", [
                "选择数字执行对应行动",
                "移动 - 在地、人、天之间移动",
                "冥想 - 获得气资源",
                "学习 - 获得道行",
                "演卦 - 打出卦牌影响区域"
            ]),
            ("资源说明", [
                "[火] AP (行动点) - 执行行动所需",
                "[电] 气 - 基础资源，用于各种行动",
                "[星] 道行 - 胜利条件之一",
                "[钻] 诚意 - 影响外交和特殊能力"
            ])
        ]
        
        for section_title, items in help_sections:
            self.print_colored(f"▶ {section_title}:", MessageType.INFO)
            for item in items:
                self.print_colored(f"  • {item}", MessageType.INFO)
            print()
    
    def get_player_input(self, prompt: str = "请选择") -> str:
        """获取玩家输入"""
        colored_prompt = self.colorize(f"{prompt}: ", MessageType.PLAYER_INPUT)
        return input(colored_prompt).strip()
    
    def display_notification(self, message: str, message_type: MessageType = MessageType.INFO):
        """显示通知"""
        icons = {
            MessageType.SUCCESS: "[完成]",
            MessageType.WARNING: "[警告]",
            MessageType.ERROR: "[错误]",
            MessageType.INFO: "[信息]",
            MessageType.HIGHLIGHT: "[星]",
            MessageType.MYSTICAL: "🔮",
            MessageType.RESOURCE: "💰"
        }
        
        icon = icons.get(message_type, "•")
        self.print_colored(f"{icon} {message}", message_type)
    
    def display_section_divider(self, title: str = ""):
        """显示区段分隔符"""
        if title:
            divider = f"─── {title} ───"
        else:
            divider = "─" * 40
        self.print_colored(divider, MessageType.INFO)
    
    def wait_for_continue(self, message: str = "按回车键继续..."):
        """等待用户继续"""
        print()
        self.get_player_input(message)

# 全局UI实例
advanced_ui = AdvancedUISystem()

# 便捷函数
def print_success(message: str):
    advanced_ui.display_notification(message, MessageType.SUCCESS)

def print_warning(message: str):
    advanced_ui.display_notification(message, MessageType.WARNING)

def print_error(message: str):
    advanced_ui.display_notification(message, MessageType.ERROR)

def print_info(message: str):
    advanced_ui.display_notification(message, MessageType.INFO)

def print_mystical(message: str, title: str = "神谕"):
    advanced_ui.display_mystical_message(message, title)

def get_input(prompt: str = "请选择") -> str:
    return advanced_ui.get_player_input(prompt)

def clear_screen():
    advanced_ui.clear_screen()

def display_title(title: str, subtitle: str = ""):
    advanced_ui.display_title(title, subtitle)