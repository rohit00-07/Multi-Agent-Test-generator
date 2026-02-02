from db.database import engine, Base
from db import models

Base.metadata.create_all(bind=engine)
print("✅ Database initialized")