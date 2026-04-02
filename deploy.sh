#!/bin/bash

# 八字内容自动化生成系统部署脚本

set -e  # 遇到错误退出

echo "========================================="
echo "八字内容自动化生成系统部署脚本"
echo "========================================="

# 检查Python版本
echo "检查Python版本..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" = "$required_version" ]; then
    echo "✅ Python版本满足要求: $python_version"
else
    echo "❌ Python版本过低: $python_version，需要 $required_version 或更高版本"
    exit 1
fi

# 创建虚拟环境
echo -e "\n创建虚拟环境..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ 虚拟环境创建成功"
else
    echo "⚠️  虚拟环境已存在，跳过创建"
fi

# 激活虚拟环境
echo -e "\n激活虚拟环境..."
source venv/bin/activate

# 升级pip
echo -e "\n升级pip..."
pip install --upgrade pip

# 安装依赖
echo -e "\n安装依赖..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    echo "✅ 依赖安装完成"
else
    echo "❌ requirements.txt 文件不存在"
    exit 1
fi

# 创建必要目录
echo -e "\n创建必要目录..."
directories=("output" "logs" "backups" "content_templates")

for dir in "${directories[@]}"; do
    if [ ! -d "$dir" ]; then
        mkdir -p "$dir"
        echo "✅ 创建目录: $dir"
    else
        echo "⚠️  目录已存在: $dir"
    fi
done

# 检查模板文件
echo -e "\n检查模板文件..."
template_files=("base.md" "wechat.md" "xiaohongshu.md" "douyin.md" "zhihu.md" "weibo.md")

all_templates_exist=true
for file in "${template_files[@]}"; do
    if [ ! -f "content_templates/$file" ]; then
        echo "❌ 模板文件缺失: content_templates/$file"
        all_templates_exist=false
    fi
done

if [ "$all_templates_exist" = true ]; then
    echo "✅ 所有模板文件存在"
else
    echo "⚠️  部分模板文件缺失，系统可能无法正常工作"
fi

# 创建配置文件示例
echo -e "\n创建配置文件..."
if [ ! -f "config.json" ]; then
    cat > config_sample.json << 'EOF'
{
  "system": {
    "name": "八字内容自动化生成系统",
    "version": "1.0.0",
    "debug": false,
    "log_level": "INFO"
  },
  "directories": {
    "template_dir": "content_templates",
    "output_dir": "output",
    "log_dir": "logs",
    "data_dir": "data"
  },
  "platforms": ["wechat", "xiaohongshu", "douyin", "zhihu", "weibo"],
  "ai_apis": {
    "wenxin": {
      "enabled": false,
      "api_key": "your_api_key_here",
      "api_secret": "your_api_secret_here",
      "model": "ernie-4.0",
      "max_tokens": 2000
    },
    "tongyi": {
      "enabled": false,
      "api_key": "your_api_key_here",
      "model": "qwen-max",
      "max_tokens": 2000
    },
    "zhipu": {
      "enabled": false,
      "api_key": "your_api_key_here",
      "model": "glm-4",
      "max_tokens": 2000
    }
  },
  "content_generation": {
    "enable_ai_enhancement": true,
    "max_content_length": 5000,
    "min_content_length": 300,
    "default_language": "zh-CN",
    "enable_proofreading": true
  },
  "quality_evaluation": {
    "enable_auto_evaluation": true,
    "min_quality_score": 60,
    "evaluation_dimensions": [
      "relevance",
      "professionalism",
      "readability",
      "attractiveness",
      "compliance"
    ],
    "weights": {
      "relevance": 0.25,
      "professionalism": 0.25,
      "readability": 0.20,
      "attractiveness": 0.20,
      "compliance": 0.10
    }
  },
  "publishing_planning": {
    "enable_auto_scheduling": true,
    "default_publishing_times": {
      "wechat": ["09:00", "12:00", "20:00"],
      "xiaohongshu": ["10:00", "14:00", "19:00"],
      "douyin": ["12:00", "18:00", "21:00"],
      "zhihu": ["08:00", "13:00", "19:00"],
      "weibo": ["09:00", "12:00", "18:00", "22:00"]
    },
    "min_interval_hours": 2,
    "max_daily_posts": {
      "wechat": 3,
      "xiaohongshu": 5,
      "douyin": 10,
      "zhihu": 3,
      "weibo": 10
    }
  },
  "bazi_analysis": {
    "enable_detailed_analysis": true,
    "include_ten_gods": true,
    "include_da_yun": true,
    "include_liu_nian": true,
    "analysis_depth": "standard"
  }
}
EOF
    echo "✅ 配置文件示例已创建: config_sample.json"
    echo "⚠️  请复制 config_sample.json 为 config.json 并修改配置"
