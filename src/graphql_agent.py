import json
import os
import asyncio
from typing import List, TypedDict, Annotated, Optional, Dict, Any

from dotenv import load_dotenv
from langchain.schema import BaseMessage
from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain.prompts import ChatPromptTemplate
from langchain_mcp_adapters.client import MultiServerMCPClient

load_dotenv()

GRAPHQL_ENDPOINT = "https://graph.web3.bio/graphql"


class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], "conversation history"]
    current_agent: Annotated[str, "current agent name"]
    user_query: Annotated[str, "user query"]
    agent_response: Annotated[str, "agent response"]
    endpoint_url: Annotated[str, "GraphQL endpoint url"]
    graphql_query: Annotated[Optional[str], "generated GraphQL query"]
    query_result: Annotated[Optional[Dict[str, Any]], "GraphQL query result"]
    query_error: Annotated[Optional[str], "GraphQL query error"]


class ReactGraphQLAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4.1-mini",
            base_url=os.getenv("BASE_URL"),
            api_key=os.getenv("OPENAI_API_KEY"),
        )
        
        self.client = MultiServerMCPClient({
            "relate-account": {
                "transport": "streamable_http",
                "url": "http://127.0.0.1:8000/mcp"
            }
        })
        
        self.tools = None
        self.agent = None
        self.agent_executor = None
        self._initialized = False

    async def _initialize(self):
        """Async initialize agent and tools"""
        if self._initialized:
            return
            
        self.tools = await self.client.get_tools()

        prompt_expert = ChatPromptTemplate.from_messages([
            ("system", """
              You are a helpful data assistant that translates natural language questions into GraphQL queries. 
              You could use the tools provided to get the query schema which can help you build the query statement.
              
              You should:
                1. Understand what data the user is asking for
                2. Create a GraphQL query to retrieve that information
                3. Execute the query and present the results

              all above steps could be done with the tools provided.
              
              Be precise and focused in your responses.
              
              Available tools: {tools}
              Tool names: {tool_names}
            """),
            ("human", "{{input}}"),
            ("ai", "{agent_scratchpad}")
        ])
        
        # Create ReAct agent
        self.agent = create_react_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=prompt_expert
        )
        
        # Create agent executor
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=True,
            handle_parsing_errors=True
        )
        
        self._initialized = True

    async def run(self, state: AgentState) -> AgentState:
        try:
            # Ensure initialized
            await self._initialize()
            
            # Use agent executor to process query
            result = self.agent_executor.invoke({
                "input": state["user_query"]
            })
            
            state["agent_response"] = result["output"]
            
        except Exception as e:
            error_msg = f"处理查询时发生错误: {str(e)}"
            state.update({
                "agent_response": error_msg,
                "query_error": str(e)
            })
        
        return state
