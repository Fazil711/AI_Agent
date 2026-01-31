from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
import os
import shutil
from app.services.rag_service import RAGService
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
        vectordb = RAGService.create_vector_store(docs)
        
        # In a real app, store vectordb reference in state/session
        return {"message": "Files processed", "docs_count": len(docs), "tables_count": len(dfs)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Cleanup temp files
        for p in saved_paths:
            if os.path.exists(p): os.remove(p)