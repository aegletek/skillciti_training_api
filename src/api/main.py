# from fastapi import FastAPI, Depends
# from src.common.py.mysql_connection import MySQLConnectionPool
# from src.services.sql_services import SQLServices
# from src.common.py.config import PROPERTIES_PATH

from fastapi import FastAPI,HTTPException
from sqlalchemy import text
from src.common.py.mysql_connection import IDEASQLConnection
from pydantic import BaseModel

app = FastAPI()

@app.get("/test-db")
def test_db_connection():
    # Get database engine
    engine = IDEASQLConnection.get_instance().get_mysqlconnection()

    # Use text() for SQL execution
    with engine.connect() as conn:
        result = conn.execute(text("SELECT DATABASE();"))
        db_name = result.scalar()  # fetchone()[0] → scalar() in 2.x

    return {"connected_database": db_name}




class AdminLoginRequest(BaseModel):
    username: str
    password: str

@app.post("/admin/login")
def admin_login(request: AdminLoginRequest):
    try:
        engine = IDEASQLConnection.get_instance().get_mysqlconnection()

        with engine.connect() as conn:
            query = text("""
                SELECT user_id, user_name, user_type, rowstate
                FROM users
                WHERE user_name = :username
                  AND password = :password
                  AND user_type = 'admin'
                  AND rowstate = '0'
            """)

            result = conn.execute(query, {
                "username": request.username,
                "password": request.password
            })

            user = result.fetchone()

            if not user:
                raise HTTPException(
                    status_code=401,
                    detail="Invalid credentials or inactive admin account"
                )

            return {
                "status": "success",
                "message": "Admin login successful",
                "data": {
                    "user_id": user.user_id,
                    "username": user.user_name,
                    "user_type": user.user_type
                }
            }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))