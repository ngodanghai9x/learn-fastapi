from pydantic_settings import BaseSettings
from pydantic import Field, SecretStr, ConfigDict
from pprint import pprint


class EnvSettings(BaseSettings):
    model_config = ConfigDict(
        env_file=".env"
        # ,extra="ignore"
    )

    app_name: str = Field(..., env="APP_NAME")
    debug: bool = Field(False, env="DEBUG")
    secret_key: SecretStr = Field(..., env="SECRET_KEY")


# env = EnvSettings(_env_file=".env")
env = EnvSettings()

pprint(env)
