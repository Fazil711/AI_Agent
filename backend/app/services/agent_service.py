from datetime import datetime
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_classic.agents import initialize_agent, AgentType
from langchain_classic.chains import retrieval_qa
from langchain_classic.memory import ConversationBufferMemory
from langchain_core.tools import Tool

from app.core.config import settings
from app.services.tool_service import ToolService

class AgentService:
    @classmethod
    def get_agent(cls, vectordb=None, dataframes=None, model_choice="Google Gemini"):
        # 1. Initialize LLM
        if model_choice == "Google Gemini":
            llm = ChatGoogleGenerativeAI(
                model="gemini-1.5-flash", 
                google_api_key=settings.GOOGLE_API_KEY,
                temperature=0,
                convert_system_message_to_human=True
            )
        else:
            llm = ChatOpenAI(
                model_name="gpt-4o", 
                openai_api_key=settings.OPENAI_API_KEY,
                temperature=0
            )

        # 2. Base Tools
        tools = [
            ToolService.get_web_search_tool(),
            Tool(
                name="YouTube Analyzer",
                func=ToolService.get_youtube_transcript,
                description="Useful for summarizing YouTube videos. Input: full URL."
            )
        ]

        # 3. Add Dynamic Tools (RAG & CSV)
        if vectordb:
            retriever = vectordb.as_retriever(search_kwargs={"k": 3})
            qa_chain = retrieval_qa.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)
            tools.append(Tool(
                name="Personal Knowledge Base",
                func=qa_chain.run,
                description="Useful for answering questions based on uploaded documents."
            ))

        if dataframes and len(dataframes) > 0:
            csv_tool = ToolService.get_csv_tool(dataframes[0], llm)
            if csv_tool:
                tools.append(csv_tool)

        # 4. Memory & Context
        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        today = datetime.now().strftime("%A, %B %d, %Y")

        agent_kwargs = {
            "prefix": f"You are a helpful AI assistant. Today is {today}.\nReturn valid JSON blobs. Escape quotes."
        }

        # 5. Initialize Agent
        return initialize_agent(
            tools, llm, 
            agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION, 
            verbose=True, memory=memory, agent_kwargs=agent_kwargs, 
            handle_parsing_errors=True, max_iterations=3
        )