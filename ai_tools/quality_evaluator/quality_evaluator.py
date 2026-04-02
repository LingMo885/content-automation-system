#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI输出质量评估器
帮你判断AI生成的内容质量，给出改进建议

用法：
  python quality_evaluator.py eval "AI生成的内容"
  python quality_evaluator.py check --file output.txt
  python quality_evaluator.py compare file1.txt file2.txt
"""

import re
import argparse
from difflib import SequenceMatcher

# ========== 评估维度 ==========

def evaluate_text(text):
    """评估文本质量"""
    scores = {}
    issues = []
    suggestions = []
    
    # 1. 长度评估
    length = len(text)
    if length < 50:
        scores['长度'] = 2
        issues.append("内容太短，可能不够深入")
        suggestions.append("扩展论述，增加具体案例或数据支撑")
    elif length < 200:
        scores['长度'] = 6
        issues.append("内容偏短，可以适当展开")
        suggestions.append("每个观点至少展开2-3句说明")
    elif length < 500:
        scores['长度'] = 8
    elif length < 1000:
        scores['长度'] = 9
    else:
        scores['长度'] = 10
    
    # 2. 结构评估
    has_headers = bool(re.search(r'^#{1,3}\s|\n【', text, re.MULTILINE))
    has_list = bool(re.search(r'\n[0-9]+[.)、]|\n[-*●]', text))
    has_conclusion = bool(re.search(r'总结|总之|综上所述|结论|因此|所以', text))
    
    structure_score = 5
    if has_headers:
        structure_score += 2
    if has_list:
        structure_score += 2
    if has_conclusion:
        structure_score += 1
    
    scores['结构'] = min(structure_score, 10)
    
    if not has_headers and not has_list:
        issues.append("缺乏结构化组织，难阅读")
        suggestions.append("使用标题、分点、项目符号来组织内容")
    if not has_conclusion:
        issues.append("缺少结论或总结")
        suggestions.append("添加总结段落，呼应开头")
    
    # 3. 重复检测
    words = re.findall(r'[\u4e00-\u9fff]{2,}', text)
    word_count = {}
    for w in words:
        word_count[w] = word_count.get(w, 0) + 1
    
    repeats = [(w, c) for w, c in word_count.items() if c >= 3 and len(w) > 3]
    if repeats:
        top_repeat = max(repeats, key=lambda x: x[1])
        scores['重复度'] = max(3, 10 - top_repeat[1] * 2)
        if top_repeat[1] >= 5:
            issues.append(f"重复词过多: '{top_repeat[0]}' 出现{top_repeat[1]}次")
            suggestions.append(f"减少'{top_repeat[0]}'的使用频率，用同义词替代")
    else:
        scores['重复度'] = 10
    
    # 4. 格式评估
    format_score = 7
    has_emoji = bool(re.search(r'[\U0001F300-\U0001F9FF]', text))
    has_punctuation = '。' in text or '！' in text or '？' in text
    
    if not has_punctuation:
        format_score -= 3
        issues.append("缺少标点符号")
        suggestions.append("添加句号、逗号等标点")
    
    if has_emoji:
        format_score = min(format_score + 1, 10)
    
    # 检查无意义字符
    meaningless = re.findall(r'[a-zA-Z]{20,}', text)
    if meaningless:
        format_score -= 2
        issues.append("包含过长无意义的字符串")
    
    scores['格式'] = max(format_score, 1)
    
    # 5. 句子长度评估
    sentences = re.split(r'[。！？\n]', text)
    sentences = [s.strip() for s in sentences if s.strip() and len(s) > 3]
    
    if sentences:
        avg_sentence_len = sum(len(s) for s in sentences) / len(sentences)
        long_sentences = sum(1 for s in sentences if len(s) > 80)
        
        if avg_sentence_len > 50:
            scores['句长'] = 7
        else:
            scores['句长'] = 9
        
        if long_sentences > len(sentences) * 0.3:
            issues.append(f"长句过多({long_sentences}句超过80字)")
            suggestions.append("拆分长句，每句不超过40字更易读")
    else:
        scores['句长'] = 5
    
    # 6. AI味检测
    ai_patterns = [
        (r'作为一个人工智能', 3),
        (r'需要注意的是', 2),
        (r'总的来说', 2),
        (r'首先、其次、最后', 3),
        (r'总而言之', 2),
        (r'这意味着', 2),
        (r'值得注意的是', 2),
        (r'让我们来', 2),
    ]
    
    ai_score = 10
    found_patterns = []
    for pattern, penalty in ai_patterns:
        matches = re.findall(pattern, text)
        if matches:
            ai_score -= penalty
            found_patterns.append(pattern)
    
    scores['AI味'] = max(ai_score, 1)
    
    if found_patterns:
        issues.append(f"包含AI常用表达: {', '.join(found_patterns[:3])}")
        suggestions.append("用更自然、口语化的表达替代AI模板句式")
    
    # 7. 情感/态度评估
    positive_words = ['好', '优秀', '棒', '赞', '厉害', '完美', '卓越']
    negative_words = ['差', '糟糕', '烂', '垃圾', '失败']
    
    pos_count = sum(1 for w in positive_words if w in text)
    neg_count = sum(1 for w in negative_words if w in text)
    
    if neg_count > pos_count:
        scores['情感平衡'] = 5
    else:
        scores['情感平衡'] = 9
    
    return scores, issues, suggestions


def print_report(scores, issues, suggestions):
    """打印评估报告"""
    overall = sum(scores.values()) / len(scores)
    
    print(f"\n📊 AI输出质量评估报告")
    print(f"{'='*50}")
    print(f"   综合得分: {overall:.1f}/10 ", end='')
    
    if overall >= 8:
        print("✅ 优秀")
    elif overall >= 6:
        print("👍 良好")
    elif overall >= 4:
        print("⚠️ 需改进")
    else:
        print("❌ 不合格")
    
    print(f"\n📈 分项得分:")
    print("-" * 50)
    for dim, score in sorted(scores.items(), key=lambda x: x[1]):
        bar = "▓" * int(score) + "░" * (10 - int(score))
        icon = "✅" if score >= 7 else "⚠️" if score >= 4 else "❌"
        print(f"   {icon} {dim:8s} [{bar}] {score:.0f}/10")
    
    if issues:
        print(f"\n⚠️ 发现问题:")
        for i, issue in enumerate(issues[:5], 1):
            print(f"   {i}. {issue}")
    
    if suggestions:
        print(f"\n💡 改进建议:")
        for i, sug in enumerate(suggestions[:5], 1):
            print(f"   {i}. {sug}")

def compare_texts(text1, text2):
    """对比两个文本"""
    s = SequenceMatcher(None, text1, text2)
    similarity = s.ratio()
    
    print(f"\n⚖️ 文本对比")
    print(f"{'='*50}")
    print(f"   相似度: {similarity*100:.1f}%")
    
    if similarity > 0.8:
        print("   🔴 相似度太高，可能有重复")
    elif similarity > 0.5:
        print("   🟡 有一定差异，内容较独立")
    else:
        print("   🟢 差异较大，内容独特")
    
    # 长度对比
    print(f"\n   文本1长度: {len(text1)} 字")
    print(f"   文本2长度: {len(text2)} 字")
    
    # 词语差异
    words1 = set(re.findall(r'[\u4e00-\u9fff]{2,}', text1))
    words2 = set(re.findall(r'[\u4e00-\u9fff]{2,}', text2))
    common = words1 & words2
    unique1 = words1 - words2
    unique2 = words2 - words1
    
    if common:
        print(f"\n   共同词汇: {len(common)} 个")
    if unique1:
        print(f"   文本1独有用词: {len(unique1)} 个 → {', '.join(list(unique1)[:5])}...")
    if unique2:
        print(f"   文本2独有用词: {len(unique2)} 个 → {', '.join(list(unique2)[:5])}...")

def quick_check(text):
    """快速检查"""
    length = len(text)
    
    if length < 50:
        return "❌ 内容太短"
    
    has_structure = bool(re.search(r'\n[【#0-9]', text))
    has_conclusion = bool(re.search(r'总结|结论|因此|所以', text))
    
    if has_structure and has_conclusion:
        return "✅ 结构完整"
    elif has_structure:
        return "⚠️ 有结构但缺总结"
    elif has_conclusion:
        return "⚠️ 有总结但缺结构"
    else:
        return "❌ 结构和总结都缺"

def main():
    parser = argparse.ArgumentParser(description='AI输出质量评估器')
    subparsers = parser.add_subparsers(dest='cmd', help='子命令')
    
    # eval
    eval_parser = subparsers.add_parser('eval', help='评估内容')
    eval_parser.add_argument('text', nargs='?', help='要评估的文本')
    eval_parser.add_argument('--file', '-f', help='从文件读取')
    
    # check
    check_parser = subparsers.add_parser('check', help='快速检查')
    check_parser.add_argument('text', nargs='?', help='要检查的文本')
    check_parser.add_argument('--file', '-f', help='从文件读取')
    
    # compare
    cmp_parser = subparsers.add_parser('compare', help='对比两个文本')
    cmp_parser.add_argument('file1', help='第一个文件')
    cmp_parser.add_argument('file2', help='第二个文件')
    
    args = parser.parse_args()
    
    text = None
    
    if args.cmd == 'eval' or args.cmd == 'check':
        if args.text:
            text = args.text
        elif args.file:
            with open(args.file, 'r', encoding='utf-8') as f:
                text = f.read()
        else:
            # 从stdin读取
            print("请输入要评估的文本（Ctrl+D结束输入）:")
            text = sys.stdin.read()
        
        if args.cmd == 'check':
            result = quick_check(text)
            print(f"\n{result}")
        else:
            scores, issues, suggestions = evaluate_text(text)
            print_report(scores, issues, suggestions)
    
    elif args.cmd == 'compare':
        with open(args.file1, 'r', encoding='utf-8') as f:
            text1 = f.read()
        with open(args.file2, 'r', encoding='utf-8') as f:
            text2 = f.read()
        compare_texts(text1, text2)
    
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
