from mcp.server.fastmcp import FastMCP
from app2 import get_realtime_info, generate_video_script

mcp = FastMCP("This is for Script Generator")

@mcp.tool()
async def get_info_mcp(query):
    return get_realtime_info(query)

@mcp.tool()
async def generate_video_mcp(query):
    real_info = get_realtime_info(query)
    info = generate_video_script(real_info)
    return info

if __name__ == "__main__":
    mcp.run(transport="stdio")