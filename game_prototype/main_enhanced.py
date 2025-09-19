#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
天机变 - 易经主题策略游戏 (增强版)
集成了优化的UI界面和用户体验
"""

import random
import sys
import time
from typing import Dict, Any, Optional

from game_state import GameState, Player, AvatarName, BonusType, Zone, Modifiers
from config_manager import get_config
from game_data import GAME_DECK, GUA_ZONE_BONUSES, EMPEROR_AVATAR, HERMIT_AVATAR
from tian_shi_cards import TIAN_SHI_CARDS
import actions
from bot_player import get_bot_choice
from yijing_actions import (
    apply_yin_yang_effect, apply_wuxing_effect, enhanced_play_card,
    enhanced_meditate, divine_fortune, consult_yijing, enhanced_study,
    display_yijing_status, check_victory_conditions_enhanced
)
from enhanced_victory import VictoryTracker, check_enhanced_victory_conditions
from wisdom_system import wisdom_system
from tutorial_system import tutorial_system, TutorialType
from achievement_system import achievement_system
from enhanced_cards import enhanced_card_system
from ui_enhancement import (
    ui_enhancement, enhanced_print, enhanced_input, 
    display_player_status_enhanced, display_game_state_summary,
    ColorCode
)

def setup_game_enhanced(num_players: int = 2) -> GameState:
    """设置游戏 (增强版)"""
    enhanced_print("正在初始化游戏...", "info")
    time.sleep(0.5)
    
    players = []
    avatars = [EMPEROR_AVATAR, HERMIT_AVATAR]
    
    for i in range(num_players):
        if i == 0:
            # 人类玩家
            ui_enhancement.clear_screen()
            print(ui_enhancement.create_title("创建角色"))
            
            name = enhanced_input("请输入您的名字: ", ColorCode.BRIGHT_CYAN)
            if not name.strip():
                name = f"玩家{i+1}"
            
            print(f"\n{ui_enhancement.create_section_header('选择头像')}")
            print(f"1. {avatars[0].name} - {avatars[0].description}")
            print(f"2. {avatars[1].name} - {avatars[1].description}")
            
            while True:
                try:
                    avatar_choice = int(enhanced_input("选择头像 (1-2): "))
                    if avatar_choice in [1, 2]:
                        chosen_avatar = avatars[avatar_choice - 1]
                        break
                    else:
                        enhanced_print("请选择 1 或 2", "warning")
                except ValueError:
                    enhanced_print("请输入有效数字", "error")
        else:
            # AI玩家
            name = f"AI修行者{i}"
            chosen_avatar = avatars[i % len(avatars)]
        
        player = Player(name, chosen_avatar)
        
        # 设置初始资源
        config = get_config("game_balance.initial_resources", {})
        player.qi = config.get("qi", 5)
        player.dao_xing = config.get("dao_xing", 0)
        player.cheng_yi = config.get("cheng_yi", 1)
        
        # 初始化易经属性
        player.yin_yang_balance = 0.5
        player.wuxing_affinity = {"金": 0, "木": 0, "水": 0, "火": 0, "土": 0}
        player.biangua_history = []
        
        # 发牌
        initial_hand_size = config.get("initial_hand_size", 3)
        for _ in range(initial_hand_size):
            if GAME_DECK:
                card = random.choice(GAME_DECK)
                player.hand.append(card)
        
        players.append(player)
    
    game_state = GameState(players)
    enhanced_print("游戏初始化完成！", "success")
    return game_state

def show_tutorial_menu_enhanced(player: Player):
    """显示教学菜单 (增强版)"""
    while True:
        ui_enhancement.clear_screen()
        print(ui_enhancement.create_title("教学系统", f"{player.name} 的学习之旅"))
        
        options = [
            "基础规则教程",
            "易经知识教程",
            "策略指导教程", 
            "高级战术教程",
            "查看所有课程",
            "学习进度统计",
            "返回游戏"
        ]
        
        descriptions = [
            "学习游戏的基本规则和操作",
            "深入了解易经哲学和文化",
            "掌握游戏策略和技巧",
            "学习高级战术和组合",
            "浏览所有可用的学习内容",
            "查看您的学习进度和成就",
            "回到主游戏界面"
        ]
        
        menu = ui_enhancement.create_menu("教学类别", options, descriptions)
        print(menu)
        print()
        
        try:
            choice = enhanced_input("请选择 (1-7): ")
            
            if choice == "7":
                break
            elif choice == "1":
                show_tutorial_category_enhanced(player, TutorialType.BASIC_RULES)
            elif choice == "2":
                show_tutorial_category_enhanced(player, TutorialType.YIJING_KNOWLEDGE)
            elif choice == "3":
                show_tutorial_category_enhanced(player, TutorialType.STRATEGY_GUIDE)
            elif choice == "4":
                show_tutorial_category_enhanced(player, TutorialType.ADVANCED_TACTICS)
            elif choice == "5":
                show_all_lessons_enhanced(player)
            elif choice == "6":
                show_learning_progress_enhanced(player)
            else:
                enhanced_print("无效选择，请重试", "warning")
                time.sleep(1)
        except KeyboardInterrupt:
            break

def show_tutorial_category_enhanced(player: Player, tutorial_type: TutorialType):
    """显示特定类别的教程 (增强版)"""
    lessons = tutorial_system.database.get_lessons_by_type(tutorial_type)
    progress = tutorial_system.get_player_progress(player.name)
    
    while True:
        ui_enhancement.clear_screen()
        print(ui_enhancement.create_title(tutorial_type.value, "选择要学习的课程"))
        
        # 创建课程表格
        headers = ["编号", "课程名称", "难度", "状态"]
        rows = []
        
        for i, lesson in enumerate(lessons, 1):
            status = "✅ 已完成" if progress.get(lesson.id, False) else "⏳ 未完成"
            rows.append([str(i), lesson.title, lesson.level.value, status])
        
        table = ui_enhancement.create_table(headers, rows)
        print(table)
        print()
        
        try:
            choice = enhanced_input("选择要学习的课程 (输入数字，0返回): ")
            
            if choice == "0":
                break
            
            choice_num = int(choice)
            if 1 <= choice_num <= len(lessons):
                lesson = lessons[choice_num - 1]
                if progress.get(lesson.id, False):
                    enhanced_print("您已经完成了这个课程！", "info")
                    enhanced_input("按回车键继续...")
                else:
                    start_lesson_enhanced(player, lesson)
            else:
                enhanced_print("无效选择", "warning")
                time.sleep(1)
        except (ValueError, KeyboardInterrupt):
            break

def start_lesson_enhanced(player: Player, lesson):
    """开始课程 (增强版)"""
    ui_enhancement.clear_screen()
    print(ui_enhancement.create_title(lesson.title, f"难度: {lesson.level.value}"))
    
    # 显示课程内容
    print(ui_enhancement.create_section_header("课程内容"))
    print(lesson.content)
    print()
    
    # 显示实例
    if lesson.practical_example:
        print(ui_enhancement.create_section_header("实例演示"))
        print(lesson.practical_example)
        print()
    
    enhanced_input("按回车键继续到测验...")
    
    # 显示测验
    ui_enhancement.clear_screen()
    print(ui_enhancement.create_title("课程测验", lesson.title))
    
    print(ui_enhancement.create_section_header("问题"))
    print(lesson.quiz_question)
    print()
    
    print(ui_enhancement.create_section_header("选项"))
    for i, option in enumerate(lesson.quiz_options, 1):
        print(f"{i}. {option}")
    print()
    
    # 获取答案
    while True:
        try:
            answer = int(enhanced_input("请选择答案 (输入数字): "))
            if 1 <= answer <= len(lesson.quiz_options):
                break
            else:
                enhanced_print("请选择有效选项", "warning")
        except ValueError:
            enhanced_print("请输入数字", "error")
    
    # 检查答案
    if answer == lesson.correct_answer:
        enhanced_print("🎉 回答正确！", "success")
        
        # 完成课程
        tutorial_system.complete_lesson(player.name, lesson.id)
        
        # 发放奖励
        if lesson.qi_reward > 0:
            player.qi += lesson.qi_reward
            enhanced_print(f"获得 {lesson.qi_reward} 点气！", "achievement")
        
        if lesson.dao_xing_reward > 0:
            player.dao_xing += lesson.dao_xing_reward
            enhanced_print(f"获得 {lesson.dao_xing_reward} 点道行！", "achievement")
        
        if lesson.cheng_yi_reward > 0:
            player.cheng_yi += lesson.cheng_yi_reward
            enhanced_print(f"获得 {lesson.cheng_yi_reward} 点诚意！", "achievement")
        
        print()
        print(lesson.reward_description)
    else:
        enhanced_print("❌ 回答错误，请继续学习", "error")
        correct_option = lesson.quiz_options[lesson.correct_answer - 1]
        enhanced_print(f"正确答案是: {lesson.correct_answer}. {correct_option}", "info")
    
    enhanced_input("\n按回车键继续...")

def show_all_lessons_enhanced(player: Player):
    """显示所有课程 (增强版)"""
    ui_enhancement.clear_screen()
    print(ui_enhancement.create_title("所有课程", "课程总览"))
    
    tutorial_system.show_available_lessons(player.name)
    enhanced_input("\n按回车键继续...")

def show_learning_progress_enhanced(player: Player):
    """显示学习进度 (增强版)"""
    ui_enhancement.clear_screen()
    print(ui_enhancement.create_title("学习进度", f"{player.name} 的修行历程"))
    
    tutorial_system.display_learning_progress(player.name)
    enhanced_input("\n按回车键继续...")

def show_enhanced_cards_menu_enhanced(player: Player):
    """显示增强卡牌菜单 (增强版)"""
    ui_enhancement.clear_screen()
    print(ui_enhancement.create_title("增强卡牌", f"{player.name} 的卡牌收藏"))
    
    # 初始化玩家卡组
    enhanced_card_system.initialize_player_deck(player.name)
    
    # 获取可用卡牌
    available_cards = enhanced_card_system.get_available_cards(player.name)
    
    if not available_cards:
        enhanced_print("暂无可用的增强卡牌", "info")
        enhanced_input("按回车键继续...")
        return
    
    # 创建卡牌表格
    headers = ["编号", "卡牌名称", "类型", "消耗", "描述"]
    rows = []
    
    for i, card in enumerate(available_cards, 1):
        rows.append([
            str(i),
            card.name,
            card.type.value,
            f"{card.cost}气",
            card.description[:30] + "..." if len(card.description) > 30 else card.description
        ])
    
    table = ui_enhancement.create_table(headers, rows)
    print(table)
    print()
    
    try:
        choice = enhanced_input("输入卡牌编号查看详细信息 (0返回): ")
        if choice and choice != "0":
            card_index = int(choice) - 1
            if 0 <= card_index < len(available_cards):
                enhanced_card_system.display_card_info(available_cards[card_index])
                enhanced_input("按回车键继续...")
    except ValueError:
        pass

def run_action_phase_enhanced(game_state: GameState, player: Player, 
                            mods: Modifiers, is_ai_player: bool) -> GameState:
    """运行行动阶段 (增强版)"""
    ap = 2 + mods.extra_ap
    flags = {"task": False, "freestudy": False, "scry": False, "ask_heart": False}

    while ap > 0:
        actions_menu = actions.get_valid_actions(game_state, player, ap, mods, **flags)
        
        if not actions_menu:
            enhanced_print("没有可用的行动", "info")
            break

        if not is_ai_player:
            # 显示玩家状态
            ui_enhancement.clear_screen()
            display_player_status_enhanced(player)
            print()
            
            # 显示行动菜单
            choice = ui_enhancement.display_action_menu(player, actions_menu, ap)
            
            try:
                choice = int(choice)
            except ValueError:
                enhanced_print("请输入有效数字", "error")
                time.sleep(1)
                continue
        else:
            # AI选择
            choice = get_bot_choice(actions_menu)

        if choice in actions_menu:
            action_data = actions_menu[choice]
            action_cost = action_data.get('cost', 0)
            
            if not is_ai_player:
                enhanced_print(f"执行: {action_data.get('description', '未知行动')}", "info")
                time.sleep(0.5)
            
            # 执行行动
            try:
                game_state = actions.execute_action(game_state, player, choice, mods, **flags)
                ap -= action_cost
                
                # 更新标志
                if choice in [6, 7]:  # task actions
                    flags["task"] = True
                elif choice == 8:  # free study
                    flags["freestudy"] = True
                elif choice == 9:  # scry
                    flags["scry"] = True
                elif choice == 10:  # ask heart
                    flags["ask_heart"] = True
                
                if not is_ai_player:
                    enhanced_print("行动执行成功", "success")
                    time.sleep(1)
                    
            except Exception as e:
                enhanced_print(f"行动执行失败: {e}", "error")
                if not is_ai_player:
                    time.sleep(2)
        else:
            if not is_ai_player:
                enhanced_print("无效选择", "warning")
                time.sleep(1)

    return game_state

def main_game_loop_enhanced(bot_mode: bool, num_players: int = 2):
    """主游戏循环 (增强版)"""
    game_state = setup_game_enhanced(num_players)
    
    ui_enhancement.clear_screen()
    print(ui_enhancement.create_title("游戏开始", "愿易经智慧指引您的修行之路"))
    
    # 显示玩家列表
    print(ui_enhancement.create_section_header("参与玩家"))
    for i, player in enumerate(game_state.players):
        player_type = " (AI)" if bot_mode and i > 0 else " (人类)"
        avatar_icon = "👤" if player.avatar.name.value == "EMPEROR" else "🧙"
        print(f"  {avatar_icon} {player.name} ({player.avatar.name.value}){player_type}")
        
        # 初始化系统
        achievement_system.on_game_start(player.name)
        enhanced_card_system.initialize_player_deck(player.name)
    
    enhanced_input("\n按回车键开始游戏...")
    
    turn_count = 0
    max_turns = 50
    
    while turn_count < max_turns:
        turn_count += 1
        
        ui_enhancement.clear_screen()
        print(ui_enhancement.create_title(f"第 {turn_count} 回合", "修行之路，步步为营"))
        
        # 显示游戏状态摘要
        display_game_state_summary(game_state)
        print()
        
        for i, player in enumerate(game_state.players):
            print(ui_enhancement.create_section_header(f"{player.name} 的回合"))
            
            # 显示易经修行状态
            display_yijing_status(player)
            
            # 计算修正值
            mods = get_current_modifiers(player, game_state)
            
            # 确定是否为AI玩家
            is_ai_player = bot_mode and i > 0
            
            if not is_ai_player:
                enhanced_input("按回车键开始您的回合...")
            
            # 运行行动阶段
            game_state = run_action_phase_enhanced(game_state, player, mods, is_ai_player)
            
            # 更新成就系统
            achievement_system.on_resource_update(player.name, player.qi, player.dao_xing, player.cheng_yi)
            
            controlled_zones = sum(1 for zone_data in game_state.board.gua_zones.values() 
                                 if zone_data.get("controller") == player.name)
            achievement_system.on_zone_control(player.name, controlled_zones)
            
            # 检查新成就
            new_achievements = achievement_system.check_achievements(player.name)
            for achievement in new_achievements:
                enhanced_print(f"🏆 解锁成就: {achievement.name}", "achievement")
                achievement_system.display_achievement_unlock(achievement)
                achievement_system.award_achievement_rewards(player, achievement)
                time.sleep(2)
            
            if not is_ai_player:
                enhanced_print(f"{player.name} 的回合结束", "info")
                time.sleep(1)
        
        # 检查胜利条件
        winner = check_victory_conditions_enhanced(game_state)
        if winner:
            ui_enhancement.clear_screen()
            print(ui_enhancement.create_title("游戏结束", f"🏆 {winner} 获得胜利！"))
            
            # 处理游戏结束成就
            for player in game_state.players:
                won = (player.name == winner)
                achievement_system.on_game_end(player.name, won)
                
                final_achievements = achievement_system.check_achievements(player.name)
                for achievement in final_achievements:
                    enhanced_print(f"🏆 最终成就: {achievement.name}", "achievement")
                    achievement_system.display_achievement_unlock(achievement)
            
            enhanced_input("按回车键继续...")
            return
        
        # 检查区域控制胜利
        for player in game_state.players:
            controlled_zones = sum(1 for zone_data in game_state.board.gua_zones.values() 
                                 if zone_data.get("controller") == player.name)
            
            if controlled_zones >= 5:
                ui_enhancement.clear_screen()
                print(ui_enhancement.create_title("区域控制胜利", f"🏆 {player.name} 获得胜利！"))
                enhanced_print(f"通过控制 {controlled_zones} 个区域获得胜利", "success")
                
                # 处理游戏结束成就
                for p in game_state.players:
                    won = (p.name == player.name)
                    achievement_system.on_game_end(p.name, won)
                
                enhanced_input("按回车键继续...")
                return
    
    enhanced_print("游戏达到最大回合数", "info")

def get_current_modifiers(player: Player, game_state: GameState) -> Modifiers:
    """计算当前修正值"""
    mods = Modifiers()
    
    for zone_name, zone_data in game_state.board.gua_zones.items():
        if zone_data.get("controller") == player.name:
            bonus_info = GUA_ZONE_BONUSES.get(zone_name, {})
            bonus_type = bonus_info.get("bonus")
            
            if bonus_type == BonusType.EXTRA_AP:
                mods.extra_ap += 1
            elif bonus_type == BonusType.HAND_LIMIT:
                mods.hand_limit_bonus += 2
            elif bonus_type == BonusType.EXTRA_INFLUENCE:
                mods.extra_influence += 1
            elif bonus_type == BonusType.FREE_STUDY:
                mods.has_free_study = True
            elif bonus_type == BonusType.QI_DISCOUNT:
                mods.qi_discount += 1
            elif bonus_type == BonusType.DAO_XING_ON_TASK:
                mods.extra_dao_xing_on_task += 1
    
    return mods

def main_enhanced():
    """主函数 (增强版)"""
    try:
        # 显示欢迎界面
        ui_enhancement.display_welcome_screen()
        enhanced_input("按回车键继续...")
        
        while True:
            ui_enhancement.clear_screen()
            choice = ui_enhancement.display_game_menu()
            
            if choice == "1":
                main_game_loop_enhanced(bot_mode=True, num_players=2)
            elif choice == "2":
                while True:
                    try:
                        num_players = int(enhanced_input("请输入玩家人数 (2-8): "))
                        if 2 <= num_players <= 8:
                            break
                        else:
                            enhanced_print("请输入2-8之间的数字", "warning")
                    except ValueError:
                        enhanced_print("请输入有效的数字", "error")
                main_game_loop_enhanced(bot_mode=False, num_players=num_players)
            elif choice == "3":
                # 创建临时玩家用于教学系统
                temp_player = Player("学习者", EMPEROR_AVATAR)
                show_tutorial_menu_enhanced(temp_player)
            elif choice == "4":
                # 成就系统
                enhanced_print("成就系统功能开发中...", "info")
                enhanced_input("按回车键继续...")
            elif choice == "5":
                # 设置选项
                enhanced_print("设置选项功能开发中...", "info")
                enhanced_input("按回车键继续...")
            elif choice == "6":
                ui_enhancement.clear_screen()
                print(ui_enhancement.create_title("再见", "愿易经智慧伴您前行！"))
                enhanced_print("感谢您体验天机变游戏", "success")
                break
            else:
                enhanced_print("无效选择，请重试", "warning")
                time.sleep(1)
                
    except KeyboardInterrupt:
        ui_enhancement.clear_screen()
        print(ui_enhancement.create_title("游戏中断", "感谢您的体验"))
        enhanced_print("游戏已中断，再见！", "info")
    except Exception as e:
        enhanced_print(f"发生错误: {e}", "error")
        enhanced_input("按回车键退出...")

if __name__ == "__main__":
    main_enhanced()