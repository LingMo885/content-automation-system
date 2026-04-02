#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI模型选择器
根据任务类型、预算、场景推荐最适合的模型

用法：
  python model_selector.py recommend --task 写作 --budget low
  python model_selector.py compare gpt-4o claude-sonnet-4
  python model_selector.py list --filter cheap
  python model_selector.py benchmark --task 写作
"""

import json
import argparse
from datetime import datetime

# ========== 模型数据库 ==========

MODELS = {
    # === OpenAI ===
    "gpt-4o": {
        "provider": "OpenAI",
        "context": 128000,
        "input_cost": 5.0,  # $/M tokens
        "output_cost": 15.0,
        "strengths": ["全能", "长上下文", "函数调用"],
        "weaknesses": ["贵", "中文略弱"],
        "best_for": ["复杂推理", "代码生成", "长文写作", "多模态"],
        "speed": "medium",
        "rank_general": 1,
    },
    "gpt-4o-mini": {
        "provider": "OpenAI",
        "context": 128000,
        "input_cost": 0.15,
        "output_cost": 0.6,
        "strengths": ["性价比高", "速度快"],
        "weaknesses": ["复杂推理弱"],
        "best_for": ["日常对话", "简单写作", "翻译"],
        "speed": "fast",
        "rank_general": 3,
    },
    "o3-mini": {
        "provider": "OpenAI",
        "context": 100000,
        "input_cost": 1.1,
        "output_cost": 4.4,
        "strengths": ["推理能力强", "便宜"],
        "weaknesses": ["无多模态"],
        "best_for": ["代码调试", "数学", "逻辑推理"],
        "speed": "medium",
        "rank_general": 2,
    },
    
    # === Anthropic ===
    "claude-sonnet-4": {
        "provider": "Anthropic",
        "context": 200000,
        "input_cost": 3.0,
        "output_cost": 15.0,
        "strengths": ["中文优秀", "长文分析", "创意写作"],
        "weaknesses": ["稍贵"],
        "best_for": ["内容创作", "深度分析", "长文本总结"],
        "speed": "medium",
        "rank_general": 1,
    },
    "claude-3-5-haiku": {
        "provider": "Anthropic",
        "context": 200000,
        "input_cost": 0.8,
        "output_cost": 4.0,
        "strengths": ["速度快", "中文好", "便宜"],
        "weaknesses": ["复杂任务弱"],
        "best_for": ["快速问答", "日常对话", "摘要"],
        "speed": "fast",
        "rank_general": 4,
    },
    
    # === Google ===
    "gemini-2.0-flash": {
        "provider": "Google",
        "context": 1000000,
        "input_cost": 0,
        "output_cost": 0,
        "strengths": ["免费", "超长上下文", "多模态"],
        "weaknesses": ["复杂推理一般"],
        "best_for": ["长文本处理", "多模态任务", "低成本"],
        "speed": "fast",
        "rank_general": 2,
    },
    "gemini-2.5-pro": {
        "provider": "Google",
        "context": 1000000,
        "input_cost": 1.25,
        "output_cost": 5.0,
        "strengths": ["超长上下文", "多模态", "性价比"],
        "weaknesses": ["中文略弱"],
        "best_for": ["长文本", "视频理解", "复杂任务"],
        "speed": "medium",
        "rank_general": 2,
    },
    
    # === DeepSeek ===
    "deepseek-chat": {
        "provider": "DeepSeek",
        "context": 64000,
        "input_cost": 0.27,
        "output_cost": 1.1,
        "strengths": ["便宜", "代码强", "中文优化"],
        "weaknesses": ["复杂推理不如o1"],
        "best_for": ["代码", "中文内容", "低成本"],
        "speed": "fast",
        "rank_general": 5,
    },
    "deepseek-r1": {
        "provider": "DeepSeek",
        "context": 64000,
        "input_cost": 0.55,
        "output_cost": 2.19,
        "strengths": ["推理能力强", "数学强"],
        "weaknesses": ["没有输入输出成本"],
        "best_for": ["复杂推理", "数学证明", "代码调试"],
        "speed": "slow",
        "rank_general": 2,
    },
    
    # === 开源本地 ===
    "qwen3:8b": {
        "provider": "本地/Ollama",
        "context": 32000,
        "input_cost": 0,
        "output_cost": 0,
        "strengths": ["免费", "隐私", "可本地"],
        "weaknesses": ["能力弱", "需要硬件"],
        "best_for": ["实验", "隐私场景", "简单任务"],
        "speed": "medium",
        "rank_general": 8,
    },
    "qwen3:32b": {
        "provider": "本地/Ollama",
        "context": 32000,
        "input_cost": 0,
        "output_cost": 0,
        "strengths": ["免费", "能力接近GPT-4"],
        "weaknesses": ["需要高配硬件"],
        "best_for": ["本地开发", "隐私场景"],
        "speed": "slow",
        "rank_general": 6,
    },
}

# ========== 任务匹配 ==========

TASK_TAGS = {
    "写作": ["gpt-4o", "claude-sonnet-4", "gemini-2.5-pro"],
    "代码": ["deepseek-chat", "gpt-4o", "o3-mini", "qwen3:32b"],
    "推理": ["o3-mini", "deepseek-r1", "gpt-4o"],
    "长文本": ["gemini-2.0-flash", "gemini-2.5-pro", "claude-sonnet-4"],
    "翻译": ["gpt-4o-mini", "claude-3-5-haiku", "deepseek-chat"],
    "摘要": ["claude-3-5-haiku", "gemini-2.0-flash", "qwen3:8b"],
    "创意": ["claude-sonnet-4", "gpt-4o", "gemini-2.5-pro"],
    "分析": ["claude-sonnet-4", "gpt-4o", "deepseek-chat"],
    "中文内容": ["claude-sonnet-4", "deepseek-chat", "qwen3:32b"],
    "低成本": ["gemini-2.0-flash", "gpt-4o-mini", "deepseek-chat", "qwen3:8b"],
    "多模态": ["gpt-4o", "gemini-2.0-flash", "gemini-2.5-pro"],
    "隐私": ["qwen3:8b", "qwen3:32b"],
    "数学": ["deepseek-r1", "o3-mini", "gpt-4o"],
}

BUDGET_LEVELS = {
    "free": ["gemini-2.0-flash", "qwen3:8b", "qwen3:32b"],
    "low": ["deepseek-chat", "gpt-4o-mini", "claude-3-5-haiku"],
    "medium": ["claude-sonnet-4", "gemini-2.5-pro", "o3-mini"],
    "high": ["gpt-4o", "claude-sonnet-4"],
}

SPEED_PRIORITY = {
    "realtime": ["gemini-2.0-flash", "gpt-4o-mini", "claude-3-5-haiku", "qwen3:8b"],
    "balanced": ["deepseek-chat", "claude-sonnet-4", "gemini-2.5-pro"],
    "quality": ["o3-mini", "deepseek-r1", "gpt-4o"],
}

def recommend(task=None, budget=None, speed=None, top_k=3):
    """推荐模型"""
    scores = {}
    
    for model_id, model in MODELS.items():
        score = 0
        
        # 任务匹配
        if task:
            task_models = TASK_TAGS.get(task, [])
            if model_id in task_models:
                score += 50
            # 部分匹配best_for
            for bf in model.get("best_for", []):
                if task.lower() in bf.lower():
                    score += 20
        
        # 预算匹配
        if budget:
            budget_models = BUDGET_LEVELS.get(budget, [])
            if model_id in budget_models:
                score += 30
        
        # 速度匹配
        if speed:
            speed_models = SPEED_PRIORITY.get(speed, [])
            if model_id in speed_models:
                score += 20
        
        # 通用能力加成
        score += (10 - model.get("rank_general", 5)) * 3
        
        scores[model_id] = score
    
    # 排序
    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    
    print(f"\n🔮 AI模型推荐")
    if task:
        print(f"   任务: {task}")
    if budget:
        print(f"   预算: {budget}")
    if speed:
        print(f"   速度: {speed}")
    print(f"\n{'='*60}")
    
    for i, (model_id, score) in enumerate(ranked[:top_k], 1):
        m = MODELS[model_id]
        cost_str = f"${m['input_cost']}/${m['output_cost']}" if m['input_cost'] > 0 else "免费"
        print(f"\n  {i}. {model_id} ({m['provider']})")
        print(f"     ⭐ 评分: {score:.0f}")
        print(f"     💰 成本: ${m['input_cost']}/M in / ${m['output_cost']}/M out")
        print(f"     📏 上下文: {m['context']//1000}K tokens")
        print(f"     ⚡ 速度: {m['speed']}")
        print(f"     ✅ 擅长: {', '.join(m['best_for'][:3])}")
        print(f"     ⚠️ 劣势: {m['weaknesses']}")

def compare(model_ids):
    """对比模型"""
    print(f"\n⚖️ 模型对比")
    print("=" * 70)
    
    for model_id in model_ids:
        if model_id not in MODELS:
            print(f"❌ 未知模型: {model_id}")
            continue
        
        m = MODELS[model_id]
        print(f"\n【{model_id}】")
        print(f"   厂商: {m['provider']}")
        print(f"   成本: ${m['input_cost']}/M in / ${m['output_cost']}/M out")
        print(f"   上下文: {m['context']//1000}K tokens")
        print(f"   擅长: {', '.join(m['best_for'])}")
        print(f"   劣势: {m['weaknesses']}")
        print(f"   速度: {m['speed']}")

def list_models(filter_type=None):
    """列出所有模型"""
    print(f"\n📋 模型列表 ({len(MODELS)}个)")
    print("=" * 70)
    
    by_provider = {}
    for model_id, m in MODELS.items():
        p = m['provider']
        if p not in by_provider:
            by_provider[p] = []
        by_provider[p].append((model_id, m))
    
    for provider, models in sorted(by_provider.items()):
        print(f"\n🏢 {provider}")
        for model_id, m in models:
            cost = f"${m['input_cost']}" if m['input_cost'] > 0 else "免费"
            print(f"   • {model_id}: {cost}/M | {m['context']//1000}K | {' '.join(m['best_for'][:2])}")

def quick_decide():
    """快速决策"""
    print(f"\n🎯 快速选择")
    print("=" * 50)
    print(f"\n  写作/内容创作 → claude-sonnet-4")
    print(f"  代码/开发       → deepseek-chat 或 o3-mini")
    print(f"  推理/分析       → o3-mini 或 deepseek-r1")
    print(f"  长文本/总结     → gemini-2.0-flash (免费!)")
    print(f"  翻译/快速问答   → gpt-4o-mini")
    print(f"  隐私/本地       → qwen3:32b (本地)")
    print(f"  多模态         → gpt-4o 或 gemini-2.5-pro")
    print(f"\n  💡 省钱组合: gemini-2.0-flash(免费) + claude-sonnet-4(写作)")

def main():
    parser = argparse.ArgumentParser(description='AI模型选择器')
    subparsers = parser.add_subparsers(dest='cmd', help='子命令')
    
    rec_parser = subparsers.add_parser('recommend', help='推荐模型')
    rec_parser.add_argument('--task', '-t', help='任务类型: 写作/代码/推理/翻译/摘要/创意/分析')
    rec_parser.add_argument('--budget', '-b', choices=['free','low','medium','high'], help='预算等级')
    rec_parser.add_argument('--speed', '-s', choices=['realtime','balanced','quality'], help='速度要求')
    rec_parser.add_argument('--top', '-k', type=int, default=3, help='推荐数量')
    
    cmp_parser = subparsers.add_parser('compare', help='对比模型')
    cmp_parser.add_argument('models', nargs='+', help='模型ID')
    
    list_parser = subparsers.add_parser('list', help='列出所有模型')
    list_parser.add_argument('--filter', '-f', choices=['cheap','expensive','fast','long_context'])
    
    subparsers.add_parser('decide', help='快速决策')
    
    args = parser.parse_args()
    
    if not args.cmd or args.cmd == 'recommend':
        recommend(args.task, args.budget, args.speed, args.top if args.cmd else 3)
        
    elif args.cmd == 'compare':
        compare(args.models)
        
    elif args.cmd == 'list':
        list_models(args.filter if hasattr(args, 'filter') else None)
        
    elif args.cmd == 'decide':
        quick_decide()

if __name__ == '__main__':
    main()
