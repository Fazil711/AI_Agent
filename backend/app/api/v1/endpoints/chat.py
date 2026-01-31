import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.agent_service import AgentService
from app.services.state_service import brain_state #

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    model: str = "Google Gemini"

@router.post("/")
async def chat(request: ChatRequest):
    try:
        # 1. Initialize the agent with the persistent brain state
        agent = AgentService.get_agent(
            vectordb=brain_state.vectordb, 
            dataframes=brain_state.dataframes, 
            model_choice=request.model
        )
        
        # 2. Run the agent logic
        response = agent.run(input=request.message)
        
        # 3. Check for generated visualizations (from ToolService.analyze_data)
        image_path = None
        if os.path.exists("visual.png"):
            image_path = "visual.png" 
            # Note: The path is relative to the backend root
        
        return {
            "response": response,
            "image_path": image_path #
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))