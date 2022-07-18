from fastapi import FastAPI
from app.routes import user_routes
from database import Base, engine

app = FastAPI()
app.include_router(user_routes.route)
Base.metadata.create_all(bind=engine)


