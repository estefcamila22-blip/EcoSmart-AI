from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from config import settings

app = FastAPI(
    title="ESAI Energy Management API",
    description="Intelligent Sustainable Energy Agent API",
    version=settings.app_version,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "🌱 Welcome to ESAI - EcoSmart AI",
        "version": settings.app_version,
        "environment": settings.environment,
        "endpoints": {
            "docs": "/docs",
            "api_v1": settings.api_prefix,
        },
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=settings.host, port=settings.port, reload=True)