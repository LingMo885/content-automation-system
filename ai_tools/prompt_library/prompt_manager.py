#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI Prompt 管理器
帮你管理、分类、搜索用过的Prompts

用法：
  python prompt_manager.py add "写作助手" "你是一个专业的文案写作助手..."
  python prompt_manager.py list
  python prompt_manager.py search 写作
  python prompt_manager.py tag "写作助手" "文案,营销,小红书"
  python prompt_manager.py random --tag 小红书
  python prompt_manager.py export --format claude
"""

import os
import sys
import json
import argparse
import hashlib
from datetime import datetime
from collections import defaultdict

# 存储路径
STORAGE_DIR = os.path.expanduser("~/.openclaw/workspace/memory/prompts")
PROMPTS_FILE = os.path.join(STORAGE_DIR, "prompts.json")
os.makedirs(STORAGE_DIR, exist_ok=True)

# ========== 数据结构 ==========

def load_prompts():
    """加载Prompts"""
    if os.path.exists(PROMPTS_FILE):
        with open(PROMPTS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"prompts": [], "tags": defaultdict(list), "categories": defaultdict(list)}

def save_prompts(data):
    """保存Prompts"""
    with open(PROMPTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2, default=lambda x: dict(x) if hasattr(x, '__dict__') else str(x))

def generate_id(text):
    """生成短ID"""
    return hashlib.md5(text.encode()).hexdigest()[:8]

def add_prompt(name, prompt, tags=None, category=None):
    """添加Prompt"""
    data = load_prompts()
    
    pid = generate_id(name + prompt)
    
    # 检查是否已存在
    for p in data['prompts']:
        if p['id'] == pid:
            print(f"⚠️ Prompt已存在: {name}")
            return pid
    
    prompt_obj = {
        "id": pid,
        "name": name,
        "prompt": prompt,
        "tags": tags or [],
        "category": category,
        "usage_count": 0,
        "created_at": datetime.now().isoformat(),
        "last_used": None
    }
    
    data['prompts'].append(prompt_obj)
    
    # 更新索引
    for tag in (tags or []):
        if tag not in data['tags']:
            data['tags'][tag] = []
        if pid not in data['tags'][tag]:
            data['tags'][tag].append(pid)
    
    if category:
        if category not in data['categories']:
            data['categories'][category] = []
        if pid not in data['categories'][category]:
            data['categories'][category].append(pid)
    
    save_prompts(data)
    print(f"✅ 已添加: {name} (ID: {pid})")
    return pid

def list_prompts(tag=None, category=None, limit=20):
    """列出Prompts"""
    data = load_prompts()
    
    prompts = data['prompts']
    
    if tag:
        pids = data['tags'].get(tag, [])
        prompts = [p for p in prompts if p['id'] in pids]
    
    if category:
        pids = data['categories'].get(category, [])
        prompts = [p for p in prompts if p['id'] in pids]
    
    prompts = sorted(prompts, key=lambda x: x.get('last_used') or x['created_at'], reverse=True)
    
    if not prompts:
        print("没有找到Prompts")
        return
    
    print(f"\n📚 Prompts库 (共 {len(prompts)} 个)")
    print("=" * 70)
    
    for p in prompts[:limit]:
        tags_str = " ".join([f"#{t}" for t in p.get('tags', [])]) or ""
        used = f"使用 {p.get('usage_count', 0)} 次" if p.get('usage_count') else ""
        print(f"\n  [{p['id']}] {p['name']}")
        print(f"     {p['prompt'][:60]}...")
        if tags_str:
            print(f"     {tags_str}")
        if used:
            print(f"     {used}")
    
    if len(prompts) > limit:
        print(f"\n... 还有 {len(prompts) - limit} 个")

def search_prompts(keyword):
    """搜索Prompts"""
    data = load_prompts()
    keyword = keyword.lower()
    
    results = []
    for p in data['prompts']:
        if keyword in p['name'].lower() or keyword in p['prompt'].lower():
            results.append(p)
    
    if not results:
        print(f"没有找到包含 '{keyword}' 的Prompts")
        return
    
    print(f"\n🔍 搜索 '{keyword}' (找到 {len(results)} 个)")
    print("=" * 70)
    
    for p in results:
        tags_str = " ".join([f"#{t}" for t in p.get('tags', [])]) or ""
        print(f"\n  [{p['id']}] {p['name']}")
        print(f"     {p['prompt'][:80]}...")
        if tags_str:
            print(f"     {tags_str}")

def get_prompt(pid):
    """获取单个Prompt"""
    data = load_prompts()
    for p in data['prompts']:
        if p['id'] == pid or p['name'] == pid:
            # 更新使用次数
            p['usage_count'] = p.get('usage_count', 0) + 1
            p['last_used'] = datetime.now().isoformat()
            save_prompts(data)
            return p
    return None

def tag_prompt(identifier, tags):
    """为Prompt添加标签"""
    data = load_prompts()
    
    # 找到prompt
    target = None
    for p in data['prompts']:
        if p['id'] == identifier or p['name'] == identifier:
            target = p
            break
    
    if not target:
        print(f"❌ 找不到: {identifier}")
        return
    
    # 添加标签
    for tag in tags:
        if tag not in target['tags']:
            target['tags'].append(tag)
        if tag not in data['tags']:
            data['tags'][tag] = []
        if target['id'] not in data['tags'][tag]:
            data['tags'][tag].append(target['id'])
    
    save_prompts(data)
    print(f"✅ 已为 '{target['name']}' 添加标签: {tags}")

def random_prompt(tag=None):
    """随机选一个Prompt"""
    data = load_prompts()
    
    prompts = data['prompts']
    if tag:
        pids = data['tags'].get(tag, [])
        prompts = [p for p in prompts if p['id'] in pids]
    
    if not prompts:
        print("没有Prompts可选")
        return
    
    import random
    p = random.choice(prompts)
    p['usage_count'] = p.get('usage_count', 0) + 1
    p['last_used'] = datetime.now().isoformat()
    save_prompts(data)
    
    print(f"\n🎲 随机选择: {p['name']}")
    print("=" * 70)
    print(f"\n{p['prompt']}\n")
    print(f"ID: {p['id']}")

def export_prompts(fmt='json'):
    """导出Prompts"""
    data = load_prompts()
    
    if fmt == 'json':
        print(json.dumps(data, ensure_ascii=False, indent=2))
    elif fmt == 'claude':
        # 导出为Claude可用的格式
        lines = []
        for p in data['prompts']:
            lines.append(f"# {p['name']}")
            lines.append(f"{p['prompt']}")
            lines.append("")
        print("\n".join(lines))
    elif fmt == 'markdown':
        lines = ["# Prompt Library\n"]
        for p in data['prompts']:
            tags = " ".join([f"`{t}`" for t in p.get('tags', [])])
            lines.append(f"## {p['name']} {tags}")
            lines.append(f"```\n{p['prompt']}\n```")
            lines.append("")
        print("\n".join(lines))

def show_tags():
    """显示所有标签"""
    data = load_prompts()
    
    print(f"\n🏷️ 标签列表 ({len(data['tags'])} 个)")
    print("=" * 40)
    
    for tag, pids in sorted(data['tags'].items(), key=lambda x: len(x[1]), reverse=True):
        print(f"  {tag}: {len(pids)} 个")

def main():
    parser = argparse.ArgumentParser(description='AI Prompt 管理器')
    subparsers = parser.add_subparsers(dest='cmd', help='子命令')
    
    # add
    add_parser = subparsers.add_parser('add', help='添加Prompt')
    add_parser.add_argument('name', help='Prompt名称')
    add_parser.add_argument('prompt', help='Prompt内容')
    add_parser.add_argument('--tag', '-t', nargs='+', help='标签')
    add_parser.add_argument('--category', '-c', help='分类')
    
    # list
    list_parser = subparsers.add_parser('list', help='列出Prompts')
    list_parser.add_argument('--tag', '-t', help='按标签筛选')
    list_parser.add_argument('--category', '-c', help='按分类筛选')
    list_parser.add_argument('--limit', '-n', type=int, default=20)
    
    # search
    search_parser = subparsers.add_parser('search', help='搜索Prompts')
    search_parser.add_argument('keyword', help='关键词')
    
    # get
    get_parser = subparsers.add_parser('get', help='获取Prompt详情')
    get_parser.add_argument('identifier', help='ID或名称')
    
    # tag
    tag_parser = subparsers.add_parser('tag', help='添加标签')
    tag_parser.add_argument('identifier', help='ID或名称')
    tag_parser.add_argument('tags', nargs='+', help='标签列表')
    
    # random
    random_parser = subparsers.add_parser('random', help='随机选一个')
    random_parser.add_argument('--tag', '-t', help='限定标签')
    
    # export
    export_parser = subparsers.add_parser('export', help='导出')
    export_parser.add_argument('--format', '-f', choices=['json','claude','markdown'], default='json')
    
    # tags
    subparsers.add_parser('tags', help='显示所有标签')
    
    args = parser.parse_args()
    
    if not args.cmd:
        parser.print_help()
        return
    
    if args.cmd == 'add':
        add_prompt(args.name, args.prompt, args.tag, args.category)
        
    elif args.cmd == 'list':
        list_prompts(args.tag, args.category, args.limit)
        
    elif args.cmd == 'search':
        search_prompts(args.keyword)
        
    elif args.cmd == 'get':
        p = get_prompt(args.identifier)
        if p:
            print(f"\n📄 {p['name']}")
            print(f"   ID: {p['id']}")
            print(f"   标签: {p.get('tags', [])}")
            print(f"   使用次数: {p.get('usage_count', 0)}")
            print(f"\n内容:\n{p['prompt']}")
        else:
            print(f"❌ 找不到: {args.identifier}")
        
    elif args.cmd == 'tag':
        tag_prompt(args.identifier, args.tags)
        
    elif args.cmd == 'random':
        random_prompt(args.tag)
        
    elif args.cmd == 'export':
        export_prompts(args.format)
        
    elif args.cmd == 'tags':
        show_tags()

if __name__ == '__main__':
    main()
