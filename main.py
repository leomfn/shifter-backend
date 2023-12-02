from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from shifts.router import router as shifts_router
from signups.router import router as signups_router
from users.router import router as users_router
from auth.router import router as auth_router

# import crud, models, schemas, helpers, auth
from database import SessionLocal, engine, get_db, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

# TODO: rethink this for prod environment
# https://fastapi.tiangolo.com/tutorial/cors/
origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(shifts_router)
app.include_router(signups_router)
