#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""热点文章发布 - 蹭全网热搜流量"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from wechat_publisher import WechatPublisher
from ba_zi_analyzer import BaZiAnalyzer
from lunarcalendar import Converter, Solar
from datetime import date

def generate_ai_entrepreneur_article():
    """生成AI创业风口命理文章"""
    
    analyzer = BaZiAnalyzer()
    today = date.today()
    date_str = today.strftime("%Y-%m-%d")
    
    pillar = analyzer.calculate_bazi_pillar(date_str, "08:00")
    lunar = analyzer.convert_to_lunar(date_str)
    ri_zhu = pillar["ri_zhu"]
    ri_gan = ri_zhu[0]
    ri_zhi = ri_zhu[1]
    
    y, m, d = today.year, today.month, today.day
    solar = Solar(y, m, d)
    lunar_obj = Converter.Solar2Lunar(solar)
    lunar_str = f"{lunar_obj.year}年{lunar_obj.month}月{lunar_obj.day}日"
    
    wu_xing_map = {"甲": "木", "乙": "木", "丙": "火", "丁": "火", "戊": "土", "己": "土", "庚": "金", "辛": "金", "壬": "水", "癸": "水"}
    gan_wx = wu_xing_map.get(ri_gan, "木")
    zhi_wx_map = {"子": "水", "丑": "土", "寅": "木", "卯": "木", "辰": "土", "巳": "火", "午": "火", "未": "土", "申": "金", "酉": "金", "戌": "土", "亥": "水"}
    zhi_wx = zhi_wx_map.get(ri_zhi, "木")
    
    title = "男子靠AI年营收150万！命理解读3种命格"  # 小红书20字限制
    
    html = f"""<p style="text-align:center;"><strong>男子靠AI开一人公司年营收150万！命理揭示：这3种命格最易抓住AI风口</strong></p>
<p style="text-align:center;color:#b43c3c;">{lunar_str} · 凌墨命理</p>
<hr/>

<h2>一、事件回顾</h2>
<p>近日，一则"男子靠AI开一人公司年营收达150万"的消息刷屏热搜。</p>
<p>没有团队，没有合伙人，一台电脑+AI工具，一个人一年营收150万。这个故事正在成为现实。</p>
<p>很多人问：为什么是他？</p>
<p><strong>命理角度，答案藏在八字里。</strong></p>

<h2>二、从八字看：什么样的人最能抓住AI风口？</h2>

<h3>1. 日主为火（丙火、丁火）—— 创新者</h3>
<p>火主礼、主文明。丙火如太阳，光芒万丈、照耀四方；丁火如烛光，温暖细腻、照亮角落。</p>
<p>这类人天生对新生事物敏感，敢于第一个吃螃蟹。ChatGPT出来，最先尝试的是他们；AI工具出来，最先研究变现方法的也是他们。</p>
<p><strong style="color:#c83c3c;">🔥 命理特征：</strong>丙、丁日生，眼神明亮，做事雷厉风行，敢为人先。</p>

<h3>2. 日主为木（甲木、乙木）—— 连接者</h3>
<p>木主仁、主生发。木命人有一颗仁爱之心，善于发现别人的需求，并用自己的能力去满足它。</p>
<p>AI时代，真正的机会不是"取代谁"，而是"帮谁做得更好"。木命人天生具备这种商业嗅觉。</p>
<p><strong style="color:#3c783c;">🌱 命理特征：</strong>甲、乙日生，性格温和，人脉广泛，善于整合资源。</p>

<h3>3. 日主为水（壬水、癸水）—— 洞察者</h3>
<p>水主智、主流动。水命人思维活跃，善于发现趋势背后的规律。</p>
<p>AI时代的本质是效率革命。水命人能在海量信息中快速找到规律，把AI工具用到极致。</p>
<p><strong style="color:#2860b4;">💧 命理特征：</strong>壬、癸日生，头脑灵活，直觉敏锐，善于独立思考。</p>

<h2>三、这波AI浪潮，八字里早有信号</h2>
<p>从五行来看，AI属火——它是人类智慧的结晶，是文明之火。</p>
<p>2024-2026年，火气当令，正是AI发展最旺的年份。</p>
<p>日柱为火（丙寅、丁卯、丙午、丁巳等）的人，这几年运势最旺。</p>
<p>日支带火（寅、巳、午）的人，木火相生，也能搭上这波红利。</p>

<h2>四、今日{ri_zhu}，这3种命格如何抓住机会？</h2>

<h3>🔴 日主为火（丙、丁）—— 立即行动</h3>
<ul>
<li>你现在处于运势高峰，不要犹豫，立刻开始用AI工具</li>
<li>最适合方向：AI内容创作、AI工具开发、AI教育</li>
<li>今日能量加持：木火相生，宜快速推进</li>
</ul>

<h3>🟢 日主为木（甲、乙）—— 整合资源</h3>
<ul>
<li>你擅长连接人与资源，这是AI时代最稀缺的能力</li>
<li>最适合方向：AI服务中介、AI培训、AI解决方案</li>
<li>今日能量加持：木火相生，宜合作洽谈</li>
</ul>

<h3>🔵 日主为水（壬、癸）—— 深耕细分</h3>
<ul>
<li>你擅长深度思考，找到AI工具的最佳应用场景</li>
<li>最适合方向：AI数据分析、AI提示词工程、AI垂直应用</li>
<li>今日能量加持：智慧流动，宜规划布局</li>
</ul>

<h2>五、给所有人的建议</h2>
<p>不管你是什么命格，记住这3点：</p>
<ol>
<li><strong>用AI不是取代你，而是放大你。</strong>找到你最强的能力，让AI帮你放大100倍。</li>
<li><strong>一人公司是趋势。</strong>未来最有价值的人，是能用AI杠杆撬动资源的人。</li>
<li><strong>现在开始，永远不晚。</strong>AI还在早期，就像20年前的互联网，你现在的每一步都在决定5年后的位置。</li>
</ol>

<hr/>
<p><strong>💬 今日互动</strong></p>
<p>① 你是以上哪种命格？有没有感受到AI浪潮的机会？</p>
<p>② 你现在用AI做什么？欢迎留言分享！</p>
<p><strong>👇 想知道自己更适合哪个AI方向？发送出生年月日时，小墨帮你详细分析！</strong></p>
<p>更多命理干货、每日运势分析，关注我不迷路～</p>
<p>#AI创业 #一人公司 #人工智能 #命理 #八字 #财富自由 #创业 #副业 #被动收入 #五行能量 #凌墨</p>"""
    
    digest = f"靠AI年营收150万！命理揭示：这3种命格最易抓住AI风口"
    return title, html, digest


