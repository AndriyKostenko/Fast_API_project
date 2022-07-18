from fastapi import FastAPI
from app.routes import user_routes, quiz_routes
from app.database import Base, engine


app = FastAPI()
app.include_router(user_routes.route)
app.include_router(quiz_routes.route)

Base.metadata.create_all(bind=engine)


