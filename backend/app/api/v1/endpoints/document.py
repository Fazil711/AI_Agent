from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
import os
import shutil
from app.services.rag_service import RAGService
from app.services.state_service import brain_state
from app.core.config import settings

router = APIRouter()

@router.get("/files") # New endpoint to sync state on refresh
async def get_files():
    return {"filenames": brain_state.filenames}

@router.post("/upload")
async def upload_documents(files: List[UploadFile] = File(...)):
    if not os.path.exists(settings.UPLOAD_DIR):
        os.makedirs(settings.UPLOAD_DIR)
        
    saved_paths = []
    try:
        for file in files:
            path = os.path.join(settings.UPLOAD_DIR, file.filename)
            with open(path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            saved_paths.append(path)
            
        docs, dfs = RAGService.load_files(saved_paths)
        
        # Update global state
        brain_state.vectordb = RAGService.create_vector_store(docs)
        brain_state.dataframes.extend(dfs)
        
        # Prevent duplicate names in the sidebar
        new_names = [f.filename for f in files]
        brain_state.filenames = list(set(brain_state.filenames + new_names))
        
        return {
            "message": "Files processed", 
            "filenames": brain_state.filenames
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))