# Clockpla AI (Phase 2 能力实装)

本版本从“架构demo”升级到“能力实装”：

- Worker 不再是纯文案，改为工具执行层（DesignTool / CodeTool / ValidationTool）
- Turing 验证失败会自动回流 Linus 返工，再次验证（重试闭环）
- 状态落盘到 `.clockpla_state.json`，支持查看持久化状态
- 保留 TRACE 级 Loguru 全链路日志

## 运行

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

## 命令
- 输入任意业务意图
- `status` 查看已完成任务
- `feedback <内容>` 添加反馈
- `state` 查看持久化状态
- `exit` 退出

## 日志
- `logs/clockpla.trace.log`
- `logs/clockpla.jsonl`
