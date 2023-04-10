from fastapi import FastAPI
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware
from logging.config import dictConfig

from .config import PROJECT_NAME
from .api import router as api_router
from .database import close_mongo_connection, connect_to_mongo
from .errors import http_error_handler
from .app_logger_conf import log_config

dictConfig(log_config)

app = FastAPI(
    docs_url="/", 
    openapi_url="/openapi.json", 
    redoc_url="/redoc",
    title=PROJECT_NAME
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_event_handler("startup", connect_to_mongo)
app.add_event_handler("shutdown", close_mongo_connection)

app.add_exception_handler(HTTPException, http_error_handler)

app.include_router(api_router, prefix='/v1')