from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware

from application.api.categories import categories_router
from application.api.users import users_router
from application.api.locations import locations_router
from application.api.posts import posts_router
from application.api.auth import router as auth_router

def create_app() -> FastAPI:
    app = FastAPI(root_path="/api/v1", debug=True)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.mount("/images", StaticFiles(directory="/yandex-project/images"),name="images")
    app.include_router(categories_router, prefix="/categories", tags=["Categories"])
    app.include_router(users_router, prefix="/users", tags=["Users"])
    app.include_router(locations_router, prefix="/locations", tags=["Locations"])
    app.include_router(posts_router,prefix="/posts", tags=["Posts"])
    app.include_router(auth_router, tags=["Auth APIs"])
    return app
