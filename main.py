from fastapi import FastAPI
from domain.employ import employ_router

app = FastAPI()


# 라우터 등록
app.include_router(employ_router.router)
