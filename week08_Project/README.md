# 学科智能问答助手 v1.0

## 功能
- 基于 RAG 的学科问答；支持纯对话 / 基于资料两种模式（use_rag开关）。
- 本地优先，云端兜底（双引擎自动回退）。

## 怎么装
1. 安装依赖：`pip install -r requirements.txt`
2. 启动本地模型：`ollama pull qwen2.5:0.5b` 及 `ollama pull nomic-embed-text`
3. 复制 `.env.example` 为 `.env`，填入 `DEEPSEEK_API_KEY`。

## 怎么用
- 在终端运行：`python assistant_v1.py`

## 已知问题
- 本地小模型（0.5b）在处理长文本时生成速度较慢，若超时程序会自动切换至云端API。
- 若未启动 Ollama，程序会报错并自动尝试连接云端。