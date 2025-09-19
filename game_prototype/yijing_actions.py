"""
集成易经哲学的增强动作系统
包含阴阳平衡、五行相生相克、变卦等机制
"""

import copy
import random
from typing import Optional, List, Dict

from game_state import GameState, Player, Zone
from yijing_mechanics import (
    YinYang, WuXing, YinYangBalance, WuXingCycle, TaijiMechanism, 
    ZhouYiWisdom, GUA_ATTRIBUTES, get_gua_synergy_bonus
)
from game_data import GAME_DECK

def apply_yin_yang_effect(player: Player, yin_yang: YinYang, points: int = 1):
    """应用阴阳效果"""
    if yin_yang == YinYang.YIN:
        player.yin_yang_balance.yin_points += points
    else:
        player.yin_yang_balance.yang_points += points

def apply_wuxing_effect(player: Player, element: WuXing, points: int = 1):
    """应用五行效果"""
    player.wuxing_affinities[element] += points
    
    # 检查五行相生效果
    target_element = WuXingCycle.get_sheng_target(element)
    if player.wuxing_affinities[element] >= 3:
        player.wuxing_affinities[target_element] += 1
        return f"五行相生：{element.value}生{target_element.value}"
    
    return None

def enhanced_play_card(game_state: GameState, card_index: int, target_gua: str, mods=None) -> GameState:
    """增强的打牌动作，集成易经哲学机制"""
    new_state = copy.deepcopy(game_state)
    current_player = new_state.get_current_player()
    
    if card_index >= len(current_player.hand):
        return new_state
    
    card = current_player.hand[card_index]
    
    # 基础打牌逻辑
    current_player.hand.pop(card_index)
    
    # 获取卦象属性
    gua_attr = GUA_ATTRIBUTES.get(target_gua, {})
    if gua_attr:
        # 应用阴阳效果
        apply_yin_yang_effect(current_player, gua_attr["yin_yang"], 1)
        
        # 应用五行效果
        wuxing_msg = apply_wuxing_effect(current_player, gua_attr["wuxing"], 1)
        if wuxing_msg:
            print(f"[星] {wuxing_msg}")
    
    # 检查卦象协同效果
    if len(card.associated_guas) == 2:
        synergy_bonus = get_gua_synergy_bonus(card.associated_guas[0], card.associated_guas[1])
        if synergy_bonus > 0:
            current_player.dao_xing += synergy_bonus
            print(f"🔮 卦象协同奖励：+{synergy_bonus}道行")
    
    # 应用太极转化机制
    current_player.yin_yang_balance = TaijiMechanism.apply_transformation(current_player.yin_yang_balance)
    
    # 检查阴阳平衡奖励
    balance_bonus = current_player.yin_yang_balance.get_balance_bonus()
    if balance_bonus > 0:
        current_player.qi += balance_bonus
        print(f"[阴阳] 阴阳平衡奖励：+{balance_bonus}气")
    
    return new_state

def enhanced_meditate(game_state: GameState, mods=None) -> GameState:
    """增强的冥想动作，体现易经修行理念"""
    new_state = copy.deepcopy(game_state)
    current_player = new_state.get_current_player()
    
    # 基础冥想效果
    base_qi = 3
    position_bonus = 0
    
    # 根据位置获得不同的修行效果
    if current_player.position == Zone.TIAN:
        position_bonus = 2
        apply_yin_yang_effect(current_player, YinYang.YANG, 2)
        print("🌅 天部修行：阳气充盈")
    elif current_player.position == Zone.REN:
        position_bonus = 1
        # 人部平衡阴阳
        if current_player.yin_yang_balance.yin_points > current_player.yin_yang_balance.yang_points:
            apply_yin_yang_effect(current_player, YinYang.YANG, 1)
        else:
            apply_yin_yang_effect(current_player, YinYang.YIN, 1)
        print("[平衡] 人部修行：调和阴阳")
    elif current_player.position == Zone.DI:
        position_bonus = 0
        apply_yin_yang_effect(current_player, YinYang.YIN, 2)
        print("🌙 地部修行：阴气深厚")
    
    current_player.qi += base_qi + position_bonus
    
    # 检查是否激活智慧格言
    wisdom_activated = ZhouYiWisdom.check_wisdom_activation({}, [])
    current_player.active_wisdom.extend(wisdom_activated)
    
    return new_state

