from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.base import router as base_router
from api.categories import categories_router
from api.users import router as users_router
from api.locations import locations_router
from api.posts import router as posts_router


def create_app() -> FastAPI:
    app = FastAPI(root_path="/api/v1", debug=True)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(base_router, prefix="/base")
    app.include_router(categories_router, prefix="/categories")
    app.include_router(users_router, prefix="/users")
    app.include_router(locations_router, prefix="/locations")
    app.include_router(posts_router,prefix="/posts")
    return app
