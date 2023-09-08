import sys
import os
from dotenv import load_dotenv
import Agently
import blueprints

# 加载配置文件
load_dotenv('private_settings')

llm_name = os.getenv('llm_name')
group_id = os.getenv('group_id') 
api_key = os.getenv('api_key')
llm_url = os.getenv('llm_url')
proxy = os.getenv('proxy')
blueprint_name = os.getenv('blueprint').replace('./examples/blueprints/','').replace('.py','')
print('已经加载: ', blueprint_name)

if not api_key:
    print("用户输入的 KEY 为空，请提供有效的 KEY。")
    sys.exit(1)

agently = Agently.create()
blueprint = blueprints.get_blueprint(blueprint_name)
agent = agently.create_agent(blueprint)
agent_name = agent.runtime_ctx.get("agent_name")
agent_name = agent_name if agent_name else "机器人"

#添加模型相关授权信息
agent.set_llm_name(llm_name)
if llm_name == "GPT":
    agent.set_llm_auth(llm_name, api_key)
    if llm_url:
        agent.set_llm_url(llm_name, llm_url)
    if proxy:
        agent.set_proxy(proxy)
elif llm_name == "MiniMax":
    agent.set_llm_auth(llm_name, { "group_id": group_id, "api_key": api_key })
    if llm_url:
        agent.set_llm_url(llm_name, llm_url)

def generate_reply(user_input, session):
    reply = session\
        .input(user_input)\
        .start()
    return reply

def chatbot():
    session = agent.create_session()
    session.use_context(True)#<-开启一下agent的多轮会话自动记录
    print("欢迎使用多轮对话CLI界面！输入exit可以退出对话。")
    conversation = []
    while True:
        # 提示用户输入对话内容
        user_input = input("用户: ")
        
        # 将用户输入加入对话列表
        conversation.append(("用户", user_input))

        # 判断用户是否要结束对话
        if user_input.lower() == "exit":
            try:
                break
            except Exception as e:
                pass
        
        # 对用户输入进行处理并生成回复
        # 在这里替换成你的对话生成代码
        bot_reply = generate_reply(user_input, session)
        
        # 将机器人回复加入对话列表
        conversation.append((agent_name, bot_reply))
        
        # 输出机器人回复
        print(f"{ agent_name }: ", bot_reply)
    
    # 输出完整对话（暂时不需要）
    #print("对话记录：")
    #for role, content in conversation:
    #    print(role + ": " + content)

if __name__ == "__main__":
    chatbot()