import {download} from "./main-dl";
import {trigger} from "./main";
import {getArgs} from "./utils";
import * as core from "@actions/core";
import {WorkflowRunConclusion} from "./workflow-handler";

async function run(): Promise<void> {
  const args = getArgs();
  try {
    core.debug(`Test DL: ${args.downloadArtifacts ? 'true' : 'false'}`)
    if ((args.downloadArtifacts||args.downloadArtifactsNoTrigger) && !args.forceTrigger) {
      try {
        await download()
      }catch (e) {
        if (!args.downloadArtifactsNoTrigger || args.forceTrigger){
          throw 'next step'
        }
      }
    } else {
      throw 'next step'
    }
  } catch (e) {
    core.setOutput('result', 'success') // Reset Failure if any
    core.setOutput('workflow-conclusion', WorkflowRunConclusion.SUCCESS); // Reset Failure if any
    process.exitCode = 0 // Reset Failure if any
    try {
      await trigger()
      if (args.downloadArtifacts) {
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
