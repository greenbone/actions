import * as core from '@actions/core'
import * as github from '@actions/github'
import AdmZip from 'adm-zip'
import filesize from 'filesize'
import pathname from 'path'
import fs from 'fs'

export async function download() {
  try {
    const token = core.getInput("gh-token", {required: true})
    const workflow = core.getInput("workflow", {required: true})
    const [owner, repo] = core.getInput("repo", {required: true}).split("/")
    const path = core.getInput("path", {required: true})
    const name = core.getInput("name")
    let workflowConclusion = core.getInput("workflow-conclusion")
    let pr = Number(core.getInput("pr"))
    let commit = core.getInput("commit")
    let branch = core.getInput("branch")
    let event = core.getInput("event")
    let runID = Number(core.getInput("run-id"))
    let runNumber = Number(core.getInput("run-number"))
    let checkArtifacts = core.getInput("check-artifacts")
    let searchArtifacts = core.getInput("search-artifacts")

    const client = github.getOctokit(token)

    console.log("==> Workflow:", workflow)

    console.log("==> Repo:", owner + "/" + repo)

    console.log("==> Conclusion:", workflowConclusion)

    if (pr) {
      console.log("==> PR:", pr)

      const pull = await client.rest.pulls.get({
        owner: owner,
        repo: repo,
        pull_number: pr,
      })
      commit = pull.data.head.sha
    }

    if (commit) {
      console.log("==> Commit:", commit)
    }

    if (branch) {
      branch = branch.replace(/^refs\/heads\//, "")
      console.log("==> Branch:", branch)
    }

    if (event) {
      console.log("==> Event:", event)
    }

    if (runNumber) {
      console.log("==> RunNumber:", runNumber)
    }

    if (!runID) {

      for await (const runs of client.paginate.iterator(client.rest.actions.listWorkflowRuns, {
          owner: owner,
          repo: repo,
          workflow_id: workflow,
          branch: branch,
          event: event,
        }
      )) {
        for (const run of runs.data) {
          if (commit && run.head_sha != commit) {
            continue
          }
          if (runNumber && run.run_number != runNumber) {
            continue
          }
          if (workflowConclusion && (workflowConclusion != run.conclusion && workflowConclusion != run.status)) {
            continue
          }
          if (checkArtifacts || searchArtifacts) {
            let artifacts = await client.rest.actions.listWorkflowRunArtifacts({
              owner: owner,
              repo: repo,
              run_id: run.id,
            })
            if (artifacts.data.artifacts.length == 0) {
              continue
            }
            if (searchArtifacts) {
              const artifact = artifacts.data.artifacts.find((artifact: { name: string }) => {
                return artifact.name == name
              })
              if (!artifact) {
                continue
              }
            }
          }
          runID = run.id
          break
        }
        if (runID) {
          break
        }
      }
    }

    if (runID) {
      console.log("==> RunID:", runID)
    } else {
      throw new Error("no matching workflow run found");
    }

    let artifacts = await client.paginate(client.rest.actions.listWorkflowRunArtifacts, {
      owner: owner,
      repo: repo,
      run_id: runID,
    })

    // One artifact or all if `name` input is not specified.
    if (name) {
      // @ts-ignore
      artifacts = artifacts.filter((artifact) => {
        return artifact.name == name
      })
    }

    if (artifacts.length == 0) {
      throw new Error("no artifacts found")
    }

    for (const artifact of artifacts) {
      console.log("==> Artifact:", artifact.id)

      const size = filesize(artifact.size_in_bytes, {base: 10})

      console.log(`==> Downloading: ${artifact.name}.zip (${size})`)

      const zip = await client.rest.actions.downloadArtifact({
        owner: owner,
        repo: repo,
        artifact_id: artifact.id,
        archive_format: "zip",
      })

      const dir = name ? path : pathname.join(path, artifact.name)

      fs.mkdirSync(dir, {recursive: true})

      const adm = new AdmZip(Buffer.from(zip.data as string))

      adm.getEntries().forEach((entry) => {
        const action = entry.isDirectory ? "creating" : "inflating"
        const filepath = pathname.join(dir, entry.entryName)

        console.log(`  ${action}: ${filepath}`)
      })

      adm.extractAllTo(dir, true)
    }
  } catch (error) {
    if (typeof error === "string") {
      core.setFailed(error.toUpperCase()); // works, `e` narrowed to string
    } else if (error instanceof Error) {
      core.setFailed(error.message); // works, `e` narrowed to Error
    }
    throw error
  }
}
