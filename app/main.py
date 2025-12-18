from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from sqlalchemy import text

from app.core.config import settings

# -------------------------
# CREATE FASTAPI APP
# -------------------------
app = FastAPI(
    title="JobTrackAI API",
    description="AI-Powered Job Application Tracker",
    version="1.0.0"
)

# -------------------------
# CORS CONFIG
# -------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        settings.FRONTEND_URL,
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# STARTUP EVENT
# -------------------------
@app.on_event("startup")
async def startup_event():
    try:
        from app.core.database import engine, Base
        from app.models import User, Application, Resume

        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully!")
    except Exception as e:
        print(f"⚠️ Database initialization error: {e}")

# -------------------------
# ROOT & HEALTH
# -------------------------
@app.get("/")
def read_root():
    return {
        "message": "Welcome to JobTrackAI API",
        "status": "running",
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/api/test-db")
def test_database():
    try:
        from app.core.database import SessionLocal
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        return {"status": "Database connection successful!"}
    except Exception as e:
        return {"status": "Database connection failed", "error": str(e)}

# -------------------------
# ROUTERS
# -------------------------
from app.api import auth, applications, resumes, users, ai


app.include_router(auth.router, prefix="/api", tags=["Authentication"])
app.include_router(applications.router, prefix="/api", tags=["Applications"])
app.include_router(resumes.router, prefix="/api", tags=["Resumes"])
app.include_router(users.router, prefix="/api", tags=["Users"])
app.include_router(ai.router)


# -------------------------
# CUSTOM OPENAPI (HTTP BEARER)
# -------------------------
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="JobTrackAI API",
        version="1.0.0",
        description="AI-Powered Job Application Tracker",
        routes=app.routes,
    )

    # 🔐 Define Bearer Auth
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }

    # 🔒 Apply globally
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method["security"] = [{"BearerAuth": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
