from fastapi import FastAPI

from order_app.infrastructure.persistence.sqlite.init_db import init_db
from order_app.infrastructure.web.fastapi.routes.user import router as user_router


def create_web_app(testing: bool = False):
    app = FastAPI(title="Order Management App", version="0.1.0")

    if testing:
        app.testing = True
    else:
        init_db()
    app.include_router(user_router, prefix="/users", tags=["Users"])
    return app
