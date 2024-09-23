from __future__ import annotations

import minio

from sw_assignment.config import Config, Mode
from sw_assignment.printer import (
    JsonPrinter,
    Printer,
    PrintItem,
    StdOutPrinter,
)
from sw_assignment.storage import StorageReader


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
        iterator = self._storage.iter_file_infos(self._config.prefix)
        self._printer.print(
            [PrintItem(f.path) for f in iterator],
        )
