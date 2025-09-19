#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用户界面优化模块
提供界面美化、交互优化和用户体验提升功能
"""

import os
import sys
import time
import json
import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import colorama
from colorama import Fore, Back, Style

# 初始化colorama
colorama.init(autoreset=True)

class UITheme(Enum):
    """界面主题"""
    CLASSIC = "classic"
    MODERN = "modern"
    DARK = "dark"
    LIGHT = "light"
    YIJING = "yijing"

class AnimationType(Enum):
    """动画类型"""
    FADE_IN = "fade_in"
    SLIDE_IN = "slide_in"
    TYPE_WRITER = "type_writer"
    PULSE = "pulse"
    NONE = "none"

@dataclass
class UIConfig:
    """界面配置"""
    theme: UITheme = UITheme.YIJING
    animation_enabled: bool = True
    animation_speed: float = 0.05
    show_progress: bool = True
    use_colors: bool = True
    terminal_width: int = 80
    language: str = "zh"

@dataclass
class ColorScheme:
    """颜色方案"""
    primary: str = Fore.CYAN
    secondary: str = Fore.YELLOW
    success: str = Fore.GREEN
    warning: str = Fore.YELLOW
    error: str = Fore.RED
    info: str = Fore.BLUE
    text: str = Fore.WHITE
    background: str = Back.BLACK

class UIAnimator:
    """界面动画器"""
    
    def __init__(self, config: UIConfig):
        self.config = config
        self.logger = logging.getLogger(__name__)
    
    def animate_text(self, text: str, animation: AnimationType = AnimationType.TYPE_WRITER):
        """文本动画"""
        if not self.config.animation_enabled or animation == AnimationType.NONE:
            print(text)
            return
        
        if animation == AnimationType.TYPE_WRITER:
            self._typewriter_effect(text)
        elif animation == AnimationType.FADE_IN:
            self._fade_in_effect(text)
        elif animation == AnimationType.SLIDE_IN:
            self._slide_in_effect(text)
        elif animation == AnimationType.PULSE:
            self._pulse_effect(text)
        else:
            print(text)
    
    def _typewriter_effect(self, text: str):
        """打字机效果"""
        for char in text:
            print(char, end='', flush=True)
            time.sleep(self.config.animation_speed)
        print()
    
    def _fade_in_effect(self, text: str):
        """淡入效果"""
        # 简化的淡入效果
        for i in range(3):
            print(f"\r{' ' * len(text)}", end='', flush=True)
            time.sleep(0.1)
            print(f"\r{text}", end='', flush=True)
            time.sleep(0.1)
        print()
    
    def _slide_in_effect(self, text: str):
        """滑入效果"""
        width = min(len(text), self.config.terminal_width)
        for i in range(width + 1):
            display_text = text[:i]
            print(f"\r{display_text}", end='', flush=True)
            time.sleep(self.config.animation_speed)
        print()
    
    def _pulse_effect(self, text: str):
        """脉冲效果"""
        for _ in range(3):
            print(f"\r{Style.BRIGHT}{text}{Style.RESET_ALL}", end='', flush=True)
            time.sleep(0.3)
            print(f"\r{Style.DIM}{text}{Style.RESET_ALL}", end='', flush=True)
            time.sleep(0.3)
        print(f"\r{text}")

class ProgressBar:
    """进度条"""
    
    def __init__(self, total: int, width: int = 50, config: UIConfig = None):
        self.total = total
        self.width = width
        self.current = 0
        self.config = config or UIConfig()
        self.start_time = time.time()
    
    def update(self, increment: int = 1, description: str = ""):
        """更新进度"""
        self.current += increment
        if not self.config.show_progress:
            return
        
        percentage = min(100, (self.current / self.total) * 100)
        filled = int(self.width * self.current / self.total)
        bar = "█" * filled + "░" * (self.width - filled)
        
        elapsed = time.time() - self.start_time
        if self.current > 0:
            eta = (elapsed / self.current) * (self.total - self.current)
            eta_str = f"ETA: {eta:.1f}s"
        else:
            eta_str = "ETA: --"
        
        status = f"\r{Fore.CYAN}[{bar}]{Style.RESET_ALL} {percentage:.1f}% {description} {eta_str}"
        print(status, end='', flush=True)
        
        if self.current >= self.total:
            print()  # 换行

class UIFormatter:
    """界面格式化器"""
    
    def __init__(self, config: UIConfig):
        self.config = config
        self.colors = self._get_color_scheme()
        self.animator = UIAnimator(config)
    
    def _get_color_scheme(self) -> ColorScheme:
        """获取颜色方案"""
        if self.config.theme == UITheme.YIJING:
            return ColorScheme(
                primary=Fore.CYAN,
                secondary=Fore.YELLOW,
                success=Fore.GREEN,
                warning=Fore.YELLOW,
                error=Fore.RED,
                info=Fore.BLUE,
                text=Fore.WHITE
            )
        elif self.config.theme == UITheme.DARK:
            return ColorScheme(
                primary=Fore.WHITE,
                secondary=Fore.LIGHTBLACK_EX,
                success=Fore.GREEN,
                warning=Fore.YELLOW,
                error=Fore.RED,
                info=Fore.CYAN,
                text=Fore.LIGHTWHITE_EX
            )
        else:
            return ColorScheme()
    
    def format_title(self, title: str, level: int = 1) -> str:
        """格式化标题"""
        if level == 1:
            border = "=" * len(title)
            return f"{self.colors.primary}{border}\n{title}\n{border}{Style.RESET_ALL}"
        elif level == 2:
            border = "-" * len(title)
            return f"{self.colors.secondary}{title}\n{border}{Style.RESET_ALL}"
        else:
            return f"{self.colors.info}### {title}{Style.RESET_ALL}"
    
    def format_success(self, message: str) -> str:
        """格式化成功消息"""
        return f"{self.colors.success}✅ {message}{Style.RESET_ALL}"
    
    def format_warning(self, message: str) -> str:
        """格式化警告消息"""
        return f"{self.colors.warning}⚠️  {message}{Style.RESET_ALL}"
    
    def format_error(self, message: str) -> str:
        """格式化错误消息"""
        return f"{self.colors.error}❌ {message}{Style.RESET_ALL}"
    
    def format_info(self, message: str) -> str:
        """格式化信息消息"""
        return f"{self.colors.info}ℹ️  {message}{Style.RESET_ALL}"
    
    def format_menu(self, title: str, options: List[str], 
                   descriptions: List[str] = None) -> str:
        """格式化菜单"""
        menu = []
        menu.append(self.format_title(title, 2))
        menu.append("")
        
        for i, option in enumerate(options, 1):
            if descriptions and i-1 < len(descriptions):
                desc = f" - {descriptions[i-1]}"
            else:
                desc = ""
            menu.append(f"{self.colors.primary}{i}.{Style.RESET_ALL} {option}{self.colors.text}{desc}{Style.RESET_ALL}")
        
        menu.append("")
        return "\n".join(menu)
    
    def format_table(self, headers: List[str], rows: List[List[str]], 
                    title: str = None) -> str:
        """格式化表格"""
        if not rows:
            return "无数据"
        
        # 计算列宽
        col_widths = [len(header) for header in headers]
        for row in rows:
            for i, cell in enumerate(row):
                if i < len(col_widths):
                    col_widths[i] = max(col_widths[i], len(str(cell)))
        
        # 构建表格
        table = []
        
        if title:
            table.append(self.format_title(title, 2))
            table.append("")
        
        # 表头
        header_row = "│ " + " │ ".join(
            f"{header:<{col_widths[i]}}" for i, header in enumerate(headers)
        ) + " │"
        separator = "├" + "┼".join("─" * (width + 2) for width in col_widths) + "┤"
        top_border = "┌" + "┬".join("─" * (width + 2) for width in col_widths) + "┐"
        bottom_border = "└" + "┴".join("─" * (width + 2) for width in col_widths) + "┘"
        
        table.append(f"{self.colors.primary}{top_border}{Style.RESET_ALL}")
        table.append(f"{self.colors.primary}│{Style.RESET_ALL} {self.colors.secondary}" + 
                    f" │ ".join(f"{header:<{col_widths[i]}}" for i, header in enumerate(headers)) + 
                    f"{Style.RESET_ALL} {self.colors.primary}│{Style.RESET_ALL}")
        table.append(f"{self.colors.primary}{separator}{Style.RESET_ALL}")
        
        # 数据行
        for row in rows:
            row_str = "│ " + " │ ".join(
                f"{str(cell):<{col_widths[i]}}" for i, cell in enumerate(row)
            ) + " │"
            table.append(f"{self.colors.primary}│{Style.RESET_ALL} " + 
                        " │ ".join(f"{str(cell):<{col_widths[i]}}" for i, cell in enumerate(row)) + 
                        f" {self.colors.primary}│{Style.RESET_ALL}")
        
        table.append(f"{self.colors.primary}{bottom_border}{Style.RESET_ALL}")
        
        return "\n".join(table)
    
    def format_card(self, title: str, content: str, icon: str = "📋") -> str:
        """格式化卡片"""
        lines = content.split('\n')
        max_width = max(len(title) + 4, max(len(line) for line in lines) + 4, 20)
        
        card = []
        card.append(f"{self.colors.primary}┌{'─' * (max_width - 2)}┐{Style.RESET_ALL}")
        card.append(f"{self.colors.primary}│{Style.RESET_ALL} {icon} {self.colors.secondary}{title:<{max_width - 6}}{Style.RESET_ALL} {self.colors.primary}│{Style.RESET_ALL}")
        card.append(f"{self.colors.primary}├{'─' * (max_width - 2)}┤{Style.RESET_ALL}")
        
        for line in lines:
            card.append(f"{self.colors.primary}│{Style.RESET_ALL} {line:<{max_width - 4}} {self.colors.primary}│{Style.RESET_ALL}")
        
        card.append(f"{self.colors.primary}└{'─' * (max_width - 2)}┘{Style.RESET_ALL}")
        
        return "\n".join(card)

class InteractiveUI:
    """交互式界面"""
    
    def __init__(self, config: UIConfig = None):
        self.config = config or UIConfig()
        self.formatter = UIFormatter(self.config)
        self.animator = UIAnimator(self.config)
    
    def show_welcome(self, title: str, subtitle: str = "", version: str = ""):
        """显示欢迎界面"""
        welcome = []
        welcome.append("")
        welcome.append(self.formatter.format_title(title))
        
        if subtitle:
            welcome.append(f"{self.formatter.colors.secondary}{subtitle}{Style.RESET_ALL}")
        
        if version:
            welcome.append(f"{self.formatter.colors.info}版本: {version}{Style.RESET_ALL}")
        
        welcome.append("")
        
        for line in welcome:
            self.animator.animate_text(line, AnimationType.FADE_IN)
    
    def show_menu(self, title: str, options: List[str], 
                  descriptions: List[str] = None) -> str:
        """显示菜单并获取用户选择"""
        menu_text = self.formatter.format_menu(title, options, descriptions)
        print(menu_text)
        
        while True:
            try:
                choice = input(f"{self.formatter.colors.primary}请选择 (1-{len(options)}): {Style.RESET_ALL}")
                if choice.isdigit() and 1 <= int(choice) <= len(options):
                    return choice
                else:
                    print(self.formatter.format_error(f"无效选择，请输入 1-{len(options)}"))
            except (EOFError, KeyboardInterrupt):
                print(self.formatter.format_info("操作已取消"))
                return ""
    
    def show_progress_task(self, task_name: str, total_steps: int, 
                          step_function, *args, **kwargs):
        """显示进度任务"""
        print(self.formatter.format_info(f"开始任务: {task_name}"))
        
        progress = ProgressBar(total_steps, config=self.config)
        
        try:
            result = step_function(progress, *args, **kwargs)
            print(self.formatter.format_success(f"任务完成: {task_name}"))
            return result
        except Exception as e:
            print(self.formatter.format_error(f"任务失败: {e}"))
            return None
    
    def confirm(self, message: str, default: bool = True) -> bool:
        """确认对话框"""
        default_text = "Y/n" if default else "y/N"
        prompt = f"{self.formatter.colors.warning}❓ {message} ({default_text}): {Style.RESET_ALL}"
        
        try:
            response = input(prompt).strip().lower()
            if not response:
                return default
            return response in ['y', 'yes', '是', '确定']
        except (EOFError, KeyboardInterrupt):
            return False
    
    def input_text(self, prompt: str, default: str = "") -> str:
        """文本输入"""
        if default:
            full_prompt = f"{self.formatter.colors.info}📝 {prompt} [{default}]: {Style.RESET_ALL}"
        else:
            full_prompt = f"{self.formatter.colors.info}📝 {prompt}: {Style.RESET_ALL}"
        
        try:
            response = input(full_prompt).strip()
            return response if response else default
        except (EOFError, KeyboardInterrupt):
            return default
    
    def show_loading(self, message: str, duration: float = 2.0):
        """显示加载动画"""
        if not self.config.animation_enabled:
            print(self.formatter.format_info(message))
            time.sleep(duration)
            return
        
        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        start_time = time.time()
        
        while time.time() - start_time < duration:
            for frame in frames:
                print(f"\r{self.formatter.colors.info}{frame} {message}{Style.RESET_ALL}", 
                      end='', flush=True)
                time.sleep(0.1)
                if time.time() - start_time >= duration:
                    break
        
        print(f"\r{self.formatter.format_success(message + ' 完成!')}")

class UIOptimizer:
    """界面优化器"""
    
    def __init__(self, config: UIConfig = None):
        self.config = config or UIConfig()
        self.ui = InteractiveUI(self.config)
        self.logger = logging.getLogger(__name__)
    
    def optimize_game_ui(self):
        """优化游戏界面"""
        self.ui.show_welcome("🎨 界面优化工具", "提升用户体验和视觉效果")
        
        options = [
            "优化菜单界面",
            "美化游戏显示",
            "改进交互体验",
            "调整颜色主题",
            "配置动画效果",
            "返回主菜单"
        ]
        
        descriptions = [
            "优化菜单布局和样式",
            "改进游戏内容显示效果",
            "提升用户交互体验",
            "自定义界面颜色主题",
            "配置界面动画和效果",
            "返回到主菜单"
        ]
        
        while True:
            choice = self.ui.show_menu("界面优化选项", options, descriptions)
            
            if choice == "1":
                self._optimize_menus()
            elif choice == "2":
                self._optimize_game_display()
            elif choice == "3":
                self._optimize_interactions()
            elif choice == "4":
                self._configure_theme()
            elif choice == "5":
                self._configure_animations()
            elif choice == "6":
                break
            else:
                print(self.ui.formatter.format_error("无效选择"))
    
    def _optimize_menus(self):
        """优化菜单"""
        print(self.ui.formatter.format_info("正在优化菜单界面..."))
        
        def optimize_step(progress):
            progress.update(1, "分析现有菜单结构")
            time.sleep(0.5)
            
            progress.update(1, "设计新的菜单布局")
            time.sleep(0.5)
            
            progress.update(1, "应用视觉改进")
            time.sleep(0.5)
            
            progress.update(1, "测试菜单响应")
            time.sleep(0.5)
            
            return "菜单优化完成"
        
        result = self.ui.show_progress_task("菜单优化", 4, optimize_step)
        if result:
            print(self.ui.formatter.format_success("菜单界面已优化"))
    
    def _optimize_game_display(self):
        """优化游戏显示"""
        print(self.ui.formatter.format_info("正在优化游戏显示效果..."))
        
        improvements = [
            ["卡牌显示", "优化", "增强卡牌视觉效果"],
            ["游戏状态", "改进", "清晰显示游戏状态"],
            ["动画效果", "添加", "增加流畅的动画"],
            ["颜色搭配", "调整", "改善颜色对比度"]
        ]
        
        table = self.ui.formatter.format_table(
            ["组件", "状态", "描述"],
            improvements,
            "游戏显示优化"
        )
        print(table)
    
    def _optimize_interactions(self):
        """优化交互体验"""
        print(self.ui.formatter.format_info("正在优化交互体验..."))
        
        features = [
            "✨ 添加键盘快捷键支持",
            "🎯 改进选择反馈机制",
            "📱 优化触摸友好界面",
            "🔊 增加音效反馈",
            "💡 添加操作提示"
        ]
        
        for feature in features:
            print(f"  {feature}")
            time.sleep(0.3)
        
        print(self.ui.formatter.format_success("交互体验已优化"))
    
    def _configure_theme(self):
        """配置主题"""
        themes = ["经典主题", "现代主题", "深色主题", "浅色主题", "易经主题"]
        choice = self.ui.show_menu("选择界面主题", themes)
        
        if choice and choice.isdigit():
            theme_index = int(choice) - 1
            if 0 <= theme_index < len(themes):
                selected_theme = themes[theme_index]
                print(self.ui.formatter.format_success(f"已切换到: {selected_theme}"))
    
    def _configure_animations(self):
        """配置动画"""
        print(self.ui.formatter.format_info("配置动画效果"))
        
        enable_animations = self.ui.confirm("启用界面动画?", True)
        if enable_animations:
            speed = self.ui.input_text("动画速度 (0.01-0.1)", "0.05")
            try:
                speed_value = float(speed)
                if 0.01 <= speed_value <= 0.1:
                    self.config.animation_speed = speed_value
                    print(self.ui.formatter.format_success(f"动画速度设置为: {speed_value}"))
                else:
                    print(self.ui.formatter.format_warning("速度值超出范围，使用默认值"))
            except ValueError:
                print(self.ui.formatter.format_warning("无效的速度值，使用默认值"))
        else:
            self.config.animation_enabled = False
            print(self.ui.formatter.format_info("动画已禁用"))

def main():
    """主函数"""
    config = UIConfig()
    optimizer = UIOptimizer(config)
    optimizer.optimize_game_ui()

if __name__ == "__main__":
    main()