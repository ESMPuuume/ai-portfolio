import os
from dotenv import load_dotenv
from llm import LLM
from rag_qa import rag_qa 

load_dotenv()

# 设定助手的角色（W2提示词工程的落地）
SYSTEM_HINT = "你是国际中文教学助手，面向HSK3-4学习者，回答需给出依据。"

# 实例化双引擎
llm = LLM()

# 🌟 加分改造点：新增 return_citation 开关
def answer(question, use_rag=True, prefer="local", return_citation=True):
    """
    核心粘合逻辑：
    1. use_rag 控制是否查资料
    2. return_citation 控制是否返回出处
    """
    if use_rag:
        # 走 RAG 检索
        print("🔍 [系统日志] 正在查阅本地知识库...")
        ans = rag_qa(question)
        
        # 如果关闭了返回出处，就把字符串里的来源截断掉
        if not return_citation and "[来源：" in ans:
            ans = ans.split("[来源：")[0].strip()
        return ans
    else:
        # 纯对话模式
        print("💬 [系统日志] 直接呼叫大模型（不查资料）...")
        prompt = SYSTEM_HINT + "\n" + question
        return llm.ask(prompt, prefer=prefer)

if __name__ == "__main__":
    print("========== 助手 v1.0 演示开始 ==========\n")
    
    # 老师要求的三个必问学科问题之一
    q = "HSK4词汇量要求是多少"
    print(f"Q: {q}\n")
    
    # 演示场景 1：开启 RAG 且返回出处
    print("--- 场景 1：基于资料回答，且【显示】出处 ---")
    ans_with_citation = answer(q, use_rag=True, return_citation=True)
    print(f"A: {ans_with_citation}\n")
    
    print("-" * 50)
    
    # 演示场景 2：开启 RAG 但隐藏出处（加分改造项演示）
    print("--- 场景 2：基于资料回答，但【隐藏】出处 (加分改造) ---")
    ans_without_citation = answer(q, use_rag=True, return_citation=False)
    print(f"A: {ans_without_citation}\n")
    
    print("-" * 50)
    
    # 演示场景 3：关闭 RAG 纯对话模式
    print("--- 场景 3：纯对话模式（不查资料）---")
    ans_pure_chat = answer(q, use_rag=False)
    print(f"A: {ans_pure_chat}\n")
