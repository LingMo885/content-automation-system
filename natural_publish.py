#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自然语言发布引擎
接收自然语言指令，自动生成并发布内容

使用方式：
  python3 natural_publish.py "发一篇关于清明节运势的小红书"
  python3 natural_publish.py "写一篇公众号文章，关于最近AI创业风口"
  python3 natural_publish.py "发一条八字科普小红书"

平台支持：
  - 小红书（xiaohongshu）
  - 微信公众号（wechat）
"""

import sys
import os
import json
import time
import subprocess
import random
from datetime import datetime, date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ========== 自然语言解析 ==========

def parse_command(command: str) -> dict:
    """解析自然语言命令，返回结构化指令"""
    
    command = command.strip()
    
    # 检测平台
    platform = detect_platform(command)
    
    # 检测主题
    topic = extract_topic(command)
    
    # 检测语气/风格
    style = detect_style(command)
    
    # 检测紧急程度
    urgent = detect_urgent(command)
    
    return {
        "platform": platform,
        "topic": topic,
        "style": style,
        "urgent": urgent,
        "original": command
    }


def detect_platform(cmd: str) -> str:
    """检测目标平台"""
    cmd_lower = cmd.lower()
    
    if any(k in cmd_lower for k in ['小红书', 'xhs', 'redbook']):
        return 'xiaohongshu'
    elif any(k in cmd_lower for k in ['公众号', '微信', 'wechat']):
        return 'wechat'
    elif any(k in cmd_lower for k in ['抖音', 'douyin']):
        return 'douyin'
    elif any(k in cmd_lower for k in ['b站', 'bilibili', '专栏']):
        return 'bilibili'
    else:
        return 'xiaohongshu'  # 默认小红书


def extract_topic(cmd: str) -> str:
    """提取主题"""
    # 去掉命令词，保留核心主题
    cmd = cmd.replace('发一篇', '').replace('写一篇', '').replace('发一条', '')
    cmd = cmd.replace('关于', '').replace('关于', '').replace('的', '')
    cmd = cmd.replace('小红书', '').replace('公众号', '').replace('抖音', '')
    cmd = cmd.replace('文章', '').replace('内容', '').strip()
    return cmd if cmd else None


def detect_style(cmd: str) -> str:
    """检测风格"""
    if any(k in cmd for k in ['干货', '专业', '深度']):
        return 'professional'
    elif any(k in cmd for k in ['轻松', '有趣', '搞笑']):
        return 'fun'
    elif any(k in cmd for k in ['情感', '感性']):
        return 'emotional'
    else:
        return 'balanced'


def detect_urgent(cmd: str) -> bool:
    """检测是否紧急"""
    return any(k in cmd for k in ['马上', '立即', '现在', '加急'])


# ========== 内容生成 ==========

def generate_content(platform: str, topic: str, style: str = 'balanced'):
    """生成内容"""
    
    if not topic:
        topic = get_random_topic()
    
    # 根据平台选择生成器
    if platform == 'xiaohongshu':
        return generate_xhs_content(topic, style)
    elif platform == 'wechat':
        return generate_wechat_content(topic, style)
    else:
        return generate_xhs_content(topic, style)


def get_random_topic() -> str:
    """获取随机主题（从热点话题中选）"""
    topics = [
        "清明节运势",
        "三月运势总结",
        "五行穿衣指南",
        "事业运提升",
        "财运亨通",
        "感情运势",
        "健康提醒",
        "贵人运",
    ]
    return random.choice(topics)


def generate_xhs_content(topic: str, style: str) -> dict:
    """生成小红书内容"""
    
    # 标题库
    title_templates = [
        f"清明节将至，你的运势准备好了吗？",
        f"【{topic}】命理师说实话",
        f"命理角度看{topic}，我顿悟了",
        f"{topic}，这一篇说透",
        f"关于{topic}，我有话要说",
    ]
    
    # 正文开头
    opening_templates = [
        "我看了十几年八字，有个规律越来越清晰。\n\n",
        "最近很多人问我关于「{}」的问题，今天说透。\n\n",
        "做命理咨询这么久，这个话题必须聊清楚。\n\n",
    ]
    
    title = random.choice(title_templates).format(topic)
    
    opening = random.choice(opening_templates).format(topic)
    
    body = f"""我在十几年的命理咨询中，看到过太多人因为没看懂运势，错过了关键机会。

今天就拿「{topic}」这个话题，说说我的一些观察。

{opening}

从我接触的案例来看，这个话题背后其实有规律可循。

我的判断是：抓住这个时间窗口很重要。

你们觉得呢？评论区聊聊你们的看法。

我是凌墨，研究命理十几年。关注我，每天分享一个命理真相。"""

    return {
        "title": title,
        "content": body,
        "topic": topic
    }


def generate_wechat_content(topic: str, style: str) -> dict:
    """生成微信公众号内容"""
    
    title = f"今日{topic} | 命理角度深度解析"
    
    content = f"""<p>我从事命理咨询十几年，观察到一个规律：看懂运势的人，和看不懂的人，十年后的差距是巨大的。</p>

<h2>{topic}背后的命理逻辑</h2>

<p>最近很多人问我关于「{topic}」的问题。今天从命理角度，说说我的一些观察。</p>

<h2>我的核心观点</h2>

<p>从我的经验来看，这个话题其实有三个层面：</p>

<ol>
<li>表面现象 vs 深层规律</li>
<li>短期波动 vs 长期趋势</li>
<li>个人选择 vs 运势推动</li>
</ol>

<h2>具体建议</h2>

<p>基于我的分析，对于{topic}，有以下建议供大家参考：</p>

