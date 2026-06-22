# Agent Working Ledger Skill - Specification v0.3

## 1. Working title

**Agent Working Ledger**

## 2. Version summary

Version 0.3 refines the Agent Working Ledger specification around separation of concerns.

The main changes from v0.2 are:

* Introduces a layered architecture:

  * Core standard
  * Ledger data model
  * Operation protocols
  * Runtime wrappers
  * Optional tooling
  * Templates
  * Documentation, examples, and evaluations
* Formalises architectural invariants.
* Makes ledger operations explicit as protocols.
* Clarifies the distinction between:

  * plans
  * ledgers
  * evidence
  * handoff notes
  * machine-readable state
  * issue trackers
  * source control
* Adds optional `handoff.md`.
* Adds optional `machine-state.json`.
* Adds `Stale` as a validation status.
* Defines allowed lifecycle transitions.
* Strengthens ownership and anti-contamination rules.
* Clarifies that wrappers must not fork or redefine the core schema.
* Introduces future evaluation criteria for resumability, auditability, and contamination resistance.

## 3. Purpose

Agent Working Ledger is a reusable, agent-agnostic skill for long-running, multi-step, uncertain, or interruption-prone work.

Its purpose is to make an agent externalise volatile task state into a structured Markdown ledger that can be read, updated, reviewed, resumed, handed off, or used after context compaction.

The skill does not replace planning. It adds a durable execution-state layer beneath planning.

A plan says what the agent intends to do.

A working ledger records what the agent has actually done, what it discovered, what decisions it made, what remains, what evidence exists, and how another agent or human can safely continue.

## 4. Core architectural principle

Each agent thread owns exactly one active working-ledger scope unless the user explicitly directs it to use an existing one.

An agent must only create, read for task-state purposes, or update ledgers inside:

1. The working-ledger scope it created for the current thread.
2. A working-ledger scope explicitly supplied by the user.
3. A working-ledger scope explicitly assigned by an agent wrapper or project instruction.

The user may point a later conversation, agent, or coding session at a previous working-ledger directory to continue that work.

The agent must not freely browse, merge, edit, or infer from unrelated ledger scopes just because they exist in the repository.

Existing ledgers are discoverable artifacts, not automatically adoptable memory.

## 5. Separation of concerns

Agent Working Ledger separates seven concerns:

1. **The core standard** defines required behaviour, ownership rules, lifecycle states, and invariants.
2. **The ledger data model** defines durable task-state artifacts such as `OWNER.md`, `ledger.md`, evidence files, notes, and optional sidecars.
3. **Operation protocols** define permitted operations on a ledger, such as create, adopt, update, validate, recover, hand off, close, and supersede.
4. **Runtime wrappers** adapt the core standard to specific agent environments such as Claude Code, Codex, Cursor, Gemini CLI, Aider, or generic CLI agents.
5. **Optional tooling** automates mechanical operations such as creating, checking, summarising, listing, and closing ledgers.
6. **Templates** provide reusable document skeletons.
7. **Documentation, examples, and evaluations** teach, demonstrate, and test the skill.

No layer should silently redefine another layer.

Wrappers must not fork the ledger schema.

Tools must not invent lifecycle states.

Examples must not become normative.

Evidence files must not replace validation summaries.

Ledgers must not act as issue trackers.

The root `working-ledger/` directory must not become shared memory by accident.

## 6. Architectural invariants

The following invariants define the core safety properties of Agent Working Ledger.

1. An agent may write to only one active ledger scope at a time.
2. A ledger scope is not active unless it was created by the current agent thread, explicitly supplied by the user, or explicitly assigned by a wrapper or project instruction.
3. The root `working-ledger/` directory is a container for isolated scopes, not a shared working-memory file.
4. `OWNER.md` is the authority for scope identity and write permission.
5. `ledger.md` is the durable human-readable execution-state authority for the active scope.
6. Optional machine-readable state must mirror the ledger; it must not contain authoritative state absent from `ledger.md`.
7. Validation claims must be backed by command output, manual check notes, evidence references, or an explicit non-run status.
8. A ledger must be accurate enough that another agent or human can resume from it without the original chat.
9. Agents must not silently adopt the newest, nearest, or most plausible existing ledger.
10. Agents must not write secrets, credentials, tokens, private keys, or unnecessary personal data into a ledger.
11. Discoveries that change the approach must be reflected in the active plan.
12. Decisions must record rationale and consequences.
13. Closed ledgers must contain an outcome or retrospective.
14. Superseded ledgers must name what superseded them, where possible.
15. Ledger updates must keep the document internally consistent.

## 7. Problem statement

Long-running agentic tasks often fail because important state remains implicit in the model’s current context window.

Common failure modes include:

* The agent forgets why a decision was made.
* The agent repeats investigation already completed.
* The agent loses track of partial progress.
* The agent treats stale assumptions as still valid.
* The agent resumes after context compaction with a plausible but inaccurate sense of state.
* A user cannot easily audit what happened.
* A second agent cannot safely pick up the work.
* A native plan exists, but discoveries made during execution are not reflected in a durable, mutable artifact.
* Multiple agent threads accidentally overwrite or contaminate each other’s task state.
* Validation results are remembered as “passed” after later changes make them stale.
* A generic project plan becomes confused with task-local execution state.
* Shared scratch files are used as accidental coordination mechanisms without ownership boundaries.

Agent Working Ledger addresses this by requiring each agent thread to maintain an explicit, task-local ledger scope as the authoritative source for that thread’s execution state.

## 8. Scope

This skill applies to tasks that are:

* Long-running.
* Multi-step.
* Ambiguous or exploratory.
* Likely to involve design decisions.
* Likely to uncover new information during work.
* Dependent on validation loops.
* Vulnerable to interruption, context compaction, session loss, or agent handoff.
* Likely to involve multiple agentic runs, subagents, or future continuation.
* Broad enough that progress needs to be recoverable from durable state.
* Risky enough that hidden plan drift would be harmful.

Examples:

* Implementing a feature across several files.
* Performing a refactor.
* Debugging a difficult defect.
* Running an eval-driven improvement loop.
* Migrating between libraries, frameworks, APIs, or architectures.
* Investigating unknown repo behaviour before making changes.
* Building a prototype where discoveries affect later design.
* Executing an existing plan over many turns.
* Preparing work that another agent or future thread may need to resume.
* Auditing or improving an agent-generated codebase.
* Coordinating parent-agent and subagent work without shared mutable scratch state.

## 9. Non-goals

This skill is not:

* A replacement for an agent’s native planning mode.
* A replacement for formal execution plans.
* A replacement for project instruction files such as `AGENTS.md`, `CLAUDE.md`, `.cursorrules`, or equivalent.
* A replacement for platform-level long-term memory.
* A project-management system.
* A ticket tracker.
* A substitute for source control.
* A substitute for tests, builds, or validation.
* A dependency-management tool.
* A design-document system for permanent architecture records.
* A place to store secrets, credentials, tokens, private keys, or unnecessary personal data.
* A shared scratchpad for every agent thread in a repository.
* A mechanism for agents to silently coordinate through global mutable state.
* A guarantee that the agent’s work is correct.

