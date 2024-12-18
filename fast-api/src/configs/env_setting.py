from pydantic_settings import BaseSettings
from pydantic import Field, SecretStr, ConfigDict
from pprint import pprint


class EnvSettings(BaseSettings):
    model_config = ConfigDict(
        env_file=".env"
        # ,extra="ignore"
    )

    APP_NAME: str = Field(..., env="APP_NAME")
    DEBUG: bool = Field(False, env="DEBUG")

    DB_HOST: str = Field('0.0.0.0', env="DB_HOST")
    DB_PORT: int = Field(5432, env="DB_PORT")
    DB_NAME: str = Field('postgres', env="DB_NAME")
    DB_USER: str = Field('postgres', env="DB_USER")
    DB_PASSWORD: SecretStr = Field(..., env="DB_PASSWORD")


# env = EnvSettings(_env_file=".env")
env = EnvSettings()

pprint(env)
