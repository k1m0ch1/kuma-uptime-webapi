import uvicorn
import argparse

from fastapi import FastAPI
from routers import root, tags, status_pages, notifications, monitors

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(redoc_url=None, docs_url=None)
app.include_router(root.router)
app.include_router(tags.router)
app.include_router(status_pages.router)
app.include_router(notifications.router)
app.include_router(monitors.router)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run('main:app', host='0.0.0.0', port=8000, log_level="info", reload=True)