The ledger is deliberately task-local and operational.

## 10. Relationship to plans, evidence, issue trackers, and source control

Agent Working Ledger must maintain clear boundaries between related artifacts.

| Artifact         | Purpose                                                                         |
| ---------------- | ------------------------------------------------------------------------------- |
| Plan             | Intended approach                                                               |
| Working ledger   | Actual execution state                                                          |
| Evidence         | Proof, observations, logs, command output, screenshots, or manual check records |
| Handoff note     | Compressed continuation summary                                                 |
| Issue tracker    | Project-level work item or backlog                                              |
| Source control   | History of source changes                                                       |
| Long-term memory | Cross-task or cross-session remembered context                                  |

A plan is allowed to be wrong.

A ledger must not be knowingly wrong.

The active plan section inside `ledger.md` is not sacred. It is the currently valid operational plan, and it must change when discoveries invalidate the previous approach.

Obsolete plans belong in the decision log, discovery notes, or supporting notes, not in the live active-plan section.

## 11. Agent-agnostic architecture

Agent Working Ledger should be implemented as a core, agent-agnostic standard plus thin agent-specific wrappers.

The core standard defines:

* Ledger ownership rules.
* Directory structure.
* Ledger schema.
* Lifecycle states.
* Operation protocols.
* Update protocol.
* Recovery protocol.
* Validation expectations.
* Handoff behaviour.
* Acceptance criteria.
* Optional helper-tool expectations.

Agent-specific wrappers define:

* Where the skill should be installed for that agent.
* How that agent exposes session or thread identity.
* How to invoke the skill directly.
* Any agent-specific variables, command syntax, hooks, or permissions.
* Any limitations of that agent’s environment.
* Whether the runtime supports native skills, project rules, subagents, hooks, shell commands, or persistent files.

The core skill must not depend on a single agent platform.

Wrappers may adapt invocation mechanics, but must not redefine the core ledger schema or ownership model.

## 12. Recommended repository structure

Recommended repository layout:

```text
agent-working-ledger/
  README.md
  LICENSE
  CHANGELOG.md

  spec/
    SPEC.md
    glossary.md
    invariants.md
    lifecycle.md
    ownership-model.md
    ledger-scope.md
    validation-model.md
    threat-model.md

  protocols/
    create-ledger.md
    adopt-ledger.md
    orient.md
    update-ledger.md
    record-discovery.md
    record-decision.md
    record-validation.md
    recover.md
    handoff.md
    close-ledger.md
    supersede-ledger.md

  templates/
    OWNER.md.template
    ledger.md.template
    handoff.md.template
    evidence-README.md.template
    machine-state.json.template

  skills/
    agent-working-ledger/
      SKILL.md
      README.md

  wrappers/
    claude-code/
      README.md
      SKILL.md
      CLAUDE.md-snippet.md
      runtime-capabilities.md

    codex/
      README.md
      SKILL.md
      AGENTS.md-snippet.md
      runtime-capabilities.md

    cursor/
      README.md
      rules-snippet.md
      runtime-capabilities.md

    generic-cli-agent/
      README.md
      prompt-wrapper.md
      runtime-capabilities.md

  tools/
    awl/
      __init__.py
      cli.py
      create.py
      check.py
      summarize.py
      close.py
      list.py
      models.py
      markdown.py
      paths.py

  examples/
    feature-implementation/
    debugging/
    migration/
    handoff/
    parallel-subagents/

  evals/
    README.md
    scenarios/
      interrupted-refactor.md
      failed-test-loop.md
      stale-assumption.md
      parallel-agent-contamination.md
      handoff-after-compaction.md
    rubrics/
      resumability.md
      auditability.md
      contamination-resistance.md
      validation-quality.md

  docs/
    quickstart.md
    concepts.md
    installation.md
    anti-patterns.md
    comparison-with-plans.md
    multi-agent-use.md
    faq.md
```

The `skills/agent-working-ledger/` directory is the canonical distributable skill
package. It contains `SKILL.md` plus bundled templates needed by a copied skill
installation.

The top-level `spec/`, `protocols/`, `templates/`, `wrappers/`, `tools/`, `examples/`, `evals/`, and `docs/` directories support the wider project.

## 13. Skill metadata

The core `SKILL.md` front matter should use a trigger-rich description.

Recommended metadata:

```yaml
---
name: agent-working-ledger
description: Use for long-running, multi-step, exploratory, interruptible, validation-heavy, or handoff-prone agentic work. Creates or adopts exactly one task-local working-ledger scope, then maintains a Markdown ledger recording progress, discoveries, decisions, validation evidence, blockers, next actions, and recovery state. Each agent thread must write only to its active ledger scope unless the user explicitly directs it to use an existing one. Do not use for simple one-shot tasks.
---
```

The description should front-load:

* long-running work
* multi-step work
* exploratory work
* interruptible work
* validation-heavy work
* task-local ledger scope
* ownership isolation
* progress
* discoveries
* decisions
* validation evidence
* recovery and handoff

## 14. Trigger conditions

The agent should use this skill when any of the following are true:

* The user explicitly asks for a working memory, working ledger, task ledger, worklog, continuation file, implementation log, recovery file, or handoff note.
* The task is expected to require more than one meaningful implementation checkpoint.
* The task involves uncertain investigation before implementation.
* The task may require context compaction or session resume.
* The task involves a migration, refactor, eval loop, or debugging process.
* The task already uses a plan file and needs live progress tracking.
* The user says to write the plan to a file and update it as work proceeds.
* The agent discovers critical information that changes the original plan.
* The task has enough complexity that another agent should be able to continue from the file alone.
* The user points the agent at an existing working-ledger directory and asks it to continue, review, summarize, or close out the work.
* The task involves parent-agent and subagent coordination.
* The task involves validation whose results may become stale as work proceeds.
* The task is likely to pause and resume across multiple agent sessions.

The agent should not use this skill when:

* The task is a simple answer.
* The task is a small, single-file edit.
* The task can be safely completed in one short turn.
* The user explicitly asks not to create files.
* The repository already has a more specific ledger/planning convention and that convention fully covers the need.
* The agent has not been directed to an existing ledger scope and would need to guess which previous ledger belongs to the current work.
* The task is purely conversational and creates no durable working state.
* The ledger would create more overhead than value.

## 15. Working-ledger root

Default root directory:

```text
working-ledger/
```

This is the human-facing **Working Ledger** directory, expressed as a hyphenated filesystem path to avoid quoting and shell issues.

All ledger scopes must live under this directory unless the user, repository, or wrapper explicitly specifies another location.

If a repository already has an established convention, the agent may use that convention only when it is clearly intended for agent working ledgers or the user has directed it to do so.

