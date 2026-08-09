from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi_pagination import add_pagination

from app.api.endpoints import auth, users, knowledge_base, courses,learning_paths,personal_schedule,rag
from app.db.base import Base
from app.db.session import engine


app = FastAPI()
Base.metadata.create_all(bind=engine)

app.include_router(auth.router,tags=["Authentication"])
app.include_router(users.router,tags=["Users"])
app.include_router(knowledge_base.router,tags=["Knowledge_Base"])
app.include_router(courses.router,tags=["Courses"])
app.include_router(learning_paths.router, tags=["Learning Paths"])
app.include_router(personal_schedule.router, tags=["Personal Schedule"])
app.include_router(rag.router, tags=["Rag"])

add_pagination(app)