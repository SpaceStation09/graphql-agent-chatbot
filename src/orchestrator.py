from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import JsonOutputToolsParser
from langchain.schema import BaseMessage
from typing import List, TypedDict, Annotated
import os
from dotenv import load_dotenv
import json

load_dotenv()

class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], "conversation history"]
    current_agent: Annotated[str, "current agent name"]
    user_query: Annotated[str, "user query"]
    agent_response: Annotated[str, "agent response"]

class Orchestrator:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            base_url=os.getenv("BASE_URL"),
            api_key=os.getenv("OPENAI_API_KEY"),
        )

        self.parser = JsonOutputToolsParser()
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """你是一个智能Orchestrator，负责协调多个Agent完成任务。

            可用的agents:
            1. weather_agent: 处理天气查询，当用户询问某地天气时使用

            你的任务:
            1. 分析用户查询
            2. 决定使用哪个agent处理
            3. 返回JSON格式的决策，包含agent_name字段

            示例输出:
            {{"agent_name": "weather_agent"}}

            如果查询不匹配任何agent，返回: {{"agent_name": "none"}}
            """),
            ("human", "{user_query}")
        ])

    def route_query(self, state: AgentState) -> AgentState:
        """indent detect and routing"""
        user_query = state["user_query"]
        
        # use LLM to analyze query and decide routing
        response = self.llm.invoke(
            self.prompt.format_messages(user_query=user_query)
        )
        
        try:
            # try to parse json response
            decision = json.loads(response.content)
            agent_name = decision.get("agent_name", "none")
        except:
            # if parse failed, default to none
            agent_name = "none"
        
        # update state
        state["current_agent"] = agent_name
        
        return state

    def should_continue(self, state: AgentState) -> str:
        """decide next step"""
        current_agent = state["current_agent"]
        
        if current_agent == "weather_agent":
            return "weather_agent"
        else:
            return "end"

    def format_response(self, state: AgentState) -> AgentState:
        if state["current_agent"] == "none":
            # when no suitable agent, use orchestrator's LLM to answer question
            response = self.llm.invoke(
                f"用户询问: {state['user_query']}\n\n请直接回答用户的问题，不需要使用任何特定的agent。"
            )
            state["agent_response"] = response.content
        else:
            # if agent response, use it directly
            if "agent_response" not in state or not state["agent_response"]:
                state["agent_response"] = "抱歉，我没有找到合适的响应。"
        
        return state
        