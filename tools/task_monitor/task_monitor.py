#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenClaw定时任务监控工具
通过Gateway API获取任务状态

用法：
  python task_monitor.py list
  python task_monitor.py status <job_id>
  python task_monitor.py alerts
  python task_monitor.py health
"""

import sys
import os
import json
import argparse
import requests
from datetime import datetime

# Gateway配置
GATEWAY_HOST = "127.0.0.1"
GATEWAY_PORT = 18789
GATEWAY_TOKEN = None  # 从配置文件读取

def get_gateway_token():
    """从配置文件获取token"""
    config_path = os.path.expanduser("~/.openclaw/openclaw.json")
    try:
        with open(config_path) as f:
            raw = f.read()
            # 找token
            import re
            m = re.search(r'token:\s*[\'"]([^\'"]+)[\'"]', raw)
            if m:
                return m.group(1)
    except:
        pass
    return None

def api_get(endpoint):
    """GET请求Gateway API"""
    token = get_gateway_token()
    headers = {}
    if token:
        headers['Authorization'] = f'Bearer {token}'
    
    url = f"http://{GATEWAY_HOST}:{GATEWAY_PORT}{endpoint}"
    try:
        resp = requests.get(url, headers=headers, timeout=5)
        return resp.json()
    except Exception as e:
        return {"error": str(e)}

def api_post(endpoint, data=None):
    """POST请求Gateway API"""
    token = get_gateway_token()
    headers = {'Content-Type': 'application/json'}
    if token:
        headers['Authorization'] = f'Bearer {token}'
    
    url = f"http://{GATEWAY_HOST}:{GATEWAY_PORT}{endpoint}"
    try:
        resp = requests.post(url, json=data or {}, headers=headers, timeout=5)
        return resp.json()
    except Exception as e:
        return {"error": str(e)}

def get_gateway_health():
    """获取Gateway健康状态"""
    return api_get("/health")

def get_cron_jobs():
    """获取cron任务列表"""
    result = api_get("/api/cron/list")
    if "error" in result:
        # 尝试旧版API
        result = api_post("/api/cron/status")
    return result

def get_job_runs(job_id, limit=5):
    """获取任务执行历史"""
    return api_post("/api/cron/runs", {"jobId": job_id, "limit": limit})

def parse_schedule(schedule):
    """解析cron表达式"""
    if isinstance(schedule, dict):
        kind = schedule.get('kind', '')
        if kind == 'every':
            ms = schedule.get('everyMs', 0)
            if ms >= 3600000:
                return f"每 {ms/3600000:.1f} 小时"
            elif ms >= 60000:
                return f"每 {ms/60000:.0f} 分钟"
            else:
                return f"每 {ms/1000:.0f} 秒"
        elif kind == 'cron':
            return f"Cron: {schedule.get('expr', '')}"
        elif kind == 'at':
            return f"一次: {schedule.get('at', '')}"
    return str(schedule) if schedule else '未知'

def format_time(ts):
    """格式化时间戳"""
    if not ts:
        return '从未'
    try:
        dt = datetime.fromtimestamp(ts)
        now = datetime.now()
        diff = (now - dt).total_seconds()
        
        if diff < 60:
            return f"{int(diff)}秒前"
        elif diff < 3600:
            return f"{int(diff/60)}分钟前"
        elif diff < 86400:
            return f"{int(diff/3600)}小时前"
        else:
            return dt.strftime('%m-%d %H:%M')
    except:
        return str(ts)

def check_failures(jobs):
    """检查失败任务"""
    alerts = []
    if not isinstance(jobs, list):
        return alerts
    
    for job in jobs:
        last_run = job.get('lastRun') or job.get('last_run')
        last_status = job.get('lastStatus') or job.get('last_status') or job.get('status', 'unknown')
        enabled = job.get('enabled', True)
        
        if last_status in ['failed', 'error', 'FAILED', 'ERROR']:
            alerts.append({
                'job_id': job.get('id') or job.get('name', 'unknown'),
                'name': job.get('name', '未命名'),
                'last_run': last_run,
                'status': last_status
            })
            continue
        
        # 检查超过24小时没运行的任务
        if enabled and last_run:
            try:
                diff = (datetime.now() - datetime.fromtimestamp(last_run)).total_seconds()
                if diff > 86400:
                    alerts.append({
                        'job_id': job.get('id') or job.get('name', 'unknown'),
                        'name': job.get('name', '未命名'),
                        'last_run': last_run,
                        'status': 'stale',
                        'message': f'超过 {int(diff/3600)} 小时未运行'
                    })
            except:
                pass
    
    return alerts

def print_job_list(jobs):
    """打印任务列表"""
    if not isinstance(jobs, list):
        print(f"❌ 获取任务列表失败: {jobs}")
        return
    
    enabled = [j for j in jobs if j.get('enabled', True)]
    disabled = [j for j in jobs if not j.get('enabled', True)]
    
    print(f"\n📋 定时任务")
    print(f"   启用中: {len(enabled)} | 已停用: {len(disabled)}")
    print("=" * 70)
    
    for job in enabled:
        job_id = job.get('id') or job.get('name', '?')
        name = job.get('name', '未命名')
        schedule = parse_schedule(job.get('schedule', {}))
        last_run = format_time(job.get('lastRun') or job.get('last_run'))
        last_status = job.get('lastStatus') or job.get('last_status') or 'unknown'
        
        status_icon = {
            'success': '✅',
            'failed': '❌',
            'error': '❌',
            'running': '🔄',
            'unknown': '❓'
        }.get(str(last_status).lower(), '❓')
        
        print(f"\n  🔹 {name}")
        print(f"     ID: {job_id}")
        print(f"     调度: {schedule}")
        print(f"     上次运行: {last_run} {status_icon}")
    
    if disabled:
        print(f"\n\n⏸ 已停用任务 ({len(disabled)}):")
        for job in disabled:
            name = job.get('name', '未命名')
            print(f"  - {name}")

def print_alerts(alerts):
    """打印报警信息"""
    if not alerts:
        print("\n✅ 没有异常")
        return
    
    print(f"\n🚨 任务异常 ({len(alerts)}):")
    print("=" * 70)
    for alert in alerts:
        status_icon = '❌' if alert['status'] in ['failed', 'error'] else '⚠️'
        print(f"\n  {status_icon} {alert['name']}")
        print(f"     ID: {alert['job_id']}")
        print(f"     问题: {alert.get('message', alert['status'])}")
        print(f"     上次运行: {format_time(alert['last_run'])}")

def print_health():
    """打印Gateway健康状态"""
    health = get_gateway_health()
    if "error" in health:
        print(f"❌ Gateway未响应: {health['error']}")
        return
    
    print(f"\n🏥 Gateway健康状态")
    print("=" * 50)
    print(f"   状态: {'✅ 正常' if health.get('ok') or health.get('status') == 'ok' else '⚠️ 异常'}")
    
    # 尝试获取更多状态
    status = api_get("/api/status")
    if "error" not in status:
        if 'uptime' in status:
            uptime_sec = status.get('uptime', 0)
            print(f"   运行时间: {uptime_sec/3600:.1f} 小时")
        if 'version' in status:
            print(f"   版本: {status['version']}")
    
    print()

def main():
    parser = argparse.ArgumentParser(description='OpenClaw定时任务监控工具')
    subparsers = parser.add_subparsers(dest='cmd', help='子命令')
    
    subparsers.add_parser('list', help='列出所有任务')
    subparsers.add_parser('alerts', help='检查异常任务')
    subparsers.add_parser('health', help='Gateway健康状态')
    
    status_parser = subparsers.add_parser('status', help='查看任务详情')
    status_parser.add_argument('job_id', nargs='?', help='任务ID')
    
    history_parser = subparsers.add_parser('history', help='查看执行历史')
    history_parser.add_argument('job_id', nargs='?', help='任务ID')
    history_parser.add_argument('--limit', '-n', type=int, default=5)
    
    args = parser.parse_args()
    
    if not args.cmd or args.cmd == 'list':
        print_health()
        jobs = get_cron_jobs()
        print_job_list(jobs)
        
    elif args.cmd == 'alerts':
        jobs = get_cron_jobs()
        alerts = check_failures(jobs) if isinstance(jobs, list) else []
        print_alerts(alerts)
        
    elif args.cmd == 'health':
        print_health()
        
    elif args.cmd == 'status':
        jobs = get_cron_jobs()
        if isinstance(jobs, list):
            for job in jobs:
                if job.get('id') == args.job_id or job.get('name') == args.job_id:
                    print(f"\n📊 {job.get('name', '?')}")
                    for k, v in job.items():
                        if k not in ['id', 'name']:
                            print(f"   {k}: {v}")
                    return
            print(f"未找到任务: {args.job_id}")
        else:
            print(f"获取失败: {jobs}")
        
    elif args.cmd == 'history':
        if not args.job_id:
            jobs = get_cron_jobs()
            if isinstance(jobs, list):
                print(f"\n📜 所有任务执行历史:")
                for job in jobs[:10]:
                    print(f"\n  {job.get('name', '?')}:")
                    runs = get_job_runs(job.get('id', ''), args.limit)
                    if isinstance(runs, list):
                        for r in runs[:3]:
                            print(f"    - {format_time(r.get('timestamp'))}: {r.get('status', 'unknown')}")
                    else:
                        print(f"    (无可用历史)")
        else:
            runs = get_job_runs(args.job_id, args.limit)
            if isinstance(runs, list):
                print(f"\n📜 任务 {args.job_id} 执行历史:")
                for i, r in enumerate(runs, 1):
                    print(f"  {i}. {format_time(r.get('timestamp'))}: {r.get('status', 'unknown')}")
            else:
                print(f"获取失败: {runs}")

if __name__ == '__main__':
    main()
