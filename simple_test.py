#!/usr/bin/env python3
"""
Simple test script for the GraphQL Agent
"""

import asyncio
from dotenv import load_dotenv
from src.graphql_agent import ReactGraphQLAgent, AgentState

load_dotenv()

async def test_graphql_agent():
    print("测试GraphQL Agent...")
    
    try:
        # Create agent instance
        agent = ReactGraphQLAgent()
        print("✓ Agent instance created successfully")
        
        # Test asynchronous initialization
        await agent._initialize()
        print("✓ Initialization successful")
        
        # Test run
        test_state = AgentState(
            messages=[],
            current_agent="graphql_agent",
            user_query="query the ethereum address of sujiyan.eth on web3.bio",
            agent_response="",
            endpoint_url="https://graph.web3.bio/graphql",
            graphql_query=None,
            query_result=None,
            query_error=None
        )
        
        result = await agent.run(test_state)
        print("✓ Agent run successfully")
        print(f"Response: {result['agent_response']}")
        
    except Exception as e:
        print(f"✗ Test failed: {e}")
        return False
    
    return True

async def main():
    """Main test function"""
    print("Starting test...")
    print("=" * 50)
    
    success = await test_graphql_agent()
    
    print("=" * 50)
    if success:
        print("✓ All tests passed!")
    else:
        print("✗ Test failed, need further debugging.")

if __name__ == "__main__":
    asyncio.run(main()) 