def main():
    publisher = WechatPublisher()
    
    print(f"\n{'='*50}")
    print(f"🔥 热点文章发布 | {date.today()}")
    print(f"选题：男子靠AI开一人公司年营收150万")
    print(f"{'='*50}")
    
    # 生成文章
    print("\n[1/4] 生成热点文章...")
    title, content, digest = generate_ai_entrepreneur_article()
    print(f"  标题: {title}")
    
    # 封面图 - 找最新的
    print("\n[2/4] 查找封面图...")
    image_path = None
    # 找最近生成的封面
    for root, dirs, files in os.walk(os.path.expanduser("~")):
        for f in files:
            if f.endswith(".png") and "openclaw" in root.lower():
                image_path = os.path.join(root, f)
                break
        if image_path:
            break
    
    # 找今日命理封面图
    if not image_path:
        today_dir = f"/Users/yyf/.openclaw/workspace/daily_content/{date.today().strftime('%Y-%m-%d')}/post_1_morning"
        if os.path.exists(today_dir):
            cover = os.path.join(today_dir, "cover_image.jpg")
            if os.path.exists(cover):
                image_path = cover
    
    # 用之前上传成功的media_id作为封面
    print(f"  封面图: {'找到本地图片' if image_path else '使用默认封面'}")
    
    # 上传封面
    print("\n[3/4] 上传封面...")
    if image_path and os.path.exists(image_path):
        thumb_id = publisher.upload_image(image_path)
    else:
        thumb_id = None
    
    if not thumb_id:
        # 用已知的有效media_id
        thumb_id = "P7pU8h-oLBTgbv4idTjk8fF-x362pPyYvsmykRm3I1EKtyDx4Rj5GHPKx1BNkrds"
        print("  使用默认封面")
    
    # 创建草稿
    print("\n[4/4] 创建草稿...")
    media_id = publisher.create_draft(title, content, thumb_id, digest=digest)
    
    print(f"\n{'='*50}")
    if media_id:
        print(f"✅ 发布成功! media_id: {media_id}")
        print(f"📝 请到微信公众号后台草稿箱查看并发布")
    else:
        print(f"❌ 发布失败")
    print(f"{'='*50}")


if __name__ == "__main__":
    main()
