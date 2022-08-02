// ----------------------------------------------------------------------------
// Copyright (c) Greenbone Networks GmbH - Josef Fröhle, 2022
// Licensed under the MIT License.
// ----------------------------------------------------------------------------

import {debug} from "./debug"
import * as core from "@actions/core"
import * as github from "@actions/github"

enum TimeUnit {
  S = 1000,
  M = 60 * 1000,
  H = 60 * 60 * 1000
}

function toMilliseconds(timeWithUnit: string): number {
  const unitStr = timeWithUnit.substr(timeWithUnit.length - 1)
  const unit = TimeUnit[unitStr.toUpperCase() as keyof typeof TimeUnit]
  debug("toMilliseconds", {timeWithUnit, unitStr, unit})
  if (!unit) {
    throw new Error("Unknown time unit " + unitStr)
  }
  const time = parseFloat(timeWithUnit)
  return time * unit
}

export function getArgs(dl: boolean) {
  let args: { downloadArtifacts: "" | boolean; pr: number; workflowConclusion: string; inputs: {}; repo: string; displayWorkflowUrlInterval: number; commit: string; workflowRef: string | number; branch: string; waitForCompletionTimeout: number; path: string; ref: string; displayWorkflowUrl: "" | boolean; checkArtifacts: boolean; searchArtifacts: boolean; checkStatusInterval: number; artifactName: string; runID: number; event: string; downloadArtifactsNoTrigger: "" | boolean; owner: string; displayWorkflowUrlTimeout: number; waitForCompletion: "" | boolean; token: string; forceTrigger: "" | boolean; runNumber: number }
  // Required inputs
  const token = core.getInput("gh-token", {required: true})
  const workflowRef = core.getInput("workflow", {required: true})
  // Optional inputs, with defaults
  let ref = core.getInput("ref") || github.context.ref
  const [owner, repo] = core.getInput("repo")
    ? core.getInput("repo").split("/")
    : [github.context.repo.owner, github.context.repo.repo]

  // const token = core.getInput("gh-token", {required: true})
  // const workflow = core.getInput("workflow", {required: true})
  // const [owner, repo] = core.getInput("repo", {required: true}).split("/")
  let path = core.getInput("path", {required: dl})
  const artifactName = core.getInput("artifact-name")
  let workflowConclusion = core.getInput("workflow-conclusion")
  let pr = Number(core.getInput("pr"))
  let commit = core.getInput("commit")
  if (commit !== "") {
    ref = commit
  }
  let branch = core.getInput("branch")
  if (branch !== "") {
    ref = branch
  }
  let event = core.getInput("event")
  let runID = Number(core.getInput("run-id"))
  let runNumber = Number(core.getInput("run-number"))
  let checkArtifacts = core.getInput("check-artifacts") === "true"
  let searchArtifacts = core.getInput("search-artifacts") === "true"


  // Decode inputs, this MUST be a valid JSON string
  let inputs = {}
  const inputsJson = core.getInput("inputs")
  if (inputsJson) {
    inputs = JSON.parse(inputsJson)
  }


  const displayWorkflowUrlStr = core.getInput("display-workflow-run-url")
  const displayWorkflowUrl = displayWorkflowUrlStr && displayWorkflowUrlStr === "true"
  let displayWorkflowUrlTimeout: number
  try {
    displayWorkflowUrlTimeout = toMilliseconds(core.getInput("display-workflow-run-url-timeout"))
  } catch (e) {
    core.info(`Fallback for 'displayWorkflowUrlTimeout': 10m`)
    displayWorkflowUrlTimeout = toMilliseconds("10m")
  }
  let displayWorkflowUrlInterval: number
  try {
    displayWorkflowUrlInterval = toMilliseconds(core.getInput("display-workflow-run-url-interval"))
  } catch (e) {
    core.info(`Fallback for 'displayWorkflowUrlInterval': 1m`)
    displayWorkflowUrlInterval = toMilliseconds("1m")
  }


  const waitForCompletionStr = core.getInput("wait-for-completion")
  const waitForCompletion = waitForCompletionStr && waitForCompletionStr === "true"

  let waitForCompletionTimeout: number
  try {
    waitForCompletionTimeout = toMilliseconds(core.getInput("wait-for-completion-timeout"))
  } catch (e) {
    core.info(`Fallback for 'waitForCompletionTimeout': 1h`)
    waitForCompletionTimeout = toMilliseconds("1h")
  }
  let checkStatusInterval: number
  try {
    checkStatusInterval = toMilliseconds(core.getInput("wait-for-completion-interval"))
  } catch (e) {
    core.info(`Fallback for 'checkStatusInterval': 1m`)
    checkStatusInterval = toMilliseconds("1m")
  }

  const downloadArtifactsStr = core.getInput("download-artifacts")
  const downloadArtifacts = downloadArtifactsStr && downloadArtifactsStr === "true"
  const downloadArtifactsNoTriggerStr = core.getInput("download-artifacts-no-trigger")
  const downloadArtifactsNoTrigger = downloadArtifactsNoTriggerStr && downloadArtifactsNoTriggerStr === "true"
  const forceTriggerStr = core.getInput("force-trigger")
  const forceTrigger = forceTriggerStr && forceTriggerStr === "true"

  args = {
    token,
    workflowRef,
    ref,
    owner,
    repo,
    inputs,
    displayWorkflowUrl,
    displayWorkflowUrlTimeout,
    displayWorkflowUrlInterval,
    checkStatusInterval,
    waitForCompletion,
    waitForCompletionTimeout,
    downloadArtifacts,
    downloadArtifactsNoTrigger,
    forceTrigger,
    path,
    artifactName,
    workflowConclusion,
    pr,
    commit,
    branch,
    event,
    runID,
    runNumber,
    checkArtifacts,
    searchArtifacts
  }
  debug("Args:", args)
  return args
}

export function sleep(ms: number) {
  return new Promise(resolve => setTimeout(resolve, ms))
}

export function isTimedOut(start: number, waitForCompletionTimeout: number) {
  return Date.now() > start + waitForCompletionTimeout
}

export function formatDuration(duration: number) {
  const durationSeconds = duration / 1000
  const hours = Math.floor(durationSeconds / 3600)
  const minutes = Math.floor((durationSeconds - (hours * 3600)) / 60)
  const seconds = durationSeconds - (hours * 3600) - (minutes * 60)

  let hoursStr = hours + ""
  let minutesStr = minutes + ""
  let secondsStr = seconds + ""

  if (hours < 10) {
    hoursStr = "0" + hoursStr
  }
  if (minutes < 10) {
    minutesStr = "0" + minutesStr
  }
  if (seconds < 10) {
    secondsStr = "0" + secondsStr
  }
  return hoursStr + "h " + minutesStr + "m " + secondsStr + "s"
}