The root directory is not itself a ledger.

The root directory must not be used as shared working memory unless the user explicitly asks for a cross-ledger index, summary, or coordination artifact.

## 16. Ledger scope and ownership

Each agent thread works inside one active ledger scope.

A ledger scope is a directory containing at minimum:

```text
working-ledger/
  <ledger-owner-id>/
    OWNER.md
    ledger.md
    evidence/
    notes/
```

Optional files may include:

```text
working-ledger/
  <ledger-owner-id>/
    handoff.md
    machine-state.json
```

The `ledger.md` file is the primary human-readable working ledger.

The `OWNER.md` file records the identity and boundary of the ledger scope.

The `evidence/` directory may contain logs, command outputs, screenshots, benchmark results, diffs, or other validation artifacts.

The `notes/` directory may contain supporting notes too bulky or unstable for the main ledger.

The optional `handoff.md` file contains a compressed continuation note.

The optional `machine-state.json` file contains non-authoritative machine-readable metadata mirrored from the ledger.

An agent must not write to a ledger scope unless one of the following is true:

1. It created the scope in the current thread.
2. The user explicitly directed it to use that scope.
3. The wrapper or project instructions explicitly assigned that scope.

## 17. Ledger owner ID

The ledger owner ID identifies the agent thread or assigned working scope.

When the agent runtime exposes a stable session or thread ID, the owner ID should include it.

Examples:

```text
claude-code-${CLAUDE_SESSION_ID}
codex-<session-id-if-available>
cursor-<session-id-if-available>
```

When no stable session or thread ID is available, the agent must mint an owner ID using:

```text
<UTC timestamp>-<agent-slug>-<short-random-nonce>
```

Example:

```text
20260620T143012Z-generic-agent-a7f3
```

If the task has a useful human-readable slug, it may be appended:

```text
20260620T143012Z-generic-agent-a7f3-oauth-refresh-fix
```

The owner ID must be recorded in:

1. The ledger scope path.
2. The `OWNER.md` file.
3. The header of `ledger.md`.
4. The optional `handoff.md`, if present.
5. The optional `machine-state.json`, if present.

## 18. Owner marker file

Every ledger scope must contain an `OWNER.md` file.

Template:

```markdown
# Working Ledger Owner

Ledger owner ID: <ledger-owner-id>
Owner source: session-id | generated-id | user-assigned | wrapper-assigned
Agent runtime: <agent/runtime name>
Created: <ISO timestamp>
Created by: <agent or user>
Scope path: <repo-relative path>
Primary ledger: ledger.md

## Ownership rule

This ledger scope belongs to the agent thread or assigned continuation explicitly identified above.

Agents must not update this scope unless:
1. They created it.
2. The user explicitly directed them to use it.
3. A wrapper or project instruction explicitly assigned it.

Agents must not update unrelated working-ledger scopes merely because they exist.
```

Before writing to a ledger scope, the agent should read `OWNER.md` and confirm that the scope is the active one.

If the active scope is ambiguous, the agent must stop and ask the user to specify the ledger directory.

If `OWNER.md` is missing but the user explicitly provided the directory, the agent may create one after noting that ownership metadata was missing.

## 19. Ledger file responsibilities

### 19.1 `OWNER.md`

Concern: identity and write boundary.

It answers:

* who owns this scope
* how the owner ID was created
* which runtime created it
* when it was created
* when another agent may write here

It must not contain progress, plans, discoveries, or validation details.

### 19.2 `ledger.md`

Concern: durable human-readable execution state.

It answers:

* what the task is trying to achieve
* what has happened
* what has been discovered
* what decisions were made
* what evidence exists
* what remains
* what is blocked
* how someone should resume

It is the primary task-state authority.

### 19.3 `evidence/`

Concern: bulky or external proof.

It stores logs, command outputs, screenshots, benchmark results, generated reports, diffs, or other validation artifacts.

The ledger should reference evidence files rather than copying excessive output into `ledger.md`.

### 19.4 `notes/`

Concern: supporting material.

It may contain investigation notes, API notes, design alternatives, scratch reasoning, failed approaches, dependency comparisons, or other supporting material.

Notes are not the active state authority.

Important discoveries from notes must be reflected in `ledger.md`.

### 19.5 `handoff.md`

Concern: compressed continuation state.

This optional file is used when handing off work to another agent or human.

It should contain enough information to start safely but should not replace `ledger.md`.

### 19.6 `machine-state.json`

Concern: machine-readable metadata.

This optional file may mirror stable state from `ledger.md`.

It must not contain authoritative task state that is absent from `ledger.md`.

## 20. No default shared state

There is no shared ledger mode in v0.3.

The root `working-ledger/` directory is a container for isolated ledger scopes.

Agents must not create or update shared state in the root directory unless the user explicitly asks for a cross-ledger index, summary, or coordination file.

If the user asks for such a file, it should be clearly marked as human-requested shared state.

Example:

```text
working-ledger/
  INDEX.md
```

The default rule remains:

> Agents write only inside their active ledger scope.

If cross-ledger coordination is added in a future version, it must be defined as a separate protocol with explicit ownership, merge, and conflict rules.

## 21. Default creation protocol

When the skill is invoked and no existing ledger scope is provided:

1. Create `working-ledger/` if it does not exist.
2. Determine the ledger owner ID.
3. Create `working-ledger/<ledger-owner-id>/`.
4. Create `OWNER.md`.
5. Create `ledger.md` from the template.
6. Create `evidence/`.
7. Create `notes/`.
8. Optionally create `handoff.md` if a handoff is expected.
9. Optionally create `machine-state.json` if tooling or wrapper support exists.
10. Record the scope path in the agent’s response.
11. Continue work using only that ledger scope for task-state writes.

Creation must leave the ledger in lifecycle state `Created`.

The first ledger update should include:

* current objective
* assumptions
* initial progress checklist
* active plan or orientation step
* first next actions
* initial recovery notes

## 22. Existing ledger adoption protocol

When the user points the agent at an existing working-ledger directory:

1. Treat that directory as the active ledger scope.
2. Read `OWNER.md` if present.
3. Read `ledger.md`.
4. Read `handoff.md` if present and relevant.
5. Summarize current state before making changes.
6. Check whether the ledger appears internally consistent.
7. Continue from the ledger’s `Next actions` and `Recovery notes`.
8. Update the ledger as work proceeds.

If `OWNER.md` is missing but the user explicitly provided the directory, the agent may create one after noting that ownership metadata was missing.

If multiple possible ledgers exist and the user has not identified one, the agent must not guess.

It may list candidate paths and ask which one to use.

Adoption is explicit.

Discovery is not adoption.

## 23. Ledger lifecycle

A ledger moves through these lifecycle states:

