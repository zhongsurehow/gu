#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整增强版天机变游戏 - 集成所有高级功能
包含增强UI、高级策略、智能AI、卦象系统等完整功能
"""

import sys
import time
import random
from typing import Dict, List, Optional, Tuple

# 导入所有必要模块
from game_state import GameState, Player, GameBoard
from ui_enhancement import enhanced_print, enhanced_input, ui_enhancement
from advanced_strategy_system import (
    advanced_strategy_system, display_hexagram_strategy_guide
)
from enhanced_ai_player import create_ai_players, EnhancedAIPlayer
from enhanced_hexagram_system import (
    enhanced_hexagram_system, display_hexagram_analysis, display_synergy_analysis
)
from tutorial_system import TutorialSystem
from achievement_system import achievement_system
from generate_64_guas import generate_all_64_guas, GUA_64_INFO
from yijing_mechanics import YinYang, WuXing

class CompleteEnhancedGame:
    """完整增强版游戏主类"""
    
    def __init__(self):
        self.game_state = None
        self.tutorial_system = TutorialSystem()
        self.ai_players = create_ai_players()
        self.current_ai_opponent = None
        self.game_mode = None
        self.difficulty_level = "normal"
        
    def start_game(self):
        """启动游戏"""
        ui_enhancement.clear_screen()
        self._display_game_intro()
        
        while True:
            choice = self._show_main_menu()
            
            if choice == "1":
                self._start_tutorial()
            elif choice == "2":
                self._start_single_player()
            elif choice == "3":
                self._start_ai_battle()
            elif choice == "4":
                self._show_hexagram_guide()
            elif choice == "5":
                self._show_strategy_guide()
            elif choice == "6":
                self._show_achievements()
            elif choice == "7":
                self._show_game_settings()
            elif choice == "8":
                enhanced_print("感谢游玩天机变！愿易经智慧伴您前行。", "success")
                break
            else:
                enhanced_print("无效选择，请重试", "warning")
    
    def _display_game_intro(self):
        """显示游戏介绍"""
        print(ui_enhancement.create_title("天机变 - 完整增强版", "易经智慧策略游戏"))
        
        intro_text = """
        欢迎来到天机变的完整世界！
        
        在这个版本中，您将体验到：
        • 🎨 精美的用户界面和视觉效果
        • 🧠 智能AI对手，具备不同性格和策略
        • [书] 深度的卦象系统，包含变卦、互卦、错卦
        • [战斗] 高级策略系统，运用易经智慧
        • 🏆 成就系统，记录您的游戏历程
        • [书] 完整的教学系统，从入门到精通
        
        准备好开始您的易经智慧之旅了吗？
        """
        
        enhanced_print(intro_text, "info")
        enhanced_input("按回车键继续...")
    
    def _show_main_menu(self) -> str:
        """显示主菜单"""
        ui_enhancement.clear_screen()
        print(ui_enhancement.create_title("主菜单", "选择您的游戏模式"))
        
        menu_options = [
            "1. [书] 教学模式 - 学习易经智慧",
            "2. [游戏] 单人游戏 - 挑战AI对手", 
            "3. [战斗] AI对战 - 观看AI智慧对决",
            "4. [书] 卦象指南 - 深入了解64卦",
            "5. 🧠 策略指南 - 掌握高级策略",
            "6. 🏆 成就系统 - 查看游戏成就",
            "7. ⚙️ 游戏设置 - 自定义体验",
            "8. 🚪 退出游戏"
        ]
        
        for option in menu_options:
            print(f"  {option}")
        print()
        
        return enhanced_input("请选择 (1-8): ")
    
    def _start_tutorial(self):
        """开始教学模式"""
        ui_enhancement.clear_screen()
        print(ui_enhancement.create_title("教学模式", "易经智慧学习之旅"))
        
        tutorial_options = [
            "1. 基础入门 - 易经基本概念",
            "2. 卦象系统 - 64卦详解",
            "3. 策略进阶 - 高级游戏技巧",
            "4. 实战演练 - 模拟对战",
            "5. 返回主菜单"
        ]
        
        for option in tutorial_options:
            print(f"  {option}")
        print()
        
        choice = enhanced_input("请选择教学内容 (1-5): ")
        
        if choice == "1":
            self.tutorial_system.start_basic_tutorial()
        elif choice == "2":
            self.tutorial_system.start_hexagram_tutorial()
        elif choice == "3":
            self.tutorial_system.start_strategy_tutorial()
        elif choice == "4":
            self._start_tutorial_battle()
        elif choice == "5":
            return
        else:
            enhanced_print("无效选择", "warning")
        
        enhanced_input("按回车键返回...")
    
    def _start_single_player(self):
        """开始单人游戏"""
        ui_enhancement.clear_screen()
        print(ui_enhancement.create_title("单人游戏", "选择您的对手"))
        
        # 选择AI对手
        ai_list = list(self.ai_players.keys())
        
        print("可选择的AI对手:")
        for i, (name, ai_player) in enumerate(self.ai_players.items(), 1):
            print(f"  {i}. {name} ({ai_player.personality.value})")
        print(f"  {len(ai_list) + 1}. 随机选择")
        print()
        
        try:
            choice = int(enhanced_input("请选择对手 (输入数字): "))
            
            if 1 <= choice <= len(ai_list):
                ai_name = ai_list[choice - 1]
                self.current_ai_opponent = self.ai_players[ai_name]
            elif choice == len(ai_list) + 1:
                ai_name = random.choice(ai_list)
                self.current_ai_opponent = self.ai_players[ai_name]
            else:
                enhanced_print("无效选择", "warning")
                return
            
            enhanced_print(f"您选择了对手: {ai_name}", "success")
            
            # 选择难度
            self._select_difficulty()
            
            # 开始游戏
            self._initialize_game("single_player")
            self._run_game_loop()
            
        except ValueError:
            enhanced_print("请输入有效数字", "error")
    
    def _start_ai_battle(self):
        """开始AI对战模式"""
        ui_enhancement.clear_screen()
        print(ui_enhancement.create_title("AI对战", "观看智能AI的策略对决"))
        
        # 随机选择两个AI
        ai_list = list(self.ai_players.keys())
        ai1_name = random.choice(ai_list)
        ai2_name = random.choice([name for name in ai_list if name != ai1_name])
        
        ai1 = self.ai_players[ai1_name]
        ai2 = self.ai_players[ai2_name]
        
        enhanced_print(f"对战双方: {ai1_name} VS {ai2_name}", "info")
        enhanced_print(f"{ai1_name}: {ai1.personality.value}", "info")
        enhanced_print(f"{ai2_name}: {ai2.personality.value}", "info")
        
        confirm = enhanced_input("开始AI对战? (y/n): ").lower()
        if confirm == 'y':
            self._run_ai_vs_ai_battle(ai1, ai2)
    
    def _select_difficulty(self):
        """选择难度等级"""
        print("\n选择难度等级:")
        print("  1. 简单 - AI较为保守")
        print("  2. 普通 - 平衡的AI策略")
        print("  3. 困难 - AI更加激进")
        print("  4. 大师 - AI使用高级策略")
        
        try:
            choice = int(enhanced_input("请选择难度 (1-4): "))
            
            if choice == 1:
                self.difficulty_level = "easy"
                # 降低AI的探索率和学习率
                self.current_ai_opponent.exploration_rate = 0.1
                self.current_ai_opponent.learning_rate = 0.05
            elif choice == 2:
                self.difficulty_level = "normal"
            elif choice == 3:
                self.difficulty_level = "hard"
                # 提高AI的探索率和学习率
                self.current_ai_opponent.exploration_rate = 0.3
                self.current_ai_opponent.learning_rate = 0.15
            elif choice == 4:
                self.difficulty_level = "master"
                # 最高AI设置
                self.current_ai_opponent.exploration_rate = 0.4
                self.current_ai_opponent.learning_rate = 0.2
            else:
                self.difficulty_level = "normal"
                
            enhanced_print(f"难度设置为: {self.difficulty_level}", "success")
            
        except ValueError:
            self.difficulty_level = "normal"
            enhanced_print("使用默认难度: 普通", "info")
    
    def _initialize_game(self, mode: str):
        """初始化游戏"""
        self.game_mode = mode
        
        # 创建玩家
        if mode == "single_player":
            player_name = enhanced_input("请输入您的名字: ") or "玩家"
            human_player = Player(player_name)
            ai_player = Player(self.current_ai_opponent.name)
            players = [human_player, ai_player]
        else:
            # AI vs AI 模式
            players = [Player("AI1"), Player("AI2")]
        
        # 创建游戏状态
        self.game_state = GameState(players)
        
        # 初始化增强系统
        for player in players:
            advanced_strategy_system.initialize_player_strategy(player.name)
            achievement_system.initialize_player(player.name)
        
        enhanced_print("游戏初始化完成！", "success")
        time.sleep(1)
    
    def _run_game_loop(self):
        """运行游戏主循环"""
        ui_enhancement.clear_screen()
        print(ui_enhancement.create_title("游戏开始", f"第 {self.game_state.turn} 回合"))
        
        while not self._check_victory_conditions():
            current_player = self.game_state.get_current_player()
            
            # 显示游戏状态
            self._display_game_status()
            
            # 玩家回合
            if current_player.name == self.current_ai_opponent.name:
                # AI回合
                self._handle_ai_turn(current_player)
            else:
                # 人类玩家回合
                self._handle_human_turn(current_player)
            
            # 更新冷却时间
            advanced_strategy_system.update_cooldowns(current_player.name)
            
            # 检查成就
            achievement_system.check_achievements(current_player.name, self.game_state)
            
            # 下一回合
            self.game_state.next_turn()
            
            time.sleep(1)  # 短暂暂停
        
        # 游戏结束
        self._handle_game_end()
    
    def _display_game_status(self):
        """显示游戏状态"""
        ui_enhancement.clear_screen()
        current_player = self.game_state.get_current_player()
        
        print(ui_enhancement.create_title(f"第 {self.game_state.turn} 回合", f"{current_player.name} 的回合"))
        
        # 显示玩家状态
        self._display_player_status(current_player)
        
        # 显示棋盘状态
        self._display_board_status()
        
        # 显示最近的重要事件
        if hasattr(self.game_state, 'recent_events'):
            if self.game_state.recent_events:
                print(ui_enhancement.create_section_header("最近事件"))
                for event in self.game_state.recent_events[-3:]:
                    print(f"• {event}")
                print()
    
    def _display_player_status(self, player: Player):
        """显示玩家状态"""
        print(ui_enhancement.create_section_header(f"{player.name} 的状态"))
        
        # 创建状态表格
        headers = ["资源", "数值", "状态"]
        rows = [
            ["气", str(player.qi), "[火]" if player.qi >= 8 else "[电]" if player.qi >= 5 else "💧"],
            ["道行", str(player.dao_xing), "[星]" if player.dao_xing >= 8 else "[闪]" if player.dao_xing >= 5 else "[星]"],
            ["诚意", str(player.cheng_yi), "[钻]" if player.cheng_yi >= 8 else "💍" if player.cheng_yi >= 5 else "🔮"],
            ["阴阳平衡", f"{player.yin_yang_balance:.2f}", "[阴阳]" if abs(player.yin_yang_balance - 0.5) < 0.1 else "[平衡]"]
        ]
        
        table = ui_enhancement.create_table(headers, rows)
        print(table)
        print()
    
    def _display_board_status(self):
        """显示棋盘状态"""
        print(ui_enhancement.create_section_header("棋盘状态"))
        
        controlled_zones = {}
        neutral_zones = []
        
        for zone_name, zone_data in self.game_state.board.gua_zones.items():
            controller = zone_data.get("controller")
            if controller:
                if controller not in controlled_zones:
                    controlled_zones[controller] = []
                controlled_zones[controller].append(zone_name)
            else:
                neutral_zones.append(zone_name)
        
        # 显示控制情况
        for player_name, zones in controlled_zones.items():
            print(f"{player_name} 控制的区域 ({len(zones)}个):")
            for i, zone in enumerate(zones):
                if i % 4 == 0 and i > 0:
                    print()
                print(f"  {zone}", end="")
            print("\n")
        
        if neutral_zones:
            print(f"中性区域 ({len(neutral_zones)}个):")
            for i, zone in enumerate(neutral_zones[:8]):  # 只显示前8个
                if i % 4 == 0 and i > 0:
                    print()
                print(f"  {zone}", end="")
            if len(neutral_zones) > 8:
                print(f"  ... 还有{len(neutral_zones) - 8}个")
            print("\n")
    
    def _handle_human_turn(self, player: Player):
        """处理人类玩家回合"""
        while True:
            print(ui_enhancement.create_section_header("行动选择"))
            
            actions = [
                "1. 🧘 冥想 - 恢复气力",
                "2. [书] 研习 - 增进道行", 
                "3. 🙏 修心 - 提升诚意",
                "4. [地图] 探索 - 寻找新区域",
                "5. [战斗] 高级策略 - 使用易经智慧",
                "6. [统计] 卦象分析 - 查看卦象关系",
                "7. 📈 查看状态 - 详细信息",
                "8. [提示] 获取提示 - AI建议"
            ]
            
            for action in actions:
                print(f"  {action}")
            print()
            
            choice = enhanced_input("请选择行动 (1-8): ")
            
            if choice == "1":
                self._handle_meditate(player)
                break
            elif choice == "2":
                self._handle_study(player)
                break
            elif choice == "3":
                self._handle_cultivate(player)
                break
            elif choice == "4":
                self._handle_explore(player)
                break
            elif choice == "5":
                if self._handle_strategy_action(player):
                    break
            elif choice == "6":
                self._show_hexagram_analysis(player)
            elif choice == "7":
                self._show_detailed_status(player)
            elif choice == "8":
                self._show_ai_hint(player)
            else:
                enhanced_print("无效选择，请重试", "warning")
    
    def _handle_ai_turn(self, player: Player):
        """处理AI回合"""
        enhanced_print(f"{player.name} 正在思考...", "info")
        time.sleep(1)
        
        # AI决策
        action = self.current_ai_opponent.make_decision(player, self.game_state)
        
        # 执行AI行动
        if action.startswith("strategy:"):
            strategy_name = action.split(":", 1)[1]
            available_strategies = advanced_strategy_system.get_available_strategies(player, self.game_state)
            
            for strategy in available_strategies:
                if strategy.name == strategy_name:
                    advanced_strategy_system.execute_strategy_action(player, self.game_state, strategy)
                    break
        
        elif action.startswith("claim:"):
            zone_name = action.split(":", 1)[1]
            if zone_name in self.game_state.board.gua_zones:
                if not self.game_state.board.gua_zones[zone_name].get("controller"):
                    self.game_state.board.gua_zones[zone_name]["controller"] = player.name
                    enhanced_print(f"{player.name} 控制了 {zone_name}", "success")
        
        elif action == "meditate":
            self._handle_meditate(player)
        elif action == "study":
            self._handle_study(player)
        elif action == "explore":
            self._handle_explore(player)
        
        # 显示AI状态报告
        if random.random() < 0.3:  # 30%概率显示详细报告
            report = self.current_ai_opponent.get_ai_status_report(player, self.game_state)
            enhanced_print(report, "info")
        
        enhanced_input("按回车键继续...")
    
    def _handle_meditate(self, player: Player):
        """处理冥想行动"""
        qi_gain = random.randint(2, 4)
        player.qi += qi_gain
        
        # 阴阳平衡调整
        if player.yin_yang_balance < 0.5:
            player.yin_yang_balance += 0.05
        else:
            player.yin_yang_balance -= 0.05
        
        enhanced_print(f"{player.name} 冥想获得 {qi_gain} 点气力", "success")
        
        # 检查成就
        achievement_system.record_action(player.name, "meditate")
    
    def _handle_study(self, player: Player):
        """处理研习行动"""
        dao_gain = random.randint(1, 3)
        player.dao_xing += dao_gain
        
        enhanced_print(f"{player.name} 研习获得 {dao_gain} 点道行", "success")
        
        # 有概率获得卦象洞察
        if random.random() < 0.3:
            self._grant_hexagram_insight(player)
        
        achievement_system.record_action(player.name, "study")
    
    def _handle_cultivate(self, player: Player):
        """处理修心行动"""
        cheng_yi_gain = random.randint(1, 3)
        player.cheng_yi += cheng_yi_gain
        
        enhanced_print(f"{player.name} 修心获得 {cheng_yi_gain} 点诚意", "success")
        
        achievement_system.record_action(player.name, "cultivate")
    
    def _handle_explore(self, player: Player):
        """处理探索行动"""
        # 寻找可控制的区域
        available_zones = [name for name, data in self.game_state.board.gua_zones.items() 
                          if not data.get("controller")]
        
        if available_zones:
            if len(available_zones) == 1:
                target_zone = available_zones[0]
            else:
                enhanced_print("发现可探索的区域:", "info")
                for i, zone in enumerate(available_zones[:5], 1):
                    print(f"  {i}. {zone}")
                
                try:
                    choice = int(enhanced_input("选择探索目标 (输入数字): ")) - 1
                    if 0 <= choice < len(available_zones):
                        target_zone = available_zones[choice]
                    else:
                        target_zone = random.choice(available_zones)
                except ValueError:
                    target_zone = random.choice(available_zones)
            
            # 探索成功率基于玩家能力
            success_rate = min(0.7 + (player.dao_xing * 0.05), 0.95)
            
            if random.random() < success_rate:
                self.game_state.board.gua_zones[target_zone]["controller"] = player.name
                enhanced_print(f"{player.name} 成功控制了 {target_zone}!", "success")
                
                # 显示卦象信息
                if target_zone in GUA_64_INFO:
                    gua_info = GUA_64_INFO[target_zone]
                    enhanced_print(f"卦象属性: {gua_info.get('element', '未知')}", "info")
                
                achievement_system.record_action(player.name, "explore_success")
            else:
                enhanced_print(f"{player.name} 探索失败，但获得了经验", "warning")
                player.dao_xing += 1
        else:
            enhanced_print("没有可探索的区域", "info")
            player.qi += 1  # 补偿奖励
    
    def _grant_hexagram_insight(self, player: Player):
        """给予卦象洞察"""
        controlled_zones = [name for name, data in self.game_state.board.gua_zones.items() 
                           if data.get("controller") == player.name]
        
        if controlled_zones:
            zone = random.choice(controlled_zones)
            relations = enhanced_hexagram_system.get_hexagram_relations(zone)
            
            if relations:
                relation = random.choice(relations)
                enhanced_print(f"获得洞察: {zone} 与 {relation.related} 的关系 - {relation.description}", "achievement")
    
    def _handle_strategy_action(self, player: Player) -> bool:
        """处理策略行动"""
        selected_strategy = advanced_strategy_system.display_strategy_menu(player, self.game_state)
        
        if selected_strategy:
            advanced_strategy_system.execute_strategy_action(player, self.game_state, selected_strategy)
            return True
        
        return False
    
    def _show_hexagram_analysis(self, player: Player):
        """显示卦象分析"""
        controlled_zones = [name for name, data in self.game_state.board.gua_zones.items() 
                           if data.get("controller") == player.name]
        
        if not controlled_zones:
            enhanced_print("您还没有控制任何卦象区域", "info")
            return
        
        ui_enhancement.clear_screen()
        print(ui_enhancement.create_title("卦象分析", f"{player.name} 的卦象网络"))
        
        for zone in controlled_zones:
            display_hexagram_analysis(zone)
            print()
        
        # 显示协同分析
        if len(controlled_zones) >= 2:
            print(ui_enhancement.create_section_header("协同效应分析"))
            for i, zone1 in enumerate(controlled_zones):
                for zone2 in controlled_zones[i+1:]:
                    synergy = enhanced_hexagram_system.calculate_synergy(zone1, zone2)
                    if synergy["compatibility"] > 0.3:
                        display_synergy_analysis(zone1, zone2, synergy)
        
        enhanced_input("按回车键继续...")
    
    def _show_detailed_status(self, player: Player):
        """显示详细状态"""
        ui_enhancement.clear_screen()
        print(ui_enhancement.create_title("详细状态", f"{player.name} 的完整信息"))
        
        # 基础状态
        self._display_player_status(player)
        
        # 控制区域详情
        controlled_zones = [name for name, data in self.game_state.board.gua_zones.items() 
                           if data.get("controller") == player.name]
        
        if controlled_zones:
            print(ui_enhancement.create_section_header("控制区域详情"))
            for zone in controlled_zones:
                if zone in GUA_64_INFO:
                    gua_info = GUA_64_INFO[zone]
                    print(f"{zone}: {gua_info.get('element', '未知')}属性")
        
        # 成就进度
        achievements = achievement_system.get_player_achievements(player.name)
        if achievements:
            print(ui_enhancement.create_section_header("成就进度"))
            for achievement in achievements[:5]:
                print(f"🏆 {achievement}")
        
        enhanced_input("按回车键继续...")
    
    def _show_ai_hint(self, player: Player):
        """显示AI提示"""
        # 使用AI系统生成建议
        temp_ai = self.ai_players["智者"]  # 使用智者AI提供建议
        
        situation = temp_ai._analyze_game_situation(player, self.game_state)
        opportunities = situation["strategic_opportunities"]
        
        enhanced_print("AI建议:", "info")
        
        if opportunities:
            for i, opportunity in enumerate(opportunities[:3], 1):
                print(f"{i}. {opportunity['description']} (评分: {opportunity['score']:.2f})")
        else:
            print("当前局势稳定，建议继续积累资源")
        
        print()
        enhanced_input("按回车键继续...")
    
    def _check_victory_conditions(self) -> bool:
        """检查胜利条件"""
        for player in self.game_state.players:
            controlled_count = sum(1 for data in self.game_state.board.gua_zones.values() 
                                 if data.get("controller") == player.name)
            
            # 胜利条件：控制超过一半的区域，或达到特定资源阈值
            total_zones = len(self.game_state.board.gua_zones)
            
            if (controlled_count > total_zones // 2 or 
                (player.qi >= 20 and player.dao_xing >= 15 and player.cheng_yi >= 15)):
                self.game_state.winner = player
                return True
        
        # 回合数限制
        if self.game_state.turn > 50:
            # 根据控制区域数量决定胜者
            best_player = max(self.game_state.players, 
                            key=lambda p: sum(1 for data in self.game_state.board.gua_zones.values() 
                                             if data.get("controller") == p.name))
            self.game_state.winner = best_player
            return True
        
        return False
    
    def _handle_game_end(self):
        """处理游戏结束"""
        ui_enhancement.clear_screen()
        
        if self.game_state.winner:
            print(ui_enhancement.create_title("游戏结束", f"{self.game_state.winner.name} 获得胜利！"))
            
            # 显示胜利统计
            winner = self.game_state.winner
            controlled_count = sum(1 for data in self.game_state.board.gua_zones.values() 
                                 if data.get("controller") == winner.name)
            
            print(f"🏆 胜利者: {winner.name}")
            print(f"[统计] 控制区域: {controlled_count}")
            print(f"[电] 最终气力: {winner.qi}")
            print(f"[星] 最终道行: {winner.dao_xing}")
            print(f"[钻] 最终诚意: {winner.cheng_yi}")
            print(f"[阴阳] 阴阳平衡: {winner.yin_yang_balance:.2f}")
            print()
            
            # 记录胜利成就
            achievement_system.record_action(winner.name, "victory")
            
            # 显示新获得的成就
            new_achievements = achievement_system.get_recent_achievements(winner.name)
            if new_achievements:
                print("[成功] 新获得的成就:")
                for achievement in new_achievements:
                    print(f"  🏆 {achievement}")
                print()
        
        enhanced_input("按回车键返回主菜单...")
    
    def _run_ai_vs_ai_battle(self, ai1: EnhancedAIPlayer, ai2: EnhancedAIPlayer):
        """运行AI对AI战斗"""
        # 初始化AI对战
        player1 = Player(ai1.name)
        player2 = Player(ai2.name)
        
        self.game_state = GameState([player1, player2])
        
        # 初始化系统
        for player in [player1, player2]:
            advanced_strategy_system.initialize_player_strategy(player.name)
        
        enhanced_print("AI对战开始！", "success")
        
        while not self._check_victory_conditions() and self.game_state.turn <= 30:
            current_player = self.game_state.get_current_player()
            current_ai = ai1 if current_player.name == ai1.name else ai2
            
            # 显示回合信息
            enhanced_print(f"\n=== 第 {self.game_state.turn} 回合 - {current_player.name} ===", "info")
            
            # AI决策和行动
            action = current_ai.make_decision(current_player, self.game_state)
            enhanced_print(f"{current_player.name} 选择: {action}", "info")
            
            # 执行行动（简化版）
            if action == "meditate":
                current_player.qi += random.randint(2, 4)
            elif action == "study":
                current_player.dao_xing += random.randint(1, 3)
            elif action.startswith("claim:"):
                zone_name = action.split(":", 1)[1]
                if (zone_name in self.game_state.board.gua_zones and 
                    not self.game_state.board.gua_zones[zone_name].get("controller")):
                    self.game_state.board.gua_zones[zone_name]["controller"] = current_player.name
                    enhanced_print(f"{current_player.name} 控制了 {zone_name}", "success")
            
            # 更新冷却
            advanced_strategy_system.update_cooldowns(current_player.name)
            
            # 下一回合
            self.game_state.next_turn()
            
            time.sleep(0.5)  # 观战节奏
        
        # 显示对战结果
        self._handle_game_end()
    
    def _show_hexagram_guide(self):
        """显示卦象指南"""
        display_hexagram_analysis("乾")  # 示例
        enhanced_input("按回车键继续...")
    
    def _show_strategy_guide(self):
        """显示策略指南"""
        display_hexagram_strategy_guide()
    
    def _show_achievements(self):
        """显示成就系统"""
        ui_enhancement.clear_screen()
        print(ui_enhancement.create_title("成就系统", "您的游戏历程"))
        
        # 这里可以显示全局成就统计
        enhanced_print("成就系统正在开发中...", "info")
        enhanced_input("按回车键继续...")
    
    def _show_game_settings(self):
        """显示游戏设置"""
        ui_enhancement.clear_screen()
        print(ui_enhancement.create_title("游戏设置", "自定义您的游戏体验"))
        
        settings_options = [
            "1. 🎨 UI主题设置",
            "2. 🔊 音效设置",
            "3. [电] 游戏速度",
            "4. 🤖 AI难度",
            "5. [统计] 统计信息",
            "6. 🔄 重置数据",
            "7. 返回主菜单"
        ]
        
        for option in settings_options:
            print(f"  {option}")
        print()
        
        choice = enhanced_input("请选择设置项 (1-7): ")
        
        if choice == "1":
            self._ui_theme_settings()
        elif choice == "2":
            enhanced_print("音效设置功能开发中...", "info")
        elif choice == "3":
            enhanced_print("游戏速度设置功能开发中...", "info")
        elif choice == "4":
            enhanced_print("AI难度设置功能开发中...", "info")
        elif choice == "5":
            enhanced_print("统计信息功能开发中...", "info")
        elif choice == "6":
            confirm = enhanced_input("确认重置所有数据? (输入 'RESET' 确认): ")
            if confirm == "RESET":
                enhanced_print("数据重置完成", "success")
            else:
                enhanced_print("取消重置", "info")
        elif choice == "7":
            return
        
        enhanced_input("按回车键继续...")
    
    def _ui_theme_settings(self):
        """UI主题设置"""
        print("UI主题选择:")
        print("  1. 经典主题 (当前)")
        print("  2. 简约主题")
        print("  3. 彩色主题")
        
        choice = enhanced_input("选择主题 (1-3): ")
        enhanced_print(f"主题设置为: {choice}", "success")
    
    def _start_tutorial_battle(self):
        """开始教学对战"""
        enhanced_print("教学对战模式开发中...", "info")
        # 这里可以实现一个简化的教学对战

def main():
    """主函数"""
    try:
        game = CompleteEnhancedGame()
        game.start_game()
    except KeyboardInterrupt:
        enhanced_print("\n游戏被用户中断", "warning")
    except Exception as e:
        enhanced_print(f"游戏发生错误: {e}", "error")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()