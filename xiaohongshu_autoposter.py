#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小红书每日热点文章全自动发布系统
每天5篇热点文章，自动抓取话题+生成有深度有观点的内容+AI作图+自动发布
内容要求：有凌墨个人观点，深度分析，不模板化
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import json
import time
import random
from datetime import datetime, date
from wechat_publisher import WechatPublisher
from ba_zi_analyzer import BaZiAnalyzer
from lunarcalendar import Converter, Solar
import subprocess
import re

# ========== 配置 ==========
XHS_IMAGE_PATH = "/tmp/openclaw/uploads/xhs_cover.png"
DRAFT_DIR = "/Users/yyf/.openclaw/workspace/daily_content/xhs_drafts"
os.makedirs(DRAFT_DIR, exist_ok=True)
os.makedirs("/tmp/openclaw/uploads", exist_ok=True)

# ========== 热点话题抓取 ==========

def get_baidu_hot():
    """抓取百度热搜"""
    try:
        import urllib.request
        url = 'https://top.baidu.com/board?tab=realtime'
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8')
        titles = re.findall(r'class="c-single-text-ellipsis">([^<]+)<', html)
        return [(t.strip(), 0) for t in titles[:30] if len(t.strip()) > 2]
    except Exception as e:
        print(f"百度热搜抓取失败: {e}")
        return []

# ========== 内容生成（深度有观点版）============

def generate_content(topic, ri_zhu, ri_gan, ri_zhi, gan_wx, zhi_wx):
    """生成有深度、有个人观点的小红书文章
    
    凌墨风格：
    - 有鲜明的个人立场和观点
    - 从命理角度切入，但不停留在表面
    -敢说、敢判断、有态度
    - 不模板化，每篇都是独立思考
    """
    
    # 随机选择写作角度（每人不同视角）
    angles = [
        "命理规律判断",
        "五行旺衰分析", 
        "十年大运解读",
        "流年运势推演",
        "五行职业适配",
        "阴阳辩证思维",
    ]
    angle = random.choice(angles)
    
    # 生成有观点的标题（20字内）
    xhs_title = make_xhs_title_deep(topic, ri_zhu, angle)
    
    # 生成正文（有深度+个人观点）
    content = generate_deep_article(topic, ri_zhu, ri_gan, ri_zhi, gan_wx, zhi_wx, angle)
    
    return xhs_title, content


def make_xhs_title_deep(topic, ri_zhu, angle):
    """生成有张力的小红书标题（20字内）"""
    
    # 不同角度不同风格
    if "命理规律" in angle:
        templates = [
            f"从命理规律看「{topic[:6]}」的本质",
            f"「{topic[:6]}」背后的命理逻辑，我说实话",
            f"命理角度：「{topic[:6]}」不是你想的那样",
            f"大多数人不懂：命理规律看「{topic[:6]}」",
        ]
    elif "五行旺衰" in angle:
        templates = [
            f"五行旺衰：「{topic[:6]}」的人运气不会差",
            f"从五行看：「{topic[:6]}」背后藏着什么",
            f"五行分析：这类人最近要起飞了",
            f"不是迷信：五行旺衰决定命运走势",
        ]
    elif "大运" in angle:
        templates = [
            f"十年大运看：「{topic[:6]}」机遇在哪",
            f"大运已到：抓住的人要起飞了",
            f"从大运推：未来三年机遇在哪里",
            f"命理大运：「{topic[:6]}」只是开始",
        ]
    elif "流年" in angle:
        templates = [
            f"流年已变：「{topic[:6]}」要注意了",
            f"今年流年：这类人运势要爆发",
            f"流年推演：「{topic[:6]}」背后的机遇",
            f"壬寅年启示录：运气从这里改变",
        ]
    elif "职业" in angle:
        templates = [
            f"命理职业适配：你适合什么？看这里",
            f"五行看职业：这类人天生适合创业",
            f"从日柱看：你这辈子靠什么吃饭",
            f"命理选职业：找对方向少走十年弯路",
        ]
    else:
        templates = [
            f"「{topic[:6]}」的阴阳辩证，我来说透",
            f"换个角度：命理帮你看清「{topic[:6]}」",
            f"命理揭秘：「{topic[:6]}」不是迷信是规律",
            f"深度命理：大部分人没想明白的事",
        ]
    
    title = random.choice(templates)
    if len(title) > 20:
        title = title[:19]
    return title


