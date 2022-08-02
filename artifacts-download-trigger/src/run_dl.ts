// ----------------------------------------------------------------------------
// Copyright (c) Greenbone Networks GmbH - Josef Fröhle, 2022
// Licensed under the MIT License.
// ----------------------------------------------------------------------------

import * as core from "@actions/core"
import {download} from "./downloader"

async function run(): Promise<void> {
  try {
    await download()
  } catch (e) {
    if (typeof e === "string") {
      core.setFailed(e.toUpperCase())
    } else if (e instanceof Error) {
      console.log(e.stack)
      core.setFailed(e.message)
    }
  }

}

run()
