import os 
import asyncio
from dotenv import load_dotenv
import ollama  
from ollama import AsyncClient
from tavily import TavilyClient
from mcp.server.fastmcp import FastMCP

load_dotenv()

client = AsyncClient()
mcp = FastMCP("Tools for content generation")
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

MODEL_INFO = "phi3" 
MODEL_SCRIPT = "phi3" 


@mcp.tool()
async def get_realtime_info(query: str) -> str: 
    try:
        loop = asyncio.get_event_loop()
        resp = await loop.run_in_executor (None, lambda: tavily.search( 
            query=query,
            max_results=3, 
            topic="general"
        ))
        if resp and resp.get("results"):
            summaries = []
            for r in resp["results"]:
                title = r.get("title", "")
                snippet = r.get("snippet", "")
                url = r.get("url", "")
                summaries.append(f"**{title}**\n\n{snippet}\n\n 🔗{url}")
            source_info = "\n\n---\n\n".join(summaries)
        
        else:
            source_info = f"No recent Updates found on '{query}'."

    except Exception as e:
        return str(e)
    
    prompt=f"""
    You are a professional researcher and content creator with expertise in multiple fields.
    Using the following real-time information, write an accurate, engaging, and human-like summary
    for the topic: '{query}'.
     
    Requirements:
    - Keep it factual, insightful, and concise (around 200 words).
    - Maintain a smooth, natural tone.
    - Highlight key takeaways or trends
    - Avoid greetings or self-references.

    Source information:
    {source_info}

    Output only the refined, human-readable content.
    """
    try: 
        response = await client.generate(model=MODEL_INFO, prompt=prompt)
        return response['response'].strip() if response and 'response' in response else source_info

    except Exception as e:
        return f"Error is {e} and Info is {source_info}"

@mcp.tool()
async def generate_video_script(info_text: str) -> str:
    prompt= f"""
    You are a creative scriptwriter.
    Turn this real-time information into an engaging short video script ( for Youtube shots or Instagram Reels)
    Use a conversational tone with a strong hook and a clear call to action at the end.
    Keep it around 100-200 words.

    {info_text}
    """
    try:
        response = await client.generate(model=MODEL_SCRIPT, prompt=prompt)
        return response['response'] if response and 'response' in response else "Could not generate video script"
    except Exception as e:
        raise Exception(f"Research failed: {str(e)}")