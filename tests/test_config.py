from __future__ import annotations

import pytest
from pydantic import ValidationError

from sw_assignment.config import Config
from sw_assignment.constants import ENV_PREFIX


@pytest.fixture
def config_environment_variables() -> dict[str, str]:
    return {
        ENV_PREFIX + "DEBUG": "true",

        ENV_PREFIX + "MODE": "1",
        ENV_PREFIX + "OUTPUT_PATH": "out.json",
        ENV_PREFIX + "PREFIX": "my_prefix",

        ENV_PREFIX + "SUFFIX_FILTER": ".dcm",

        # Minio config
        ENV_PREFIX + "MINIO_URL": "localhost:9000",
        ENV_PREFIX + "MINIO_BUCKET": "nicolab",
        ENV_PREFIX + "MINIO_ACCESS_KEY": "peter",
        ENV_PREFIX + "MINIO_SECRET_KEY": "griffin",
        ENV_PREFIX + "MINIO_DISABLE_SSL": "true",
    }


@pytest.fixture
def empty_config_environment_variables() -> dict[str, str]:
    return {
        ENV_PREFIX + "DEBUG": "",

        # Minio config
        ENV_PREFIX + "MINIO_URL": "",
        ENV_PREFIX + "MINIO_BUCKET": "",
        ENV_PREFIX + "MINIO_ACCESS_KEY": "",
        ENV_PREFIX + "MINIO_SECRET_KEY": "",
        ENV_PREFIX + "MINIO_DISABLE_SSL": "",
    }


def test_config_valid(
    config_environment_variables: dict[str, str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:

    for k, v in config_environment_variables.items():
        monkeypatch.setenv(k, v)

    # Loading configuration from environment variables.
    c = Config()

    # Asserting the configuration.
    assert_valid_config(c)


def test_config_invalid(
        config_environment_variables: dict[str, str],
        monkeypatch: pytest.MonkeyPatch,
) -> None:

    # Removing a required key.
    del config_environment_variables[ENV_PREFIX + "MINIO_BUCKET"]

    for k, v in config_environment_variables.items():
        monkeypatch.setenv(k, v)

    # Loading configuration should raise a ValueError.
    with pytest.raises(ValidationError, match="Field required"):
        Config()


def test_config_empty(
        empty_config_environment_variables: dict[str, str],
        monkeypatch: pytest.MonkeyPatch,
) -> None:

    # Setting all values to empty.
    for k, v in empty_config_environment_variables.items():
        monkeypatch.setenv(k, v)

    # Loading configuration should raise a ValueError.
    with pytest.raises(ValidationError, match=r"Field required|Input should be"):
        Config()


def assert_valid_config(c: Config) -> None:
    assert c.debug
    assert c.mode == 1
    assert c.output_path == "out.json"
    assert c.prefix == "my_prefix"

    assert c.suffix_filter == ".dcm"

    # Minio config
    assert c.minio_url == "localhost:9000"
    assert c.minio_bucket == "nicolab"
    assert c.minio_access_key == "peter"
    assert c.minio_secret_key.get_secret_value() == "griffin"
    assert c.minio_disable_ssl
