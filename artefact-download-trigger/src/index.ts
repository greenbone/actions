import {download} from "./main-dl";
import {trigger} from "./main";
import * as core from "@actions/core";

async function run(): Promise<void> {
  try {
    await download()
  } catch (e) {
    process.exitCode = 0 // Reset Failure if any
    try {
      await trigger()
      await download()
    } catch (e) {
      if (typeof e === "string") {
        core.setFailed(e.toUpperCase());
      } else if (e instanceof Error) {
        core.setFailed(e.message);
      }
    }
  }
}

run()