from pathlib import Path
from sys import prefix

import minio
import pytest

from sw_assignment.storage import (
    FileInfo,
    NoSuchBucket,
    NotFoundError,
    StorageReader,
)
from tests.helpers import write_data_to_files


@pytest.fixture
def storage_reader(minio_client: minio.Minio, bucket_name: str) -> StorageReader:
    return StorageReader(minio_client, bucket_name)


class TestStorageReader:

    def test_storage_reader__raises_exception_if_bucket_not_exist(self, minio_client: minio.Minio) -> None:
        with pytest.raises(NoSuchBucket):
            StorageReader(minio_client, "none-existing-bucket")

    @pytest.mark.parametrize(
        "prefix", ["", "prefix/"],
    )
    def test_iter_file_infos__happy_flow(
            self,
            storage_reader: StorageReader,
            minio_client: minio.Minio,
            bucket_name: str,
            data: bytes,
            prefix: str,
    ) -> None:
        # Seed the bucket.
        files_to_write = [
            f"{prefix}file1.txt",
            f"{prefix}file2.dcm",
            f"{prefix}file3.dcm",
        ]
        write_data_to_files(minio_client, bucket_name, data, files_to_write)
        file_infos = [FileInfo(path=f, size=len(data), suffix=Path(f).suffix) for f in files_to_write]

        # Create iterator.
        iterator = storage_reader.iter_file_infos(prefix=prefix)
        # Read the iterator.
        got = [file_info for file_info in iterator]

        want = file_infos
        assert got == want

    @pytest.mark.parametrize(
        "prefix", ["", "prefix/"],
    )
    def test_iter_file_infos__with_suffix_filter(
            self,
            storage_reader: StorageReader,
            minio_client: minio.Minio,
            bucket_name: str,
            data: bytes,
            prefix: str,
    ) -> None:
        # Seed the bucket.
        files_to_write = [
            f"{prefix}file1.txt",
            f"{prefix}file2.dcm",
            f"{prefix}file3.dcm",
        ]
        write_data_to_files(minio_client, bucket_name, data, files_to_write)
        file_infos = [FileInfo(path=f, size=len(data), suffix=Path(f).suffix) for f in files_to_write]

        # Create iterator.
        iterator = storage_reader.iter_file_infos(prefix=prefix, suffix_filter=".dcm")
        # Read the iterator.
        got = [file_info for file_info in iterator]

        # We expect only the files with suffix .dcm. So not the
        # first file (index 0).
        want = file_infos[1:]
        assert got == want

    @pytest.mark.parametrize(
        "prefix", ["", "prefix/"],
    )
    def test_list_file_infos__happy_flow(
            self,
            storage_reader: StorageReader,
            minio_client: minio.Minio,
            bucket_name: str,
            data: bytes,
            prefix: str,
    ) -> None:
        # Seed the bucket.
        files_to_write = [
            f"{prefix}file1.txt",
            f"{prefix}file2.dcm",
            f"{prefix}file3.dcm",
        ]
        write_data_to_files(minio_client, bucket_name, data, files_to_write)
        file_infos = [FileInfo(path=f, size=len(data), suffix=Path(f).suffix) for f in files_to_write]

        # No min or max files specified, we expect all files.
        got = storage_reader.list_file_infos(prefix=prefix)
        want = file_infos   # We expect all.
        assert got == want

        # Specify max files more than there are, we expect all files.
        got = storage_reader.list_file_infos(prefix=prefix, min_files=2, max_files=4)
        want = file_infos  # We expect all.
        assert got == want

        # Specify max files less than there are, we expect not all files.
        got = storage_reader.list_file_infos(prefix=prefix, min_files=1, max_files=2)
        want = file_infos[:2]  # We expect only the first two.
        assert got == want[:2]

    @pytest.mark.parametrize(
        "prefix", ["", "prefix/"],
    )
    def test_list_file_infos__with_suffix_filter(
            self,
            storage_reader: StorageReader,
            minio_client: minio.Minio,
            bucket_name: str,
            data: bytes,
            prefix: str,
    ) -> None:
        # Seed the bucket.
        files_to_write = [
            f"{prefix}file1.txt",
            f"{prefix}file2.dcm",
            f"{prefix}file3.dcm",
        ]
        write_data_to_files(minio_client, bucket_name, data, files_to_write)
        file_infos = [FileInfo(path=f, size=len(data), suffix=Path(f).suffix) for f in files_to_write]

        # No min or max files specified. Suffix filter on .dcm.
        # We expect the last two files.
        got = storage_reader.list_file_infos(prefix=prefix, suffix_filter=".dcm")
        want = file_infos[1:]   # We expect the last two.
        assert got == want

        # Specify max files more than there are. Suffix filter on dcm.
        # We expect the last two files.
        got = storage_reader.list_file_infos(prefix=prefix, min_files=2, max_files=4, suffix_filter=".dcm")
        want = file_infos[1:]   # We expect the last two.
        assert got == want

        # Specify max files less than there are. Suffix filter on .dcm.
        # We only expect the second file.
        got = storage_reader.list_file_infos(prefix=prefix, min_files=1, max_files=1, suffix_filter=".dcm")
        want = [file_infos[1]]  # We expect only the second file.
        assert got == want

    def test_list_file_infos__raises_not_found_error_if_not_min_files(
            self,
            storage_reader: StorageReader,
            minio_client: minio.Minio,
            bucket_name: str,
    ) -> None:
        # Seed the bucket.
        files_to_write = [
            "file1.txt",
        ]
        write_data_to_files(minio_client, bucket_name, b"dummy", files_to_write)

        with pytest.raises(NotFoundError):
            storage_reader.list_file_infos(prefix, min_files=1002)
