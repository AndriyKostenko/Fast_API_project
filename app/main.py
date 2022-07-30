from fastapi import FastAPI

from app.db.database import Base, engine
from app.routes import user_routes, quiz_routes

app_ = FastAPI()

app_.include_router(user_routes.route)
app_.include_router(quiz_routes.route)

Base.metadata.create_all(bind=engine)



