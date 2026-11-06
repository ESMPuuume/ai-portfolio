import os
import requests
import math
from dotenv import load_dotenv
from llm import LLM

load_dotenv()

# ================= 步骤1：加载与分块 (Chunking) =================
def load_and_chunk(file_path, chunk_size=200): 
    # 把 chunk_size 调到了 200，让段落更完整，避免答案被截断
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

# ================= 步骤2：向量化 (Embedding) =================
def get_embedding(text):
    url = "http://localhost:11434/api/embeddings"
    payload = {"model": "nomic-embed-text", "prompt": text}
    # 使用 Session 并关闭环境代理，防止校园网拦截
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
    print(f"📦 步骤1：文本已成功切分为 {len(chunks)} 个小块")
    
    # 2. 向量化
    print("🔢 步骤2：正在将文字转换为向量 (nomic-embed-text)...")
    q_emb = get_embedding(question)
    chunk_embs = [get_embedding(c) for c in chunks]
    
    # 3. 检索
    print("🔍 步骤3：正在计算相似度，检索相关资料...")
    similarities = [cosine_similarity(q_emb, c_emb) for c_emb in chunk_embs]
    best_idx = similarities.index(max(similarities))
    best_chunk = chunks[best_idx]
    print(f"📄 命中资料片段：【{best_chunk}】\n")
    
    # 4. 生成
    print("🤖 步骤4：将资料与问题拼装，发给 llm.ask() 生成答案...")
    prompt = f"请严格根据以下资料回答问题，资料中没有的内容就如实说「资料中未提及」：\n\n【资料】：\n{best_chunk}\n\n【问题】：{question}"
    
    llm = LLM()
    answer = llm.ask(prompt, prefer="local")
    
    # 🌟 满足进阶方案A：强制让答案附带出处
    answer_with_citation = f"{answer}\n\n[来源：本地知识库《HSK4_标准.txt》相关片段]"
    
    print("="*50)
    return answer_with_citation

if __name__ == "__main__":
    q = "HSK4级的词汇量和汉字要求分别是多少？" 
    ans = rag_qa(q)
    print(f"✅ 最终回答（含出处）：\n{ans}")