#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多平台热点聚合工具
同时抓取：百度热搜、微博热搜、知乎热榜、小红书站内热点
输出：JSON格式，便于后续处理

用法：
  python hot_topics.py              # 抓取所有平台
  python hot_topics.py --platform baidu --limit 10
  python hot_topics.py --save
  python hot_topics.py --watch     # 持续监控模式
"""

import os
import sys
import json
import time
import argparse
import requests
import re
from datetime import datetime
from collections import defaultdict

# 输出目录
OUTPUT_DIR = os.path.expanduser("~/.openclaw/workspace/output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ========== 平台抓取函数 ==========

def fetch_baidu_hot(limit=20):
    """抓取百度热搜"""
    try:
        url = 'https://top.baidu.com/board?tab=realtime'
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'}
        resp = requests.get(url, headers=headers, timeout=10)
        resp.encoding = 'utf-8'
        html = resp.text
        
        # 解析热搜标题
        titles = re.findall(r'class="c-single-text-ellipsis">([^<]+)<', html)
        results = []
        for i, title in enumerate(titles[:limit], 1):
            results.append({
                'rank': i,
                'title': title.strip(),
                'platform': 'baidu',
                'url': ''
            })
        return results
    except Exception as e:
        return [{'error': str(e), 'platform': 'baidu'}]

def fetch_weibo_hot(limit=20):
    """抓取微博热搜"""
    try:
        url = 'https://weibo.com/ajax/side/hotSearch'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Referer': 'https://weibo.com',
            'Accept': 'application/json'
        }
        resp = requests.get(url, headers=headers, timeout=10)
        data = resp.json()
        
        results = []
        if data.get('data') and data['data'].get('realtime'):
            for i, item in enumerate(data['data']['realtime'][:limit], 1):
                results.append({
                    'rank': i,
                    'title': item.get('word', ''),
                    'platform': 'weibo',
                    'url': f"https://s.weibo.com/weibo?q={item.get('word', '')}",
                    'hot_value': item.get('raw_hot', '')
                })
        return results
    except Exception as e:
        return [{'error': str(e), 'platform': 'weibo'}]

def fetch_zhihu_hot(limit=10):
    """抓取知乎热榜"""
    try:
        url = 'https://api.zhihu.com/topics/19776749/feeds/top_activity'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Accept': 'application/json'
        }
        resp = requests.get(url, headers=headers, timeout=10)
        data = resp.json()
        
        results = []
        if 'data' in data:
            for i, item in enumerate(data['data'][:limit], 1):
                question = item.get('question', {})
                results.append({
                    'rank': i,
                    'title': question.get('title', ''),
                    'platform': 'zhihu',
                    'url': f"https://www.zhihu.com/question/{question.get('id', '')}",
                    'answer_count': question.get('comment_count', 0)
                })
        return results
    except Exception as e:
        return [{'error': str(e), 'platform': 'zhihu'}]

def fetch_toutiao_hot(limit=20):
    """抓取头条热搜"""
    try:
        url = 'https://www.toutiao.com/hot-event/hot-board/?origin=hot_board'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Accept': 'application/json'
        }
        resp = requests.get(url, headers=headers, timeout=10)
        data = resp.json()
        
        results = []
        if 'data' in data:
            for i, item in enumerate(data['data'][:limit], 1):
                results.append({
                    'rank': i,
                    'title': item.get('Title', ''),
                    'platform': 'toutiao',
                    'url': item.get('Url', '')
                })
        return results
    except Exception as e:
        return [{'error': str(e), 'platform': 'toutiao'}]

def fetch_douyin_hot(limit=10):
    """抓取抖音热榜（抖音热点榜）"""
    try:
        url = 'https://www.douyin.com/aweme/v1/web/hot/search/list/?keyword=1'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Accept': 'application/json'
        }
        resp = requests.get(url, headers=headers, timeout=10)
        data = resp.json()
        
        results = []
        if 'word_list' in data:
            for i, item in enumerate(data['word_list'][:limit], 1):
                results.append({
                    'rank': i,
                    'title': item.get('word', ''),
                    'platform': 'douyin',
                    'url': '',
                    'hot_value': item.get('hot_value', '')
                })
        return results
    except Exception as e:
        return [{'error': str(e), 'platform': 'douyin'}]

# ========== 核心功能 ==========

def aggregate_all(platforms=None, limit=20):
    """聚合所有平台热点"""
    all_results = {
        'timestamp': datetime.now().isoformat(),
        'platforms': {},
        'all_topics': []
    }
    
    platform_funcs = {
        'baidu': (fetch_baidu_hot, limit),
        'weibo': (fetch_weibo_hot, limit),
        'zhihu': (fetch_zhihu_hot, 10),
        'toutiao': (fetch_toutiao_hot, limit),
        'douyin': (fetch_douyin_hot, 10),
    }
    
    if platforms:
        platform_funcs = {k: v for k, v in platform_funcs.items() if k in platforms}
    
    total_count = 0
    for platform, (func, lim) in platform_funcs.items():
        print(f"📡 正在抓取 {platform}...", end=' ')
        results = func(lim)
        error_items = [r for r in results if 'error' in r]
        if error_items:
            print(f"❌ {error_items[0]['error']}")
        else:
            print(f"✅ {len(results)} 条")
            all_results['platforms'][platform] = results
            all_results['all_topics'].extend(results)
            total_count += len(results)
    
    # 按平台排序all_topics
    all_results['total_count'] = total_count
    
    return all_results

def save_results(results, filename=None):
    """保存结果到文件"""
    if not filename:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"hot_topics_{timestamp}.json"
    
    filepath = os.path.join(OUTPUT_DIR, filename)
    
    # 也保存一份最新
    latest_path = os.path.join(OUTPUT_DIR, 'hot_topics_latest.json')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    with open(latest_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 已保存: {filepath}")
    return filepath

def print_summary(results):
    """打印汇总"""
    print(f"\n{'='*60}")
    print(f"📊 热点汇总 | {results['timestamp']}")
    print(f"{'='*60}")
    
    for platform, items in results['platforms'].items():
        print(f"\n🔥 {platform.upper()} ({len(items)}条)")
        print("-" * 40)
        for item in items[:5]:
            print(f"  {item['rank']:2}. {item['title'][:30]}")
        if len(items) > 5:
            print(f"  ... 还有 {len(items)-5} 条")
    
    print(f"\n📈 总计: {results['total_count']} 条热点")

def match_keywords(topics, keywords):
    """匹配关键词"""
    matched = []
    for topic in topics:
        title = topic.get('title', '').lower()
        for kw in keywords:
            if kw.lower() in title:
                matched.append({**topic, 'matched_keyword': kw})
                break
    return matched

def watch_mode(interval=300, platforms=None):
    """持续监控模式"""
    print(f"👀 监控模式启动，每 {interval}秒 更新一次")
    print("按 Ctrl+C 退出\n")
    
    last_hash = ''
    try:
        while True:
            results = aggregate_all(platforms)
            current_hash = json.dumps(results['all_topics'][:5], sort_keys=True)
            
            if current_hash != last_hash:
                print_summary(results)
                save_results(results)
                last_hash = current_hash
            else:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] 热点无变化")
            
            time.sleep(interval)
            
    except KeyboardInterrupt:
        print("\n\n👋 监控已停止")

def main():
    parser = argparse.ArgumentParser(description='多平台热点聚合工具')
    parser.add_argument('--platform', '-p', nargs='+', choices=['baidu','weibo','zhihu','toutiao','douyin'], help='指定平台')
    parser.add_argument('--limit', '-n', type=int, default=20, help='每平台数量')
    parser.add_argument('--save', '-s', action='store_true', help='保存到文件')
    parser.add_argument('--output', '-o', help='输出文件路径')
    parser.add_argument('--watch', '-w', action='store_true', help='持续监控模式')
    parser.add_argument('--interval', '-i', type=int, default=300, help='监控间隔(秒)')
    parser.add_argument('--keywords', '-k', nargs='+', help='匹配关键词')
    parser.add_argument('--json', '-j', action='store_true', help='输出JSON')
    
    args = parser.parse_args()
    
    if args.watch:
        watch_mode(args.interval, args.platform)
        return
    
    results = aggregate_all(args.platform, args.limit)
    
    if args.keywords:
        matched = match_keywords(results['all_topics'], args.keywords)
        print(f"\n🔍 关键词匹配: {args.keywords}")
        print(f"找到 {len(matched)} 条相关热点:")
        for m in matched:
            print(f"  [{m['platform']}] {m['title']}")
    
    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        print_summary(results)
    
    if args.save or args.output:
        save_results(results, args.output)

if __name__ == '__main__':
    main()
