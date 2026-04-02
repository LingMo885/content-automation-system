# 🌟 凌墨内容自动化系统

> 命理师的AI工作站 — 让内容生产全自动运转

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

---

## 📌 这是什么

一套为**命理内容创作者**打造的自动化工具，解决三个核心问题：

| 痛点 | 解决方案 |
|------|---------|
| 每天手动发文章太费时间 | 自动生成+定时发布 |
| 不知道写什么选题 | 热点自动抓取+命理角度分析 |
| 草稿箱乱成一团 | CLI工具管理草稿箱 |

---

## 🛠 核心工具

### 1. 热点聚合器 `tools/hot_aggregator/`

```
python hot_topics.py -p baidu,weibo --limit 10
```

同时抓取 **百度/微博/知乎/头条/抖音** 热搜，自动筛选命理相关话题。

### 2. 草稿箱管理 `tools/draft_manager/`

```
python wechat_drafts.py list --limit 20
python wechat_drafts.py delete <media_id>
```

查看、删除公众号草稿箱，一目了然。

### 3. 任务监控 `tools/task_monitor/`

```
python task_monitor.py list
python task_monitor.py alerts
```

监控定时任务执行状态，失败自动报警。

### 4. 八字分析引擎 `ba_zi_analyzer.py`

```python
from ba_zi_analyzer import BaZiAnalyzer
bazi = BaZiAnalyzer()
pillar = bazi.calculate_bazi_pillar('1990-05-15', '14:30')
print(pillar)
# {'nian_zhu': '庚午', 'yue_zhu': '辛巳', 'ri_zhu': '壬申', 'shi_zhu': '丙午'}
```

完整八字排盘，支持大运、流年、命局分析。

### 5. 深度文章生成 `deep_articles_wechat.py`

生成**婚姻/健康/财富**三大主题的深度公众号文章，风格真实有温度，不是模板套话。

---

## 🚀 快速开始

```bash
# 克隆仓库
git clone https://github.com/LingMo885/content-automation-system.git
cd content-automation-system

# 安装依赖
pip install requests

# 查看热点
python tools/hot_aggregator/hot_topics.py -p baidu --limit 10

# 管理草稿
python tools/draft_manager/wechat_drafts.py count
```

---

## 📂 目录结构

```
content_automation_system/
├── ba_zi_analyzer.py          # 八字排盘引擎
├── wechat_publisher.py         # 公众号发布
├── xiaohongshu_autoposter.py  # 小红书自动发布
├── deep_articles_wechat.py     # 深度文章生成
├── hot_topic_tracker.py        # 热点追踪
├── daily_article_generator.py  # 每日文章生成
├── tools/
│   ├── hot_aggregator/        # 多平台热点聚合
│   ├── draft_manager/         # 草稿箱管理
│   └── task_monitor/          # 任务监控
└── content_templates/         # 内容模板
```

---

## 🎯 适用人群

- 命理师 / 占卜师
- 内容创作者（玄学/传统文化方向）
- 想用AI提升内容生产效率的自媒体人
- 有编程能力的五行爱好者

---

## ⚠️ 注意事项

- 部分功能需要微信公众号API权限
- 热点抓取受平台限制，可能有延迟
- 本工具仅供个人学习研究使用

---

## 📜 License

MIT License — 随意Fork和改进

---

> 如果对你有用，欢迎 ⭐ 一个
