import os 
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from orchestrator import Orchestrator, AgentState
from weather_agent import WeatherAgent

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
base_url = os.getenv("BASE_URL")

def create_chatbot():
    """create chatbot state graph"""
    
    # init agents
    orchestrator = Orchestrator()
    weather_agent = WeatherAgent()
    
    # create state graph
    workflow = StateGraph(AgentState)
    
    # add nodes
    workflow.add_node("orchestrator", orchestrator.route_query)
    workflow.add_node("weather_agent", weather_agent.process_query)
    workflow.add_node("format_response", orchestrator.format_response)
    
    # set entry point
    workflow.set_entry_point("orchestrator")
    
    # add conditional edges
    workflow.add_conditional_edges(
        "orchestrator",
        orchestrator.should_continue,
        {
            "weather_agent": "weather_agent",
            "end": "format_response"
        }
    )
    
    # add edges from expert agents to end
    workflow.add_edge("weather_agent", "format_response")
    workflow.add_edge("format_response", END)
    
    # compile graph
    app = workflow.compile()
    
    return app

def process_user_input(user_query: str) -> str:
    """process user input and return response"""
    app = create_chatbot()
    
    # create initial state
    initial_state = {
        "messages": [],
        "current_agent": "",
        "user_query": user_query,
        "agent_response": ""
    }
    
    # run graph
    result = app.invoke(initial_state)
    
    return result["agent_response"]
