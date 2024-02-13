# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: AGPL-3.0-or-later

"""
Module for interacting with OCI (Open Container Initiative) registries.
"""

from enum import Enum

import httpx
from pydantic import ValidationError
from .oci_model import OciAnnotations, OciImageTags, OciIndex


class OciMediaTypes(Enum):
    """
    Enumeration of different media types for OCI registries.

    Attributes:
        DOCKER_MANIFEST_V2_JSON (str): Media type for Docker manifest v2.
        DOCKER_MANIFEST_LIST_V2_JSON (str): Media type for Docker manifest list v2.
        OCI_MANIFEST_V1_JSON (str): Media type for OCI image manifest v1.
        OCI_IMAGE_INDEX_V1_JSON (str): Media type for OCI image index v1.
        JSON (str): Media type for JSON.
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
            user (str): User for authentication.
            password (str): Password for authentication.
            timeout (int): Timeout in seconds for HTTP requests (default is 10).
            reg_domain (str): Domain of the registry (default is 'registry-1.docker.io').
            reg_auth_domain (str): Domain for authentication (default is 'auth.docker.io').
            reg_auth_service (str): Authentication service (default is 'registry.docker.io').
            namespace (str): Namespace within the registry (default is 'library').
        """
        # pylint: disable=too-many-arguments

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

    def _get_data_as_dict(self, url: str) -> dict:
        res = self.get(url)
        res.raise_for_status()
        return res.json()

    def _get_token(self, repository) -> None:
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
            repository (str): Name of the repository.

        Returns:
            OciImageTags: Object containing image tags.
        """

        self._get_token(repository)
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
            repository (str): Name of the repository.
            tag (str): Tag of the image.

        Returns:
            OciManifestIndex: Object containing image manifests.
        """

        self._get_token(repository)
        url = f"/v2/{self.namespace}/{repository}/manifests/{tag}"
        return OciIndex(**self._get_data_as_dict(url))

    def get_oci_annotations(
        self, repository: str, tag: str, architecture: str
    ) -> OciAnnotations:
        """
        Retrieve OCI annotations for a given repository, tag, and architecture.

        Args:
            repository (str): Name of the repository.
            tag (str): Tag of the image.
            architecture (str): Architecture of the platform.

        Returns:
            Optional[OciAnnotations]: Object containing OCI annotations if found, else None.
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
