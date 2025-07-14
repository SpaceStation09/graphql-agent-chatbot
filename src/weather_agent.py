from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import BaseMessage
from typing import List, TypedDict, Annotated
import os
from dotenv import load_dotenv

load_dotenv()

class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], "conversation history"]
    current_agent: Annotated[str, "current agent name"]
    user_query: Annotated[str, "user query"]
    agent_response: Annotated[str, "agent response"]

class WeatherAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            base_url=os.getenv("BASE_URL"),
            api_key=os.getenv("OPENAI_API_KEY"),
        )

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """你是一个天气专家，专门处理天气相关的查询。

            你的任务：
            1. 理解用户的天气查询
            2. 提供天气信息和建议
            3. 如果用户询问特定城市的天气，提供相关信息

            示例查询：
            - "北京今天天气怎么样？"
            - "明天上海会下雨吗？"
            - "纽约的天气预报"

            请以友好的方式回复，并说明你是Weather Agent。
            注意：由于这是演示，你可能需要模拟一些天气数据。 如果是模拟的数据，请在回复中说明。
            """),
            ("human", "{user_query}")
        ])

    def process_query(self, state: AgentState) -> AgentState:
        """process weather related query"""
        user_query = state["user_query"]
        
        # use LLM to process query
        response = self.llm.invoke(
            self.prompt.format_messages(user_query=user_query)
        )
        
        # update state
        state["agent_response"] = response.content
        state["current_agent"] = "weather_agent"
        
        return state 