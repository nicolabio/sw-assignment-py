from __future__ import annotations

import io
import uuid

import minio


def uuid4() -> str:
    return uuid.uuid4().hex


def write_same_data_to_files(
        minio_client: minio.Minio,
        bucket_name: str,
        data: bytes,
        file_names_to_write: list[str],
) -> None:
    """Write the provided to all files in file_names_to_write."""
    for file_name in file_names_to_write:
        minio_client.put_object(
            bucket_name=bucket_name,
            object_name=file_name,
            data=io.BytesIO(data),
            length=len(data),
            content_type="text/plain",
        )
