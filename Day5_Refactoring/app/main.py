from fastapi import FastAPI
from app.api.tasks import router as task_router

app = FastAPI()

app.include_router(task_router)

from fastapi.responses import JSONResponse
from fastapi import Request
from fastapi.exceptions import HTTPException

# 비동기 함수로 선언 / 예외 처리 통일
@app.exception_handlers(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False, 
            "data": None, 
            "message": exc.detail
        },
    )