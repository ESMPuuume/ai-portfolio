# 官方 RAG 流水线与我的代码映射表

| 官方流水线 | llm-universe 对应章节 | 我自己的代码组件 (rag_qa.py) |
| :--- | :--- | :--- |
| **1. Load + Split** | C3「数据处理:读取、清洗与切片」 | 没有用第三方类，手写了 `load_and_chunk()`，按 200 字长度切分 `HSK4_标准.txt`。 |
| **2. Embed + Store** | C3「词向量及向量知识库介绍」 | 调用本地 `OllamaEmbeddings(nomic-embed-text)` 接口，手算余弦相似度，省去了庞大的 Chroma 依赖。 |
| **3. Retrieve** | C4「基于 LangChain 搭建检索问答链」 | 手写 `cosine_similarity()` 取最高分，并加入 0.55 的阈值拦截，防止无关问题产生幻觉。 |
| **4. Prompt + Generate** | C4「将 LLM 接入 LangChain」 | 用 `SYSTEM_HINT` 强制人设，拼上资料和问题，交给我在 W6 封装的 `LLM().ask(prefer="local")`。 |
| **5. Deploy + Evaluate** | C4「Streamlit 部署」；C5「系统评估」 | 用 `assistant_v1.py` 终端交互演示；用 W7 的幻觉对照表做评估。 |