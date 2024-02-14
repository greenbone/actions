# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: AGPL-3.0-or-later

"""
This module provides models representing various components
of the Open Container Initiative specifications.
"""

# pylint: disable=too-few-public-methods

from datetime import datetime
from typing import Callable, Optional

from pydantic import BaseModel, Field


def exclude_undefined_keys(cls) -> Callable:
    """
    A decorator to exclude undefined keys from keyword arguments
    passed to the constructor of a Pydantic model.

    Args:
        cls: The Pydantic model class.

    Returns:
        Callable: The wrapper function.
    """

    def wrapper(**kwargs):
        model_fields = {v.alias for v in cls.__fields__.values()} | set(
            cls.__fields__.keys()
        )
        filtered_kwargs = {k: v for k, v in kwargs.items() if k in model_fields}
        return cls(**filtered_kwargs)

    return wrapper


@exclude_undefined_keys
class OciAnnotations(BaseModel):
    """
    Model representing standardized OCI image annotations.

    Args:
        created: The creation datetime of the image.
        url: The URL of the image.
        source: The source of the image.
        authors: Authors of the image.
        documentation: Documentation URL of the image.
        version: Version of the image.
        revision: Revision of the image.
        vendor: Vendor of the image.
        licenses: Licenses of the image.
        ref_name: Reference name of the image.
        title: Title of the image.
        description: Description of the image.
    """

    created: datetime = Field(..., alias="org.opencontainers.image.created")
    url: str = Field(..., alias="org.opencontainers.image.url")
    source: str = Field(..., alias="org.opencontainers.image.source")
    authors: Optional[str] = Field(
        default=None, alias="org.opencontainers.image.authors"
    )
    documentation: Optional[str] = Field(
        default=None, alias="org.opencontainers.image.documentation"
    )
    version: Optional[str] = Field(
        default=None, alias="org.opencontainers.image.version"
    )
    revision: Optional[str] = Field(
        default=None, alias="org.opencontainers.image.revision"
    )
    vendor: Optional[str] = Field(
        default=None, alias="org.opencontainers.image.vendor"
    )
    licenses: Optional[str] = Field(
        default=None, alias="org.opencontainers.image.licenses"
    )
    ref_name: Optional[str] = Field(
        default=None, alias="org.opencontainers.image.ref_name"
    )
    title: Optional[str] = Field(
        default=None, alias="org.opencontainers.image.title"
    )
    description: Optional[str] = Field(
        default=None, alias="org.opencontainers.image.description"
    )


class OciImageTags(BaseModel):
    """
    Model representing OCI image tags.

    Args:
        name: The name of the image.
        tags: The list of tags associated with the image.
    """

    name: str
    tags: list[str]


class OciPlatform(BaseModel):
    """
    Model representing OCI platform information.

    Args:
        architecture: The architecture of the platform.
        os: The operating system of the platform.
    """

    architecture: str
    os: str


class OciManifest(BaseModel):
    """
    Model representing OCI manifest.

    Info:
        The OciAnnotations model is not utilized for 'annotations' because
        custom annotations are allowed, while this model is specifically
        designed to parse only standard ones.

    Args:
        mediaType: The media type of the manifest.
        digest: The digest of the image.
        size: The size of the image.
        annotations: Annotations associated with the manifest.
        platform: Platform information associated with the manifest.
    """

    mediaType: str
    digest: str
    size: int
    annotations: Optional[dict[str, str]] = None
    platform: Optional[OciPlatform] = None


class OciIndex(BaseModel):
    """
    Model representing OCI index.

    Args:
        schemaVersion: The schema version of the index.
        mediaType: The media type of the index.
        manifests: List of manifests associated with the index.
    """

    schemaVersion: int
    mediaType: str
    manifests: list[OciManifest]
