#!/usr/bin/env python3
"""
每日三篇文章生成器 - 热点选题 + 命理角度 + 人设风格
"""
import json
import random
from datetime import datetime, date

# 人设配置
PERSONA = {
    'name': '凌墨',
    'style': '温暖、专业、实用',
    'avatar': '从事命理研究20年，创业者出身，懂企业管理和职场心理',
    'tone': '用聊天的口吻，像朋友一样分享命理智慧',
    'avoid': ['一定', '绝对', '迷信', '算命', '破财', '死亡']
}

# 三篇文章的时间分配
ARTICLE_SLOTS = {
    'morning': {
        'time': '07:00-08:00',
        'type': '热点借势类',
        'purpose': '蹭流量，扩大曝光',
        'length': '800-1200字'
    },
    'noon': {
        'time': '12:00-13:00', 
        'type': '知识科普类',
        'purpose': '建立专业信任',
        'length': '1000-1500字'
    },
    'evening': {
        'time': '18:00-19:00',
        'type': '互动/运势类',
        'purpose': '粘住粉丝',
        'length': '600-1000字'
    }
}

def read_hot_topics():
    """读取今日热点"""
    today = datetime.now().strftime('%Y%m%d')
    filepath = f"/Users/yyf/.openclaw/workspace/content_automation_system/output/hot_topics_{today}.json"
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('filtered', [])
    except:
        return []

def generate_article_1_hot_topic(topic_info):
    """第一篇：热点借势类"""
    topic = topic_info['topic']
    keyword = topic_info['keyword']
    
    templates = [
        f"""# 【命理热点】{topic}后，这三个生肖要特别注意

大家好，我是凌墨。

今天打开手机，满屏都是{topic}的消息。

作为从业二十年的命理师，我习惯用天干地支的角度来看这些社会现象。

**从命理角度看{topic}：**

这类事情的发生，往往跟流年、流月的气场变化有关。

我说三个近期特别需要注意的生肖：

**🐴 生肖马 — 感情变化**
地支午火被引动，最近在感情上容易有波动。已有伴侣的朋友，多沟通；单身的朋友，可能遇到让你心动的人。

**🐍 生肖蛇 — 事业转折**
巳火与午火相生，工作上可能有意外好消息。但注意口舌是非，低调行事。

**🐐 生肖羊 — 财运波动**
丑未冲土，财运上会有一些意外开支。提前做好预算，别冲动消费。

**凌墨建议：**
{topic}这件事，本质上是气场聚集的结果。与其围观吃瓜，不如借这个机会，看看自己的运势走向。

有什么问题，评论区聊聊。

——

🏷️ #命理热点 #热点解读 #生肖运势 #{keyword} #凌墨说命理

❤️ 温馨提示：命理分析仅供参考，人生道路还需自己努力把握。愿你把握当下，创造美好！""",
        
        f"""# 【深度解读】为什么{topic}的人，最近运势特别旺？

老铁们好，我是凌墨。

今天想聊聊{topic}这个话题。

从命理角度看，能在这个时间点遇到{keyword}相关事情的人，往往有几个共同特征：

**第一，八字里带有明显的燥土或旺火**

土代表稳重、积累；火代表热情、行动力。当流年流月加强了这部分能量，人就更容易做出成绩。

**第二，大运正处于上升期**

我看过几千个命盘，总结出一个规律：好运的人，遇到好事；背运的人，遇到坏事。这不是玄学，是气场共振。

**第三，身边有贵人相助**

有时候你遇到{topic}，不是你自己多厉害，而是你身边的人在推你。所以要懂得感恩，珍惜身边的贵人。

**凌墨总结：**
{topic}只是一个现象，背后反映的是你的运势阶段。如果你最近运势不错，大胆去做；如果感觉不顺，先休息调整。

关注我，每天分享一个命理硬核知识点。

——

🏷️ #命理 #运势分析 #{keyword} #创业者必看 #凌墨说命理

❤️ 温馨提示：命理分析仅供参考，人生道路还需自己努力把握。"""
    ]
    return random.choice(templates)