1. **Created** — initial task framing and assumptions recorded.
2. **Oriented** — relevant repo context, task context, files, or constraints identified.
3. **Planned** — current executable approach written down.
4. **Active** — progress, findings, decisions, and validation updated as work proceeds.
5. **Blocked** — blocker and recovery options recorded.
6. **Ready for Review** — implementation or task milestone completed and validation evidence recorded.
7. **Closed** — final outcome, remaining risks, and follow-up work recorded.
8. **Superseded** — another ledger, plan, issue, or execution path has replaced this one.

The lifecycle state must be visible near the top of `ledger.md`.

## 24. Lifecycle state transitions

Allowed transitions:

```text
Created
  ↓
Oriented
  ↓
Planned
  ↓
Active
  ├── Blocked
  │     ↓
  │   Active
  ├── Ready for Review
  │     ↓
  │   Closed
  ├── Superseded
  └── Closed
```

Allowed transition meanings:

| From             | To               | Meaning                                                   |
| ---------------- | ---------------- | --------------------------------------------------------- |
| Created          | Oriented         | Relevant context has been inspected                       |
| Oriented         | Planned          | Initial executable approach exists                        |
| Planned          | Active           | Work has begun                                            |
| Active           | Blocked          | Progress cannot safely continue                           |
| Blocked          | Active           | Blocker resolved or workaround chosen                     |
| Active           | Ready for Review | Work appears complete and validation has been recorded    |
| Ready for Review | Active           | Review or validation found more work                      |
| Ready for Review | Closed           | Work accepted or completed                                |
| Active           | Closed           | Work completed or deliberately stopped                    |
| Any non-Closed   | Superseded       | Another ledger, plan, or execution path replaces this one |

Agents should avoid skipping states unless the task genuinely moves quickly through them.

A ledger may move directly from `Created` to `Active` for short but still ledger-worthy tasks, but the missing orientation and planning detail should still be recorded in the appropriate sections.

Closed ledgers should not be reopened casually.

If a closed ledger must be continued, the agent should either:

1. Create a new ledger that references the closed one.
2. Mark the old ledger as superseded.
3. Continue only if the user explicitly directs the agent to reopen it.

## 25. Required ledger sections

Every `ledger.md` must contain these sections.

### 25.1 Header

Includes:

* Title
* Lifecycle state
* Created timestamp
* Last updated timestamp
* Ledger owner ID
* Owner source
* Agent/runtime
* User objective
* Ledger scope path
* Primary ledger path
* Related branch, issue, plan, or previous ledger, if applicable

### 25.2 Current objective

A plain-language statement of what the task is trying to achieve.

This should be outcome-focused, not implementation-focused.

### 25.3 Current state summary

A short summary of where the work stands right now.

This section is for fast resumption.

It should be updated whenever the task reaches a stopping point.

### 25.4 Assumptions

A list of assumptions currently being relied on.

Each assumption should be marked as:

* Confirmed
* Unconfirmed
* Invalidated
* Superseded

### 25.5 Progress

A checkbox list of granular progress items.

Every stopping point must update this section.

Partially completed work must be split into completed and remaining portions.

### 25.6 Active plan

The current plan of work.

This may begin as the approved plan, but it must be revised when discoveries change the approach.

The plan should not pretend the original approach is still current after the agent has changed course.

### 25.7 Discoveries

Unexpected behaviours, repo facts, bugs, constraints, performance findings, dependency quirks, validation surprises, or other observations discovered during work.

Each discovery should include concise evidence where possible.

### 25.8 Decision log

Every meaningful decision made during the task.

Each entry should include:

* Decision
* Rationale
* Alternatives considered
* Date/time
* Author or agent
* Consequences

### 25.9 Validation evidence

Commands run, tests executed, outputs observed, screenshots inspected, manual checks performed, or other evidence of correctness.

This section should distinguish between:

* Not Run
* Failed
* Passed
* Partially Verified
* Stale
* Not Applicable

### 25.10 Blockers and risks

Anything preventing completion or increasing risk.

Each blocker should include the next sensible action.

### 25.11 Next actions

The immediate next actions, written so another agent or human can continue without reconstructing the task from conversation.

### 25.12 Recovery notes

Instructions for resuming safely after interruption.

This should include:

* files touched
* commands to inspect state
* tests to rerun
* what not to redo
* known traps
* validation that may be stale
* assumptions to re-check

### 25.13 Outcome / retrospective

At task completion or major milestone completion, summarize:

* what changed
* what now works
* how it was verified
* what remains
* lessons learned
* whether the ledger is closed, superseded, or intentionally left active

## 26. Ledger template

A new `ledger.md` should use this structure:

```markdown
# <Task title>

Lifecycle State: Created | Oriented | Planned | Active | Blocked | Ready for Review | Closed | Superseded
Created: <ISO timestamp>
Last updated: <ISO timestamp>
Ledger owner ID: <ledger-owner-id>
Owner source: session-id | generated-id | user-assigned | wrapper-assigned
Agent/runtime: <agent/runtime name>
User objective: <user's requested outcome>
Ledger scope: <repo-relative path>
Primary ledger: <repo-relative path>/ledger.md
Related branch/issue/plan/ledger: <optional>

## Current objective

<Plain-language description of the outcome being pursued.>

## Current state summary

<Short resumption-focused summary of the actual current state.>

## Assumptions

- [Unconfirmed] <assumption>
- [Confirmed] <assumption>
- [Invalidated] <assumption>
- [Superseded] <assumption>

## Progress

- [ ] <granular work item>
- [ ] <granular work item>

## Active plan

<The current plan, revised as work proceeds.>

## Discoveries

- Observation: <what was discovered>
  Evidence: <file, command output, test result, evidence path, or concise explanation>
  Impact: <how this affects the task>

## Decision log

- Decision: <decision made>
  Rationale: <why>
  Alternatives considered: <alternatives>
  Consequences: <what follows from this>
  Date/Author: <timestamp / agent>

## Validation evidence

- Command/check: <what was run or inspected>
  Result: Not Run | Failed | Passed | Partially Verified | Stale | Not Applicable
  Evidence: <short output, observation, or evidence file path>
  Follow-up: <if needed>

## Blockers and risks

- Blocker/risk: <description>
  Impact: <why it matters>
  Next action: <what to do next>

## Next actions

1. <next action>
2. <next action>

## Recovery notes

To resume safely:
1. Read this ledger.
2. Inspect these files: <paths>
3. Run these commands: <commands>
4. Re-check these assumptions: <assumptions>
5. Re-run or review this validation: <commands/checks>
6. Do not redo: <work already completed>
7. Watch out for: <known traps>

## Outcome / retrospective

<Complete at major milestones and task closeout.>
```

## 27. Operation protocols

Agent Working Ledger defines explicit operation protocols.

Each protocol should be documented with:

* Inputs
* Preconditions
* Steps
* Required updates
* Failure behaviour
* Postconditions

The core protocols are:

1. Create ledger
2. Adopt ledger
3. Orient
4. Update ledger
5. Record discovery
6. Record decision
7. Record validation
8. Recover
9. Handoff
10. Close ledger
11. Supersede ledger

