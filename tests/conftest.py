from __future__ import annotations

import tempfile
from typing import Any, Generator

import minio
import pytest
import testcontainers.minio

import tests.helpers
from sw_assignment import SUPPORTED_MINIO_IMAGE


@pytest.fixture
def out_file() -> Generator[Any, None, None]:
    with tempfile.NamedTemporaryFile(mode="w+") as temp_file:
        yield temp_file


@pytest.fixture(scope="session")
def bucket_name() -> str:
    return tests.helpers.uuid4()


@pytest.fixture(scope="session")
def minio_access_key() -> str:
    return "minio_access_key"


@pytest.fixture(scope="session")
def minio_secret_key() -> str:
    return "minio_secret_key"


@pytest.fixture(scope="session")
def minio_port() -> int:
    return 9000


@pytest.fixture(scope="session")
def minio_container(
        minio_access_key: str,
        minio_secret_key: str,
        minio_port: int,
        bucket_name: str,
) -> Generator[testcontainers.minio.MinioContainer, None, None]:
    container = testcontainers.minio.MinioContainer(
        image=SUPPORTED_MINIO_IMAGE,
        port=minio_port,
        access_key=minio_access_key,
        secret_key=minio_secret_key,
    )
    with container as m:
        # MinioContainer performs its own healthcheck
        client = m.get_client()
        client.make_bucket(bucket_name)
        yield m


@pytest.fixture
def minio_url(minio_container: testcontainers.minio.MinioContainer, minio_port: int) -> str:
    return f"{minio_container.get_container_host_ip()}:{minio_container.get_exposed_port(minio_port)}"


@pytest.fixture
def minio_client(minio_container: testcontainers.minio.MinioContainer) -> minio.Minio:
    return minio_container.get_client()


@pytest.fixture
def broken_minio_client() -> minio.Minio:
    """Minio client with some random port s.t. connections always fail. """
    return minio.Minio(endpoint="127.0.0.1:32381")
