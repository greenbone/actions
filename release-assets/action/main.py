# SPDX-FileCopyrightText: 2025 Greenbone AG
#
# SPDX-License-Identifier: AGPL-3.0-or-later

"""
Main module manage release assets for a GitHub repository release tag.
"""

import asyncio
import sys
from argparse import Namespace
from enum import IntEnum, auto

import httpx
from pontos.github.api import GitHubAsyncRESTApi

from action.args import parse_args


class ReleaseAssetReturnValue(IntEnum):
    """
    Enumeration of possible return values for a release asset operation.

    Attributes:
        SUCCESS: The operation completed successfully.
        NO_RELEASE: No release was found to attach the asset to.
        NO_MODE: No supported mode was found.
        UPLOAD_ASSET_ERROR: An error occurred during asset upload.
    """

    SUCCESS = 0
    NO_RELEASE = auto()
    NO_MODE = auto()
    UPLOAD_ASSET_ERROR = auto()


async def upload(arg: Namespace):
    """
    Uploads release assets to a GitHub repository for a specified release tag.

    Args:
        arg: A namespace object containing:
            - token: GitHub personal access token.
            - repository: The full repository name (e.g., "owner/repo").
            - tag: The release tag to upload assets to.
            - files: List of file paths (Path object) to upload as assets.

    Returns:
        ReleaseAssetReturnValue: An enum indicating the result of the operation.
            - SUCCESS: All assets were uploaded successfully.
            - NO_RELEASE: The specified tag was not found in the repository.
            - UPLOAD_ASSET_ERROR: An error occurred during the upload process.
    """

    async with GitHubAsyncRESTApi(token=arg.token) as github:
        if not await github.releases.exists(arg.repository, arg.tag):
            print(f"Tag {arg.tag} not found in {arg.repository}.")
            return ReleaseAssetReturnValue.NO_RELEASE
        try:
            async for uploaded_file in github.releases.upload_release_assets(
                arg.repository, arg.tag, arg.files
            ):
                print(f"Uploaded file: {uploaded_file}")
        except httpx.HTTPStatusError as e:
            print(f"Failed uploading asset {e}.")
            return ReleaseAssetReturnValue.UPLOAD_ASSET_ERROR
    return ReleaseAssetReturnValue.SUCCESS


def main() -> int:
    """
    Parses command-line arguments and dispatches to the appropriate handler
    based on the selected mode. Currently supports only the 'upload' mode,
    which uploads release assets to a GitHub repository.

    Returns:
        int: An integer status code representing the outcome of the operation.
    """

    arg = parse_args()

    if arg.mode == "upload":
        return asyncio.run(upload(arg))

    return ReleaseAssetReturnValue.NO_MODE


if __name__ == "__main__":
    sys.exit(main())
