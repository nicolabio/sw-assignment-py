import logging
import sys
from typing import NoReturn, TextIO

from sw_assignment.app import App
from sw_assignment.config import Config


def _main(stream: TextIO) -> None:
    config = Config()

    log_level = logging.DEBUG if config.debug else logging.INFO
    logging.basicConfig(
        stream=stream,
        level=log_level,
        format="%(asctime)s %(levelname)-8s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    app = App(config)
    app.run()


def _entrypoint() -> NoReturn:
    try:
        _main(stream=sys.stdout)
    except SystemExit as exc:
        sys.exit(exc.code)
    sys.exit(0)


_entrypoint()
