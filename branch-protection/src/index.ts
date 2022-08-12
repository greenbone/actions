import {getInput, info, warning, isDebug, debug, error} from "@actions/core"
import {context as GHContext, getOctokit} from "@actions/github"

async function run() {
  const args = getArgs()
  const octokit = getOctokit(args.gh_token)

  let protection: any = await octokit.request("GET /repos/{owner}/{repo}/branches/{branch}/protection/enforce_admins", {
    owner: args.owner,
    repo: args.repo,
    branch: args.branch
  })
  debugOutput("protection", protection)
  let success = false
  if (protection.data.enabled !== args.enforce_admins) {
    let methode = protection.data.enabled === true ? "DELETE" : "POST"
    debugOutput("methode", methode)
    for (let i = 0; i <= args.retries; i++) {
      try {

        const req = await octokit.request(methode + " /repos/{owner}/{repo}/branches/{branch}/protection/enforce_admins",
          {
            owner: args.owner,
            repo: args.repo,
            branch: args.branch
          })
        debugOutput("req", req)
        warning(`Change enforce_admins state to ${args.enforce_admins.toString()}.`)

        success = true
        break
      } catch (e) {
        warning(`Failed to set enforce_admins to ${args.enforce_admins.toString()}. Retrying...`)
        warning(e)
        success = false
        await sleep((i * 1000) ** 2)
      }
    }
  } else {
    success = true
    warning("Current requested enforce_admins state is already set.")
  }

  if (!success) {
    error(`Not able to change branch protection enforce_admins to ${args.enforce_admins.toString()}`)
  }

  await sleep((10 * 1000))
}

function getArgs() {
  // Required inputs
  const gh_token = getInput("gh-token", {required: true})
  // Optional inputs, with defaults
  const branch = getInput("branch") || GHContext.ref
  const [owner, repo] = getInput("repo")
    ? getInput("repo").split("/")
    : [GHContext.repo.owner, GHContext.repo.repo]
  const retries = Number(getInput("retries") || 5)
  let enforce_admins: boolean
  let tmp_enforce_admins = getInput("enforce_admins")
  enforce_admins = (tmp_enforce_admins.toLowerCase() === "true")

  return {
    gh_token,
    owner,
    repo,
    branch,
    retries,
    enforce_admins
  }
}

function sleep(ms: number) {
  return new Promise(resolve => setTimeout(resolve, ms))
}

function debugOutput(title: string, content: any) {
  if (isDebug()) {
    info(`::group::${title}`)
    debug(JSON.stringify(content, null, 2))
    info("::endgroup::")
  }
}

run()
