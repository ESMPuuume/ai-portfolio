# W3 生词表 CSV -> 自动生成练习题 + 按词性分组输出
# 运行：python vocab_tool.py

import csv
import os

def init_data_folder():
    """自动创建数据文件夹和CSV文件，彻底解决文件找不到、后缀名错误的问题"""
    if not os.path.exists("data"):
        os.makedirs("data")
    
    csv_path = os.path.join("data", "生词表.csv")
    if not os.path.exists(csv_path):
        print("🔄 未检测到 data/生词表.csv，正在自动生成数据...")
        default_data = """词汇,HSK等级,词性,拼音,释义
阿姨,4,名,āyí,
啊,4,叹,a,
矮,4,形,ǎi,
矮小,4,形,ǎixiǎo,
爱国,4,动,ài guó,
爱护,4,动,àihù,
安,4,动、形,ān,
安置,4,动,ānzhì,
按时,4,副,ànshí,
暗,4,形,àn,
暗示,4,动,ànshì,
巴士,4,名,bāshì,
百货,4,名,bǎihuò,
摆,4,动,bǎi,
摆动,4,动,bǎidòng,
摆脱,4,动,bǎituō,
败,4,动,bài,
办事,4,动,bàn shì,
包裹,4,名、动,bāoguǒ,
包含,4,动,bāohán,
包括,4,动,bāokuò,
薄,4,形,báo,
宝,4,名,bǎo,
宝宝,4,名,bǎobǎo,
宝贝,4,名,bǎobèi,
宝贵,4,形,bǎoguì,
宝石,4,名,bǎoshí,
保密,4,动,bǎo mì,
保守,4,动、形,bǎoshǒu,
抱,4,动,bào,
背景,4,名,bèijǐng,
倍,4,量,bèi,
被迫,4,动,bèipò,
本科,4,名,běnkē,
笨,4,形,bèn,
比分,4,名,bǐfēn,
毕业,4,动,bì yè,
毕业生,4,名,bìyèshēng,
避,4,动,bì,
避免,4,动,bìmiǎn,
"""
        with open(csv_path, "w", encoding="utf-8") as f:
            f.write(default_data)
        print("✅ 已成功创建 data/生词表.csv")

def load_words(path):
    """① 读：读取CSV文件，返回字典列表"""
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))

def filter_by_level(words, level="4"):
    """② 筛：筛选出指定等级的词汇"""
    return [w for w in words if w.get("HSK等级") == level]

def count_by_pos(words):
    """③ 统：统计词性分布（数量）"""
    counts = {}
    for w in words:
        pos = w.get("词性", "未知")
        counts[pos] = counts.get(pos, 0) + 1
    return counts

# 👇 新增的功能：按词性分组输出（作业2的扩展功能）
def group_by_pos(words):
    """④ 组：将词汇按词性分组，返回字典"""
    groups = {}
    for w in words:
        pos = w.get("词性", "未知")
        if pos not in groups:
            groups[pos] = []  # 如果是新词性，先创建一个空列表
        groups[pos].append(w.get("词汇", "未知"))  # 把词汇加进去
    return groups

def gen_exercises(words, out="练习.txt"):
    """⑤ 写：生成练习题，根据拼音和词性写词语"""
    with open(out, "w", encoding="utf-8") as f:
        for w in words:
            pinyin = w.get("拼音", "无拼音")
            pos = w.get("词性", "无词性")
            if "释义" in w and w["释义"].strip():
                f.write(f"根据释义写词语：{w['释义']} （{pinyin}，{pos}）\n")
            else:
                f.write(f"根据拼音写词语：{pinyin} （{pos}）\n")

# ---- 主程序执行区 ----
if __name__ == "__main__":
    # 自动创建文件夹和CSV文件
    init_data_folder()
    
    file_path = os.path.join("data", "生词表.csv")
    
    # 执行流程
    all_words = load_words(file_path)
    if not all_words:
        exit()
        
    hsk4_words = filter_by_level(all_words, "4")
    pos_stats = count_by_pos(hsk4_words)
    
    # 调用新增的分组功能
    pos_groups = group_by_pos(hsk4_words)
    
    print(f"✅ 总词汇 {len(all_words)} 个")
    print(f"✅ 其中 HSK4 词汇 {len(hsk4_words)} 个")
    print("📊 词性分布（数量）：", pos_stats)
    
    # 打印分组结果（美化输出）
    print("\n📂 按词性分组输出：")
    for pos, word_list in pos_groups.items():
        print(f"【{pos}】：{'、'.join(word_list)}")
    
    gen_exercises(hsk4_words)
    print("\n📄 已成功生成练习题文件：练习.txt")