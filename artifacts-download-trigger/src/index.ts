import {download} from "./main-dl";
import {trigger} from "./main";
import {getArgs} from "./utils";
import * as core from "@actions/core";
import {WorkflowRunConclusion} from "./workflow-handler";

async function run(): Promise<void> {
  core.debug("Test")
  core.setOutput('result1', 'success') // Reset Failure if any
  const dl = getArgs().downloadArtifacts;
  try {
    core.debug(`Test DL: ${dl?'true':'false'}`)
    if (dl) {
    await download()
    } else {
      throw 'next step'
    }
  } catch (e) {
    core.setOutput('result', 'success') // Reset Failure if any
    core.setOutput('workflow-conclusion', WorkflowRunConclusion.SUCCESS);
    process.exitCode = 0 // Reset Failure if any
    try {
      await trigger()
      if (dl) {
        await download()
      }
    } catch (e) {
      if (typeof e === "string") {
        core.setFailed(e.toUpperCase());
      } else if (e instanceof Error) {
        console.log(e.stack)
        core.setFailed(e.message);
      }
    }
  }
}

run()