from typing import Final


_NICOLAB_REGISTRY: Final[str] = "950466833329.dkr.ecr.eu-central-1.amazonaws.com"

# Supported versions of the services as defined in the README using a doctest.
SUPPORTED_MINIO_IMAGE: Final[str] = f"{_NICOLAB_REGISTRY}/minio:RELEASE.2023-08-23T10-07-06Z"

# Prefix for environment variables.
ENV_PREFIX = "EXTRACTOR_"
