"""
智慧格言系统增强版
提供更丰富的易经智慧和教育价值
"""

import random
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from game_state import Player, GameState

@dataclass
class WisdomQuote:
    """智慧格言数据结构"""
    id: str
    title: str
    content: str
    source: str
    category: str
    trigger_condition: str
    effect_description: str
    qi_bonus: int = 0
    dao_xing_bonus: int = 0
    cheng_yi_bonus: int = 0

class WisdomDatabase:
    """智慧格言数据库"""
    
    def __init__(self):
        self.quotes = self._initialize_quotes()
        self.categories = {
            "修行": "关于个人修养和精神提升",
            "平衡": "关于阴阳平衡和中庸之道", 
            "变化": "关于变化和适应",
            "智慧": "关于学习和智慧获得",
            "和谐": "关于人际关系和社会和谐",
            "自然": "关于自然规律和天人合一",
            "领导": "关于领导力和治理智慧",
            "品德": "关于道德品格和人格修养"
        }
    
    def _initialize_quotes(self) -> Dict[str, WisdomQuote]:
        """初始化智慧格言数据库"""
        quotes = {}
        
        # 修行类格言
        quotes["study_habit"] = WisdomQuote(
            id="study_habit",
            title="学而时习",
            content="学而时习之，不亦说乎？",
            source="论语·学而",
            category="修行",
            trigger_condition="连续学习3次",
            effect_description="学习行动获得额外道行",
            dao_xing_bonus=1
        )
        
        quotes["self_improvement"] = WisdomQuote(
            id="self_improvement",
            title="自强不息",
            content="天行健，君子以自强不息",
            source="易经·乾卦",
            category="修行",
            trigger_condition="道行达到5",
            effect_description="增强修行效果",
            qi_bonus=2
        )
        
        quotes["perseverance"] = WisdomQuote(
            id="perseverance",
            title="持之以恒",
            content="锲而舍之，朽木不折；锲而不舍，金石可镂",
            source="荀子·劝学",
            category="修行",
            trigger_condition="连续冥想5次",
            effect_description="冥想效果增强",
            qi_bonus=1,
            dao_xing_bonus=1
        )
        
        quotes["knowledge_stop"] = WisdomQuote(
            id="knowledge_stop",
            title="知止而后有定",
            content="知止而后有定，定而后能静，静而后能安",
            source="大学",
            category="修行",
            trigger_condition="冥想行动",
            effect_description="冥想行动获得额外气",
            qi_bonus=2
        )
        
        quotes["daily_reflection"] = WisdomQuote(
            id="daily_reflection",
            title="吾日三省吾身",
            content="吾日三省吾身：为人谋而不忠乎？与朋友交而不信乎？传不习乎？",
            source="论语·学而",
            category="修行",
            trigger_condition="每日反思",
            effect_description="自省增强诚意",
            cheng_yi_bonus=2
        )
        
        # 平衡类格言
        quotes["yin_yang_dao"] = WisdomQuote(
            id="yin_yang_dao",
            title="一阴一阳之谓道",
            content="一阴一阳之谓道，继之者善也，成之者性也",
            source="易经·系辞上",
            category="平衡",
            trigger_condition="阴阳平衡达到0.7",
            effect_description="阴阳平衡奖励翻倍",
            qi_bonus=3
        )
        
        quotes["middle_way"] = WisdomQuote(
            id="middle_way",
            title="中庸之道",
            content="中庸之为德也，其至矣乎",
            source="论语·雍也",
            category="平衡",
            trigger_condition="保持中庸状态3回合",
            effect_description="获得中庸奖励",
            dao_xing_bonus=2
        )
        
        quotes["harmony"] = WisdomQuote(
            id="harmony",
            title="和而不同",
            content="君子和而不同，小人同而不和",
            source="论语·子路",
            category="平衡",
            trigger_condition="五行达到平衡",
            effect_description="五行效果增强",
            cheng_yi_bonus=2
        )
        
        quotes["balance_virtue"] = WisdomQuote(
            id="balance_virtue",
            title="中庸之为德",
            content="中庸之为德也，其至矣乎！民鲜久矣",
            source="论语·雍也",
            category="平衡",
            trigger_condition="保持中庸状态奖励",
            effect_description="中庸状态下所有行动效果增强",
            qi_bonus=1,
            dao_xing_bonus=1,
            cheng_yi_bonus=1
        )
        
        # 变化类格言
        quotes["change_wisdom"] = WisdomQuote(
            id="change_wisdom",
            title="穷则变",
            content="穷则变，变则通，通则久",
            source="易经·系辞下",
            category="变化",
            trigger_condition="成功变卦5次",
            effect_description="变卦成功率提升",
            dao_xing_bonus=2
        )
        
        quotes["adaptation"] = WisdomQuote(
            id="adaptation",
            title="随时变化",
            content="君子豹变，其文蔚也",
            source="易经·革卦",
            category="变化",
            trigger_condition="适应环境变化",
            effect_description="适应能力增强",
            qi_bonus=1,
            cheng_yi_bonus=1
        )
        
        quotes["continuous_action"] = WisdomQuote(
            id="continuous_action",
            title="天行健",
            content="天行健，君子以自强不息",
            source="易经·乾卦",
            category="变化",
            trigger_condition="连续行动奖励",
            effect_description="连续行动获得额外奖励",
            qi_bonus=2
        )
        
        quotes["transformation_mastery"] = WisdomQuote(
            id="transformation_mastery",
            title="变通趋时",
            content="变通者，趋时者也",
            source="易经·系辞下",
            category="变化",
            trigger_condition="变卦成功时触发",
            effect_description="变卦技巧提升",
            dao_xing_bonus=1,
            cheng_yi_bonus=1
        )
        
        # 智慧类格言
        quotes["knowledge_action"] = WisdomQuote(
            id="knowledge_action",
            title="知行合一",
            content="知之真切笃实处即是行，行之明觉精察处即是知",
            source="王阳明",
            category="智慧",
            trigger_condition="理论与实践结合",
            effect_description="学习效果翻倍",
            dao_xing_bonus=3
        )
        
        quotes["wisdom_humility"] = WisdomQuote(
            id="wisdom_humility",
            title="知者不言",
            content="知者不言，言者不知",
            source="道德经",
            category="智慧",
            trigger_condition="道行达到10",
            effect_description="智慧深度提升",
            dao_xing_bonus=2
        )
        
        quotes["learning_joy"] = WisdomQuote(
            id="learning_joy",
            title="学而时习之",
            content="学而时习之，不亦说乎？有朋自远方来，不亦乐乎？",
            source="论语·学而",
            category="智慧",
            trigger_condition="学习行动+1道行",
            effect_description="学习带来快乐和成长",
            dao_xing_bonus=1,
            qi_bonus=1
        )
        
        quotes["wisdom_depth"] = WisdomQuote(
            id="wisdom_depth",
            title="博学而笃志",
            content="博学而笃志，切问而近思，仁在其中矣",
            source="论语·子张",
            category="智慧",
            trigger_condition="广泛学习",
            effect_description="博学增强智慧深度",
            dao_xing_bonus=2,
            cheng_yi_bonus=1
        )
        
        # 和谐类格言
        quotes["social_harmony"] = WisdomQuote(
            id="social_harmony",
            title="礼之用",
            content="礼之用，和为贵",
            source="论语·学而",
            category="和谐",
            trigger_condition="与他人和谐相处",
            effect_description="社交能力增强",
            cheng_yi_bonus=3
        )
        
        quotes["benevolence"] = WisdomQuote(
            id="benevolence",
            title="仁者爱人",
            content="仁者爱人，有礼者敬人",
            source="孟子",
            category="和谐",
            trigger_condition="帮助他人",
            effect_description="仁德增长",
            cheng_yi_bonus=2,
            dao_xing_bonus=1
        )
        
        quotes["mutual_benefit"] = WisdomQuote(
            id="mutual_benefit",
            title="己欲立而立人",
            content="己欲立而立人，己欲达而达人",
            source="论语·雍也",
            category="和谐",
            trigger_condition="互助合作",
            effect_description="合作精神增强",
            cheng_yi_bonus=2,
            qi_bonus=1
        )
        
        # 自然类格言
        quotes["nature_unity"] = WisdomQuote(
            id="nature_unity",
            title="天人合一",
            content="天人合一，万物与我为一",
            source="庄子",
            category="自然",
            trigger_condition="在不同位置修行",
            effect_description="自然亲和力增强",
            qi_bonus=2,
            dao_xing_bonus=2
        )
        
        quotes["natural_law"] = WisdomQuote(
            id="natural_law",
            title="道法自然",
            content="人法地，地法天，天法道，道法自然",
            source="道德经",
            category="自然",
            trigger_condition="遵循自然规律",
            effect_description="自然法则加成",
            qi_bonus=3
        )
        
        quotes["seasonal_wisdom"] = WisdomQuote(
            id="seasonal_wisdom",
            title="顺时而动",
            content="君子以顺德，积小以高大",
            source="易经·升卦",
            category="自然",
            trigger_condition="顺应时节",
            effect_description="时机把握能力增强",
            dao_xing_bonus=1,
            qi_bonus=2
        )
        
        # 领导类格言
        quotes["leadership"] = WisdomQuote(
            id="leadership",
            title="德治天下",
            content="为政以德，譬如北辰，居之所而众星共之",
            source="论语·为政",
            category="领导",
            trigger_condition="展现领导力",
            effect_description="领导能力提升",
            cheng_yi_bonus=3,
            dao_xing_bonus=1
        )
        
        quotes["humble_leadership"] = WisdomQuote(
            id="humble_leadership",
            title="无为而治",
            content="太上，不知有之；其次，亲而誉之",
            source="道德经",
            category="领导",
            trigger_condition="谦逊领导",
            effect_description="无为而治的智慧",
            dao_xing_bonus=3
        )
        
        quotes["servant_leadership"] = WisdomQuote(
            id="servant_leadership",
            title="先天下之忧而忧",
            content="先天下之忧而忧，后天下之乐而乐",
            source="范仲淹",
            category="领导",
            trigger_condition="服务他人",
            effect_description="服务型领导力",
            cheng_yi_bonus=3,
            dao_xing_bonus=1
        )
        
        # 品德类格言
        quotes["virtue"] = WisdomQuote(
            id="virtue",
            title="厚德载物",
            content="地势坤，君子以厚德载物",
            source="易经·坤卦",
            category="品德",
            trigger_condition="展现高尚品德",
            effect_description="品德修养提升",
            cheng_yi_bonus=2,
            dao_xing_bonus=2
        )
        
        quotes["integrity"] = WisdomQuote(
            id="integrity",
            title="诚意正心",
            content="诚意正心，修身齐家",
            source="大学",
            category="品德",
            trigger_condition="保持诚意",
            effect_description="诚意效果增强",
            cheng_yi_bonus=3
        )
        
        quotes["moral_cultivation"] = WisdomQuote(
            id="moral_cultivation",
            title="修身齐家",
            content="古之欲明明德于天下者，先治其国；欲治其国者，先齐其家",
            source="大学",
            category="品德",
            trigger_condition="品德修养",
            effect_description="道德修养全面提升",
            cheng_yi_bonus=2,
            dao_xing_bonus=1,
            qi_bonus=1
        )
        
        # 新增：实践类格言
        quotes["practice_wisdom"] = WisdomQuote(
            id="practice_wisdom",
            title="纸上得来终觉浅",
            content="纸上得来终觉浅，绝知此事要躬行",
            source="陆游",
            category="实践",
            trigger_condition="实践行动",
            effect_description="实践出真知",
            dao_xing_bonus=2
        )
        
        quotes["gradual_progress"] = WisdomQuote(
            id="gradual_progress",
            title="积土成山",
            content="积土成山，风雨兴焉；积水成渊，蛟龙生焉",
            source="荀子·劝学",
            category="实践",
            trigger_condition="持续努力",
            effect_description="积累的力量",
            qi_bonus=1,
            dao_xing_bonus=1
        )
        
        # 新增：时机类格言
        quotes["timing_wisdom"] = WisdomQuote(
            id="timing_wisdom",
            title="时乘六龙",
            content="时乘六龙以御天",
            source="易经·乾卦",
            category="时机",
            trigger_condition="把握时机",
            effect_description="时机把握能力",
            qi_bonus=2,
            dao_xing_bonus=1
        )
        
        quotes["patience_virtue"] = WisdomQuote(
            id="patience_virtue",
            title="君子藏器于身",
            content="君子藏器于身，待时而动",
            source="易经·系辞下",
            category="时机",
            trigger_condition="耐心等待",
            effect_description="耐心的智慧",
            cheng_yi_bonus=2
        )
        
        return quotes
    
    def get_quote(self, quote_id: str) -> Optional[WisdomQuote]:
        """获取指定的智慧格言"""
        return self.quotes.get(quote_id)
    
    def get_quotes_by_category(self, category: str) -> List[WisdomQuote]:
        """按类别获取智慧格言"""
        return [quote for quote in self.quotes.values() if quote.category == category]
    
    def get_random_quote(self, category: Optional[str] = None) -> WisdomQuote:
        """获取随机智慧格言"""
        if category:
            quotes = self.get_quotes_by_category(category)
        else:
            quotes = list(self.quotes.values())
        
        return random.choice(quotes) if quotes else None

