import streamlit as st
import os 
from dotenv import load_dotenv
import ollama  # <-- Changed: Using Ollama instead of google.genai
from tavily import TavilyClient
import time

load_dotenv()

# Configure API's
# <-- Changed: Removed Gemini Client, as Ollama runs locally
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

# Select the Model 
MODEL_INFO = "phi3" # <-- Changed to user's specified local model
MODEL_SCRIPT = "phi3" # <-- Changed to user's specified local model

st.set_page_config(
                   page_title="StoryForge Agent",
                   page_icon="🌐",
                   layout="centered",
                   initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
            .stApp{
                background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
                color: #f5f5f5;
            }
            h1, h2, h3 {
                text-align: center;
                color: #F9FAFB !important;
            }
            .stTextInput>div>div>input{
                border: 1px solid #6EE7B7 !important;
                border-radius: 10px;
                padding: 12px;
                background-color: #111827;
                color: white !important;
            }
            div.stButton > button {
                background: linear-gradient(90deg, #06b6d4, #3b82f6);
                color: white;
                border-radius: 8px;
                padding: 0.6rem 1.2rem;
                font-weight: 600;
                border: none;
                transition: 0.3s ease-in-out;
            }
            div.stButton > button:hover {
                transform: scale(1.05);
                background: linear-gradient(90deg, #2563eb, #06b6d4);
            }
            .card {
                background-color: rgba(255, 255, 255, 0.05);
                padding: 20px;
                border-radius: 16px;
                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
                margin-top: 20px;
            }
            .stRadio > div {
                justify-content: center;
            }
            footer, .stCaption {
                text-align: center;
                color: #9CA3AF;
            }
    </style>
            """, unsafe_allow_html=True)


def get_realtime_info(query): 
    try:
        resp = tavily.search(
            query=query,
            max_results=3, 
            topic="general"
        )
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
        st.error(f"❌ Error fetching info: {e}")
        return None
    
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
        # <-- Changed: Using ollama.generate instead of Gemini SDK
        response = ollama.generate(model=MODEL_INFO, prompt=prompt)
        return response['response'].strip() if response and 'response' in response else source_info

    except Exception as e:
        st.error(f"❌ Error generating summary with Ollama: {e}\n\nMake sure Ollama is running and you have pulled the {MODEL_INFO} model.")
        return source_info


def generate_video_script(info_text):
    prompt= f"""
    You are a creative scriptwriter.
    Turn this real-time information into an engaging short video script ( for Youtube shots or Instagram Reels)
    Use a conversational tone with a strong hook and a clear call to action at the end.
    Keep it around 100-200 words.

    {info_text}
    """
    try:
        # <-- Changed: Using ollama.generate instead of Gemini SDK
        response = ollama.generate(model=MODEL_SCRIPT, prompt=prompt)
        return response['response'] if response and 'response' in response else "Could not generate video script"
    except Exception as e:
        st.error(f"Error Generating video script with Ollama: {e}")
        return None

def main():
    st.markdown("<h1> 🌐StoryForge Agent</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color :#D1D5DB;'> Search any Topic - from world news to research trends - and get AI-powered insights & video scripts instantly </p>", unsafe_allow_html=True)

    query = st.text_input("Enter your topic or question:")
    if query:
        with st.spinner(" 🌍 Gathering latest Information..."):
            info_result = get_realtime_info(query=query)

        if info_result:
            # Fixed HTML syntax: closing quote and changed closing tag to </div>
            st.markdown("<div class='card'>", unsafe_allow_html=True) 
            st.subheader("AI-Generated summary")
            st.write(info_result)
            st.markdown("</div>", unsafe_allow_html=True)

            generate_script = st.radio(
                "🎥 Generate a short video script? ",
                ("No", "Yes"),
                index = 0,
                horizontal=True
            )

            if generate_script == "Yes":
                time.sleep(2) 
                
                with st.spinner("🎬 Crafting your script..."):
                    script = generate_video_script(info_result)

                if script:
                    # Fixed HTML syntax here as well
                    st.markdown("<div class='card'>", unsafe_allow_html=True)
                    st.subheader("Video Script")
                    st.write(script)
                    st.download_button(
                        label="Download Script",
                        data=script,
                        file_name = "video_script.txt",
                        mime="text/plain"
                    )
                    st.markdown("</div>", unsafe_allow_html=True)
                else:
                    st.warning(" ⚠️ Could not generate transciption.")
            
        else:
            st.warning("No valid information found. Please try another query")
    
    st.markdown("<hr>", unsafe_allow_html=True)
    st.caption("Made with 💝")


if __name__ == "__main__":
    main()