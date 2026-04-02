#!/bin/bash
# 凌墨公众号每日自动发布脚本

# 设置工作目录
WORKSPACE="/Users/yyf/.openclaw/workspace"
SCRIPT_DIR="$WORKSPACE/content_automation_system"
LOG_DIR="$SCRIPT_DIR/logs"

# 创建日志目录
mkdir -p "$LOG_DIR"

# 设置日志文件
LOG_FILE="$LOG_DIR/wechat_publish_$(date +%Y%m%d).log"

# 记录开始时间
echo "=== 凌墨公众号自动发布开始 ===" >> "$LOG_FILE"
echo "执行时间: $(date '+%Y-%m-%d %H:%M:%S')" >> "$LOG_FILE"

# 激活Python环境（如果需要）
# source /path/to/venv/bin/activate

# 执行Python脚本
cd "$SCRIPT_DIR"
python3 wechat_auto_publish.py >> "$LOG_FILE" 2>&1

# 检查执行结果
if [ $? -eq 0 ]; then
    echo "执行状态: 成功" >> "$LOG_FILE"
else
    echo "执行状态: 失败" >> "$LOG_FILE"
fi

echo "=== 凌墨公众号自动发布结束 ===" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

# 发送通知（可选）
# 可以在这里添加发送飞书/微信通知的代码

echo "任务执行完成，日志保存在: $LOG_FILE"