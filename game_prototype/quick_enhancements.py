"""
快速游戏增强模块 - 可立即集成的趣味性提升
Quick Game Enhancements - Immediate Fun Improvements
"""

import random
import time
import sys

class QuickEnhancements:
    """快速增强功能类"""
    
    def __init__(self):
        self.colors = {
            'red': '\033[91m',
            'green': '\033[92m', 
            'yellow': '\033[93m',
            'blue': '\033[94m',
            'purple': '\033[95m',
            'cyan': '\033[96m',
            'bold': '\033[1m',
            'end': '\033[0m'
        }
        
        self.gua_symbols = {
            '乾': '☰', '坤': '☷', '震': '☳', '巽': '☴',
            '坎': '☵', '离': '☲', '艮': '☶', '兑': '☱'
        }
        
        self.encouragements = [
            "🌟 智慧之光闪耀！",
            "⚡ 天机变化，妙不可言！", 
            "🎯 策略精妙，如有神助！",
            "🔥 气势如虹，势不可挡！",
            "💫 道法自然，顺势而为！"
        ]
        
        self.random_events = [
            "🌙 月圆之夜，所有玩家获得1点额外的气！",
            "⚡ 雷鸣阵阵，震卦威力增强！",
            "🌸 春风化雨，道行增长更快！",
            "🌊 江河奔流，水系卦象效果翻倍！",
            "🔥 烈火燎原，火系攻击力提升！"
        ]
    
    def colorize(self, text, color):
        """给文字添加颜色"""
        return f"{self.colors.get(color, '')}{text}{self.colors['end']}"
    
    def print_with_delay(self, text, delay=0.03):
        """打字机效果输出"""
        for char in text:
            print(char, end='', flush=True)
            time.sleep(delay)
        print()
    
    def show_welcome_animation(self):
        """显示欢迎动画"""
        welcome_art = """
    ╔══════════════════════════════════════╗
    ║           🌟 天 机 变 🌟            ║
    ║                                      ║
    ║        易经智慧 × 策略对战           ║
    ║                                      ║
    ║    ☰ ☷ ☳ ☴ ☵ ☲ ☶ ☱    ║
    ╚══════════════════════════════════════╝
        """
        
        print(self.colorize(welcome_art, 'cyan'))
        self.print_with_delay("正在启动游戏...", 0.1)
        time.sleep(1)
    
    def show_gua_effect(self, gua_name, effect_description):
        """显示卦象效果"""
        symbol = self.gua_symbols.get(gua_name, '◯')
        
        print(f"\n┌─────────────────────────────────┐")
        print(f"│  {symbol}  {self.colorize(gua_name, 'yellow')}  {symbol}  ")
        print(f"│                                 │")
        print(f"│  {effect_description}")
        print(f"└─────────────────────────────────┘")
        time.sleep(1)
    
    def show_random_encouragement(self):
        """显示随机鼓励语"""
        encouragement = random.choice(self.encouragements)
        print(f"\n{self.colorize(encouragement, 'green')}")
        time.sleep(0.5)
    
    def trigger_random_event(self):
        """触发随机事件"""
        if random.random() < 0.2:  # 20%概率
            event = random.choice(self.random_events)
            print(f"\n{'='*50}")
            print(self.colorize("🎲 天机变化！", 'purple'))
            print(f"{'='*50}")
            self.print_with_delay(event, 0.05)
            print(f"{'='*50}")
            return True
        return False
    
    def show_player_status(self, player_name, qi, dao_xing, cheng_yi):
        """显示玩家状态（增强版）"""
        print(f"\n📊 {self.colorize(player_name, 'bold')} 的状态：")
        
        # 气的进度条
        qi_bar = "█" * qi + "░" * (10 - qi)
        print(f"   ⚡ 气:     [{self.colorize(qi_bar, 'blue')}] {qi}/10")
        
        # 道行的进度条  
        dao_bar = "█" * dao_xing + "░" * (20 - dao_xing)
        print(f"   🧘 道行:   [{self.colorize(dao_bar, 'purple')}] {dao_xing}/20")
        
        # 诚意的进度条
        cheng_bar = "█" * cheng_yi + "░" * (10 - cheng_yi)
        print(f"   💎 诚意:   [{self.colorize(cheng_bar, 'yellow')}] {cheng_yi}/10")
    
    def show_battle_result(self, attacker, defender, result):
        """显示战斗结果动画"""
        print(f"\n⚔️  {attacker} VS {defender}")
        
        # 战斗动画
        animations = ["   ⚡", "   💥", "   🌟"]
        for anim in animations:
            print(f"\r{anim}", end='', flush=True)
            time.sleep(0.5)
        
        print(f"\n\n🏆 结果：{self.colorize(result, 'green')}")
    
    def show_victory_celebration(self, winner):
        """显示胜利庆祝"""
        celebration = f"""
    🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉
    
         🏆 {winner} 获得胜利！ 🏆
         
    🎊 恭喜！你已掌握天机变化！ 🎊
    
    🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉
        """
        print(self.colorize(celebration, 'yellow'))
        
        # 烟花效果
        for i in range(3):
            print("✨ " * 20)
            time.sleep(0.3)
    
    def show_tutorial_hint(self, hint_text):
        """显示教程提示"""
        print(f"\n💡 {self.colorize('提示', 'cyan')}: {hint_text}")
    
    def show_menu_enhanced(self, title, options):
        """显示增强版菜单"""
        print(f"\n╔{'═' * (len(title) + 4)}╗")
        print(f"║  {self.colorize(title, 'bold')}  ║")
        print(f"╚{'═' * (len(title) + 4)}╝")
        
        for i, option in enumerate(options, 1):
            print(f"  {self.colorize(str(i), 'cyan')}. {option}")
        print()
    
    def show_loading(self, text="处理中", duration=2):
        """显示加载动画"""
        chars = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
        end_time = time.time() + duration
        
        while time.time() < end_time:
            for char in chars:
                print(f"\r{char} {text}...", end='', flush=True)
                time.sleep(0.1)
                if time.time() >= end_time:
                    break
        
        print(f"\r✅ {text}完成！")
    
    def show_card_selection_enhanced(self, cards):
        """显示增强版卡牌选择"""
        print(f"\n🃏 {self.colorize('选择你的卦象', 'bold')}")
        print("┌─────────────────────────────────────┐")
        
        for i, card in enumerate(cards, 1):
            gua_name = card.get('name', '未知')
            symbol = self.gua_symbols.get(gua_name, '◯')
            cost = card.get('qi_cost', 0)
            
            print(f"│ {i}. {symbol} {gua_name:<8} (消耗: {cost}气) │")
        
        print("└─────────────────────────────────────┘")
    
    def show_game_tips(self):
        """显示游戏小贴士"""
        tips = [
            "💡 合理分配气的使用，不要一次性用完",
            "🎯 观察对手的策略，适时调整自己的战术", 
            "🌟 道行越高，可使用的高级卦象越多",
            "⚖️ 平衡攻击和防御，不要过于激进",
            "🔄 善用卦象的组合效果，创造意想不到的结果"
        ]
        
        tip = random.choice(tips)
        print(f"\n{self.colorize('游戏小贴士', 'cyan')}: {tip}")

