from typing import Any

import minio
import pytest

from sw_assignment.app import App
from sw_assignment.config import Config, Mode
from tests.helpers import write_same_data_to_files


@pytest.fixture
def config(
        minio_url: str,
        bucket_name: str,
        minio_access_key: str,
        minio_secret_key: str,
        out_file: Any,
) -> Config:
    return Config(
        mode=Mode.JSON,
        output_path=out_file.name,
        debug=False,
        minio_url=minio_url,
        minio_bucket=bucket_name,
        minio_access_key=minio_access_key,
        minio_secret_key=minio_secret_key,
        minio_disable_ssl=True,
    )


class TestApp:

    def test_run(
            self,
            minio_client: minio.Minio,
            out_file: Any,
            config: Config,
    ) -> None:
        # Seed the bucket with some files.
        write_same_data_to_files(
            minio_client=minio_client,
            bucket_name=config.minio_bucket,
            data=b"dummy",
            file_names_to_write=[
                "file1",
                "file2",
                "file3",
            ],
        )

        # Run the app.
        App(config).run()

        # Validate the output.
        assert out_file.readline() == \
            """[{"path": "file1"}, {"path": "file2"}, {"path": "file3"}]"""