def generate_article_2_knowledge():
    """第二篇：知识科普类"""
    topics = [
        ('五行', '为什么你总觉得钱不够花？从五行看你缺什么'),
        ('十神', '正官与偏官的区别：看事业必懂的两种能量'),
        ('命格', '身旺财旺的人，有什么特点？'),
        ('大运', '如何判断自己正处于好运还是坏运？'),
        ('流年', '2026年哪些人运势爆发？命理师告诉你'),
    ]
    title, subtitle = random.choice(topics)
    
    templates = [
        f"""# 【{title}入门】{subtitle}

大家好，我是凌墨。

很多老铁问我：为什么你讲的命理听起来很有道理，但不知道怎么看自己的？

今天用一个案例，把最重要的概念讲清楚。

**什么是{title}？**

{title}是八字命理中最核心的概念之一。它描述的是天干地支之间的相互作用关系。

**怎么用？**

比如说，你八字里{title}比较旺，说明你在这个方面有天赋，或者容易在这个领域遇到机会。

反过来，如果{title}比较弱，可能在这个方面需要多注意。

**真实案例：**

之前有个学员，创业总是失败。我看他八字，发现他{title}很弱，于是建议他先积累再创业。一年后再见他，已经拿到融资了。

**凌墨金句：**
命理不是算命，是看规律。懂了自己的规律，做事才能事半功倍。

有收获的老铁，点个赞呗~

——

🏷️ #八字入门 #命理科普 #{title} #传统文化 #凌墨说命理

❤️ 温馨提示：命理分析仅供参考，人生道路还需自己努力把握。愿你把握当下，创造美好！""",
    ]
    return templates[0]

def generate_article_3_interaction():
    """第三篇：互动/运势类"""
    
    templates = [
        """# 【今日互动】测测你的命格核心能量是什么？

老铁们好，我是凌墨。

今天来个有趣的测试。

回想一下：当你压力大的时候，你第一反应是什么？

A. 找人倾诉吐槽
B. 默默自己消化
C. 运动出汗发泄
D. 疯狂购物吃东西

评论区告诉我你的答案，我来帮你分析你的命格核心能量~

——

🏷️ #互动话题 #命格测试 #评论区见 #凌墨说命理

❤️ 温馨提示：命理分析仅供参考，人生道路还需自己努力把握。愿你把握当下，创造美好！""",

        """# 【每日运势】今日干支：{} | 这三个生肖要重点注意

大家好，我是凌墨。

今天是{}，天干地支组合{}。

**今日整体运势：**
今日气场平和，适合处理日常事务，但要注意控制情绪。

**🌟 事业/学业：**
今天在处理文件、沟通谈判方面运势不错，有想法可以大胆提。

**💰 财运：**
正财运势稳定，偏财一般，别贪心。

**❤️ 感情：**
单身的朋友，今天有机会认识新朋友；有伴侣的，注意沟通方式。

**今日幸运色：** 白色、金色
**今日幸运方位：** 东方

有问题的老铁，评论区聊~

——

🏷️ #每日运势 #今日运势 #{}日 #凌墨说命理

❤️ 温馨提示：命理分析仅供参考，人生道路还需自己努力把握。愿你把握当下，创造美好！"""
    ]
    return random.choice(templates)

def generate_daily_articles():
    """生成每日三篇文章"""
    today = datetime.now().strftime('%Y-%m-%d')
    print(f"\n{'='*50}")
    print(f"📝 每日三篇文章生成 - {today}")
    print(f"{'='*50}\n")
    
    # 获取热点
    hot_topics = read_hot_topics()
    
    articles = []
    
    # 文章1：热点借势（需要热点）
    if hot_topics:
        topic = hot_topics[0]
        print(f"📡 文章1：热点借势 - {topic['topic']}")
        article1 = generate_article_1_hot_topic(topic)
    else:
        print("📡 文章1：使用备用话题（无热点）")
        article1 = generate_article_2_knowledge()  # 降级为科普
    
    articles.append({
        'slot': 'morning',
        'title': '热点借势类',
        'content': article1
    })
    
    # 文章2：知识科普
    print(f"📚 文章2：知识科普类")
    article2 = generate_article_2_knowledge()
    articles.append({
        'slot': 'noon',
        'title': '知识科普类', 
        'content': article2
    })
    
    # 文章3：互动/运势
    print(f"💬 文章3：互动/运势类")
    article3 = generate_article_3_interaction()
    articles.append({
        'slot': 'evening',
        'title': '互动/运势类',
        'content': article3
    })
    
    # 保存
    output_dir = f"/Users/yyf/.openclaw/workspace/content_automation_system/output/articles/{today}"
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    for i, article in enumerate(articles, 1):
        filename = f"{output_dir}/article_{i}_{article['slot']}.md"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(article['content'])
        print(f"   ✅ 文章{i}已保存: {filename}")
    
    # 输出摘要
    print(f"\n📋 今日产出摘要:")
    print(f"   🌅 早场(07:00-08:00): 热点借势类")
    print(f"   🌞 午场(12:00-13:00): 知识科普类")
    print(f"   🌙 晚场(18:00-19:00): 互动/运势类")
    
    return articles

if __name__ == "__main__":
    generate_daily_articles()
