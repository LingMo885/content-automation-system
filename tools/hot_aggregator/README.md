# 多平台热点聚合工具

一键抓取百度、微博、知乎、头条、抖音热搜，输出JSON便于后续处理。

## 安装

```bash
pip install requests
```

## 使用

```bash
# 抓取所有平台热点
python hot_topics.py

# 只抓百度热搜
python hot_topics.py -p baidu --limit 10

# 保存到文件
python hot_topics.py --save

# 持续监控模式（每5分钟检查一次）
python hot_topics.py --watch

# 匹配关键词
python hot_topics.py -k 清明 投资 创业

# 输出JSON格式
python hot_topics.py -j
```

## 支持平台

- 百度热搜
- 微博热搜
- 知乎热榜
- 头条热点
- 抖音热榜

## 输出

```json
{
  "timestamp": "2026-04-02T12:00:00",
  "platforms": {
    "baidu": [{"rank": 1, "title": "热搜标题", "platform": "baidu"}],
    "weibo": [...]
  },
  "total_count": 100
}
```

## 依赖

- Python 3.8+
- requests
