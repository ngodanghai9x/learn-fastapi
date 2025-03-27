import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.common.types import CustomORJSONResponse
from src.common.middlewares import add_process_time_header
from src.configs.env_setting import env

from src.modules.user.routes import router as user_router
from src.modules.user.templates_routes import router as user_templates_router
from src.modules.health_check import router as health_check_router
from src.modules.sample import router as sample_router

app = FastAPI(default_response_class=CustomORJSONResponse)

app.include_router(user_templates_router, tags=["user_templates"])
app.include_router(user_router, prefix="/api", tags=["users"])
app.include_router(health_check_router, tags=["health"])
app.include_router(sample_router, tags=["sample_test"])

app.mount("/static", StaticFiles(directory="public"), name="public")

app.middleware("http")(add_process_time_header)


@app.get("/")
async def main():
    return {"main": True}

# if __name__ == "__main__":
#     uvicorn.run("src.main:app", host=env.APP_HOST, port=env.APP_PORT, reload=True)

print(f'Swagger running on http://{env.APP_HOST}:{env.APP_PORT}/docs')
