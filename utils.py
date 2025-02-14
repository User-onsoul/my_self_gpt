from langchain.chains import ConversationChain
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory

import os


def get_chat_response(prompt, memory, openai_api_key):
    model = ChatOpenAI(model="deepseek-reasoner", openai_api_key=openai_api_key, base_url="https://aiproxy.hzh.sealos.run/v1")
    chain = ConversationChain(llm=model, memory=memory)

    response = chain.invoke({"input": prompt})
    return response["response"]
