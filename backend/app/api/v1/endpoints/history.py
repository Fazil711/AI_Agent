from fastapi import APIRouter, HTTPException
from app.db.session import get_db_connection

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
async def clear_chat_history():
    try:
        conn = get_db_connection()
        conn.execute('DELETE FROM messages')
        conn.commit()
        conn.close()
        return {"status": "success", "message": "History cleared"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))