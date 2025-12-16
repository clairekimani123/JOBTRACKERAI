from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from app.core.config import settings

# Initialize FastAPI app
app = FastAPI(
    title="JobTrackAI API",
    description="AI-Powered Job Application Tracker",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL, "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    """Initialize database tables on startup"""
    try:
        from app.core.database import engine, Base
        from app.models import User, Application, Resume
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully!")
    except Exception as e:
        print(f"⚠️ Database initialization error: {e}")

@app.get("/")
def read_root():
    return {
        "message": "Welcome to JobTrackAI API",
        "version": "1.0.0",
        "status": "running",
        "docs": "Visit /docs for API documentation"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/api/test-db")
def test_database():
    """Test database connection"""
    try:
        from app.core.database import SessionLocal
        
        db = SessionLocal()
        result = db.execute(text("SELECT 1"))
        db.close()
        return {"status": "Database connection successful!"}
    except Exception as e:
        return {"status": "Database connection failed", "error": str(e)}

# Register Authentication routes
# from app.api.auth import router as auth_router
# app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])

from app.api import auth, applications, resumes, users

app.include_router(auth.router, prefix="/api")
app.include_router(applications.router, prefix="/api")
app.include_router(resumes.router, prefix="/api")
app.include_router(users.router, prefix="/api")