<p>1. 看清大方向，顺势而为<br>
2. 注意关键时间节点<br>
3. 摆正心态，不迷信也不忽视</p>

<hr/>
<p><strong>今日互动</strong><br>
你是怎么看待这个话题的？欢迎在评论区分享你的看法。</p>

<p>更多命理干货、每日运势分析，关注我不迷路～</p>
<p>#{topic} #命理 #八字 #传统文化</p>"""

    return {
        "title": title,
        "content": content,
        "topic": topic
    }


# ========== 封面图生成 ==========

def generate_cover(platform: str, topic: str) -> str:
    """生成封面图（调用AI）"""
    
    os.makedirs("/tmp/openclaw/uploads", exist_ok=True)
    output_path = f"/tmp/openclaw/uploads/cover_{int(time.time())}.png"
    
    # 封面提示词
    prompts = [
        f"新中式风格命理知识卡片，{topic}主题，白色毛笔字标题，宣纸底纹，淡雅中国风，竖版9:16，高清4K",
        f"精致中国风命理配图，{topic}元素，金色毛笔字，砚台墨香背景，竖版小红书封面风格，9:16比例",
        f"现代中式命理科普配图，{topic}主题，优雅书法字体，深紫渐变背景，竖版9:16，4K品质",
    ]
    
    prompt = random.choice(prompts)
    
    # 调用AI生成（通过mxai或其他可用工具）
    script = f'''
import requests, json, os
try:
    url = "http://127.0.0.1:11434/api/generate"
    payload = {{
        "model": "minimax/image-01",
        "prompt": {json.dumps(prompt)},
        "stream": False
    }}
    r = requests.post(url, json=payload, timeout=60)
    data = r.json()
    if "images" in data:
        img_data = data["images"][0]
        if img_data.startswith("http"):
            import urllib.request
            urllib.request.urlretrieve(img_data, {json.dumps(output_path)})
        else:
            with open({json.dumps(output_path)}, "wb") as f:
                f.write(bytes.fromhex(img_data))
        print("OK")
    else:
        print("FAIL")
except Exception as e:
    print(f"ERROR: {{e}}")
'''
    
    result = subprocess.run(['python3', '-c', script], capture_output=True, text=True, timeout=90)
    
    if result.returncode == 0 and os.path.exists(output_path):
        return output_path
    
    return None


# ========== 发布 ==========

def publish(platform: str, title: str, content: str, cover_path: str = None):
    """发布到指定平台"""
    
    if platform == 'xiaohongshu':
        return publish_xiaohongshu(title, content, cover_path)
    elif platform == 'wechat':
        return publish_wechat(title, content, cover_path)
    else:
        print(f"平台 {platform} 暂不支持自动发布")
        return False


def publish_xiaohongshu(title: str, content: str, cover_path: str = None):
    """发布到小红书"""
    
    if not cover_path or not os.path.exists(cover_path):
        print("小红书发布需要封面图")
        return False
    
    # 使用现有自动化脚本
    from xiaohongshu_autoposter import publish_to_xiaohongshu
    
    success = publish_to_xiaohongshu(title, content, cover_path)
    return success


def publish_wechat(title: str, content: str, cover_path: str = None):
    """发布到微信公众号"""
    
    from wechat_publisher import WechatPublisher
    
    publisher = WechatPublisher()
    
    # 上传封面
    thumb_media_id = None
    if cover_path and os.path.exists(cover_path):
        thumb_media_id = publisher.upload_image(cover_path)
    
    if not thumb_media_id:
        thumb_media_id = "P7pU8h-oLBTgbv4idTjk8fF-x362pPyYvsmykRm3I1EKtyDx4Rj5GHPKx1BNkrds"
    
    # 创建草稿
    media_id = publisher.create_draft(title, content, thumb_media_id)
    
    return media_id is not None


# ========== 主流程 ==========

def main():
    if len(sys.argv) < 2:
        print("使用方法: python3 natural_publish.py '发一篇关于XXX的小红书'")
        sys.exit(1)
    
    command = sys.argv[1]
    print(f"\n{'='*50}")
    print(f"📝 自然语言发布引擎")
    print(f"{'='*50}")
    print(f"原始指令: {command}")
    
    # 1. 解析命令
    print(f"\n[1/5] 解析命令...")
    parsed = parse_command(command)
    print(f"  平台: {parsed['platform']}")
    print(f"  主题: {parsed['topic']}")
    print(f"  风格: {parsed['style']}")
    
    # 2. 生成内容
    print(f"\n[2/5] 生成内容...")
    result = generate_content(parsed['platform'], parsed['topic'], parsed['style'])
    print(f"  标题: {result['title']}")
    print(f"  主题: {result['topic']}")
    
    # 3. 生成封面
    print(f"\n[3/5] 生成封面图...")
    cover = generate_cover(parsed['platform'], result['topic'])
    if cover:
        print(f"  封面: {cover}")
    else:
        print(f"  封面生成失败，跳过")
    
    # 4. 发布
    print(f"\n[4/5] 发布...")
    success = publish(parsed['platform'], result['title'], result['content'], cover)
    
    # 5. 汇报
    print(f"\n[5/5] 汇报")
    print(f"{'='*50}")
    if success:
        platform_name = {"xiaohongshu": "小红书", "wechat": "微信公众号"}.get(parsed['platform'], parsed['platform'])
        print(f"✅ {platform_name}发布成功!")
        print(f"   标题: {result['title']}")
    else:
        print(f"❌ 发布失败，请检查日志")
    print(f"{'='*50}")


if __name__ == "__main__":
    main()
