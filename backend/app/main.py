from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi_pagination import add_pagination

from app.api.endpoints import auth, users, courses,learning_paths,personal_schedule,rag
from app.db.base import Base
from app.db.session import engine
from fastapi.middleware.cors import (
    CORSMiddleware,
)


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
Base.metadata.create_all(bind=engine)

app.include_router(auth.router,tags=["Authentication"])
app.include_router(users.router,tags=["Users"])
app.include_router(courses.router,tags=["Courses"])
app.include_router(learning_paths.router, tags=["Learning Paths"])
app.include_router(personal_schedule.router, tags=["Personal Schedule"])
app.include_router(rag.router, tags=["Rag"])

add_pagination(app)