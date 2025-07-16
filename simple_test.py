#!/usr/bin/env python3
"""
测试异步修复的脚本
"""

import asyncio
import os
from dotenv import load_dotenv
from src.graphql_agent import ReactGraphQLAgent, AgentState

load_dotenv()

async def test_graphql_agent():
    print("测试GraphQL Agent...")
    
    try:
        # 创建agent实例
        agent = ReactGraphQLAgent()
        print("✓ Agent实例创建成功")
        
        # 测试异步初始化
        await agent._initialize()
        print("✓ 初始化成功")
        
        # 测试运行
        test_state = AgentState(
            messages=[],
            current_agent="graphql_agent",
            user_query="query the identity of sujiyan.eth on web3.bio",
            agent_response="",
            endpoint_url="https://graph.web3.bio/graphql",
            graphql_query=None,
            query_result=None,
            query_error=None
        )
        
        result = await agent.run(test_state)
        print("✓ Agent运行成功")
        print(f"响应: {result['agent_response']}")
        
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        return False
    
    return True

async def main():
    """主测试函数"""
    print("开始测试...")
    print("=" * 50)
    
    success = await test_graphql_agent()
    
    print("=" * 50)
    if success:
        print("✓ 所有测试通过！")
    else:
        print("✗ 测试失败，需要进一步调试。")

if __name__ == "__main__":
    asyncio.run(main()) 