# 微信公众号草稿箱管理CLI

管理公众号草稿箱，支持列出、查看、删除草稿。

## 安装

```bash
pip install requests
```

## 使用

```bash
# 查看草稿数量
python wechat_drafts.py count

# 列出所有草稿
python wechat_drafts.py list --limit 20

# 查看草稿详情
python wechat_drafts.py detail <media_id>

# 删除草稿
python wechat_drafts.py delete <media_id>
```

## 配置

需要在脚本中设置微信公众号的 `appid` 和 `appsecret`。

## 依赖

- Python 3.8+
- requests