class WisdomSystem:
    """智慧格言系统管理器"""
    
    def __init__(self):
        self.database = WisdomDatabase()
        self.player_activated_wisdom: Dict[str, set] = {}
        self.player_wisdom_progress: Dict[str, Dict[str, int]] = {}
    
    def get_player_wisdom(self, player_name: str) -> set:
        """获取玩家已激活的智慧"""
        if player_name not in self.player_activated_wisdom:
            self.player_activated_wisdom[player_name] = set()
        return self.player_activated_wisdom[player_name]
    
    def get_player_progress(self, player_name: str) -> Dict[str, int]:
        """获取玩家的智慧进度"""
        if player_name not in self.player_wisdom_progress:
            self.player_wisdom_progress[player_name] = {}
        return self.player_wisdom_progress[player_name]
    
    def check_wisdom_triggers(self, player: Player, action: str, context: Dict) -> List[WisdomQuote]:
        """检查智慧格言触发条件"""
        triggered_quotes = []
        player_wisdom = self.get_player_wisdom(player.name)
        player_progress = self.get_player_progress(player.name)
        
        # 检查各种触发条件
        for quote in self.database.quotes.values():
            if quote.id in player_wisdom:
                continue  # 已激活的智慧不重复触发
            
            triggered = False
            
            # 学习相关触发
            if quote.trigger_condition == "连续学习3次" and action == "study":
                player_progress["study_count"] = player_progress.get("study_count", 0) + 1
                if player_progress["study_count"] >= 3:
                    triggered = True
            
            # 冥想相关触发
            elif quote.trigger_condition == "连续冥想5次" and action == "meditate":
                player_progress["meditate_count"] = player_progress.get("meditate_count", 0) + 1
                if player_progress["meditate_count"] >= 5:
                    triggered = True
            
            # 道行相关触发
            elif quote.trigger_condition == "道行达到5" and player.dao_xing >= 5:
                triggered = True
            elif quote.trigger_condition == "道行达到10" and player.dao_xing >= 10:
                triggered = True
            
            # 阴阳平衡相关触发
            elif quote.trigger_condition == "阴阳平衡达到0.7" and player.yin_yang_balance.balance_ratio >= 0.7:
                triggered = True
            
            # 变卦相关触发
            elif quote.trigger_condition == "成功变卦5次" and action == "transform":
                player_progress["transform_count"] = player_progress.get("transform_count", 0) + 1
                if player_progress["transform_count"] >= 5:
                    triggered = True
            
            # 五行平衡相关触发
            elif quote.trigger_condition == "五行达到平衡":
                balanced_elements = sum(1 for affinity in player.wuxing_affinities.values() if affinity >= 3)
                if balanced_elements >= 3:
                    triggered = True
            
            # 位置修行相关触发
            elif quote.trigger_condition == "在不同位置修行" and action == "move":
                player_progress["positions_visited"] = player_progress.get("positions_visited", set())
                player_progress["positions_visited"].add(str(player.position))
                if len(player_progress["positions_visited"]) >= 3:
                    triggered = True
            
            if triggered:
                triggered_quotes.append(quote)
                player_wisdom.add(quote.id)
        
        return triggered_quotes
    
    def apply_wisdom_effects(self, player: Player, quote: WisdomQuote):
        """应用智慧格言的效果"""
        if quote.qi_bonus > 0:
            player.qi = min(25, player.qi + quote.qi_bonus)
        
        if quote.dao_xing_bonus > 0:
            player.dao_xing = min(20, player.dao_xing + quote.dao_xing_bonus)
        
        if quote.cheng_yi_bonus > 0:
            player.cheng_yi = min(15, player.cheng_yi + quote.cheng_yi_bonus)
    
    def display_wisdom_activation(self, quote: WisdomQuote):
        """显示智慧格言激活信息"""
        print(f"\n[闪] 智慧觉醒 [闪]")
        print(f"[卷] {quote.title}")
        print(f"💭 {quote.content}")
        print(f"[书] 出处：{quote.source}")
        print(f"[目标] 效果：{quote.effect_description}")
        
        effects = []
        if quote.qi_bonus > 0:
            effects.append(f"+{quote.qi_bonus}气")
        if quote.dao_xing_bonus > 0:
            effects.append(f"+{quote.dao_xing_bonus}道行")
        if quote.cheng_yi_bonus > 0:
            effects.append(f"+{quote.cheng_yi_bonus}诚意")
        
        if effects:
            print(f"🎁 奖励：{', '.join(effects)}")
        print("=" * 50)
    
    def get_wisdom_statistics(self, player_name: str) -> Dict:
        """获取玩家的智慧统计信息"""
        player_wisdom = self.get_player_wisdom(player_name)
        total_quotes = len(self.database.quotes)
        activated_count = len(player_wisdom)
        
        category_stats = {}
        for category in self.database.categories:
            category_quotes = self.database.get_quotes_by_category(category)
            activated_in_category = sum(1 for quote in category_quotes if quote.id in player_wisdom)
            category_stats[category] = {
                "total": len(category_quotes),
                "activated": activated_in_category,
                "percentage": (activated_in_category / len(category_quotes)) * 100 if category_quotes else 0
            }
        
        return {
            "total_quotes": total_quotes,
            "activated_count": activated_count,
            "completion_percentage": (activated_count / total_quotes) * 100,
            "category_stats": category_stats
        }
    
    def display_wisdom_progress(self, player_name: str):
        """显示玩家的智慧进度"""
        stats = self.get_wisdom_statistics(player_name)
        
        print(f"\n[统计] {player_name} 的智慧收集进度")
        print("=" * 50)
        print(f"总体进度: {stats['activated_count']}/{stats['total_quotes']} ({stats['completion_percentage']:.1f}%)")
        print("\n分类进度:")
        
        for category, data in stats['category_stats'].items():
            print(f"  {category}: {data['activated']}/{data['total']} ({data['percentage']:.1f}%)")
        
        print("=" * 50)
    
    def check_triggers(self, game_state, action_type=None, **kwargs):
        """检查并返回应该触发的智慧格言"""
        triggered_quotes = []
        
        for quote_id, quote in self.quotes.items():
            if quote_id in self.triggered_quotes:
                continue  # 已触发的格言不再重复触发
                
            should_trigger = False
            
            # 基于行动类型的触发检查
            if action_type:
                if action_type == "学习" and "学习" in quote.trigger_condition:
                    should_trigger = True
                elif action_type == "冥想" and "冥想" in quote.trigger_condition:
                    should_trigger = True
                elif action_type == "变卦" and "变卦" in quote.trigger_condition:
                    should_trigger = True
                elif action_type == "实践" and "实践" in quote.trigger_condition:
                    should_trigger = True
            
            # 基于游戏状态的触发检查
            if hasattr(game_state, 'player'):
                player = game_state.player
                
                # 道行相关触发
                if "道行达到5" in quote.trigger_condition and player.dao_xing >= 5:
                    should_trigger = True
                elif "道行达到10" in quote.trigger_condition and player.dao_xing >= 10:
                    should_trigger = True
                
                # 阴阳平衡触发
                if hasattr(player, 'yin_yang_balance'):
                    if "阴阳平衡达到0.7" in quote.trigger_condition and abs(player.yin_yang_balance) <= 0.3:
                        should_trigger = True
                
                # 诚意相关触发
                if "保持诚意" in quote.trigger_condition and player.cheng_yi >= 8:
                    should_trigger = True
            
            if should_trigger:
                triggered_quotes.append(quote)
                self.triggered_quotes.add(quote_id)
        
        return triggered_quotes

# 全局智慧系统实例
wisdom_system = WisdomSystem()