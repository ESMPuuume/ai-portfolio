import os
from rag_qa import rag_qa

def main():
    print("="*50)
    print("👋 欢迎使用【学科智能问答助手 v1.0】")
    print("💡 输入 'quit' 或 'exit' 退出程序。")
    print("="*50)

    while True:
        try:
            question = input("\n🙋‍♂️ 你：").strip()
            
            if question.lower() in ['quit', 'exit']:
                print("👋 助手：再见！")
                break
                
            if not question:
                continue
            
            print("🤖 助手正在查阅资料并思考中，请稍候...\n")
            answer = rag_qa(question)
            
            print(f"\n🤖 助手：\n{answer}")
            print("-" * 50)
            
        except KeyboardInterrupt:
            print("\n👋 助手：强制退出。")
            break
        except Exception as e:
            print(f"\n❌ 发生错误：{e}")

if __name__ == "__main__":
    main()