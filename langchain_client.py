import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage

llm = ChatOpenAI()

async def main():
    client = MultiServerMCPClient(
        {
            "math" : {
                "command":"python", 
                "args": [
                    "/Volumes/Transcend/LLMs_study/MCP/mcp-crash-course/servers/math_server.py"
                ],
                "transport": "stdio",
            },
            "weather":{
                "url":"http://localhost:8000/sse",
                "transport":"sse",
                },
        }
    )
    tools = await client.get_tools()
    agent = create_react_agent(llm, tools)
    # result = await agent.ainvoke({"messages": [HumanMessage(content="What is 2 + 2?
    result = await agent.ainvoke({"messages": [HumanMessage(content="What's weather in Hong Kong?")]})
    print(result["messages"][-1].content)    # print("hello langchain mcp") 
    
if __name__ == "__main__":
    asyncio.run(main())