from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.agent_service import AgentService
# Import other necessary services or schemas

router = APIRouter()  # <--- THIS MUST BE NAMED 'router'

class ChatRequest(BaseModel):
    message: str
    model: str = "Google Gemini"

@router.post("/")
async def chat(request: ChatRequest):
    try:
        # Implementation logic for the agent
        agent = AgentService.get_agent(model_choice=request.model)
        response = agent.run(input=request.message)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))