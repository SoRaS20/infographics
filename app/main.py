from fastapi import FastAPI

from app.routers import auth, uploads, templates, generate

app = FastAPI()

app.include_router(auth.router)
app.include_router(uploads.router)
app.include_router(templates.router)
app.include_router(generate.router)