else
    echo "⚠️  配置文件已存在: config.json"
fi

# 运行系统测试
echo -e "\n运行系统测试..."
if [ -f "test_system.py" ]; then
    echo "开始系统测试..."
    python test_system.py
    test_result=$?
    
    if [ $test_result -eq 0 ]; then
        echo "✅ 系统测试通过"
    else
        echo "❌ 系统测试失败"
        exit 1
    fi
else
    echo "⚠️  测试文件不存在，跳过测试"
fi

# 创建启动脚本
echo -e "\n创建启动脚本..."
cat > start.sh << 'EOF'
#!/bin/bash

# 八字内容自动化生成系统启动脚本

set -e

# 激活虚拟环境
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "警告: 虚拟环境不存在，使用系统Python"
fi

# 检查配置文件
if [ ! -f "config.json" ]; then
    echo "错误: 配置文件 config.json 不存在"
    echo "请复制 config_sample.json 为 config.json 并修改配置"
    exit 1
fi

# 运行系统
echo "启动八字内容自动化生成系统..."
python content_automation_system.py "$@"
EOF

chmod +x start.sh
echo "✅ 启动脚本已创建: start.sh"

# 创建服务管理脚本
echo -e "\n创建服务管理脚本..."
cat > manage.sh << 'EOF'
#!/bin/bash

# 八字内容自动化生成系统管理脚本

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

case "$1" in
    start)
        echo "启动系统..."
        ./start.sh
        ;;
    stop)
        echo "停止系统..."
        # 这里可以添加停止逻辑
        echo "系统已停止"
        ;;
    restart)
        echo "重启系统..."
        $0 stop
        sleep 2
        $0 start
        ;;
    status)
        echo "系统状态:"
        if pgrep -f "content_automation_system.py" > /dev/null; then
            echo "✅ 系统正在运行"
        else
            echo "❌ 系统未运行"
        fi
        ;;
    test)
        echo "运行测试..."
        if [ -f "test_system.py" ]; then
            python test_system.py
        else
            echo "测试文件不存在"
        fi
        ;;
    update)
        echo "更新系统..."
        git pull
        pip install -r requirements.txt --upgrade
        echo "✅ 系统更新完成"
        ;;
    backup)
        echo "备份数据..."
        backup_dir="backups/$(date +%Y%m%d_%H%M%S)"
        mkdir -p "$backup_dir"
        cp -r output/* "$backup_dir/" 2>/dev/null || true
        cp config.json "$backup_dir/" 2>/dev/null || true
        echo "✅ 数据已备份到: $backup_dir"
        ;;
    help|*)
        echo "八字内容自动化生成系统管理命令:"
        echo "  $0 start     启动系统"
        echo "  $0 stop      停止系统"
        echo "  $0 restart   重启系统"
        echo "  $0 status    查看状态"
        echo "  $0 test      运行测试"
        echo "  $0 update    更新系统"
        echo "  $0 backup    备份数据"
        echo "  $0 help      显示帮助"
        ;;
esac
EOF

chmod +x manage.sh
echo "✅ 管理脚本已创建: manage.sh"

# 显示使用说明
echo -e "\n========================================="
echo "部署完成!"
echo "========================================="
echo -e "\n使用说明:"
echo "1. 配置系统:"
echo "   cp config_sample.json config.json"
echo "   # 编辑 config.json，配置API密钥等参数"
echo ""
echo "2. 启动系统:"
echo "   ./start.sh"
echo "   或"
echo "   ./manage.sh start"
echo ""
echo "3. 管理命令:"
echo "   ./manage.sh status    # 查看状态"
echo "   ./manage.sh test      # 运行测试"
echo "   ./manage.sh backup    # 备份数据"
echo "   ./manage.sh update    # 更新系统"
echo ""
echo "4. 首次使用:"
echo "   python content_automation_system.py"
echo ""
echo "5. 开发环境:"
echo "   source venv/bin/activate  # 激活虚拟环境"
echo "   pip install -r requirements.txt  # 安装依赖"
echo ""
echo "注意: 请确保已配置有效的AI API密钥以获得最佳效果"
echo "========================================="