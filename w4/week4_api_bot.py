# W4 命令行学科问答机器人（原生 requests ）
import os
import sys
import json
import requests
from dotenv import load_dotenv

# 加载当前目录的 .env 文件
load_dotenv() 

BASE_URL = "https://api.deepseek.com/v1/chat/completions"

if __name__ == "__main__":
    # 1. 检查密钥
    key = os.getenv("DEEPSEEK_API_KEY")
    if not key:
        print("错误：未设置DEEPSEEK_API_KEY")
        print("处理：请在当前文件夹的 .env 文件里填入真实密钥。")
        sys.exit(1)
        
    # 2. 获取问题
    q = "".join(sys.argv[1:]) or "把字句的教学难点有哪些"
    print(f"🔄 正在呼叫大肥鱼，请稍候...")
    
    # 3. 准备请求的头部（证明身份）和数据（问什么）
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": q}],
        "temperature": 0.7,
        "max_tokens": 800
    }
    
    try:
        # 4. 发送请求
        response = requests.post(BASE_URL, headers=headers, json=data, timeout=20.0)
        response.raise_for_status() # 如果报错，这里会抛出异常
        
        # 5. 解析返回的数据
        result = response.json()
        ans = result["choices"][0]["message"]["content"]
        p_tk = result["usage"]["prompt_tokens"]
        c_tk = result["usage"]["completion_tokens"]
        
        # 6. 打印结果
        print("\n" + "="*40)
        print(ans)
        print("="*40)
        print(f"📊 Token消耗：输入 {p_tk} 个，输出 {c_tk} 个")
        
        # 7. 写入日志
        log_path = os.path.join(os.path.dirname(__file__), "chat_log.txt")
        with open(log_path, "a", encoding="utf-8") as f:
            f.write("Q: %s\nA: %s\n\n" % (q, ans))
        print(f"📄 日志已追加至：{log_path}")
        
    except Exception as e:
        print(f"错误：请求失败，原因：{e}")
        sys.exit(1)