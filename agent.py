from pathlib import Path  
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, SseConnectionParams

# import Path and resolve full path to server script
PATH_TO_YOUR_MCP_SERVER_SCRIPT = str((Path(__file__).parent / "server.py").resolve())

# Agent definition
stock_analysis_agent = LlmAgent(
    model="gemini-2.5-flash",
    name="stock_analysis_agent",
    description="Agent for answering stock technical analysis queries using MCP tools.",
    instruction="""
    Use the available tool `plot_technical_analysis` when user requests technical analysis.
    If the user doesn’t provide start_date or end_date, ask follow-up questions to collect them.
    After generating the chart, return the image filename and then hand back control to manager.
    """,
    tools=[
        MCPToolset(
            connection_params=SseConnectionParams(
                command="python3",  
                url="http://localhost:8000/sse",  
                args=[PATH_TO_YOUR_MCP_SERVER_SCRIPT],
            )
        )
    ],
)

# Run the agent
if __name__ == "__main__":
    stock_analysis_agent.run()
