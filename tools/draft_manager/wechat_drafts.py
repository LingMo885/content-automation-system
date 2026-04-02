#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信公众号草稿箱管理工具
功能：
  - 列出所有草稿（标题、日期、封面）
  - 显示草稿详情
  - 删除指定草稿
  - 统计草稿数量

用法：
  python wechat_drafts.py list
  python wechat_drafts.py list --limit 10
  python wechat_drafts.py delete <media_id>
  python wechat_drafts.py count
  python wechat_drafts.py detail <media_id>
"""

import sys
import os
import json
import argparse
import requests
from datetime import datetime

# 微信公众号配置
WECHAT_APPID = "wxa05c024a3d75eaa0"
WECHAT_APPSECRET = "a98f98457262ba27bf68a7950f4a99d7"
ACCESS_TOKEN_CACHE = "/tmp/wechat_draft_token.json"

def get_access_token(force_refresh=False):
    """获取Access Token"""
    # 检查缓存
    if not force_refresh and os.path.exists(ACCESS_TOKEN_CACHE):
        with open(ACCESS_TOKEN_CACHE, 'r') as f:
            cache = json.load(f)
            if cache.get('expires_at', 0) > datetime.now().timestamp() + 300:
                return cache['token']
    
    url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={WECHAT_APPID}&secret={WECHAT_APPSECRET}"
    try:
        resp = requests.get(url, timeout=10)
        data = resp.json()
        if 'access_token' in data:
            token = data['access_token']
            cache = {
                'token': token,
                'expires_at': datetime.now().timestamp() + data.get('expires_in', 7200)
            }
            with open(ACCESS_TOKEN_CACHE, 'w') as f:
                json.dump(cache, f)
            return token
    except Exception as e:
        print(f"获取Token失败: {e}")
    return None

def list_drafts(token, limit=20, offset=0):
    """获取草稿列表"""
    url = f"https://api.weixin.qq.com/cgi-bin/draft/count?access_token={token}"
    try:
        count_resp = requests.get(url, timeout=10)
        count_data = count_resp.json()
        total = count_data.get('total_count', 0)
        print(f"\n📋 草稿箱总计: {total} 篇\n")
        
        if total == 0:
            return []
        
        # 获取草稿列表
        list_url = f"https://api.weixin.qq.com/cgi-bin/draft/batchget?access_token={token}"
        list_payload = {
            "offset": offset,
            "count": limit,
            "no_content": 0
        }
        
        list_resp = requests.post(list_url, json=list_payload, timeout=10)
        list_data = list_resp.json()
        
        items = list_data.get('item', [])
        drafts = []
        
        for i, item in enumerate(items):
            articles = item.get('content', {}).get('news_item', [])
            if articles:
                article = articles[0]
                update_time = datetime.fromtimestamp(item.get('update_time', 0)).strftime('%Y-%m-%d %H:%M')
                digest = article.get('digest', '')[:30]
                thumb_url = article.get('thumb_url', '')
                
                drafts.append({
                    'media_id': item.get('media_id'),
                    'title': article.get('title', '无标题'),
                    'author': article.get('author', ''),
                    'digest': digest,
                    'update_time': update_time,
                    'thumb_url': thumb_url,
                    'need_open_comment': article.get('need_open_comment', 0),
                })
        
        return drafts
        
    except Exception as e:
        print(f"获取草稿列表失败: {e}")
        return []

def print_drafts(drafts, show_thumb=True):
    """打印草稿列表"""
    if not drafts:
        print("没有草稿")
        return
    
    print("=" * 70)
    for i, draft in enumerate(drafts, 1):
        print(f"  {i}. {draft['title']}")
        print(f"     作者: {draft['author'] or '未设置'}")
        print(f"     更新时间: {draft['update_time']}")
        print(f"     摘要: {draft['digest']}")
        if show_thumb and draft['thumb_url']:
            print(f"     封面: {draft['thumb_url'][:50]}...")
        print(f"     media_id: {draft['media_id']}")
        print("-" * 70)

def delete_draft(token, media_id):
    """删除草稿"""
    url = f"https://api.weixin.qq.com/cgi-bin/draft/delete?access_token={token}"
    payload = {"media_id": media_id}
    try:
        resp = requests.post(url, json=payload, timeout=10)
        data = resp.json()
        if data.get('errcode') == 0:
            print(f"✅ 删除成功: {media_id}")
            return True
        else:
            print(f"❌ 删除失败: {data.get('errmsg', '未知错误')}")
            return False
    except Exception as e:
        print(f"❌ 删除异常: {e}")
        return False

def get_draft_detail(token, media_id):
    """获取草稿详情"""
    url = f"https://api.weixin.qq.com/cgi-bin/draft/get?access_token={token}"
    payload = {"media_id": media_id}
    try:
        resp = requests.post(url, json=payload, timeout=10)
        data = resp.json()
        
        if 'news_item' in data:
            articles = data['news_item']
            for art in articles:
                print(f"\n📄 标题: {art.get('title', '无标题')}")
                print(f"   作者: {art.get('author', '')}")
                print(f"   摘要: {art.get('digest', '')}")
                print(f"   封面: {art.get('thumb_url', '')}")
                print(f"   链接: {art.get('url', '')}")
                content = art.get('content', '')
                content_clean = content.replace('<[^>]+>', '')[:200]
                print(f"   内容预览: {content_clean}...")
        else:
            print(f"获取详情失败: {data}")
            
    except Exception as e:
        print(f"获取详情异常: {e}")

def main():
    parser = argparse.ArgumentParser(description='微信公众号草稿箱管理工具')
    subparsers = parser.add_subparsers(dest='cmd', help='子命令')
    
    # list命令
    list_parser = subparsers.add_parser('list', help='列出所有草稿')
    list_parser.add_argument('--limit', type=int, default=20, help='显示数量')
    list_parser.add_argument('--offset', type=int, default=0, help='偏移量')
    
    # delete命令
    delete_parser = subparsers.add_parser('delete', help='删除草稿')
    delete_parser.add_argument('media_id', help='草稿media_id')
    
    # count命令
    subparsers.add_parser('count', help='统计草稿数量')
    
    # detail命令
    detail_parser = subparsers.add_parser('detail', help='查看草稿详情')
    detail_parser.add_argument('media_id', help='草稿media_id')
    
    args = parser.parse_args()
    
    if not args.cmd:
        parser.print_help()
        return
    
    token = get_access_token()
    if not token:
        print("❌ 无法获取Access Token")
        return
    
    if args.cmd == 'list':
        drafts = list_drafts(token, args.limit, args.offset)
        print_drafts(drafts)
        
    elif args.cmd == 'delete':
        delete_draft(token, args.media_id)
        
    elif args.cmd == 'count':
        drafts = list_drafts(token, limit=1)
        # 只取count
        url = f"https://api.weixin.qq.com/cgi-bin/draft/count?access_token={token}"
        resp = requests.get(url, timeout=10)
        data = resp.json()
        print(f"\n📋 草稿箱总计: {data.get('total_count', 0)} 篇\n")
        
    elif args.cmd == 'detail':
        get_draft_detail(token, args.media_id)

if __name__ == '__main__':
    main()