## 28. Protocol: create ledger

Use when the skill is invoked and no existing active ledger scope is provided.

### Inputs

* Task title
* User objective
* Optional task slug
* Optional root directory
* Optional owner ID
* Optional owner source
* Optional agent runtime
* Optional related issue, branch, plan, or previous ledger

### Preconditions

* The task triggers the skill.
* The user has not directed the agent to use an existing ledger.
* The agent has permission to create files.

### Steps

1. Create the working-ledger root if needed.
2. Determine owner ID.
3. Create the ledger scope directory.
4. Create `OWNER.md`.
5. Create `ledger.md`.
6. Create `evidence/`.
7. Create `notes/`.
8. Optionally create `handoff.md`.
9. Optionally create `machine-state.json`.
10. Report the scope path to the user.
11. Continue using only that scope.

### Postconditions

* A valid ledger scope exists.
* Ownership is explicit.
* Lifecycle state is `Created`.
* The ledger contains required sections.
* The next action is clear.

## 29. Protocol: adopt ledger

Use when the user explicitly points the agent at an existing ledger scope.

### Inputs

* Existing ledger scope path

### Preconditions

* The user explicitly supplied the path, or the wrapper assigned it.
* The scope exists or can reasonably be created at that location.
* The agent has permission to read the scope.

### Steps

1. Read `OWNER.md` if present.
2. Read `ledger.md`.
3. Read `handoff.md` if present.
4. Summarize current state.
5. Check for obvious inconsistencies.
6. Repair only the active ledger if needed.
7. Continue from `Next actions` and `Recovery notes`.

### Failure behaviour

If multiple ledgers are plausible and none was explicitly selected, stop and ask the user to choose.

If the ledger is missing required files, report what is missing and repair only if the user supplied that scope.

### Postconditions

* The adopted scope is active.
* The agent knows current state, next action, risks, and validation status.
* Any repaired metadata is recorded.

## 30. Protocol: orient

Use after creation or adoption when the agent needs to inspect context before planning or implementation.

### Inputs

* Active ledger scope
* User objective
* Repository or task context

### Steps

1. Inspect relevant files, instructions, plans, tests, issue descriptions, or previous outputs.
2. Record confirmed and unconfirmed assumptions.
3. Record discovered constraints.
4. Update lifecycle state to `Oriented`.
5. Update `Current state summary`.
6. Write initial or revised next actions.

### Postconditions

* Relevant context is captured.
* The agent has not made implementation changes without orientation where orientation is required.
* The ledger says what is known and what remains uncertain.

## 31. Protocol: update ledger

Use after meaningful checkpoints.

### Triggers

The agent must update the active ledger:

1. Immediately after creating it.
2. Before making risky or broad changes.
3. After each meaningful checkpoint.
4. After discovering information that changes the plan.
5. After each failed validation attempt.
6. After each successful validation attempt.
7. Before stopping, pausing, compacting context, or handing off.
8. At completion.

### Required discipline

When updating the ledger, the agent must keep the document internally consistent.

Examples:

* If a decision changes the plan, update both `Decision log` and `Active plan`.
* If a test fails, update both `Validation evidence` and `Next actions`.
* If an assumption is invalidated, update `Assumptions`, `Discoveries`, and possibly `Active plan`.
* If work is partially complete, split the progress item rather than marking it done.
* If the task is blocked, mark the lifecycle state as `Blocked` and write the recovery path.
* If validation becomes stale, mark it as `Stale`.
* If the agent changes ledger scope, record why and who directed the change.

## 32. Protocol: record discovery

Use when the agent learns something that affects the task.

A discovery may be:

* an unexpected repo behaviour
* a failing test pattern
* a hidden dependency
* a performance constraint
* an API limitation
* an invalid assumption
* a mismatch between user request and repo state
* a tool limitation
* a changed external condition

Each discovery should include:

* observation
* evidence
* impact
* follow-up action if needed

If the discovery changes the approach, the agent must update:

* `Discoveries`
* `Assumptions`
* `Active plan`
* `Next actions`
* `Blockers and risks`, if relevant

## 33. Protocol: record decision

Use when the agent chooses between meaningful alternatives.

Each decision should include:

* decision
* rationale
* alternatives considered
* consequences
* date/time
* author or agent

A decision is meaningful when reversing it would affect:

* architecture
* implementation approach
* validation strategy
* dependency choice
* file organisation
* user-facing behaviour
* project risk
* future maintainability
* agent handoff safety

Decisions must not be hidden in prose-only progress notes.

## 34. Protocol: record validation

Use whenever the agent runs or deliberately does not run a validation check.

Validation statuses are:

* **Not Run** — the check has not been run.
* **Failed** — the check was run and failed.
* **Passed** — the check was run and passed for the state that existed at that time.
* **Partially Verified** — the check gives some evidence but does not cover the full claim.
* **Stale** — the check previously passed or partially passed, but later changes may have invalidated it.
* **Not Applicable** — the check does not apply.

Each validation entry should include:

* command or check
* result
* evidence
* follow-up

Examples:

```markdown
- Command/check: `pytest tests/test_parser.py`
  Result: Passed
  Evidence: 12 passed in 1.84s
  Follow-up: Run full test suite before closeout.
```

```markdown
- Command/check: Manual review of generated report formatting
  Result: Partially Verified
  Evidence: Reviewed one sample output in `examples/output.md`; broader sample set not checked.
  Follow-up: Generate and inspect at least three more examples.
```

```markdown
- Command/check: `npm test`
  Result: Stale
  Evidence: Previously passed before changes to `src/auth/session.ts`.
  Follow-up: Re-run before marking ready for review.
```

## 35. Protocol: recover

Use at the start of a resumed work segment.

### Steps

1. Confirm active ledger scope.
2. Read `OWNER.md`.
3. Read `ledger.md`.
4. Read `handoff.md` if present.
5. Check whether lifecycle state matches actual repository state.
6. Check whether listed next actions are still valid.
7. Check whether the active plan conflicts with newer discoveries.
8. Check whether validation evidence is stale.
9. Check whether progress overstates completion.
10. Check whether files mentioned in the ledger still exist.
11. Check whether files changed unexpectedly.
12. Repair the active ledger before proceeding if inconsistencies are found.

The agent must not repair ledgers outside the active ledger scope unless the user explicitly asks it to audit or repair them.

## 36. Protocol: handoff

Use when another agent or human may need to continue the task.

The agent should update `ledger.md` and may create or update `handoff.md`.

A handoff note should include:

```markdown
# Handoff

Active ledger: <path>
Ledger owner ID: <ledger-owner-id>
Lifecycle state: <state>
Last updated: <ISO timestamp>

## Current objective

<one paragraph>

## Current state

<one paragraph>

## Files touched

- <path>: <summary>

## Do next

1. <next action>
2. <next action>

## Do not redo

- <completed investigation or work>

## Known traps

- <trap>

## Validation status

- <summary>

## Resume command/checks

- <commands or inspections>
```

