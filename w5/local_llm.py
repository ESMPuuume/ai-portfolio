import requests

s = requests.Session()
s.trust_env = False

# 用最最简单的问题测试
prompt = """帮我生成一段关于“春节”的口语课教案提纲，包含导入和活动"""

print("1. 脚本开始运行，正在呼叫本地模型...")

try:
    resp = s.post(
        "http://localhost:11434/api/chat",
        json={
            "model": "qwen2.5:0.5b",
            "messages": [{"role": "user", "content": prompt}],
            "stream": False
        },
        timeout=120
    )
    
    print("2. 模型响应成功，准备解析...")
    answer = resp.json()["message"]["content"]
    
    print("\n================ 模型说 ================\n")
    print(answer)
    print("\n========================================\n")

except Exception as e:
    print(f"出错了：{e}")