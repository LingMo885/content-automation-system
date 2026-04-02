#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI API消费追踪器
记录每次API调用，自动统计各模型花费

用法：
  python cost_tracker.py log --model gpt-4o --input 50000 --output 30000
  python cost_tracker.py report --days 7
  python cost_tracker.py top --by cost --limit 5
  python cost_tracker.py budget 50 --days 30
  python cost_tracker.py alerts
"""

import os
import sys
import json
import argparse
from datetime import datetime, timedelta
from collections import defaultdict

STORAGE_FILE = os.path.expanduser("~/.openclaw/workspace/memory/api_costs.json")
os.makedirs(os.path.dirname(STORAGE_FILE), exist_ok=True)

# 模型价格表 ($/M tokens)
MODEL_PRICES = {
    # OpenAI
    "gpt-4o": (5.0, 15.0),
    "gpt-4o-mini": (0.15, 0.6),
    "o3-mini": (1.1, 4.4),
    "gpt-4-turbo": (10.0, 30.0),
    "gpt-3.5-turbo": (0.5, 1.5),
    # Anthropic
    "claude-sonnet-4": (3.0, 15.0),
    "claude-3-5-sonnet": (3.0, 15.0),
    "claude-3-5-haiku": (0.8, 4.0),
    "claude-3-opus": (15.0, 75.0),
    # Google
    "gemini-2.0-flash": (0, 0),
    "gemini-2.5-pro": (1.25, 5.0),
    "gemini-1.5-pro": (1.25, 5.0),
    "gemini-1.5-flash": (0.075, 0.3),
    # DeepSeek
    "deepseek-chat": (0.27, 1.1),
    "deepseek-r1": (0.55, 2.19),
    # 硅基流动
    "Pro/deepseek-ai/DeepSeek-V3": (0, 0),
    "Pro/deepseek-ai/DeepSeek-R1": (0, 0),
    "Pro/Qwen/Qwen2.5-72B-Instruct": (0, 0),
}

# 默认价格（未知模型）
DEFAULT_PRICE = (0.1, 0.3)

def load_data():
    if os.path.exists(STORAGE_FILE):
        with open(STORAGE_FILE, 'r') as f:
            return json.load(f)
    return {"logs": [], "budgets": {}}

def save_data(data):
    with open(STORAGE_FILE, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_price(model):
    """获取模型价格"""
    model_lower = model.lower()
    for key, price in MODEL_PRICES.items():
        if key.lower() in model_lower or model_lower in key.lower():
            return price
    return DEFAULT_PRICE

def log_call(model, input_tokens, output_tokens=0, cost_override=None, note=""):
    """记录一次API调用"""
    data = load_data()
    
    input_price, output_price = get_price(model)
    if cost_override:
        cost = cost_override
    else:
        cost = (input_tokens / 1_000_000) * input_price + (output_tokens / 1_000_000) * output_price
    
    entry = {
        "id": len(data['logs']) + 1,
        "timestamp": datetime.now().isoformat(),
        "model": model,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "cost": round(cost, 6),
        "note": note
    }
    
    data['logs'].append(entry)
    save_data(data)
    
    print(f"✅ 记录: {model}")
    print(f"   输入: {input_tokens:,} tokens (${input_tokens/1e6*input_price:.4f})")
    print(f"   输出: {output_tokens:,} tokens (${output_tokens/1e6*output_price:.4f})")
    print(f"   合计: ${cost:.4f}")

def report(days=7, by="day"):
    """生成消费报告"""
    data = load_data()
    
    cutoff = datetime.now() - timedelta(days=days)
    logs = [l for l in data['logs'] if datetime.fromisoformat(l['timestamp']) > cutoff]
    
    if not logs:
        print(f"过去{days}天没有记录")
        return
    
    # 总计
    total = sum(l['cost'] for l in logs)
    total_input = sum(l['input_tokens'] for l in logs)
    total_output = sum(l['output_tokens'] for l in logs)
    
    print(f"\n💰 AI消费报告 (近{days}天)")
    print(f"   生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"   总花费: ${total:.2f}")
    print(f"   总输入tokens: {total_input:,}")
    print(f"   总输出tokens: {total_output:,}")
    print(f"   总请求次数: {len(logs)}次")
    print(f"   日均: ${total/days:.2f}")
    print(f"   预估月花费: ${total/days*30:.2f}")
    
    # 按模型分组
    by_model = defaultdict(lambda: {"cost": 0, "calls": 0, "input": 0, "output": 0})
    for l in logs:
        key = l['model']
        by_model[key]['cost'] += l['cost']
        by_model[key]['calls'] += 1
        by_model[key]['input'] += l['input_tokens']
        by_model[key]['output'] += l['output_tokens']
    
    print(f"\n📊 按模型分布:")
    print("-" * 50)
    for model, stats in sorted(by_model.items(), key=lambda x: x[1]['cost'], reverse=True):
        pct = stats['cost'] / total * 100
        bar = "█" * int(pct / 5)
        print(f"   {model}")
        print(f"   ${stats['cost']:.2f} ({pct:.1f}%) {bar} | {stats['calls']}次")

def top_models(limit=5, by="cost"):
    """消费最高的模型"""
    data = load_data()
    
    by_model = defaultdict(lambda: {"cost": 0, "calls": 0})
    for l in data['logs']:
        by_model[l['model']]['cost'] += l['cost']
        by_model[l['model']]['calls'] += 1
    
    sorted_models = sorted(by_model.items(), key=lambda x: x[1][by], reverse=True)
    
    print(f"\n🏆 Top {limit} 模型 (按{by}):")
    for i, (model, stats) in enumerate(sorted_models[:limit], 1):
        print(f"   {i}. {model}: ${stats['cost']:.2f} ({stats['calls']}次)")

def budget_check(monthly_limit, days=30):
    """预算检查"""
    data = load_data()
    
    cutoff = datetime.now() - timedelta(days=days)
    logs = [l for l in data['logs'] if datetime.fromisoformat(l['timestamp']) > cutoff]
    
    total = sum(l['cost'] for l in logs)
    daily_avg = total / days if days > 0 else 0
    projected = daily_avg * 30
    
    print(f"\n📅 预算检查 (月度限额: ${monthly_limit})")
    print(f"   近{days}天消费: ${total:.2f}")
    print(f"   日均: ${daily_avg:.2f}")
    print(f"   30天预估: ${projected:.2f}")
    
    if projected > monthly_limit:
        over = projected - monthly_limit
        print(f"   ⚠️ 超出预算: ${over:.2f}")
        print(f"   💡 建议: 考虑用便宜的模型(gpt-4o-mini/deepseek-chat)")
    else:
        left = monthly_limit - projected
        print(f"   ✅ 在预算范围内，还剩 ${left:.2f}")

def alerts():
    """检查异常消费"""
    data = load_data()
    
    if not data['logs']:
        print("没有消费记录")
        return
    
    recent = [l for l in data['logs'][-20:]]
    
    print(f"\n🚨 消费警报")
    print("=" * 50)
    
    # 检查高价模型
    expensive = [l for l in recent if l['cost'] > 1.0]
    if expensive:
        print(f"\n⚠️ 高价调用 (>=$1): {len(expensive)}次")
        for l in expensive:
            dt = datetime.fromisoformat(l['timestamp']).strftime('%m-%d %H:%M')
            print(f"   {dt} | {l['model']} | ${l['cost']:.2f}")
    
    # 检查日消费
    by_day = defaultdict(float)
    for l in data['logs']:
        day = datetime.fromisoformat(l['timestamp']).strftime('%Y-%m-%d')
        by_day[day] += l['cost']
    
    recent_days = sorted(by_day.items(), key=lambda x: x[0], reverse=True)[:7]
    print(f"\n📅 日消费 (近7天):")
    for day, cost in recent_days:
        icon = "🔴" if cost > 5 else "🟡" if cost > 2 else "🟢"
        print(f"   {icon} {day}: ${cost:.2f}")
    
    # 总计
    total = sum(by_day.values())
    print(f"\n💵 总计: ${total:.2f}")

def export_csv():
    """导出CSV"""
    data = load_data()
    
    print("timestamp,model,input_tokens,output_tokens,cost,note")
    for l in data['logs']:
        print(f"{l['timestamp']},{l['model']},{l['input_tokens']},{l['output_tokens']},{l['cost']},{l['note']}")

def main():
    parser = argparse.ArgumentParser(description='AI API消费追踪器')
    subparsers = parser.add_subparsers(dest='cmd', help='子命令')
    
    # log
    log_parser = subparsers.add_parser('log', help='记录API调用')
    log_parser.add_argument('--model', '-m', required=True, help='模型名')
    log_parser.add_argument('--input', '-i', type=int, required=True, help='输入tokens')
    log_parser.add_argument('--output', '-o', type=int, default=0, help='输出tokens')
    log_parser.add_argument('--cost', '-c', type=float, help='直接指定费用')
    log_parser.add_argument('--note', '-n', default='', help='备注')
    
    # report
    report_parser = subparsers.add_parser('report', help='消费报告')
    report_parser.add_argument('--days', '-d', type=int, default=7, help='统计天数')
    
    # top
    top_parser = subparsers.add_parser('top', help='Top模型')
    top_parser.add_argument('--limit', '-n', type=int, default=5)
    top_parser.add_argument('--by', choices=['cost','calls'], default='cost')
    
    # budget
    budget_parser = subparsers.add_parser('budget', help='预算检查')
    budget_parser.add_argument('limit', type=float, help='月度限额($)')
    budget_parser.add_argument('--days', '-d', type=int, default=30)
    
    # alerts
    subparsers.add_parser('alerts', help='消费警报')
    
    # export
    export_parser = subparsers.add_parser('export', help='导出CSV')
    export_parser.add_argument('--format', '-f', choices=['csv'], default='csv')
    
    args = parser.parse_args()
    
    if not args.cmd or args.cmd == 'log':
        if args.cmd == 'log':
            log_call(args.model, args.input, args.output, args.cost, args.note)
        else:
            parser.print_help()
    
    elif args.cmd == 'report':
        report(args.days)
        
    elif args.cmd == 'top':
        top_models(args.limit, args.by)
        
    elif args.cmd == 'budget':
        budget_check(args.limit, args.days)
        
    elif args.cmd == 'alerts':
        alerts()
        
    elif args.cmd == 'export':
        export_csv()

if __name__ == '__main__':
    main()