# 集成函数 - 可以直接在现有代码中调用
def enhance_game_output(func):
    """装饰器：为游戏输出添加增强效果"""
    def wrapper(*args, **kwargs):
        enhancer = QuickEnhancements()
        
        # 添加随机事件
        enhancer.trigger_random_event()
        
        # 执行原函数
        result = func(*args, **kwargs)
        
        # 添加鼓励语
        if random.random() < 0.3:  # 30%概率
            enhancer.show_random_encouragement()
        
        return result
    return wrapper

def add_visual_flair(text, style='normal'):
    """为文本添加视觉效果"""
    enhancer = QuickEnhancements()
    
    if style == 'title':
        return enhancer.colorize(text, 'bold')
    elif style == 'success':
        return enhancer.colorize(text, 'green')
    elif style == 'warning':
        return enhancer.colorize(text, 'yellow')
    elif style == 'error':
        return enhancer.colorize(text, 'red')
    elif style == 'info':
        return enhancer.colorize(text, 'cyan')
    else:
        return text

# 使用示例
if __name__ == "__main__":
    enhancer = QuickEnhancements()
    
    # 演示各种增强效果
    enhancer.show_welcome_animation()
    enhancer.show_player_status("玩家1", 8, 5, 7)
    enhancer.show_gua_effect("乾", "增加3点攻击力")
    enhancer.trigger_random_event()
    enhancer.show_game_tips()
    enhancer.show_victory_celebration("玩家1")