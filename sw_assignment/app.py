from __future__ import annotations

import minio
from pathlib import Path

from sw_assignment.config import Config, Mode
from sw_assignment.printer import (
    JsonPrinter,
    Printer,
    PrintItem,
    StdOutPrinter,
)
from sw_assignment.storage import StorageReader, NotFoundError


class App:

    def __init__(self, config: Config) -> None:
        self._config = config

        self._printer = self._init_printer()
        self._storage = self._init_storage_reader()

    def _init_storage_reader(self) -> StorageReader:
        minio_client = minio.Minio(
            endpoint=self._config.minio_url,
            access_key=self._config.minio_access_key,
            secret_key=self._config.minio_secret_key.get_secret_value(),
            secure=(not self._config.minio_disable_ssl),
        )
        return StorageReader(minio_client, self._config.minio_bucket)

    def _init_printer(self) -> Printer:
        if self._config.mode == Mode.JSON:
            return JsonPrinter(out_path=self._config.output_path)
        elif self._config.mode == Mode.STDOUT:
            return StdOutPrinter()
        else:
            raise ValueError(f"Unsupported mode: {self._config.mode}")

    def run(self) -> None:
        base_iterator = self._storage.iter_file_infos(
            self._config.prefix,
            self._config.suffix_filter,
        )

        processed_parents = []

        for file_info in base_iterator:

            parent = Path(file_info.path).parent

            if not parent:
                AssertionError(
                    "We were allowed to assume that each files is in a folder",
                )

            if parent.parent:
                AssertionError(
                    "We were allowed to assume there a not nested files.",
                )

            if parent in processed_parents:
                continue

            try:
                # We want at least one txt file. Max files is set to 1 to avoid unnecessary reads.
                txt_files = self._storage.list_file_infos(str(parent), min_files=1, max_files=1, suffix_filter=".txt")
            except NotFoundError:
                continue

            if len(txt_files) <= 1:
                continue

            try:
                # We want at least two dcm files. No max files set to read all dcm files.
                dcm_files = self._storage.list_file_infos(str(parent), min_files=2, suffix_filter=".dcm")
            except NotFoundError:
                continue

            # Combine the txt and dcm files.
            all_files = txt_files + dcm_files

            self._printer.print(
                [PrintItem(f.path, suffix=f.suffix) for f in all_files],
            )

            processed_parents.append(parent)
