from __future__ import annotations

from enum import IntEnum

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from sw_assignment.constants import ENV_PREFIX


class Mode(IntEnum):
    JSON = 1
    STDOUT = 2


class Config(BaseSettings):

    # Meta for generating Config from environment variables.
    model_config = SettingsConfigDict(env_prefix=ENV_PREFIX)

    # Debug mode.
    debug: bool = Field(default=False)

    # Mode of the output.
    mode: Mode = Field(default=Mode.STDOUT)

    # Output path.
    #
    # Only used when mode is JSON.
    output_path: str = Field(default="out.json")

    # Minio config
    minio_url: str = Field(min_length=1)
    minio_bucket: str = Field(min_length=1)
    minio_access_key: str = Field(min_length=1)
    minio_secret_key: SecretStr = Field(min_length=1)
    minio_disable_ssl: bool
