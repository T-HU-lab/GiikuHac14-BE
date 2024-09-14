from fastapi import FastAPI

from api.routers import stall, user, review, item, auth

app = FastAPI()
app.include_router(stall.router)
app.include_router(user.router)
app.include_router(review.router)
app.include_router(item.router)
app.include_router(auth.router)
