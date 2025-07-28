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

            system_prompt = """
            Your are an expert GraphQL agent. 
            You are working with a GraphQL API from web3.bio which allows you to query users' web2 and web3 identities.
            The query schema (analyzed and formatted in advanced) is as follows:
            {{analysis}}

            About web3.bio graphql query endpoint, you should know:
            - Every user can be described by an identity graph, which is a network structure of web2 and web3 identities.
            - Each node in the identity graph is a web2 or web3 identity identity record. 
                - When user wants to query the single identity info, you could query the `profile` field of the identity; 
                - If user wants to query all the identities of a user (identities across different platforms), you could query the `identityGraph` field of the user. This describes the whole identity graph of the user.
                - Each `IdentityGraph` fields contains a list of identity records (corresponding to the `vertices`). Attention here, you'd better keep it constant between the `vertices` query field and `profile` fields. For example:

                When user wants to query all the identities of "sujiyan.eth", you'd better query like this:
                 ```graphql
                query {
                    identity(platform: ens, identity: "sujiyan.eth") {
                        id
                        status
                        aliases
                        profile {
                            identity
                            address
                            displayName
                            avatar
                            texts
                            description
                            addresses {
                                address
                                network
                            }
                        }
                        identityGraph {
                            graphId
                            vertices {
                                identity
                                address
                                displayName
                                avatar
                                texts
                                description
                                addresses {
                                    address
                                    network
                                }
                            }
                        }
                    }
                }
                ```

            Data source:
            - Web2 Identity: social media accounts (e.g. twitter, instagram, personal website, github and etc.), personal contact info (e.g. email, location and etc.)
            - Web3 Identity: Onchain naming system on different blockchains (e.g. ENS, Lens, unstoppable domains, Solana name service etc.), web3 social media accounts (e.g. Lens, farcaster, etc.)
        
            The above always used as the param "platform" value.

            User query: "show me the identity profile of sujiyan.eth?"
            You:
            ```graphql
            query {
                identity(platform: ens, identity: "sujiyan.eth") {
                    id
                    status
                    aliases
                    profile {
                        identity
                        platform
                        network
                        address
                        displayName
                        avatar
                        texts
                        description
                        addresses {
                            address
                            network
                        }
                    }
                }
            }
            ```

            

            You should:
            1. Understand what data the user is asking for, and what info you are given.
            2. Use the given query schema to generate a valid GraphQL query statement
            3. Execute the query and directly present the query results

            all above steps could be done with the tools provided. if user is asking the identity info on web3.bio, you should use the given tool.

            Here are some hints for you while generating the GraphQL query statement:
            1. Pay attention to the enum types, you should pass the exact enum value instead of the string. e.g. if the enum type is ens, you should pass ens instead of the string "ens".
            2. When user doesn't clarify the specific field to query, you'd better contains the `profile` field and some other real identity-related plain text fields. e.g. `displayName`, `texts`, `description`, `addresses` and etc. The fields like "graphId", "updatedAt", "registeredAt" and etc. are not real identity-related fields.
            
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
