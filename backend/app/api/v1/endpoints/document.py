from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
import os
import shutil
from app.services.rag_service import RAGService
from app.services.state_service import brain_state #
from app.core.config import settings

router = APIRouter()

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
        
        # Save to global brain state
        brain_state.vectordb = RAGService.create_vector_store(docs)
        brain_state.dataframes = dfs
        
        return {
            "message": "Files processed", 
            "docs_count": len(docs), 
            "tables_count": len(dfs),
            "filenames": [f.filename for f in files] # Return names for confirmation
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    # Finally block removed cleanup to ensure RAGService can read files if needed, 
    # but load_files usually reads them into memory.