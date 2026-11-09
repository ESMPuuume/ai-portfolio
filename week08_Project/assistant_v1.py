import os
from dotenv import load_dotenv
from llm import LLM
# 从你上周写的 rag_qa 中导入核心函数
from rag_qa import rag_qa 

load_dotenv()

# 设定助手的角色（W2提示词工程的落地）
SYSTEM_HINT = "你是国际中文教学助手，面向HSK3-4学习者，回答需给出依据。"

# 实例化双引擎
llm = LLM()

def answer(question, use_rag=True, prefer="local"):
    """
    核心粘合逻辑：use_rag开关控制是否查资料
    """
    if use_rag:
        # 走 RAG 检索（内部已经包含了构建 prompt 的逻辑）
        # 注意：你之前的 rag_qa 里面硬编码了 prefer="api"，这里为了展示双引擎，我们用本地的
        print("🔍 [系统日志] 正在查阅本地知识库...")
        return rag_qa(question)
    else:
        # 纯对话模式
        print("💬 [系统日志] 直接呼叫大模型（不查资料）...")
        prompt = SYSTEM_HINT + "\n" + question
        return llm.ask(prompt, prefer=prefer)

if __name__ == "__main__":
    # 老师要求的三个必问学科问题
    questions = [
        "把字句的教学难点有哪些",
        "HSK4词汇量要求是多少",
        "《愚公移山》可以设计什么课堂活动"
    ]
    
    print("========== 助手 v1.0 演示开始 ==========\n")
    for q in questions:
        print(f"Q: {q}")
        try:
            # 默认开启 RAG 模式
            ans = answer(q, use_rag=True, prefer="local")
            print(f"A: {ans}\n")
        except Exception as e:
            # 异常兜底，防止现场演示崩溃
            print(f"A: [运行失败] {e}\n")
        print("-" * 40)