`handoff.md` is a compressed continuation artifact.

It does not replace `ledger.md`.

## 37. Protocol: close ledger

Use when the task or milestone is complete, abandoned, or intentionally stopped.

Closing a ledger requires updating:

* lifecycle state
* current state summary
* progress
* validation evidence
* blockers and risks
* next actions
* recovery notes
* outcome / retrospective

A closed ledger should answer:

* what changed
* what now works
* how it was verified
* what remains
* what risks remain
* whether follow-up work needs a new ledger
* whether the ledger was completed, abandoned, or partially completed

A ledger should not be marked `Closed` merely because the agent is stopping for now.

Temporary stopping requires updated recovery notes, not closure.

## 38. Protocol: supersede ledger

Use when another ledger, plan, issue, or execution path replaces the current ledger.

A superseded ledger should record:

* what superseded it
* why it was superseded
* whether any work from it remains useful
* whether any validation evidence remains relevant
* where continuation should happen

A superseded ledger should not be used for further task-state writes unless the user explicitly reactivates it.

## 39. Self-healing behaviour

At the start of each work segment, the agent should read the active ledger if it exists.

Before continuing, the agent should check whether:

* The ledger lifecycle state matches the actual repository state.
* The listed next actions are still valid.
* The active plan conflicts with newer discoveries.
* The validation evidence is stale.
* The progress checklist overstates completion.
* Any files mentioned in the ledger no longer exist.
* Any files mentioned in the ledger have changed unexpectedly.
* The ledger scope matches the owner rule.
* The optional machine-readable state conflicts with `ledger.md`.

If inconsistency is found, the agent must repair the active ledger before proceeding.

The agent must not repair ledgers outside the active ledger scope unless the user explicitly asks it to audit or repair them.

## 40. Evidence model

Evidence should be concise, inspectable, and referenced from the ledger.

Evidence may include:

* command output
* test output
* linter output
* build output
* benchmark results
* screenshots
* generated diffs
* manual inspection notes
* links to local files
* generated reports
* before/after samples

Large evidence should be stored in `evidence/`.

The ledger should include a short summary and a path to the evidence file.

Example:

```markdown
- Command/check: `pytest`
  Result: Failed
  Evidence: See `evidence/20260620T151233Z-pytest-failure.log`.
  Follow-up: Investigate parser fixture failure.
```

Evidence must not include secrets, credentials, tokens, or unnecessary personal data.

## 41. Optional machine-readable state

A ledger scope may include:

```text
machine-state.json
```

This file is optional.

It may be useful for tools, wrappers, or future automation.

Example:

```json
{
  "schema_version": "0.3",
  "ledger_owner_id": "20260620T143012Z-codex-a7f3",
  "owner_source": "generated-id",
  "agent_runtime": "codex",
  "lifecycle_state": "Active",
  "created": "2026-06-20T14:30:12Z",
  "last_updated": "2026-06-20T15:01:44Z",
  "active_plan_version": 3,
  "validation_status": "Partially Verified",
  "touched_files": [],
  "evidence_files": []
}
```

Rules:

1. `ledger.md` remains the human-readable authority.
2. `machine-state.json` must not contain authoritative state absent from `ledger.md`.
3. If `machine-state.json` conflicts with `ledger.md`, `ledger.md` wins.
4. Tools may regenerate `machine-state.json` from `ledger.md`.
5. Agents may ignore `machine-state.json` unless the wrapper or tooling requires it.

## 42. Subagents and parallel agents

Each independent agent thread, subagent, fork, background worker, or parallel agent should have its own ledger scope unless the user explicitly assigns it to an existing one.

If a main agent delegates work to subagents, the main agent should decide whether the subagent needs a ledger.

A subagent should create its own scope when:

* Its task is long-running.
* Its output may need auditing.
* It may discover information that affects implementation.
* It may run independently or in parallel.
* It may need to be resumed later.
* It may perform validation whose evidence should be preserved.

A subagent should not directly write into the parent agent’s ledger unless explicitly instructed.

Instead, it should either:

1. Return a summary to the parent agent, which updates the parent ledger.
2. Maintain its own ledger scope and provide the path to the parent agent.
3. Write a bounded handoff note in its own scope for later review.

If parent and subagent ledgers both exist, the parent ledger may reference the subagent ledger path.

The parent must not silently merge subagent state into its own ledger without summarising what was adopted.

## 43. Interaction model

When the skill is invoked, the agent should briefly state whether it is:

1. Creating a new working-ledger scope.
2. Using an existing user-specified working-ledger scope.
3. Unable to determine which scope to use.

When creating or adopting a scope, the agent should give the path.

The agent should not ask for permission merely to update the active ledger if the user has requested the skill or the task clearly triggers it.

For high-risk tasks, the agent should still ask for approval before destructive changes, migrations, dependency swaps, broad rewrites, or irreversible operations, according to the environment’s normal approval rules.

The agent should avoid verbose ledger-status chatter unless useful.

The ledger is for durable state, not constant user-facing narration.

## 44. User-facing command patterns

Useful explicit invocations:

* “Use the Agent Working Ledger skill for this.”
* “Create a working ledger and keep it updated as you work.”
* “Write the plan to a file and use it as working memory.”
* “Make this resumable by another agent.”
* “Keep a task-local ledger.”
* “Before you continue, read the active ledger and tell me where things stand.”
* “Continue from `working-ledger/<ledger-owner-id>/`.”
* “Close out the ledger with validation evidence and remaining risks.”
* “Create a new ledger for this thread; do not use the old one.”
* “Use this existing ledger directory as your active scope.”
* “Create a handoff note from the active ledger.”
* “Audit this ledger for stale validation and overstated progress.”
* “List existing ledgers, but do not adopt one yet.”

## 45. Security and privacy

The ledger must not contain:

* secrets
* credentials
* tokens
* private keys
* API keys
* passwords
* unnecessary personal data
* private user information irrelevant to the task
* copied proprietary material beyond what is needed for task state
* sensitive production data
* full logs containing secrets

If evidence output contains secrets, the agent should redact before writing it to the ledger scope.

If the agent is unsure whether material is safe to record, it should summarise at a safer level or ask the user.

The ledger is intended to be committed, shared, or handed off only when the user considers that appropriate.

By default, agents should not assume ledger contents are safe for public publication.

## 46. Anti-patterns

Agents must avoid these anti-patterns:

