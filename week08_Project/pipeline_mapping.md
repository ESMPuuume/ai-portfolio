# 官方 RAG 流水线与我的代码对照表

| 官方流水线 | 官方教程中的做法 | 我的代码组件 (rag_qa.py / assistant_v1.py) |
| :--- | :--- | :--- |
| **1. Load + Split**<br>加载与分块 | 使用 TextLoader 读取，RecursiveCharacterTextSplitter 切片 | 手写 `load_and_chunk()` 函数，每 200 字切分文本。 |
| **2. Embed + Store**<br>向量化入库 | 调用 OpenAI Embeddings 并存入 Chroma 向量数据库 | 直接调本地 `nomic-embed-text` 接口，计算出数字向量列表（省去了向量数据库，直接内存检索）。 |
| **3. Retrieve**<br>检索 | 使用向量数据库进行相似度搜索，返回 top-k | 手写 `cosine_similarity()` 余弦相似度算法，寻找得分最高片段，并加入 **0.55 的阈值拦截**。 |
| **4. Prompt + Generate**<br>拼词与生成 | 将检索结果拼入提示词，交给大模型生成 | `build_prompt()` 强制拼入系统提示词与资料，交由 W6 封装的 `llm.ask()` 生成答案。 |
| **5. Deploy + Evaluate**<br>部署与评估 | 用 Streamlit 部署网页应用，人工进行系统评估 | 使用 `assistant_v1.py` 实现终端交互，并在 W7 输出了**幻觉对照表**作为最朴素的评估证据。 |