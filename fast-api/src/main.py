from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from modules.user.routes import router as user_router
from modules.user.templates_routes import router as user_templates_router
from modules.health_check import router as health_check_router

app = FastAPI()
app.include_router(user_templates_router, tags=["user_templates"])
app.include_router(user_router, prefix="/api", tags=["users"])
app.include_router(health_check_router, tags=["health"])

app.mount("/static", StaticFiles(directory="public"), name="public")

host = '0.0.0.0'
port = 8010
print(f'Swagger running on http://{host}:{port}/docs')

@app.get("/")
async def main():
    return {"main": True}

