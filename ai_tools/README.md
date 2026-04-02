# 🤖 AI开发者工具箱

> 解决AI从业者每天都会遇到的5个真实痛点

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)]()
[![License](https://img.shields.io/badge/License-MIT-green.svg)]()

---

## 🎯 这5个痛点，你肯定遇到过

| 痛点 | 工具 | 能做什么 |
|------|------|---------|
| Prompt写完就忘，下次重头写 | `prompt_library` | 存储、分类、搜索、复用 |
| 不知道该用哪个模型 | `model_selector` | 根据任务+预算+速度智能推荐 |
| 不知道钱花在哪了 | `cost_tracker` | 记录每次调用，统计消费报表 |
| AI输出质量难以判断 | `quality_evaluator` | 7维度评分+改进建议 |
| 内容怕踩红线 | `content_guard` | 敏感词检测+合规建议 |

---

## 🛠 工具详情

### 1. Prompt库 `prompt_library/`

```bash
# 添加Prompt
python prompt_manager.py add "小红书标题生成" "你是一个专业的小红书文案专家..."

# 按标签搜索
python prompt_manager.py search 小红书

# 随机选一个
python prompt_manager.py random --tag 写作

# 导出为Claude格式
python prompt_manager.py export --format claude
```

### 2. 模型选择器 `model_selector/`

```bash
# 根据任务推荐
python model_selector.py recommend --task 写作 --budget low

# 对比多个模型
python model_selector.py compare gpt-4o claude-sonnet-4

# 快速选择
python model_selector.py decide
```

### 3. 消费追踪器 `cost_tracker/`

```bash
# 记录一次调用
python cost_tracker.py log --model gpt-4o --input 50000 --output 30000

# 周报
python cost_tracker.py report --days 7

# 预算检查
python cost_tracker.py budget 50 --days 30
```

### 4. 质量评估器 `quality_evaluator/`

```bash
# 评估AI输出
python quality_evaluator.py eval "你的AI生成内容..."

# 快速检查
python quality_evaluator.py check "内容..."

# 对比两个版本
python quality_evaluator.py compare version1.txt version2.txt
```

---

## 🚀 快速开始

```bash
# 克隆
git clone https://github.com/LingMo885/ai-tools.git
cd ai-tools

# 直接运行
python prompt_library/prompt_manager.py list
python model_selector/model_selector.py decide
```

---

## 📊 功能矩阵

| 功能 | prompt_manager | model_selector | cost_tracker | quality_evaluator |
|------|:---:|:---:|:---:|:---:|
| 存储/搜索 | ✅ | | | |
| 智能推荐 | | ✅ | | |
| 消费统计 | | | ✅ | |
| 质量评分 | | | | ✅ |
| 多模型对比 | | ✅ | | ✅ |
| 导出分享 | ✅ | | ✅ | |

---

## 💡 适用人群

- AI应用开发者
- 内容创作者（用AI辅助写作）
- 产品经理（评估AI输出质量）
- 独立开发者（控制API成本）

---

## ⚙️ 数据存储

所有数据存在 `~/.openclaw/workspace/memory/` 目录下：
- `prompts/prompts.json` — Prompt库
- `api_costs.json` — 消费记录

---

## 📜 License

MIT License
