// ----------------------------------------------------------------------------
// Copyright (c) Greenbone Networks GmbH - Josef Fröhle, 2022
// Licensed under the MIT License.
// ----------------------------------------------------------------------------

import * as core from '@actions/core'
import * as github from '@actions/github'
import AdmZip from 'adm-zip'
import filesize from 'filesize'
import pathname from 'path'
import fs from 'fs'
import {debug} from './debug';
import {getArgs} from "./utils"

export async function download() {
  try {
    const args = getArgs(true)

    const client = github.getOctokit(args.token)

    console.log("==> Workflow:", args.workflowRef)

    console.log("==> Repo:", args.owner + "/" + args.repo)

    console.log("==> Conclusion:", args.workflowConclusion)

    if (args.pr) {
      console.log("==> PR:", args.pr)

      const pull = await client.rest.pulls.get({
        owner: args.owner,
        repo: args.repo,
        pull_number: args.pr,
      })
      args.commit = pull.data.head.sha
    }

    if (args.commit) {
      console.log("==> Commit:", args.commit)
    }

    if (args.branch) {
      args.branch = args.branch.replace(/^refs\/heads\//, "")
      console.log("==> Branch:", args.branch)
    }

    if (args.event) {
      console.log("==> Event:", args.event)
    }

    if (args.runNumber) {
      console.log("==> RunNumber:", args.runNumber)
    }

    if (!args.runID) {

      for await (const runs of client.paginate.iterator(client.rest.actions.listWorkflowRuns, {
          owner: args.owner,
          repo: args.repo,
          workflow_id: args.workflowRef,
        // currently the API is broken due to some backend issues at GitHub
        // we have been advised to remove the event filter until the backend
        // has rebuild some elastic search db indexes
        //  branch: branch,
        //  event: event,
        }
      )) {
        // currently the API is broken due to some backend issues at GitHub
        // we have been advised to remove the event filter until the backend
        // has rebuild some elastic search db indexes
        debug('Before Filter for ', {
          branch: args.branch,
          event: args.event
        });

        debug('Before Filtered WorkflowRuns', runs.data);


        const run2 = runs.data.filter((r: any) => ["schedule","workflow_dispatch"].includes(r.event) ).filter((r: any) => r.head_branch === args.branch)
        debug('Filtered WorkflowRuns', run2);
        for (const run of run2) {
          if (args.commit && run.head_sha != args.commit) {
            continue
          }
          if (args.runNumber && run.run_number != args.runNumber) {
            continue
          }
          if (args.workflowConclusion && (args.workflowConclusion != run.conclusion && args.workflowConclusion != run.status)) {
            continue
          }
          if (args.checkArtifacts || args.searchArtifacts) {
            let artifacts = await client.rest.actions.listWorkflowRunArtifacts({
              owner: args.owner,
              repo: args.repo,
              run_id: run.id,
            })
            if (artifacts.data.artifacts.length == 0) {
              continue
            }
            if (args.searchArtifacts) {
              const artifact = artifacts.data.artifacts.find((artifact: { name: string }) => {
                return artifact.name == args.artifactName
              })
              if (!artifact) {
                continue
              }
            }
          }
          args.runID = run.id
          break
        }
        if (args.runID) {
          break
        }
      }
    }

    if (args.runID) {
      console.log("==> RunID:", args.runID)
    } else {
      throw new Error("no matching workflow run found");
    }

    let artifacts = await client.paginate(client.rest.actions.listWorkflowRunArtifacts, {
      owner: args.owner,
      repo: args.repo,
      run_id: args.runID,
    })

    // One artifact or all if `name` input is not specified.
    if (args.artifactName) {
      // @ts-ignore
      artifacts = artifacts.filter((artifact) => {
        return artifact.name == args.artifactName
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
        owner: args.owner,
        repo: args.repo,
        artifact_id: artifact.id,
        archive_format: "zip",
      })

      const dir = args.artifactName ? args.path : pathname.join(args.path, artifact.name)

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
