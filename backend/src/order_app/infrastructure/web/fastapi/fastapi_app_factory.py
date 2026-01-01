from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from order_app.infrastructure.persistence.sqlite.db import get_connection
from order_app.infrastructure.persistence.sqlite.init_db import init_db
from order_app.infrastructure.web.fastapi.routes.user import router as user_router


def create_web_app(testing: bool = False):
    app = FastAPI(title="Order Management App", version="0.1.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    if testing:
        app.testing = True
    else:
        conn = get_connection()
        init_db(conn=conn)
        conn.close()
    app.include_router(user_router, prefix="/users", tags=["Users"])
    return app