def divine_fortune(game_state: GameState) -> GameState:
    """占卜运势 - 易经核心功能"""
    from yijing_mechanics import ZhanBuSystem
    
    new_state = copy.deepcopy(game_state)
    current_player = new_state.get_current_player()
    
    # 消耗资源 (降低成本提高使用频率)
    if current_player.qi < 2:
        print(f"[错误] {current_player.name} 气不足，无法进行占卜（需要2点气）")
        return new_state
    
    current_player.qi -= 2
    
    # 进行占卜
    divination = ZhanBuSystem.divine_fortune(current_player.dao_xing)
    
    # 检查是否有快速增强功能
    try:
        from quick_enhancements import QuickEnhancements
        enhancer = QuickEnhancements()
        
        # 显示占卜动画
        enhancer.show_loading_animation(f"{current_player.name} 正在占卜", 3)
        enhancer.show_hexagram_effect(divination['gua'])
        
        # 增强版占卜结果显示
        print(enhancer.apply_color(f"\n🔮 {current_player.name} 占卜结果", "mystical"))
        print(enhancer.apply_color(f"[卷] 得卦：{divination['gua']}", "highlight"))
        print(enhancer.apply_color(f"[星] 运势：{divination['fortune']}", "success" if "吉" in divination['fortune'] else "warning"))
        print(enhancer.apply_color(f"[提示] 建议：{divination['advice']}", "info"))
    except ImportError:
        # 基础版显示
        print(f"\n🔮 {current_player.name} 开始占卜...")
        print(f"[卷] 得卦：{divination['gua']}")
        print(f"[星] 运势：{divination['fortune']}")
        print(f"[提示] 建议：{divination['advice']}")
    
    # 根据占卜结果给予奖励
    fortune_rewards = {
        "大吉": {"dao_xing": 2, "qi": 1},
        "中吉": {"dao_xing": 1, "qi": 1}, 
        "小吉": {"dao_xing": 1, "qi": 0},
        "平": {"dao_xing": 0, "qi": 0},
        "小凶": {"dao_xing": 0, "qi": -1},
        "中凶": {"dao_xing": -1, "qi": -1},
        "大凶": {"dao_xing": -1, "qi": -2}
    }
    
    reward = fortune_rewards[divination['fortune']]
    current_player.dao_xing = max(0, min(20, current_player.dao_xing + reward['dao_xing']))
    current_player.qi = max(0, min(25, current_player.qi + reward['qi']))
    
    if reward['dao_xing'] > 0 or reward['qi'] > 0:
        print(f"[闪] 吉卦显灵，获得奖励！")
    elif reward['dao_xing'] < 0 or reward['qi'] < 0:
        print(f"[警告] 凶卦警示，需要谨慎行事...")
    
    return new_state

def consult_yijing(game_state: GameState, action_type: str) -> GameState:
    """咨询易经指导特定行动"""
    from yijing_mechanics import ZhanBuSystem
    
    new_state = copy.deepcopy(game_state)
    current_player = new_state.get_current_player()
    
    # 消耗资源
    if current_player.dao_xing < 2:
        print(f"[错误] {current_player.name} 道行不足，无法咨询易经（需要2点道行）")
        return new_state
    
    current_player.dao_xing -= 1
    
    # 占卜行动成功率
    success_predicted = ZhanBuSystem.divine_action_outcome(action_type, current_player.dao_xing)
    
    action_names = {
        "meditate": "冥想修行",
        "study": "研习经典", 
        "transform": "变卦转化",
        "wuxing": "五行调和"
    }
    
    action_name = action_names.get(action_type, action_type)
    
    if success_predicted:
        print(f"[星] 易经指引：{action_name}时机成熟，宜行动")
        # 给予行动加成
        if not hasattr(current_player, 'action_bonus'):
            current_player.action_bonus = 0
        current_player.action_bonus += 1
    else:
        print(f"[警告] 易经警示：{action_name}时机未到，宜等待")
        # 给予防护加成
        if not hasattr(current_player, 'defense_bonus'):
            current_player.defense_bonus = 0
        current_player.defense_bonus += 1
    
    return new_state

def enhanced_study(game_state: GameState, mods=None) -> GameState:
    """增强的学习动作，体现易经求知精神"""
    new_state = copy.deepcopy(game_state)
    current_player = new_state.get_current_player()
    
    # 基础学习效果
    cards_to_draw = 2
    
    # 根据五行亲和力调整学习效果
    dominant_element = max(current_player.wuxing_affinities, key=current_player.wuxing_affinities.get)
    if current_player.wuxing_affinities[dominant_element] >= 5:
        cards_to_draw += 1
        print(f"[书] {dominant_element.value}行精通：额外抽取1张卡牌")
    
    # 抽取卡牌
    for _ in range(cards_to_draw):
        if GAME_DECK:
            card = random.choice(GAME_DECK)
            current_player.hand.append(card)
    
    # 学习获得智慧
    if len(current_player.hand) >= 7:
        current_player.dao_xing += 2
        print("🎓 博学多才：+2道行")
    elif len(current_player.hand) >= 5:
        current_player.dao_xing += 1
        print("[书] 学有所成：+1道行")
    
    return new_state

