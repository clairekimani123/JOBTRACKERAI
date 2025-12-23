from app.models.user import User
from app.models.application import Application, ApplicationStatus
from app.models.resume import Resume
from app.models.ai_match import AIMatch  # 👈 IMPORTANT


__all__ = ["User", "Application", "ApplicationStatus", "Resume"]
#python -c "from app.models import User, Application, Resume; print('✅ Models imported successfully!')"