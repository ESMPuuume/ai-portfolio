import os
import requests
import time  # 引入time模块用于计算耗时

# 说明（作业1）：我选择了“调用耗时与费用估算打印”。
# 理由：作为未来的教师，我需要清楚了解本地响应的速度优势，以及云端API的Token成本，
# 以便在课堂演示时（用本地快）或课后长文生成时（用云端好）做出合理取舍。
from dotenv import load_dotenv

load_dotenv()

class LocalEngine:
    def __init__(self, model=None):
        self.model = model or os.getenv("LOCAL_MODEL", "qwen2.5:0.5b")
        self.session = requests.Session()
        self.session.trust_env = False

    def ask(self, prompt, temperature=0.7, max_tokens=800):
        r = self.session.post(
            "http://localhost:11434/api/chat",
            json={
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "options": {"temperature": temperature, "num_predict": max_tokens},
                "stream": False
            },
            timeout=60
        )
        r.raise_for_status()
        return r.json()["message"]["content"]

class APIEngine:
    def __init__(self):
        self.client = None

    def _ensure_client(self):
        if self.client is None:
            self.api_key = os.getenv("DEEPSEEK_API_KEY")
            self.url = "https://api.deepseek.com/v1/chat/completions"

    def ask(self, prompt, temperature=0.7, max_tokens=800):
        self._ensure_client()
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        r = requests.post(self.url, headers=headers, json=data, timeout=60)
        r.raise_for_status()
        # 获取token用量用于粗略估算
        usage = r.json()["usage"]
        print(f"💰 [费用估算] 消耗Token: 输入 {usage['prompt_tokens']} / 输出 {usage['completion_tokens']}")
        return r.json()["choices"][0]["message"]["content"]

class LLM:
    def __init__(self, local_model=None):
        self.local = LocalEngine(local_model)
        self.api = APIEngine()

    def ask(self, prompt, prefer="local", **kwargs):
        first, second = (self.local, self.api) if prefer == "local" else (self.api, self.local)
        
        # 记录开始时间
        start_time = time.time()
        
        try:
            result = first.ask(prompt, **kwargs)
            # 打印耗时
            print(f"⏱️ [耗时] {time.time() - start_time:.2f} 秒")
            return result
        except Exception as e:
            print(f"\n[⚠️ 首选引擎失败，自动切换] 报错原因: {e}")
            print(f"[🔄 正在尝试使用备用引擎...]")
            result = second.ask(prompt, **kwargs)
            print(f"⏱️ [耗时] {time.time() - start_time:.2f} 秒")
            return result

if __name__ == "__main__":
    llm = LLM()
    print("正在测试...")
    # 这里你可以根据需要改成 prefer="api" 或修改 max_tokens
    ans = llm.ask("用一句话解释什么是把字句。", prefer="local", max_tokens=800)
    print("\n最终回答：\n", ans)