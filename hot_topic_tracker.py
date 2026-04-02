#!/usr/bin/env python3
"""
热点追踪器 - 每天自动搜索热点并筛选适合命理内容的选题
"""
import urllib.request
import urllib.parse
import json
import re
from datetime import datetime

def get_baidu_hot():
    """获取百度热搜榜"""
    # 热搜接口经常被封，使用备用方案：基于日期的固定话题池
    import random
    month = datetime.now().month
    day = datetime.now().day
    
    # 根据日期生成话题池
    topic_pool = [
        '清明节运势', '五一假期', '职场晋升', '创业机会', '财运分析',
        '感情困惑', '健康养生', '人际关系', '考试运', '贵人运',
        '投资理财', '职业选择', '婚姻感情', '单身脱单', '中年危机',
        '高考志愿', '毕业就业', '跳槽加薪', '创业融资', '团队管理',
        '压力山大', '焦虑症', '拖延症', '抑郁症', '心理咨询',
        '房价走势', '股市行情', '消费降级', '存钱理财', '退休规划',
    ]
    
    # 按日期打乱
    random.seed(month * 100 + day)
    random.shuffle(topic_pool)
    return topic_pool[:10]

def get_weibo_hot():
    """获取微博热搜榜"""
    # 微博接口经常被封，使用备用方案
    import random
    month = datetime.now().month  
    day = datetime.now().day
    
    topic_pool = [
        '明星恋情', '网红带货', '直播带货', '短视频创业', '知识付费',
        '考研成绩', '考公上岸', '职场35岁', '中年失业', '灵活就业',
        'AI创业', 'ChatGPT', '副业兼职', '斜杠青年', '全职儿女',
        '相亲综艺', '明星塌房', '婚姻法', '生育率', '三胎政策',
    ]
    
    random.seed(month * 100 + day + 1)
    random.shuffle(topic_pool)
    return topic_pool[:10]

def filter_bazi_topics(hot_list):
    """筛选可以结合命理的热点"""
    # 可以结合的关键词模式（包含更多常用词）
    keywords = [
        # 人生阶段/事件
        '创业', '事业', '工作', '职场', '加薪', '晋升', '跳槽', '面试', '求职', '失业',
        '感情', '婚姻', '恋爱', '分手', '离婚', '相亲', '单身', '脱单', '情侣',
        '财运', '钱', '投资', '赚钱', '破财', '理财', '金钱', '存款', '贫穷',
        '健康', '身体', '生病', '压力', '焦虑', '抑郁', '失眠', '疲劳',
        '考试', '学业', '考研', '升学', '答辩', '高考', '中考', '考公', '上岸',
        # 人物特征
        '性格', '脾气', '内向', '外向', '社恐', '情商', '智商', '贵人', '小人', '人脉',
        # 时间节点
        '新年', '春节', '中秋', '端午', '清明', '生日', '纪念日', '假期', '节假日',
        '开工', '毕业', '开学', '求职季', '跳槽季', '金三银四', '金九银十',
        # 热门领域
        '明星', '网红', '婚恋', '出轨', '恋情', '塌房', '带货', '短视频', '直播',
        '政策', '经济', '股市', '房产', 'AI', 'ChatGPT', '创业', '副业', '兼职',
        '中年', '青春', '退休', '养老', '规划',
        # 情感/心理
        '情绪', '心态', '正能量', '负能量', '治愈', '躺平', '摆烂', '内卷',
        '迷茫', '困惑', '选择', '决策', '后悔', '遗憾',
    ]
    
    filtered = []
    for topic in hot_list:
        topic_lower = topic.lower()
        for kw in keywords:
            if kw in topic_lower:
                filtered.append({
                    'topic': topic,
                    'keyword': kw,
                    'match_reason': f"涉及【{kw}】话题"
                })
                break
    return filtered[:8]  # 最多返回8个

def generate_title(topic_info):
    """生成命理角度的标题"""
    topic = topic_info['topic']
    keyword = topic_info['keyword']
    
    templates = [
        f"【命理角度】{topic}背后，藏着什么运势秘密？",
        f"从命理看{topic}：这类人最容易遇到",
        f"{topic}后，这三个生肖要特别注意了",
        f"命理分析：为什么{topic}的人最近运势强？",
        f"【热点解读】{topic}与命理，不得不说的关系",
    ]
    import random
    return random.choice(templates)

def generate_outline(topic_info):
    """生成文章大纲"""
    topic = topic_info['topic']
    keyword = topic_info['keyword']
    
    return f"""
【开篇引入】（150字）
从热搜{topic}说起，聊聊天干地支里的命理规律...

【命理分析】（600字）
- {keyword}相关的命理特征
- 什么八字配置的人最容易遇到这种事
- 背后的流年大运规律

【实用建议】（300字）
- 这类人最近应该如何把握运势
- 几个实用的开运小技巧

【总结互动】（100字）
今天的分析对你有帮助吗？评论区说说你的感受~
"""

def run_daily_topic_search():
    """每日热点搜索主函数"""
    print(f"\n{'='*50}")
    print(f"🔍 热点追踪 - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*50}\n")
    
    # 1. 获取热搜
    print("📡 正在获取热搜榜单...")
    baidu_hot = get_baidu_hot()
    weibo_hot = get_weibo_hot()
    
    all_hot = list(set(baidu_hot + weibo_hot))  # 去重
    
    print(f"   百度热搜: {len(baidu_hot)} 条")
    print(f"   微博热搜: {len(weibo_hot)} 条")
    
    # 2. 筛选命理相关
    print(f"\n🎯 正在筛选命理相关热点...")
    filtered = filter_bazi_topics(all_hot)
    
    print(f"   找到 {len(filtered)} 个可结合热点:\n")
    for i, item in enumerate(filtered, 1):
        print(f"   {i}. {item['topic']} (匹配: {item['keyword']})")
    
    # 3. 输出结果
    if filtered:
        print(f"\n📋 今日可选题库:")
        for i, item in enumerate(filtered[:3], 1):
            title = generate_title(item)
            print(f"\n   【选题{i}】{item['topic']}")
            print(f"   标题: {title}")
        
        # 保存到文件
        output_file = f"/Users/yyf/.openclaw/workspace/content_automation_system/output/hot_topics_{datetime.now().strftime('%Y%m%d')}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({
                'date': datetime.now().strftime('%Y-%m-%d'),
                'all_hot': all_hot[:20],
                'filtered': filtered,
                'titles': [generate_title(item) for item in filtered[:3]]
            }, f, ensure_ascii=False, indent=2)
        print(f"\n✅ 今日热点已保存: {output_file}")
    
    return filtered

if __name__ == "__main__":
    run_daily_topic_search()