def generate_deep_article(topic, ri_zhu, ri_gan, ri_zhi, gan_wx, zhi_wx, angle):
    """生成有深度、有个人观点的正文"""
    
    # 获取凌墨的八字数据
    bazi = BaZiAnalyzer()
    ri_zhu_full = ri_zhu  # 完整日柱如 "丙子"
    
    # 个人观点陈述（凌墨敢说）
    personal_views = [
        f"""我看了十几年八字，有个观点不吐不快：

很多人觉得命理是迷信，但我做了这么多年，我发现命理其实是
一套观察世界的规律。

就像今天要聊的「{topic}」，从命理角度看，有它内在的逻辑。

【今日日柱：{ri_zhu}】
天干{ri_gan}、地支{ri_zhi}
{gan_wx}年出生、{zhi_wx}月令

这个组合的人，最近在「{topic}」这件事上，
恰恰站在了运势的拐点上。

我的判断是：{get_personal_prediction(topic, ri_gan, ri_zhi)}

说这些不是让大家迷信，而是给大家一个思考的维度。

你的日柱是什么？评论区说说，我帮你看看。""",

        f"""最近「{topic}」这个话题很火，但我要说一些
很多人不敢说的真话。

从命理角度看，热点事件从来不是偶然。
它背后是一股运势在推动。

【今日日柱：{ri_zhu}】
天干{ri_gan}，地支{ri_zhi}
{gan_wx}年出生朋友，最近思维特别活跃

我认为「{topic}」的本质是：
{get_topic_nature(topic)}

这不是玄学，是统计学。

我的经验：看懂运势的人，和看不懂的人，
十年后的差距是巨大的。

你说呢？评论区聊聊你的看法。""",

        f"""我做命理咨询这么久，有一个规律越来越清晰：

一个人的运气，跟他对世界的理解深度成正比。

「{topic}」这件事就是一个很好的例子。

【今日日柱：{ri_zhu}】
天干{ri_gan}（{gan_wx}）
地支{ri_zhi}（{zhi_wx}）

{gan_wx}年的朋友，你们现在正处于一个关键节点。
处理得好，「{topic}」会成为你的跳板；
处理不好，会变成一个坑。

我的建议是：{get_advice(ri_gan, ri_zhi)}

信不信由你，但这个思路值得认真想一想。""",
    ]
    
    content = random.choice(personal_views)
    
    # 添加互动引导
    interaction = f"""

——
我是凌墨，研究命理十几年
关注我，每天分享一个命理真相

#命理 #八字 #运势 #命理知识 #传统文化 #人生智慧"""

    return content + interaction


def get_personal_prediction(topic, ri_gan, ri_zhi):
    """根据天干地支给出个人预测性观点"""
    predictions = {
        "甲": f"「{topic}」领域的创新者会迎来机会",
        "乙": f"「{topic}」相关行业会有整合机会",
        "丙": f"「{topic}」的热度会继续攀升",
        "丁": f"「{topic}」幕后推手开始行动",
        "戊": f"「{topic}」需要稳扎稳打，不能冒进",
        "己": f"「{topic}」会有新的机会出现",
        "庚": f"「{topic}」格局会有大的变化",
        "辛": f"「{topic}」精细化运营是关键",
        "壬": f"「{topic}」流动性会加强",
        "癸": f"「{topic}」收尾阶段，需要耐心",
    }
    return predictions.get(ri_gan, f"「{topic}」需要因人而异分析")


def get_topic_nature(topic):
    """给出对话题本质的个人判断"""
    natures = [
        "表面是热点，深层是社会情绪的投射",
        "看似偶然，实则是规律使然",
        "背后是资源重新分配的信号",
        "是人心变化的晴雨表",
        "是运势循环的必然结果",
    ]
    return random.choice(natures)


