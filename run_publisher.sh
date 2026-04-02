#!/bin/bash
# 微信公众号定时发布脚本
cd /Users/yyf/.openclaw/workspace/content_automation_system
python3 wechat_publisher.py >> logs/publisher_$(date +\%Y\%m\%d).log 2>&1
