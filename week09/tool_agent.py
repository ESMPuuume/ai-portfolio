import os
import json
import re
import ast
import operator
import datetime
import requests
from dotenv import load_dotenv

load_dotenv()

# ================= 1. 定义四个工具 =================
def get_time():
    return str(datetime.datetime.now())

# 安全计算：白名单 AST
_OPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
        ast.Div: operator.truediv, ast.Pow: operator.pow, ast.Mod: operator.mod,
        ast.USub: operator.neg, ast.UAdd: operator.pos}

def _eval_node(node):
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_eval_node(node.left), _eval_node(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_eval_node(node.operand))
    raise ValueError("只允许数字与 + - * / ** % 运算")

def calc(expr):
    try:
        return str(_eval_node(ast.parse(str(expr), mode="eval")))
    except ZeroDivisionError:
        return "错误：除数为 0"
    except Exception as e:
        return "拒绝计算：%s" % e

# 查 HSK 等级
def hsk_level(word):
    mock_dict = {"把": "3", "愚公移山": "5", "坚持": "4"}
    return "%s 是 HSK %s 级" % (word, mock_dict.get(word, "未知"))

# 🌟 新增：第 4 个工具 —— 课文难度评估
def text_difficulty(text, target_level="4"):
    # 这里做一个非常简单的模拟评估：统计字数，并瞎编几个超纲词
    char_count = len(text)
    # 假设超过 50 个字就认为偏长，或者包含特定词就认为超纲
    overlimit_words = []
    if "愚公移山" in text: overlimit_words.append("愚公移山")
    if "坚持不懈" in text: overlimit_words.append("坚持不懈")
    
    result = f"文本共计 {char_count} 字。"
    if overlimit_words:
        result += f" 发现超纲词：{'、'.join(overlimit_words)}。"
    else:
        result += " 未发现明显超纲词。"
    result += f" 整体难度评估：基本符合 HSK {target_level} 水平。"
    return result

# 将所有工具注册进字典
TOOLS = {
    "get_time": get_time, 
    "calc": calc, 
    "hsk_level": hsk_level,
    "text_difficulty": text_difficulty  # 🌟 注册新工具
}

# ================= 2. 提示词与解析 =================
# 🌟 修改 SYS 提示词，告诉模型有第 4 个工具可用
SYS = ("你是国际中文助教。可用工具只有这 4 个："
       "get_time（查当前时间，无参数）、"
       "calc（四则运算，如 calc('35*24')）、"
       "hsk_level（查生词 HSK 等级，如 hsk_level('把')）、"
       "text_difficulty（评估课文难度，需要两个参数：课文文本、目标等级，如 text_difficulty('愚公移山的故事', '4')）。"
       "如需调用，只输出一行 JSON，格式：{\"tool\": \"工具名\", \"args\": [参数]}；"
       "一次只调用一个工具，绝不编造不存在的工具名；无需工具时直接回答。")

def parse_calls(txt):
    s = (txt or "").strip()
    s = s.replace("```json", "").replace("```", "").strip()
    try:
        obj = json.loads(s)
        return [obj] if isinstance(obj, dict) else []
    except Exception:
        m = re.search(r"\{.*\}", s, re.S)
        if m:
            try:
                obj = json.loads(m.group())
                if isinstance(obj, dict): return [obj]
            except: pass
    calls = []
    for blk in re.findall(r"\{[^}]*\}", s):
        try:
            obj = json.loads(blk)
            if isinstance(obj, dict): calls.append(obj)
        except: continue
    return calls

# ================= 3. 循环与调用云端 =================
def call_llm(messages):
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {os.getenv('DEEPSEEK_API_KEY')}", "Content-Type": "application/json"}
    data = {"model": "deepseek-chat", "messages": messages, "temperature": 0}
    r = requests.post(url, headers=headers, json=data, timeout=30)
    return r.json()["choices"][0]["message"]["content"]

def run(user_msg, max_calls=3):
    msgs = [{"role": "system", "content": SYS}, {"role": "user", "content": user_msg}]
    for _ in range(max_calls):
        print(f"\n--- 正在询问模型 (第 {_+1} 轮) ---")
        txt = call_llm(msgs)
        print(f"模型输出: {txt}")
        
        calls = [c for c in parse_calls(txt) if isinstance(c.get("tool"), str) and c.get("tool") in TOOLS]
        if not calls:
            return txt
            
        results = []
        for call in calls:
            args = call.get("args") or []
            if not isinstance(args, list):
                results.append("工具参数格式错误")
                continue
            try:
                res = TOOLS[call["tool"]](*args) # 执行工具
                results.append(f"{call['tool']}{args} → {res}")
                print(f"🔧 执行工具: {call['tool']}, 结果: {res}")
            except Exception as e:
                results.append(f"工具执行失败：{e}")
                
        msgs += [{"role": "assistant", "content": txt},
                 {"role": "user", "content": "工具返回：" + "；".join(results) + "。请据此作答。"}]
                 
    return call_llm(msgs)

if __name__ == "__main__":
    print("========== 工具调用 Agent 测试 ==========")
    # 🌟 测试新工具：问一个需要评估难度的问题
    test_question = "帮我评估一下这段课文：'愚公移山的故事家喻户晓，他坚持不懈的精神值得我们学习。' 难度适合 HSK 四级吗？"
    print("最终回答:", run(test_question))