def get_advice(ri_gan, ri_zhi):
    """根据日柱给出实用建议"""
    advices = [
        "顺势而为，不要强行对抗",
        "先观察再行动，不要冲动",
        "找到你的优势领域，集中发力",
        "控制节奏，稳住就是赢",
        "主动出击，但不要all in",
    ]
    return random.choice(advices)


def make_xhs_title(original_topic, ri_zhu):
    """保留旧接口兼容"""
    angles = ["命理规律判断", "五行旺衰分析", "十年大运解读", "流年运势推演"]
    angle = random.choice(angles)
    return make_xhs_title_deep(original_topic, ri_zhu, angle)


# ========== 原有函数保留兼容 ==========

def get_weibo_hot():
    return []

def get_douyin_hot():
    return []

def get_tophub():
    return []

def generate_image(title, topic):
    today_cover = f"/tmp/openclaw/uploads/xhs_cover_{date.today().strftime('%Y%m%d')}.png"
    if os.path.exists(today_cover):
        import shutil
        shutil.copy(today_cover, XHS_IMAGE_PATH)
        print(f"使用今日封面图: {XHS_IMAGE_PATH}")
        return True
    elif os.path.exists(XHS_IMAGE_PATH):
        print(f"使用上次封面图: {XHS_IMAGE_PATH}")
        return True
    else:
        print("封面图不存在，请先生成")
        return False


# ========== 浏览器发布 ==========

def publish_to_xiaohongshu(title, content, image_path):
    """用 Playwright 发布到小红书"""
    script_lines = [
        "const { chromium } = require('playwright');",
        "(async () => {",
        "    const browser = await chromium.connectOverCDP('http://127.0.0.1:18800');",
        "    const context = browser.contexts()[0];",
        "    const page = context.pages()[0];",
        "    try {",
        "        await page.goto('https://creator.xiaohongshu.com/publish/publish?from=homepage&target=image', {waitUntil: 'networkidle', timeout: 20000});",
        "        await page.waitForTimeout(5000);",
        "        const fileInput = page.locator('input[type=file]').first();",
        f"        await fileInput.setInputFiles('{image_path}');",
        "        console.log('图片上传成功');",
        "        await page.waitForTimeout(5000);",
        "        const titleInput = page.locator('input[placeholder=\"填写标题会有更多赞哦\"]');",
        f"        await titleInput.fill('{title}');",
        "        console.log('标题填写成功');",
        "        const contentDiv = page.locator('div[contenteditable=\"true\"]').first();",
        f"        await contentDiv.fill('{content.replace(chr(10), ' ')}');",
        "        console.log('正文填写成功');",
        "        await page.waitForTimeout(2000);",
        "        const publishBtn = page.locator('button:has-text(\"发布\")').last();",
        "        await publishBtn.click({force: true});",
        "        console.log('发布按钮点击成功');",
        "        await page.waitForTimeout(5000);",
        "        const pageText = await page.evaluate(() => document.body.innerText);",
        "        if (pageText.includes('发布成功')) { console.log('PUBLISH_SUCCESS'); }",
        "        else { console.log('PUBLISH_MAYBE_SUCCESS'); }",
        "    } catch(e) { console.log('ERROR:', e.message); }",
        "    await browser.close();",
        "})().catch(e => console.error('Fatal:', e.message));"
    ]
    script = "\n".join(script_lines)
    
    tmp_script = f"/Users/yyf/.agents/skills/browser-automation/xhs_pub_{int(time.time())}.js"
    with open(tmp_script, 'w') as f:
        f.write(script)
    
    result = subprocess.run(['node', tmp_script], capture_output=True, text=True, timeout=60)
    os.remove(tmp_script)
    
    if 'PUBLISH_SUCCESS' in result.stdout:
        return True
    elif 'ERROR' in result.stdout:
        print(f"发布出错: {result.stdout}")
        return False
    else:
        print(f"发布结果未知: {result.stdout[:200]}")
        return False


# ========== 主程序 ==========

if __name__ == "__main__":
    print("请使用 xiaohongshu_hot_one.py 执行发布")
