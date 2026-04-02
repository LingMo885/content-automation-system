#!/bin/bash
# 凌墨公众号自动发布系统 - 定时任务安装脚本

echo "=== 凌墨公众号自动发布系统安装 ==="
echo "安装时间: $(date '+%Y-%m-%d %H:%M:%S')"

# 检查Python环境
echo "检查Python环境..."
python3 --version
if [ $? -ne 0 ]; then
    echo "错误: Python3未安装"
    exit 1
fi

# 检查必要的Python包
echo "检查Python依赖包..."
python3 -c "import requests" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "安装requests包..."
    pip3 install requests
fi

# 设置脚本权限
echo "设置脚本权限..."
chmod +x /Users/yyf/.openclaw/workspace/content_automation_system/run_daily_publish.sh
chmod +x /Users/yyf/.openclaw/workspace/content_automation_system/wechat_auto_publish.py

# 创建必要的目录
echo "创建输出目录..."
mkdir -p /Users/yyf/.openclaw/workspace/content_automation_system/output/articles
mkdir -p /Users/yyf/.openclaw/workspace/content_automation_system/output/images
mkdir -p /Users/yyf/.openclaw/workspace/content_automation_system/output/reports
mkdir -p /Users/yyf/.openclaw/workspace/content_automation_system/output/logs

# 配置crontab
echo "配置crontab定时任务..."
echo "当前crontab内容:"
crontab -l 2>/dev/null || echo "(无crontab配置)"

echo ""
echo "是否要添加定时任务？(每天09:00执行)"
echo "输入 y 确认，其他键跳过: "
read -r answer

if [ "$answer" = "y" ] || [ "$answer" = "Y" ]; then
    # 备份现有crontab
    backup_file="/tmp/crontab_backup_$(date +%Y%m%d_%H%M%S)"
    crontab -l 2>/dev/null > "$backup_file"
    echo "已备份现有crontab到: $backup_file"
    
    # 添加新任务
    (crontab -l 2>/dev/null; echo "# 凌墨公众号每天09:00自动发布") | crontab -
    (crontab -l 2>/dev/null; echo "0 9 * * * /Users/yyf/.openclaw/workspace/content_automation_system/run_daily_publish.sh") | crontab -
    
    echo "定时任务已添加"
    echo "新的crontab内容:"
    crontab -l
else
    echo "跳过crontab配置"
    echo "您可以手动添加以下行到crontab:"
    echo "0 9 * * * /Users/yyf/.openclaw/workspace/content_automation_system/run_daily_publish.sh"
fi

# 测试脚本
echo ""
echo "是否要测试脚本？(输入 y 测试，其他键跳过): "
read -r test_answer

if [ "$test_answer" = "y" ] || [ "$test_answer" = "Y" ]; then
    echo "开始测试脚本..."
    cd /Users/yyf/.openclaw/workspace/content_automation_system
    ./run_daily_publish.sh
    echo "测试完成，请查看日志文件"
else
    echo "跳过测试"
fi

echo ""
echo "=== 安装完成 ==="
echo ""
echo "重要信息:"
echo "1. 飞书Bitable链接: https://acnxjky8hwsv.feishu.cn/base/XalIb4esLa7oUjsTDvCcYA8tnoe"
echo "2. 脚本目录: /Users/yyf/.openclaw/workspace/content_automation_system/"
echo "3. 日志目录: /Users/yyf/.openclaw/workspace/content_automation_system/output/logs/"
echo "4. 配置文件: /Users/yyf/.openclaw/workspace/content_automation_system/config.json"
echo ""
echo "使用方法:"
echo "- 手动运行: ./run_daily_publish.sh"
echo "- 查看日志: tail -f output/logs/wechat_publish_$(date +%Y%m%d).log"
echo "- 编辑配置: vi config.json"
echo ""
echo "注意: 微信公众号发布功能需要有效的thumb_media_id，"
echo "      您需要先上传图片到微信公众号素材库获取media_id。"