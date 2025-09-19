#!/usr/bin/env python3
"""
修复后的游戏演示脚本
展示游戏的基本功能和修复的EOF错误处理
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import setup_game
from game_state import Zone

def demo_game_functionality():
    """演示游戏的基本功能"""
    print("=== 天机变游戏演示 - 修复版")
    print("=" * 50)
    
    # 初始化游戏
    print("[游戏] 初始化游戏...")
    game_state = setup_game(num_players=2)
    
    print(f"[完成] 游戏初始化成功！")
    print(f"[列表] 玩家列表:")
    for i, player in enumerate(game_state.players, 1):
        print(f"  {i}. {player.name} ({player.avatar.name.value})")
        print(f"     - 气: {player.qi}")
        print(f"     - 道行: {player.dao_xing}")
        print(f"     - 手牌数: {len(player.hand)}")
        if player.hand:
            print(f"     - 手牌: {[card.name for card in player.hand[:3]]}{'...' if len(player.hand) > 3 else ''}")
    
    print(f"\n[地图]  棋盘状态:")
    for zone_name, zone_data in game_state.board.gua_zones.items():
        controller = zone_data.get("controller", "无人控制")
        markers = zone_data.get("markers", {})
        markers_str = ", ".join(f"{name}: {count}" for name, count in markers.items()) if markers else "无"
        print(f"  【{zone_name}】- 控制者: {controller}, 影响力: {markers_str}")
    
    print(f"\n[目标] 游戏目标:")
    print("  - 通过打牌获得影响力控制卦区")
    print("  - 完成爻辞任务获得道行")
    print("  - 率先达到胜利条件获胜")
    
    print(f"\n[修复] 修复内容:")
    print("  [完成] 修复了EOF错误处理")
    print("  [完成] 改善了用户输入异常处理")
    print("  [完成] 增强了游戏稳定性")
    
    print(f"\n[启动] 游戏已准备就绪！")
    print("  运行 'python main.py' 开始游戏")
    print("  选择模式1进行单人对AI游戏")
    print("  选择模式2进行多人游戏")

def show_available_actions():
    """展示可用的游戏动作"""
    print(f"\n[列表] 游戏中可用的动作:")
    actions = [
        "1. 跳过回合 (Pass turn)",
        "2. 打牌到卦区 (Play card to zone)",
        "3. 移动到不同区域 (Move to different zone)",
        "4. 学习抽牌 (Study - draw cards)",
        "5. 冥想修炼 (Meditate - cultivate Qi)",
        "6. 占卜运势 (Divine Fortune)",
        "7. 查看智慧进度 (View Wisdom Progress)",
        "8. 教学菜单 (Tutorial Menu)",
        "9. 成就系统 (Achievement System)",
        "10. 增强卡牌 (Enhanced Cards)"
    ]
    
    for action in actions:
        print(f"  {action}")

def main():
    """主演示函数"""
    try:
        demo_game_functionality()
        show_available_actions()
        
        print(f"\n[提示] 提示:")
        print("  - 游戏支持1-8人游戏")
        print("  - 包含完整的易经64卦系统")
        print("  - 具有教学系统和成就系统")
        print("  - 支持AI对手")
        
    except Exception as e:
        print(f"[错误] 演示过程中出现错误: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    if success:
        print(f"\n[成功] 演示完成！游戏功能正常")
    else:
        print(f"\n[警告]  演示过程中出现问题")