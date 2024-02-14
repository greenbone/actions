# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: AGPL-3.0-or-later

"""
Module for interacting with OCI (Open Container Initiative) registries.
"""

from enum import Enum
from typing import Any

import httpx
from pydantic import ValidationError
from .oci_model import OciAnnotations, OciImageTags, OciIndex


class OciMediaTypes(Enum):
    """
    Enumeration of different media types for OCI registries.

    Attributes:
        DOCKER_MANIFEST_V2_JSON: Media type for Docker manifest v2.
        DOCKER_MANIFEST_LIST_V2_JSON: Media type for Docker manifest list v2.
        OCI_MANIFEST_V1_JSON: Media type for OCI image manifest v1.
        OCI_IMAGE_INDEX_V1_JSON: Media type for OCI image index v1.
        JSON: Media type for JSON.
    """

    DOCKER_MANIFEST_V2_JSON = (
        "application/vnd.docker.distribution.manifest.v2+json"
    )
    DOCKER_MANIFEST_LIST_V2_JSON = (
        "application/vnd.docker.distribution.manifest.list.v2+json"
    )
    OCI_MANIFEST_V1_JSON = "application/vnd.oci.image.manifest.v1+json"
    OCI_IMAGE_INDEX_V1_JSON = "application/vnd.oci.image.index.v1+json"
    JSON = "application/json"


class OciError(Exception):
    """Oci class base exception"""


class OciAnnotationsError(OciError):
    """OciAnnotationsError exception"""


class Oci(httpx.Client):
    """Class for interacting with OCI (Open Container Initiative) registries."""

    def __init__(
        self,
        user: str = "",
        password: str = "",
        timeout: int = 10,
        reg_domain: str = "registry-1.docker.io",
        reg_auth_domain: str = "auth.docker.io",
        reg_auth_service: str = "registry.docker.io",
        namespace: str = "library",
    ):
        """
        Initialize an instance of the Oci class.

        Args:
            user: User for authentication.
            password: Password for authentication.
            timeout: Timeout in seconds for HTTP requests (default is 10).
            reg_domain: Domain of the registry (default is 'registry-1.docker.io').
            reg_auth_domain: Domain for authentication (default is 'auth.docker.io').
            reg_auth_service: Authentication service (default is 'registry.docker.io').
            namespace: Namespace within the registry (default is 'library').
        """

        super().__init__(
            base_url=f"https://{reg_domain}",
            timeout=timeout,
            auth=(user, password) if user else None,
            headers={"accept": ",".join([h.value for h in OciMediaTypes])},
        )
        self.reg_domain = reg_domain
        self.reg_auth_domain = reg_auth_domain
        self.reg_auth_service = reg_auth_service
        self.namespace = namespace

    def _get_data_as_dict(self, url: str) -> dict[str, Any]:
        res = self.get(url)
        res.raise_for_status()
        return res.json()

    def _set_auth_token(self, repository) -> None:
        res = self.get(
            f"https://{self.reg_auth_domain}/token?service={self.reg_auth_service}"
            f"&scope=repository:{self.namespace}/{repository}:pull"
        )
        res.raise_for_status()
        self.headers["authorization"] = f"Bearer {res.json()['token']}"

    def get_tags(
        self,
        repository: str,
    ) -> OciImageTags:
        """
        Retrieve tags for a given repository.

        Args:
            repository: Name of the repository.

        Returns:
            Object containing image tags.
        """

        self._set_auth_token(repository)
        url = f"/v2/{self.namespace}/{repository}/tags/list"
        return OciImageTags(**self._get_data_as_dict(url))

    def get_manifests(
        self,
        repository: str,
        tag: str,
    ) -> OciIndex:
        """
        Retrieve manifests for a given repository and tag.

        Args:
            repository: Name of the repository.
            tag: Tag of the image.

        Returns:
            Object containing image manifests.
        """

        self._set_auth_token(repository)
        url = f"/v2/{self.namespace}/{repository}/manifests/{tag}"
        return OciIndex(**self._get_data_as_dict(url))

    def get_oci_annotations(
        self, repository: str, tag: str, architecture: str
    ) -> OciAnnotations:
        """
        Retrieve OCI annotations for a given repository, tag, and architecture.

        Args:
            repository: Name of the repository.
            tag: Tag of the image.
            architecture: Architecture of the platform.

        Returns:
            Object containing OCI annotations if found,
            otherwise an OciAnnotationsError is raised.
        """

        for manifest in self.get_manifests(repository, tag).manifests:
            if (
                manifest.annotations
                and manifest.mediaType
                == OciMediaTypes.OCI_MANIFEST_V1_JSON.value
                and manifest.platform
                and manifest.platform.architecture == architecture
            ):
                try:
                    return OciAnnotations(**manifest.annotations)
                except ValidationError as exc:
                    raise OciAnnotationsError(
                        f"Failed to get OCI annotations from repository {repository} on tag {tag}."
                    ) from exc
        raise OciAnnotationsError(
            f"No OCI annotations exist in repository {repository} on tag {tag}."
        )
