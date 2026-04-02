#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小红书热点全自动发布 - 定时执行版
每次抓取当日热点，选1个最合适的发1篇
每次生成专属AI封面图，不重复
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import json, time, random, subprocess
from datetime import datetime, date
from xiaohongshu_autoposter import (
    get_baidu_hot, get_bazi_info, generate_content,
    publish_to_xiaohongshu, XHS_IMAGE_PATH, DRAFT_DIR
)

# 封面图存放目录
COVER_GEN_DIR = os.path.expanduser("~/Desktop/凌墨视频素材/小红书封面")

def generate_unique_cover(topic, title, content_snippet):
    """根据文章主题用AI生成专属封面图"""
    os.makedirs(COVER_GEN_DIR, exist_ok=True)

    # 封面图提示词——根据话题定制
    prompt_templates = [
        f"新中式风格命理知识卡片，{topic}主题，白色毛笔字标题，宣纸底纹，淡雅中国风，竖版9:16，高清4K",
        f"精致中国风命理配图，{topic}元素，金色毛笔字，砚台墨香背景，竖版小红书封面风格，9:16比例",
        f"现代中式命理科普配图，{topic}相关内容，优雅书法字体，深紫渐变背景，竖版9:16，4K品质",
        f"命理知识可视化配图，{topic}主题，中国传统纹样装饰，毛笔字标题，竖版小红书封面构图，9:16",
    ]
    prompt = random.choice(prompt_templates)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = f"{COVER_GEN_DIR}/cover_{timestamp}.png"

    # 调用AI生成封面
    script = f'''
import requests, json, os
url = "http://127.0.0.1:11434/api/generate"
payload = {{
    "model": "minimax/image-01",
    "prompt": {json.dumps(prompt)},
    "stream": False
}}
r = requests.post(url, json=payload)
data = r.json()
if "images" in data:
    img_data = data["images"][0]
    img_bytes = requests.get(img_data) if img_data.startswith("http") else bytes.fromhex(img_data)
    with open({json.dumps(output_path)}, "wb") as f:
        f.write(img_bytes)
    print("OK")
else:
    print("FAIL")
'''
    result = subprocess.run(['python3', '-c', script], capture_output=True, text=True, timeout=60)
    if result.returncode == 0 and os.path.exists(output_path):
        print(f"专属封面生成成功: {output_path}")
        return output_path
    print(f"封面生成失败: {result.stderr}")
    return None

def run_one_post():
    """执行1次发布（选1个热点话题发1篇）"""
    print(f"\n{'='*60}")
    print(f"📕 小红书热点发布 | {datetime.now().strftime('%H:%M')}")
    print(f"{'='*60}")

    # 获取八字
    ri_zhu, ri_gan, ri_zhi, gan_wx, zhi_wx, lunar_str = get_bazi_info()

    # 抓热点
    print("\n抓取热点...")
    topics = get_baidu_hot()
    if not topics:
        print("没有抓到热点，退出")
        return

    # 过滤
    skip = ['彩票', '赌博', '色情', '毒品', '特朗普', '拜登', '习近平', '战争', '军事机密']
    filtered = [t for t, n in topics if not any(s in t for s in skip) and len(t) > 3]

    if not filtered:
        filtered = [t for t, n in topics[:5]]

    # 随机选1个
    topic = random.choice(filtered[:10])
    print(f"选中的话题: {topic}")

    # 生成内容
    title, content = generate_content(topic, topic, ri_zhu, ri_gan, ri_zhi, gan_wx, zhi_wx)
    print(f"标题: {title}")

    # 保存草稿
    os.makedirs(DRAFT_DIR, exist_ok=True)
    draft_file = f"{DRAFT_DIR}/{date.today().strftime('%Y%m%d')}_{datetime.now().strftime('%H%M%S')}.json"
    with open(draft_file, 'w', encoding='utf-8') as f:
        json.dump({'title': title, 'content': content, 'topic': topic}, f, ensure_ascii=False, indent=2)

    # 生成专属封面图
    print("\n生成专属AI封面...")
    content_snippet = content[:100]
    cover_path = generate_unique_cover(topic, title, content_snippet)

    # 发布
    if cover_path and os.path.exists(cover_path):
        success = publish_to_xiaohongshu(title, content, cover_path)
        print(f"发布{'成功' if success else '完成'}")
    elif os.path.exists(XHS_IMAGE_PATH):
        print(f"使用默认封面发布: {XHS_IMAGE_PATH}")
        success = publish_to_xiaohongshu(title, content, XHS_IMAGE_PATH)
        print(f"发布{'成功' if success else '完成'}")
    else:
        print("没有封面图，跳过自动发布")


if __name__ == "__main__":
    run_one_post()