def biangua_transformation(game_state: GameState, source_gua: str, target_gua: str) -> Optional[GameState]:
    """变卦机制：将一个卦象转化为另一个"""
    new_state = copy.deepcopy(game_state)
    current_player = new_state.get_current_player()
    
    # 检查是否有足够的资源进行变卦
    cost = 3  # 变卦需要消耗3点诚意
    if current_player.cheng_yi < cost:
        return None
    
    current_player.cheng_yi -= cost
    
    # 记录变卦历史
    transformation = f"{source_gua}→{target_gua}"
    current_player.transformation_history.append(transformation)
    
    # 变卦效果：获得目标卦的属性加成
    target_attr = GUA_ATTRIBUTES.get(target_gua, {})
    if target_attr:
        apply_yin_yang_effect(current_player, target_attr["yin_yang"], 2)
        apply_wuxing_effect(current_player, target_attr["wuxing"], 2)
    
    # 检查是否有快速增强功能
    try:
        from quick_enhancements import QuickEnhancements
        enhancer = QuickEnhancements()
        
        # 显示变卦动画
        enhancer.show_loading_animation(f"{current_player.name} 正在变卦", 2)
        enhancer.show_hexagram_effect(target_gua)
        
        # 增强版变卦成功显示
        print(enhancer.apply_color(f"🔄 变卦成功：{transformation}", "success"))
        print(enhancer.apply_color(f"[闪] 获得 {target_gua} 的力量加持！", "highlight"))
        
        # 随机显示变卦智慧
        wisdom_quotes = [
            "穷则变，变则通，通则久",
            "易者，变也。不变则无以应万变",
            "天行健，君子以自强不息",
            "变化者，进退之象也"
        ]
        import random
        print(enhancer.apply_color(f"[智慧] {random.choice(wisdom_quotes)}", "mystical"))
        
    except ImportError:
        # 基础版显示
        print(f"🔄 变卦成功：{transformation}")
    
    return new_state

def wuxing_interaction(game_state: GameState, element1: WuXing, element2: WuXing) -> GameState:
    """五行相互作用"""
    new_state = copy.deepcopy(game_state)
    current_player = new_state.get_current_player()
    
    if WuXingCycle.is_sheng_relationship(element1, element2):
        # 相生：增强效果
        current_player.qi += 2
        current_player.dao_xing += 1
        print(f"🌱 五行相生：{element1.value}生{element2.value}，获得额外奖励")
    elif WuXingCycle.is_ke_relationship(element1, element2):
        # 相克：制衡效果
        current_player.wuxing_affinities[element2] = max(0, current_player.wuxing_affinities[element2] - 1)
        current_player.cheng_yi += 1
        print(f"[战斗] 五行相克：{element1.value}克{element2.value}，获得制衡之道")
    
    return new_state

def check_victory_conditions_enhanced(game_state: GameState) -> Optional[Player]:
    """增强的胜利条件检查，体现易经智慧的多元化成就"""
    for player in game_state.players:
        # 1. 大道至简路径 - 道行修为达到高深境界
        if player.dao_xing >= 12:
            print(f"🏆 {player.name} 通过大道至简之路获胜！道行已臻化境")
            return player
        
        # 2. 太极宗师路径 - 阴阳平衡的极致体现
        if player.yin_yang_balance.balance_ratio >= 0.85 and player.dao_xing >= 8:
            print(f"🏆 {player.name} 通过太极宗师之道获胜！阴阳调和，天人合一")
            return player
        
        # 3. 五行圆满路径 - 五行亲和力均衡发展
        total_wuxing = sum(player.wuxing_affinities.values())
        min_wuxing = min(player.wuxing_affinities.values())
        if total_wuxing >= 15 and min_wuxing >= 2:
            print(f"🏆 {player.name} 通过五行圆满之道获胜！五行调和，生生不息")
            return player
        
        # 4. 变化之道路径 - 深谙变化规律
        if hasattr(player, 'transformation_history') and len(player.transformation_history) >= 5 and player.dao_xing >= 6:
            print(f"🏆 {player.name} 通过变化之道获胜！穷则变，变则通，通则久")
            return player
        
        # 5. 中庸之道路径 - 各项修为均衡发展
        if (player.dao_xing >= 8 and 
            player.yin_yang_balance.balance_ratio >= 0.7 and
            total_wuxing >= 10 and
            player.qi >= 15):
            print(f"🏆 {player.name} 通过中庸之道获胜！不偏不倚，和而不同")
            return player
    
    return None

def display_yijing_status(player: Player):
    """显示玩家的易经修行状态"""
    print(f"\n[统计] {player.name} 的修行状态:")
    print(f"   [阴阳]  阴阳平衡: 阴{player.yin_yang_balance.yin_points} 阳{player.yin_yang_balance.yang_points} (平衡度: {player.yin_yang_balance.balance_ratio:.2f})")
    
    print(f"   [星] 五行亲和力:")
    for element, affinity in player.wuxing_affinities.items():
        print(f"      {element.value}: {affinity}")
    
    if player.active_wisdom:
        print(f"   [提示] 激活智慧: {', '.join(player.active_wisdom)}")
    
    if player.transformation_history:
        print(f"   🔄 变卦历史: {' → '.join(player.transformation_history[-3:])}")  # 显示最近3次变卦