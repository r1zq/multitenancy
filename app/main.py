from fastapi import FastAPI
from app.api.endpoints import auth, users
from app.db.base import Base
from app.db.session import engine

app = FastAPI()

# Include routers
app.include_router(auth.router)
app.include_router(users.router)

# Create tables
Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)