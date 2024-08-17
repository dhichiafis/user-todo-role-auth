from fastapi import FastAPI 
import uvicorn 
from api.users import user_router
import models.sqlmodels 
from db import engine
models.sqlmodels.Base.metadata.create_all(bind=engine)
app=FastAPI() 
app.include_router(user_router,prefix='/users')


if __name__=="__main__":
    uvicorn.run("main:app",reload=True,host='127.0.0.1',port=8008)