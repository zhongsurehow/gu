#!/usr/bin/env python3
"""
修复Windows环境下的Unicode编码问题
将emoji字符替换为兼容的文本符号
"""

import os
import re
import sys

# emoji到文本的映射
EMOJI_REPLACEMENTS = {
    '🎋': '===',
    '🎮': '[游戏]',
    '🃏': '[卡牌]',
    '👤': '[玩家]',
    '📋': '[列表]',
    '🗺️': '[地图]',
    '🎯': '[目标]',
    '🔧': '[修复]',
    '🚀': '[启动]',
    '💡': '[提示]',
    '🎉': '[成功]',
    '⚠️': '[警告]',
    '❌': '[错误]',
    '✅': '[完成]',
    '📤': '[输入]',
    '📥': '[输出]',
    '📊': '[统计]',
    '🧪': '[测试]',
    '⏰': '[时间]',
    '🏛️': '[区域]',
    '⚔️': '[战斗]',
    '🌫️': '[空白]',
    '☯️': '[阴阳]',
    '⚖️': '[平衡]',
    'ℹ️': '[信息]',
    '🧙': '[法师]',
    '⏳': '[等待]',
    '🏷️': '[标签]',
    '🌟': '[星]',
    '⭐': '[星]',
    '✨': '[闪]',
    '🔥': '[火]',
    '⚡': '[电]',
    '💎': '[钻]',
    '💫': '[星]',
    '📚': '[书]',
    '📖': '[书]',
    '📝': '[笔]',
    '📄': '[页]',
    '📜': '[卷]',
}

def fix_unicode_in_file(file_path):
    """修复单个文件中的Unicode问题"""
    try:
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 替换emoji字符
        for emoji, replacement in EMOJI_REPLACEMENTS.items():
            content = content.replace(emoji, replacement)
        
        # 如果内容有变化，写回文件
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
        
    except Exception as e:
        print(f"处理文件 {file_path} 时出错: {e}")
        return False

def main():
    """主函数"""
    print("开始修复Unicode编码问题...")
    
    # 需要处理的文件列表
    files_to_fix = [
        'main.py',
        'test_interaction.py',
        'demo_fixed.py',
        'test_game_basic.py',
        'achievement_system.py',
        'tutorial_system.py',
        'ui_enhancement.py',
        'advanced_ui_system.py',
        'actions.py',
        'yijing_actions.py',
        'enhanced_victory.py',
        'wisdom_system.py',
        'enhanced_cards.py',
        'tianshi_system.py',
        'complete_enhanced_game.py',
        'core/logging_system.py',
        'test_systems_integration.py'
    ]
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    fixed_count = 0
    
    for filename in files_to_fix:
        file_path = os.path.join(current_dir, filename)
        if os.path.exists(file_path):
            if fix_unicode_in_file(file_path):
                print(f"[完成] 修复了 {filename}")
                fixed_count += 1
            else:
                print(f"[跳过] {filename} 无需修复")
        else:
            print(f"[警告] 文件不存在: {filename}")
    
    print(f"\n修复完成！共处理了 {fixed_count} 个文件")
    print("现在游戏应该可以在Windows环境下正常运行了")

if __name__ == "__main__":
    main()