* Silently adopting the most recent ledger.
* Updating multiple ledger scopes in one task.
* Treating `working-ledger/INDEX.md` as shared memory by default.
* Recording aspirational progress instead of actual progress.
* Marking work complete without validation evidence or an explicit “Not Run”.
* Leaving stale validation marked as passed.
* Hiding meaningful decisions in prose.
* Keeping an obsolete active plan after discoveries changed the approach.
* Using the ledger as a dumping ground for long logs.
* Storing secrets or private data.
* Treating the ledger as a substitute for tests.
* Treating the ledger as a substitute for source control.
* Using one ledger for several unrelated tasks.
* Allowing subagents to write into the parent ledger without explicit instruction.
* Creating ledgers for trivial one-shot tasks.
* Closing a ledger merely because the agent is stopping temporarily.
* Reopening closed ledgers without recording why.

## 47. Claude Code wrapper

Claude Code should use the core skill with a thin wrapper.

Recommended project install path:

```text
.claude/skills/agent-working-ledger/SKILL.md
```

Recommended personal install path:

```text
~/.claude/skills/agent-working-ledger/SKILL.md
```

Claude Code exposes `${CLAUDE_SESSION_ID}` for session-specific files. The Claude Code wrapper should use it when available.

Recommended Claude Code owner ID:

```text
claude-code-${CLAUDE_SESSION_ID}
```

If the wrapper needs a human-readable task slug, append it:

```text
claude-code-${CLAUDE_SESSION_ID}-<task-slug>
```

Recommended Claude Code skill behaviour:

* Use `${CLAUDE_SESSION_ID}` as the owner source when available.
* Create `working-ledger/claude-code-${CLAUDE_SESSION_ID}/`.
* Create `OWNER.md`.
* Create `ledger.md`.
* Create `evidence/`.
* Create `notes/`.
* Optionally create `handoff.md`.
* Do not update other `working-ledger/*/` scopes unless the user explicitly names one.
* If running subagents, do not assume subagents may write to the parent scope.
* If a subagent needs durable task state, give it a separate scope or require it to return a summary to the parent.

Possible Claude Code wrapper front matter:

```yaml
---
name: agent-working-ledger
description: Maintain a session-specific working ledger for long-running, multi-step, exploratory, interruptible, validation-heavy, or handoff-prone work. Uses the active Claude Code session ID when available to create or adopt one ledger scope under working-ledger/. Do not write to unrelated ledger scopes unless the user explicitly provides one.
argument-hint: "[optional-existing-ledger-scope-or-task-title]"
---
```

## 48. Codex wrapper

Codex should use the core skill with a thin wrapper.

Recommended behaviour:

* Use a Codex-provided session or conversation ID if one is available to the agent.
* If no stable session ID is available, mint an owner ID using timestamp, agent slug, and nonce.
* Create a ledger scope under `working-ledger/`.
* Record whether the owner ID came from a session ID or was generated.
* Do not update other ledger scopes unless the user explicitly names one.
* Treat project instructions such as `AGENTS.md` as wrapper-level invocation material, not as a replacement for the core standard.

Recommended Codex owner ID, if session ID is available:

```text
codex-<session-id>
```

Fallback:

```text
<UTC timestamp>-codex-<short-random-nonce>
```

Codex wrapper material may include:

```text
wrappers/codex/
  README.md
  SKILL.md
  AGENTS.md-snippet.md
  runtime-capabilities.md
```

Suggested `AGENTS.md` snippet:

```markdown
## Agent Working Ledger

For long-running, multi-step, exploratory, interruptible, validation-heavy, or handoff-prone tasks, use the Agent Working Ledger skill.

Each agent thread must work inside exactly one active ledger scope under `working-ledger/`.

If the user gives an existing ledger scope, use that. Otherwise create a new scope for this thread.

Do not write to unrelated ledger scopes merely because they exist.

Keep the active ledger updated with progress, discoveries, decisions, validation evidence, blockers, next actions, and recovery notes.

A plan records intended work. The working ledger records actual execution state.
```

## 49. Generic agent wrapper

For agents without first-class skill support, use a prompt wrapper.

The wrapper should instruct the agent to:

1. Create or adopt exactly one active ledger scope.
2. Use a real session/thread ID if available.
3. Otherwise mint a timestamped owner ID.
4. Write only within that active scope.
5. Maintain `OWNER.md` and `ledger.md`.
6. Create `evidence/` and `notes/`.
7. Update the ledger at every checkpoint.
8. Treat the ledger as the durable task-state authority.
9. Avoid unrelated ledger scopes unless the user explicitly assigns one.
10. Distinguish plans, ledgers, evidence, and handoff notes.

## 50. Runtime capability documents

Each wrapper should include a `runtime-capabilities.md` file.

This file should answer:

* Does the runtime expose a session or thread ID?
* Can the runtime create files?
* Can the runtime read existing project files?
* Can the runtime run shell commands?
* Can the runtime run tests?
* Does the runtime support native skills?
* Does the runtime support project rules?
* Does the runtime support subagents?
* Does the runtime support hooks?
* Does the runtime persist state across sessions?
* Are there environment-specific safety constraints?
* What owner ID pattern should be used?

Runtime capability documents are descriptive.

They must not redefine the core standard.

## 51. Optional scripts

The first version can be instruction-only.

Later versions may include scripts.

### 51.1 `new-ledger.py`

Creates a ledger scope from the template.

Inputs:

* task title
* optional task slug
* optional destination root
* optional owner ID
* optional owner source
* optional agent runtime
* optional related issue, branch, plan, or previous ledger

Outputs:

* scope path
* owner marker path
* primary ledger path

### 51.2 `check-ledger.py`

Checks that a ledger scope contains required files and basic consistency.

Possible checks:

* `OWNER.md` exists
* `ledger.md` exists
* owner ID appears in both files
* required headings present
* lifecycle state value is valid
* lifecycle transition appears plausible
* last updated exists
* progress section contains checkboxes
* decision log exists
* validation evidence exists
* validation statuses are from the permitted set
* next actions exists
* closed ledgers contain outcome/retrospective text
* superseded ledgers name the superseding path or reason where possible
* optional `machine-state.json` does not obviously conflict with `ledger.md`

### 51.3 `summarize-ledger.py`

Produces a short continuation prompt from the active ledger.

Useful for:

* agent handoff
* context compaction
* user review
* continuation in a new thread

### 51.4 `list-ledgers.py`

Lists existing ledger scopes without modifying them.

This should be used only when the user asks to find or choose an existing ledger.

It must not cause the agent to adopt a ledger automatically unless the user chooses one.

### 51.5 `close-ledger.py`

Assists with closing a ledger.

It should check that:

* lifecycle state can be moved to `Closed`
* outcome / retrospective exists
* validation status is clear
* remaining risks are recorded
* next actions are either empty, follow-up work, or explain why no further action is needed

## 52. CLI interface

A future CLI may expose:

```bash
awl new "OAuth refresh fix"
awl check working-ledger/20260620T143012Z-codex-a7f3/
awl summarize working-ledger/20260620T143012Z-codex-a7f3/
awl close working-ledger/20260620T143012Z-codex-a7f3/
awl list
```

CLI principles:

