from fastapi import APIRouter, HTTPException
from app.db.session import get_db_connection
import os
import shutil
import glob
from fastapi import APIRouter
from app.services.state_service import brain_state
from app.core.config import settings

router = APIRouter()

@router.get("/")
async def get_chat_history():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT role, content, timestamp FROM messages ORDER BY id ASC')
        rows = cursor.fetchall()
        conn.close()
        
        return [{"role": row["role"], "content": row["content"], "timestamp": row["timestamp"]} for row in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.delete("/clear")
async def clear_history():
    # 1. Reset the AI's internal state
    brain_state.reset()
    
    # 2. Delete all uploaded files
    if os.path.exists(settings.UPLOAD_DIR):
        shutil.rmtree(settings.UPLOAD_DIR)
        os.makedirs(settings.UPLOAD_DIR) # Recreate empty folder
    
    # 3. Delete generated visualizations (*.png)
    for img in glob.glob("*.png"):
        try:
            os.remove(img)
        except Exception:
            pass
            
    # 4. Optional: Clear Chroma DB persistent storage
    if os.path.exists(settings.CHROMA_PERSIST_DIR):
        shutil.rmtree(settings.CHROMA_PERSIST_DIR)

    return {"message": "Memory, files, and plots have been wiped clean."}