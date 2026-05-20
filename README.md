# Clockpla AI (Transcript-based 1:1 Reconstruction)

这是一个基于闭门分享逐字稿实现的 **“一人公司 + 多 Agent”** 最小可运行复刻版。

## 核心结构（对应逐字稿）

- **唯一人类（Chairman）**：通过 Telegram 风格消息输入意图
- **Elon（CEO Agent）**：负责理解意图并拆解任务
- **Jobs（产品/设计）**：产出 PRD/设计建议
- **Linus（工程）**：实现代码任务（在本 demo 中产出实现计划/伪执行）
- **Turing（验证）**：独立验证，避免“同模型自证正确”
- **BOSS（客户成功）**：每 4 小时汇总用户反馈并生成改进建议
- **Clock Engine**：任务编排与调度（分钟级轮询 + 四小时反馈巡检）

## 快速开始

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

启动后可在终端发送指令：

- 输入业务意图（例如：`给房产中介做一个自动跟进和预约系统`）
- 输入 `status` 查看任务状态
- 输入 `feedback <内容>` 添加客户反馈
- 输入 `exit` 退出

## 设计原则（来自逐字稿）

1. **手机/对话优先**：人类只做“表达意图”，不手动拆任务。
2. **CEO 负责沟通，Worker 负责执行**：Elon 不下场干活，保持随时响应。
3. **执行与验证分离**：Linus 与 Turing 使用不同执行器，降低“自证偏差”。
4. **面向 SMB/小微**：重点解决多流程碎片化问题，而不是单点 SaaS。
5. **责任边界明确**：系统提供工具，决策责任仍归使用者（Human-in-the-loop）。

## 目录

- `app.py`：CLI 入口
- `clock_engine/`：核心编排与 Agent
- `clock_engine/scheduler.py`：轮询与周期任务
- `clock_engine/models.py`：任务与反馈模型


- `clock_engine/engine.py`：统一业务入口（提交意图/状态快照）
- `clock_engine/storage.py`：JSON 状态持久化组件
- `tests/test_engine.py`：核心流程测试


## 日志（Loguru）

- 默认输出最详细 `TRACE` 级别日志。
- 每个动作（意图解析、任务拆分、调度 tick、worker 执行、反馈扫描）都会写入日志。
- 日志文件：
  - `logs/clockpla.trace.log`（文本）
  - `logs/clockpla.jsonl`（结构化 JSON）
- 可通过环境变量调整：
  - `CLOCKPLA_LOG_LEVEL`（默认 `TRACE`）
  - `CLOCKPLA_LOG_DIR`（默认 `logs`）
  - `CLOCKPLA_LOG_RETENTION`（默认 `14 days`）
  - `CLOCKPLA_LOG_ROTATION`（默认 `50 MB`）
