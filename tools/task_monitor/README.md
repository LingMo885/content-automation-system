# OpenClaw任务监控工具

监控OpenClaw定时任务状态，检查失败任务，查看执行历史。

## 安装

```bash
pip install requests
```

## 使用

```bash
# 查看Gateway健康状态
python task_monitor.py health

# 列出所有定时任务
python task_monitor.py list

# 检查异常任务
python task_monitor.py alerts

# 查看任务详情
python task_monitor.py status <job_id>

# 查看执行历史
python task_monitor.py history <job_id>
```

## 依赖

- Python 3.8+
- requests
- OpenClaw Gateway (需本地运行)
