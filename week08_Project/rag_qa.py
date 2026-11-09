import os
import requests
import math
from dotenv import load_dotenv
from llm import LLM

load_dotenv()

# ================= 步骤1：加载与分块 (Chunking) =================
def load_and_chunk(file_path, chunk_size=200): 
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

# ================= 步骤2：向量化 (Embedding) =================
def get_embedding(text):
    url = "http://localhost:11434/api/embeddings"
    payload = {"model": "nomic-embed-text", "prompt": text}
    session = requests.Session()
    session.trust_env = False
    response = session.post(url, json=payload)
    return response.json()["embedding"]

# ================= 步骤3：检索 (Retrieval) =================
def cosine_similarity(v1, v2):
    dot_product = sum(x * y for x, y in zip(v1, v2))
    magnitude1 = math.sqrt(sum(x * x for x in v1))
    magnitude2 = math.sqrt(sum(x * x for x in v2))
    return dot_product / (magnitude1 * magnitude2)

# ================= 步骤4：生成 (Generation) =================
def rag_qa(question):
    print("="*50)
    print(f"❓ 提问：{question}")
    
    # 1. 加载分块
    chunks = load_and_chunk("HSK4_标准.txt")
    
    # 2. 向量化
    q_emb = get_embedding(question)
    chunk_embs = [get_embedding(c) for c in chunks]
    
    # 3. 检索与相似度计算
    similarities = [cosine_similarity(q_emb, c_emb) for c_emb in chunk_embs]
    max_sim = max(similarities) 
    best_idx = similarities.index(max_sim)
    best_chunk = chunks[best_idx]
    
    print(f"📊 最高相似度得分：{max_sim:.4f}")
    
    # 🌟 护甲一：阈值拦截（拦截不相关的问题）
    THRESHOLD = 0.55 
    if max_sim < THRESHOLD:
        print("❌ 拦截：相似度过低，资料库中没有相关内容。")
        return "【系统拦截】抱歉，我的本地知识库中未提及相关内容，无法作答。"
        
    print(f"📄 命中资料片段：【{best_chunk}】\n")
    
    # 4. 生成（强化提示词）
    print("🤖 步骤4：将资料与问题拼装，发给 llm.ask() 生成答案...")
    # 🌟 护甲二：强化提示词（给云端模型上紧箍咒）
    prompt = f"""你是一个极其严格的资料检索助手。你必须且只能根据以下【资料】回答问题。
如果【资料】中完全没有提到该问题的答案，你必须且只能回答：“资料中未提及。” 
绝对禁止使用你自带的任何外部知识，绝对禁止编造！不要解释为什么，直接作答。

【资料】：
{best_chunk}

【问题】：{question}
"""
    
    llm = LLM()
    # 路演建议用云端模型，防止本地小模型超时或胡言乱语
    answer = llm.ask(prompt, prefer="api") 
    
    # 🌟 护甲三：后置风控（只有真答案才给加出处）
    if "未提及" in answer or "不知道" in answer:
        answer_with_citation = answer
    else:
        answer_with_citation = f"{answer}\n\n[来源：本地知识库《HSK4_标准.txt》相关片段]"
        
    print("="*50)
    return answer_with_citation

if __name__ == "__main__":
    q = "HSK4级的词汇量和汉字要求分别是多少？" 
    ans = rag_qa(q)
    print(f"✅ 最终回答（含出处）：\n{ans}")