from app.core.database import engine, Base
from app.models import User, Application, Resume

print("=" * 50)
print("JobTrackAI Database Initialization")
print("=" * 50)

try:
    print("\n1. Importing models...")
    print(f"   ✓ User model: {User.__tablename__}")
    print(f"   ✓ Application model: {Application.__tablename__}")
    print(f"   ✓ Resume model: {Resume.__tablename__}")
    
    print("\n2. Creating database tables...")
    Base.metadata.create_all(bind=engine)
    
    print("\n3. Verifying tables were created...")
    from sqlalchemy import inspect
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    
    if tables:
        print(f"   ✓ Tables created successfully!")
        for table in tables:
            print(f"     - {table}")
    else:
        print("   ✗ No tables found!")
    
    print("\n4. Testing database connection...")
    from app.core.database import SessionLocal
    db = SessionLocal()
    result = db.execute("SELECT current_database(), current_user")
    row = result.fetchone()
    print(f"   ✓ Connected to database: {row[0]}")
    print(f"   ✓ Connected as user: {row[1]}")
    db.close()
    
    print("\n" + "=" * 50)
    print("✅ Database initialization completed successfully!")
    print("=" * 50)
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\nTroubleshooting tips:")
    print("1. Check if PostgreSQL is running: sudo systemctl status postgresql")
    print("2. Verify database credentials in .env file")
    print("3. Make sure database 'jobtrack' exists")
