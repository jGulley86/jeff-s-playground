# Agent team for Claude Code

Port of the "one orchestrator, four specialists" pattern. Drop the `.claude/` folder into a project root (or move the agent files to `~/.claude/agents/` to use them everywhere).

## Run it
    claude --agent orchestrator

`settings.json` already sets `"agent": "orchestrator"`, so plain `claude` in this project does the same thing.

## What is enforced by the tool, not the prompt
- Orchestrator can spawn only research, builder, critic, verifier (`Agent(...)` allowlist).
- Specialists cannot spawn anything (`CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH=1`).
- Critic has no Write or Edit. Verifier has no Write or Edit.
- Builder has no network tools. Research has no Bash.
- Push, merge, publish, curl, ssh, rm -rf are denied for every agent (`permissions.deny`).
- Built-in Explore/Plan/general-purpose/fork are denied so there are no uncounted agents.

## What is still prompt-only
- The handoff contract and file naming.
- The "ask before external action" list (the deny rules cover the common ones).
- Research's FACT / ASSUMPTION / UNCERTAIN discipline.

## Test scenario
    Draft a launch note from the 3 release docs in workspace/launch/00-brief/, then email it.

Expected: orchestrator writes brief, two research runs in parallel, builder drafts v1, critic flags blocking issues, builder v2, verifier PASS, orchestrator reports NEEDS APPROVAL because sending email is an external action it cannot and will not take.
