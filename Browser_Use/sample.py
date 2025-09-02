#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from browser_use import Agent

load_dotenv()

#llm = ChatOpenAI(model="gpt-4o")
llm=ChatOpenAI(base_url='https://api.deepseek.com/v1', model='deepseek-chat', api_key="sk-81d695f0638f4520b1360e8b5cf7e94b")


async def main():
    agent = Agent(
        task="打开 https://cn.vuejs.org/guide/essentials/computed，获取页面里所有的 h2 标签文本及所有的 a 标签文本（以及它的 href）",
        llm=llm,
    )
    result = await agent.run()
    print('result:',result)

if __name__ == "__main__":
    asyncio.run(main())