* `list` may discover ledgers.
* `new` may create a ledger.
* `check` may inspect a specified ledger.
* `summarize` may read a specified ledger.
* `close` may modify only a specified ledger.
* No command should casually mutate all ledgers.
* Tooling must obey the same ownership and adoption principles as agents.
* Tooling must not become the source of truth.

## 53. Evaluation scenarios

Agent Working Ledger should eventually include evaluation scenarios.

Possible scenarios:

### 53.1 Interrupted refactor

An agent begins a multi-file refactor, updates the ledger, stops midway, and another agent resumes from the ledger alone.

Evaluation questions:

* Can the second agent identify completed and remaining work?
* Does it avoid repeating investigation?
* Does it re-run stale validation?

### 53.2 Failed test loop

An agent runs tests, observes failure, changes approach, and records the failed validation.

Evaluation questions:

* Is the failed validation preserved?
* Does the active plan change?
* Are next actions specific?

### 53.3 Stale assumption

An agent records an assumption, later discovers it is invalid, and must update the ledger.

Evaluation questions:

* Is the assumption marked invalidated?
* Is the discovery recorded?
* Is the active plan revised?

### 53.4 Parallel-agent contamination

Two agents operate in the same repository.

Evaluation questions:

* Do they create separate scopes?
* Does either agent write to the other’s ledger?
* Is parent/subagent state passed by summary rather than uncontrolled shared writes?

### 53.5 Handoff after compaction

The conversation context is lost or compacted.

Evaluation questions:

* Can the task resume from `ledger.md` and `handoff.md`?
* Are files touched and validation status clear?
* Are known traps recorded?

## 54. Evaluation rubrics

Possible rubrics:

### 54.1 Resumability

A ledger is resumable when another agent or human can continue without the original chat.

Criteria:

* objective is clear
* current state is accurate
* next actions are specific
* files touched are listed
* validation state is clear
* recovery notes identify what not to redo

### 54.2 Auditability

A ledger is auditable when a human can understand what happened and why.

Criteria:

* decisions include rationale
* discoveries include evidence
* validation results are recorded
* risks are visible
* outcome is clear

### 54.3 Contamination resistance

A ledger system is contamination-resistant when separate agents do not accidentally merge state.

Criteria:

* owner IDs are unique
* `OWNER.md` exists
* agents do not write unrelated scopes
* shared state is not created by default
* subagent state is explicitly passed

### 54.4 Validation quality

Validation quality is high when correctness claims are proportional to evidence.

Criteria:

* commands/checks are named
* results use permitted statuses
* stale validation is marked
* failures are preserved
* manual checks are labelled as manual
* partial verification is not overstated

## 55. Acceptance criteria for the skill

The skill is working when:

1. Given a complex task, the agent creates a ledger scope under `working-ledger/`.
2. The scope contains `OWNER.md`, `ledger.md`, `evidence/`, and `notes/`.
3. The ledger owner ID is recorded consistently.
4. The agent updates only its active ledger scope.
5. The agent does not modify unrelated ledger scopes unless explicitly directed.
6. The ledger contains all required sections.
7. The agent updates the ledger after meaningful checkpoints.
8. Discoveries that change the approach are reflected in the active plan.
9. Decisions include rationale, alternatives, consequences, and date/author.
10. Validation evidence records commands/checks and results.
11. Validation status distinguishes Not Run, Failed, Passed, Partially Verified, Stale, and Not Applicable.
12. A second agent or human can resume from the ledger alone when pointed at the scope.
13. The skill does not trigger for trivial one-shot tasks.
14. The skill integrates with existing repo planning conventions rather than duplicating them.
15. No secrets or credentials are written into the ledger.
16. Closed ledgers contain an outcome or retrospective.
17. Superseded ledgers say what replaced them where possible.
18. Wrappers do not redefine the core schema.
19. Optional tooling obeys ownership and adoption rules.
20. The root `working-ledger/` directory does not become shared state by default.

## 56. README positioning

Suggested public description:

Agent Working Ledger is an agent-agnostic skill for long-running software-agent work. It teaches coding agents to create or adopt a single task-local ledger scope under `working-ledger/`, then maintain a mutable Markdown ledger as explicit execution state. Each agent thread writes only to its own ledger scope unless the user explicitly points it at an existing one. The ledger captures progress, discoveries, decisions, validation evidence, blockers, next actions, and recovery notes, improving resumability, auditability, and handoff safety across Codex, Claude Code, and other agentic coding systems.

## 57. CV positioning

Suggested CV bullet:

Built Agent Working Ledger, an agent-agnostic skill for Codex, Claude Code, and related coding agents that formalises task-local execution state for long-running agentic work. The skill creates isolated per-thread ledger scopes and maintains structured Markdown records of progress, discoveries, decisions, validation evidence, blockers, and recovery state, improving resumability, auditability, and handoff safety across complex software tasks.

## 58. Future extensions

Possible future work:

* JSON/YAML sidecar for richer machine-readable state.
* CLI to create, validate, summarize, list, and close ledger scopes.
* Git hook or CI check for required ledger sections.
* Integration with issue trackers.
* Conversion between lightweight ledgers and full execution plans.
* Ledger-to-PR-summary generation.
* Ledger-to-handoff-prompt generation.
* Multi-agent merge protocol for parallel subagents.
* Evaluation suite measuring whether agents using the skill resume work more accurately after context compaction.
* Agent-specific installers for Claude Code, Codex, Cursor, Gemini CLI, Aider, and other coding agents.
* Schema versioning.
* Migration helpers between specification versions.
* Linting for stale validation, invalid lifecycle states, and missing decision rationale.
* Repository dashboard for human review of active and closed ledgers.

## 59. Minimal v0.3 release package

A minimal practical v0.3 release may include:

```text
agent-working-ledger/
  README.md
  LICENSE

  spec/
    SPEC.md
    invariants.md
    ownership-model.md

  protocols/
    create-ledger.md
    adopt-ledger.md
    update-ledger.md
    recover.md
    close-ledger.md

  templates/
    OWNER.md.template
    ledger.md.template
    handoff.md.template

  skills/
    agent-working-ledger/
      SKILL.md
      templates/
        OWNER.md.template
        ledger.md.template
        handoff.md.template

  wrappers/
    claude-code/
      SKILL.md
      CLAUDE.md-snippet.md

    codex/
      SKILL.md
      AGENTS.md-snippet.md

    generic-cli-agent/
      prompt-wrapper.md

  docs/
    quickstart.md
    anti-patterns.md
    comparison-with-plans.md
```

The first release should prove the conceptual architecture before overbuilding tooling.

## 60. One-sentence architecture

Agent Working Ledger is a layered, agent-agnostic execution-state architecture in which each agent thread creates or adopts exactly one isolated ledger scope under `working-ledger/`; the core standard defines ownership and lifecycle invariants, the ledger schema defines durable Markdown artifacts, protocols define safe operations, wrappers adapt the standard to specific agent runtimes, and optional tools validate and summarize ledgers without becoming the source of truth.
