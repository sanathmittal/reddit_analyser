from fastapi import FastAPI
from .routes import router

app = FastAPI()

# Include API routes
app.include_router(router)

@app.get("/")
def home():
    return {"message": "Reddit Analyzer API is running!"}
