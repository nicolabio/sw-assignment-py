from typing import Iterable, Tuple

import minio
import pytest

from sw_assignment.storage import (
    FileInfo,
    NoSuchBucket,
    NotFoundError,
    StorageReader,
)
from tests.helpers import uuid4, write_same_data_to_files


@pytest.fixture
def storage_reader(minio_client: minio.Minio, bucket_name: str) -> StorageReader:
    return StorageReader(minio_client, bucket_name)


@pytest.fixture
def write_dummy_data_to_bucket(minio_client: minio.Minio, bucket_name: str) -> Tuple[int, int, str]:
    """Write files to the bucket with a random prefix.

    Returns:
        int: The number of files written.
        int: Length of each file.
        str: Prefix of each file.
    """
    # num_files is an arbitrary number of files to write.
    # It's worth keeping the number of files small to keep the test fast.
    num_files = 3
    prefix = uuid4()
    data = b"dummy data"
    out_file_names = [f"{prefix}/{i}.txt" for i in range(num_files)]

    write_same_data_to_files(minio_client, bucket_name, data, out_file_names)
    return num_files, len(data), prefix


class TestStorageReader:

    def test_storage_reader__raises_exception_if_bucket_not_exist(self, minio_client: minio.Minio) -> None:
        with pytest.raises(NoSuchBucket):
            StorageReader(minio_client, "none-existing-bucket")

    def test_iter_file_infos__happy_flow(
            self,
            storage_reader: StorageReader,
            write_dummy_data_to_bucket: Tuple[int, int, str],
    ) -> None:
        # Init bucket with dummy data.
        num_files, len_data, prefix = write_dummy_data_to_bucket

        # Create iterator.
        file_infos = storage_reader.iter_file_infos(prefix)

        # Iterate of iterator and verify all properties.
        self.verify_file_infos(file_infos, num_files, len_data, prefix)

    def test_list_file_infos__happy_flow(
            self,
            storage_reader: StorageReader,
            write_dummy_data_to_bucket: Tuple[int, int, str],
    ) -> None:
        # Init bucket with dummy data.
        num_files, len_data, prefix = write_dummy_data_to_bucket

        # No min or max files specified, we expect all files.
        file_infos = storage_reader.list_file_infos(prefix)
        self.verify_file_infos(file_infos, num_files, len_data, prefix)

        # Specify max files more than there are, we expect all files.
        file_infos = storage_reader.list_file_infos(prefix, min_files=2, max_files=4)
        self.verify_file_infos(file_infos, num_files, len_data, prefix)

        # Specify max files less than there are, we expect not all files.
        file_infos = storage_reader.list_file_infos(prefix, min_files=1, max_files=2)
        self.verify_file_infos(file_infos, 2, len_data, prefix)

    def test_list_file_infos__raises_not_found_error_if_not_min_files(
            self,
            storage_reader: StorageReader,
            write_dummy_data_to_bucket: Tuple[int, int, str],
    ) -> None:
        # Init bucket with dummy data.
        num_files, len_data, prefix = write_dummy_data_to_bucket

        with pytest.raises(NotFoundError):
            storage_reader.list_file_infos(prefix, min_files=1002)

    @staticmethod
    def verify_file_infos(
            file_infos: Iterable[FileInfo],
            expected_file_count: int,
            expected_size: int,
            expected_prefix: str,
    ) -> None:
        """Verify: type, prefix, size and number of files."""
        files_count = 0
        for fi in file_infos:
            assert isinstance(fi, FileInfo)
            assert fi.path.startswith(expected_prefix)
            assert fi.size == expected_size
            files_count += 1
        assert files_count == expected_file_count
