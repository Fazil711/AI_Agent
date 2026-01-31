import os
from langchain_core.tools import Tool
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.document_loaders import YoutubeLoader
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent

class ToolService:
    @staticmethod
    def get_web_search_tool():
        search = DuckDuckGoSearchRun()
        return Tool(
            name="Web Search",
            func=search.run,
            description="Useful for finding current information, news, or general knowledge."
        )

    @staticmethod
    def get_youtube_transcript(video_url: str):
        try:
            loader = YoutubeLoader.from_youtube_url(video_url, add_video_info=False, language=["en", "hi"])
            docs = loader.load()
            return docs[0].page_content[:4000] if docs else "No transcript found."
        except Exception as e:
            return f"Error fetching YouTube transcript: {str(e)}"

    @staticmethod
    def get_csv_tool(df, llm):
        if df is None:
            return None
            
        prefix = """
        You are working with a pandas dataframe in Python. The name of the dataframe is `df`.
        IMPORTANT RULES FOR PLOTTING:
        1. If asked to visualize, use 'matplotlib.pyplot'.
        2. ALWAYS save the plot to a file named 'visual.png'.
        3. DO NOT use plt.show().
        4. WHEN FINISHED, YOU MUST RESPOND WITH: "Final Answer: I have saved the plot to visual.png"
        """
        
        pandas_agent = create_pandas_dataframe_agent(
            llm, df, verbose=True, allow_dangerous_code=True,
            prefix=prefix, handle_parsing_errors=True 
        )

        def analyze_data(query):
            if os.path.exists("visual.png"):
                os.remove("visual.png")
            return pandas_agent.run(query)

        return Tool(
            name="Data Analyst",
            func=analyze_data,
            description="Useful for analyzing structured data (CSV/Excel). Input the math or plotting question directly."
        )