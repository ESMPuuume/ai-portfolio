# smolagents 5行流水线映射表

| 我手写的 tool_agent.py | smolagents 里对应什么 |
| :--- | :--- |
| `TOOLS` 字典 | `@tool` 装饰器把函数变成 `Tool` 对象 |
| `SYS` 提示词要求输出 JSON | 框架内部自带的 Prompt 模板 |
| `parse_calls` 正则抓取 JSON | 框架内部自动解析 `ChatMessageToolCall` |
| `TOOLS[name](*args)` 执行 | 框架自动校验参数并执行 |
| `run()` 循环 + `max_calls` | `MultiStepAgent` 多步循环管理 |