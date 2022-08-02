// ----------------------------------------------------------------------------
// Copyright (c) Greenbone Networks GmbH - Josef Fröhle, 2022
// Licensed under the MIT License.
// ----------------------------------------------------------------------------

import * as core from "@actions/core"
import {trigger} from "./trigger"
import {download} from "./downloader"
import {getArgs} from "./utils"
import {WorkflowRunConclusion} from "./workflow-handler"

async function run(): Promise<void> {
  const args = getArgs(true)
  try {
    core.debug(`Test DL: ${args.downloadArtifacts ? "true" : "false"}`)
    if ((args.downloadArtifacts || args.downloadArtifactsNoTrigger) && !args.forceTrigger) {
      try {
        await download()
      } catch (e) {
        if (!args.downloadArtifactsNoTrigger || args.forceTrigger) {
          throw "next step"
        }
      }
    } else {
      throw "next step"
    }
  } catch (e) {
    core.info(`Test DL: ${args.downloadArtifacts ? "true" : "false"}`)
    core.setOutput("result", "success") // Reset Failure if any
    core.setOutput("workflow-conclusion", WorkflowRunConclusion.SUCCESS) // Reset Failure if any
    process.exitCode = 0 // Reset Failure if any
    try {

      core.info(`trigger()`)
      await trigger()
      if (args.downloadArtifacts) {
        core.info(`download()`)
        await download()
      }
    } catch (e) {
      if (typeof e === "string") {
        core.setFailed(e.toUpperCase())
      } else if (e instanceof Error) {
        console.log(e.stack)
        core.setFailed(e.message)
      }
    }
  }
}

run()
