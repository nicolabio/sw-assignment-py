import dataclasses
from typing import Iterator, Optional

import minio


@dataclasses.dataclass
class FileInfo:
    path: str
    size: int


class StorageReader:

    def __init__(self, minio_client: minio.Minio, bucket_name: str):
        self._minio_client = minio_client
        self._bucket_name = bucket_name

        if not self._minio_client.bucket_exists(bucket_name):
            raise NoSuchBucket(
                f"Bucket with bucket_name {bucket_name} does not exists.",
            )

    def list_file_infos(
            self,
            prefix: str,
            min_files: Optional[int] = None,
            max_files: Optional[int] = None,
    ) -> list[FileInfo]:
        """Perform list_object call, iterate over all results and return results
         as FileInfo object.

        Raises:
            RetryableError: if we consider the error retryable. This is
                different from the default Minio retryable errors. See:
                RetryableError
            NotFoundError: if less the min_files are present.
        """
        result: list[FileInfo] = []
        try:
            iterator = self.iter_file_infos(prefix)
            while True:
                if max_files and len(result) == max_files:
                    return result
                result.append(next(iterator))
        except StopIteration:
            if min_files and len(result) < min_files:
                raise NotFoundError(f"Not found the minimum of {min_files} min_files.")
        return result

    def iter_file_infos(self, prefix: str) -> Iterator[FileInfo]:
        """Perform list_object call and return results as FileInfo object.

        Raises:
            RetryableError: if we consider the error retryable. This is
                different from the default Minio retryable errors. See:
                RetryableError
        """
        iterator = self._minio_client.list_objects(
            self._bucket_name,
            prefix=prefix,
            recursive=True,
        )
        for obj in iterator:
            yield FileInfo(path=obj.object_name, size=obj.size)


class NotFoundError(Exception):
    """Raised when a file or series is not found."""


class NoSuchBucket(Exception):
    """Raised when a bucket is not found."""
