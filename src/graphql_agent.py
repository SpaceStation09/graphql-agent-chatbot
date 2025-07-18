import os
from typing import List, TypedDict, Annotated, Optional, Dict, Any

from dotenv import load_dotenv
from langchain.schema import BaseMessage
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
import json


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

        
        # Create ReAct agent
        self.agent = create_react_agent(
            # TODO: temperature low
            model=self.llm,
            tools=self.tools,
        )
        
        self._initialized = True

    async def run(self, state: AgentState) -> AgentState:
        try:
            # Ensure initialized
            await self._initialize()

            with open("src/schema.json", "r", encoding="utf-8") as f:
                schema_data = json.load(f).get("data", {})

            types = schema_data.get("__schema", {}).get("types", [])
            # Filter out internal types
            filtered_types = [t for t in types if not t.get("name", "").startswith("__")]
            
            analysis = {
                "schema_name": "web3.bio",
                "endpoint": GRAPHQL_ENDPOINT,
                "type_count": len(filtered_types),
                "object_types": [t.get("name") for t in filtered_types if t.get("kind") == "OBJECT"],
                "scalar_types": [t.get("name") for t in filtered_types if t.get("kind") == "SCALAR"],
                "enum_types": [t.get("name") for t in filtered_types if t.get("kind") == "ENUM"],
            }

            # 1. return json rather than a summary
            # 2. explain the identity terminology
            system_prompt = """
              You are a helpful data assistant that translates natural language questions into GraphQL queries. 
              The query schema (analyzed and formatted in advanced) is as follows:
              {{analysis}}
              
              You should:
                1. Understand what data the user is asking for
                2. Create a GraphQL query to retrieve that information
                3. Execute the query and present the results

              all above steps could be done with the tools provided. if user is asking the identity info on web3.bio, you should use the given tool

              Pay attention to the enum types, you should pass the exact enum value instead of the string. e.g. if the enum type is ens, you should pass ens instead of the string "ens".
              
              Be precise and focused in your responses.
              
            """

            initial_msg = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=state["user_query"])
            ]
            
            # Use agent executor to process query
            result = await self.agent.ainvoke({
                "messages": initial_msg
            })
            messages = result["messages"]
            state["agent_response"] = next((msg for msg in reversed(messages) if isinstance(msg, AIMessage)), None)
            
        except Exception as e:
            error_msg = f"处理查询时发生错误: {str(e)}"
            state.update({
                "agent_response": error_msg,
                "query_error": str(e)
            })
        
        return state
