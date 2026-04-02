#!/usr/bin/env python3
"""
公众号每日运营任务追踪器
每天自动记录关键数据，帮助分析优化
"""
import json
from datetime import datetime, date
from pathlib import Path

DATA_FILE = Path("/Users/yyf/.openclaw/workspace/content_automation_system/output/daily_stats.json")

def load_stats():
    """加载历史数据"""
    if DATA_FILE.exists():
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_stats(stats):
    """保存数据"""
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)

def log_daily_stats(reading: int = None, new_fans: int = None, shares: int = None, notes: str = ""):
    """记录每日数据"""
    stats = load_stats()
    today = date.today().isoformat()
    
    if today not in stats:
        stats[today] = {"articles": []}
    
    stats[today]["updated_at"] = datetime.now().isoformat()
    if reading is not None:
        stats[today]["reading"] = reading
    if new_fans is not None:
        stats[today]["new_fans"] = new_fans
    if shares is not None:
        stats[today]["shares"] = shares
    if notes:
        stats[today]["notes"] = notes
    
    save_stats(stats)
    print(f"✅ 今日数据已记录: {today}")
    print(f"   阅读量: {reading or '未记录'}")
    print(f"   新增粉丝: {new_fans or '未记录'}")
    print(f"   转发数: {shares or '未记录'}")

def show_recent_stats(days: int = 7):
    """显示最近数据"""
    stats = load_stats()
    print(f"\n{'='*50}")
    print(f"📊 最近 {days} 天数据概览")
    print(f"{'='*50}\n")
    
    sorted_dates = sorted(stats.keys(), reverse=True)[:days]
    
    total_reading = 0
    total_fans = 0
    total_shares = 0
    
    for d in sorted_dates:
        s = stats[d]
        reading = s.get('reading', 0) or 0
        fans = s.get('new_fans', 0) or 0
        shares = s.get('shares', 0) or 0
        
        total_reading += reading
        total_fans += fans
        total_shares += shares
        
        print(f"📅 {d}")
        print(f"   阅读: {reading} | 新粉: {fans} | 转发: {shares}")
        if s.get('notes'):
            print(f"   备注: {s['notes']}")
        print()
    
    avg_reading = total_reading / len(sorted_dates) if sorted_dates else 0
    print(f"{'='*50}")
    print(f"📈 汇总:")
    print(f"   总阅读: {total_reading} | 日均: {avg_reading:.0f}")
    print(f"   总新增粉丝: {total_fans}")
    print(f"   总转发: {total_shares}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "log":
            # python3 daily_stats.py log --reading 1000 --fans 20 --shares 5
            reading = int(sys.argv[2].split("=")[1]) if len(sys.argv) > 2 and sys.argv[2].startswith("--reading=") else None
            fans = int(sys.argv[3].split("=")[1]) if len(sys.argv) > 3 and sys.argv[3].startswith("--fans=") else None
            shares = int(sys.argv[4].split("=")[1]) if len(sys.argv) > 4 and sys.argv[4].startswith("--shares=") else None
            log_daily_stats(reading, fans, shares)
        elif sys.argv[1] == "show":
            days = int(sys.argv[2]) if len(sys.argv) > 2 else 7
            show_recent_stats(days)
        else:
            print("用法:")
            print("  python3 daily_stats.py log --reading=1000 --fans=20 --shares=5")
            print("  python3 daily_stats.py show [天数]")
    else:
        show_recent_stats()
