# Starship of Chameleons Protocol, OpenClaw Architecture Translation

## Purpose
Translate the white paper into something implementable as an OpenClaw upgrade, extension, or companion project.

## My Read of the White Paper
The protocol is not one feature. It is a coordinated operating model made of:
- hierarchical agent orchestration
- structured roles and rank
- persistent multi-tier memory
- human approval gates
- review agents and quality workflows
- reusable mission templates and skill packaging
- observability, rollback, and audit trails
- secure communication boundaries
- fleet level multi-starship coordination
- deployment and GUI layers

In other words, this should be treated as a platform layer, not a single plugin.

## Important Reality Check
Some of the protocol already overlaps with OpenClaw primitives:
- sessions and subagents already provide isolated execution contexts
- memory files and memory search already provide part of the memory layer
- tools and skills already exist
- approvals already exist for sensitive tool execution
- message routing and multi-agent support already exist
- TaskFlow exists for durable work orchestration

So the project should not clone OpenClaw. It should compose around OpenClaw.

## Recommended Product Shape
Build Starship of Chameleons Protocol as a companion framework with four layers.

### Layer 1, Domain Model
A Python package that defines protocol objects and rules.

Candidate modules:
- `csp/core/chameleon.py`
- `csp/core/officer.py`
- `csp/core/captain.py`
- `csp/core/crew_captain.py`
- `csp/core/specialist.py`
- `csp/core/oxpecker.py`
- `csp/core/uhura.py`
- `csp/core/fleet.py`
- `csp/core/starship.py`
- `csp/core/memory.py`
- `csp/core/gates.py`
- `csp/core/skills.py`
- `csp/core/snapshots.py`
- `csp/core/stardate.py`
- `csp/core/logbook.py`

This layer should be OpenClaw-aware but not tightly coupled to its runtime.

### Layer 2, OpenClaw Adapter Layer
Adapters that map protocol concepts onto OpenClaw capabilities.

Candidate mappings:
- Captain or Crew Captain to orchestrator session or agent role
- Specialist to subagent or ACP task session
- Working memory to recent session context and bounded memory buffers
- Lessons and directives to workspace files, managed memory files, or protocol stores
- Gate checks to approval policies, explicit user checkpoints, and workflow state
- Uhura pattern to message tool wrappers and outbound guard hooks
- Mission templates to TaskFlow backed templates or structured project definitions
- Fleet to multi-agent routing across isolated OpenClaw agents

Candidate adapter modules:
- `csp/openclaw/session_adapter.py`
- `csp/openclaw/memory_adapter.py`
- `csp/openclaw/message_adapter.py`
- `csp/openclaw/taskflow_adapter.py`
- `csp/openclaw/skills_adapter.py`
- `csp/openclaw/dashboard_adapter.py`

### Layer 3, Control Plane
A service that tracks state across missions.

Responsibilities:
- registry of starships, rooms, roles, and assignments
- state snapshots and rollback metadata
- gate configuration persistence
- mission state machine
- performance metrics
- audit logs

This can begin as local JSON or SQLite, then grow up later.

### Layer 4, Operator Surface
User-facing controls.

Potential forms:
- CLI first
- later a lightweight web GUI called Captain's Console
- dashboards for crew, gates, missions, logs, and costs

## Best OpenClaw Integration Path

### Phase 1, build as a companion project
Do not fork OpenClaw yet.

Reason:
- faster iteration
- less maintenance pain
- easier to prove value before invasive changes
- lets us leverage existing OpenClaw sessions, tools, memory, and multi-agent routing

### Phase 2, integrate through documented seams
Target these seams first:
- TaskFlow for durable mission orchestration
- session and subagent tools for role execution
- memory files and memory search for tiered memory persistence
- plugin hooks for outbound communication control and audit
- multi-agent routing for fleet concepts

### Phase 3, add optional GUI and bootstrap deployment
Once the orchestration core works, then add:
- setup wizard
- docker packaging
- Captain's Console

## Mapping White Paper Concepts to OpenClaw

| White Paper Concept | OpenClaw Primitive | Build Needed |
|---|---|---|
| Chameleon base class | Agent/session model | Domain model + adapters |
| Captain | Main orchestrator session | Mission coordinator layer |
| Crew Captain | Subagent/session coordinator | Role orchestration |
| Specialist | Subagent or ACP session | Task routing conventions |
| Oxpecker | Review subagent/session | QA workflow layer |
| Prime Directives | System or protocol constants | Domain rules |
| Directives | Workspace memory/config files | Managed directive store |
| Lessons | Curated memory artifacts | Promotion workflow |
| Working Memory | Session context/history | Bounded buffer abstraction |
| Skill Library | Skills plus protocol packages | Skill packaging model |
| Gates | Approval checkpoints | Gate policy engine |
| Snapshots | Session state plus protocol store | Snapshot persistence |
| Fleet | Multi-agent routing | Fleet registry and comms layer |
| Uhura | Messaging guardrails and hooks | Secure comms adapter |
| Captain's Log | Logs and memory files | Structured log subsystem |

## First Build Target
The smartest first milestone is not the whole fleet fantasy. It is:

### Mission Engine v0
A local prototype that can:
1. define a Starship with a Captain and a few Specialists
2. create a mission
3. decompose it into tasks
4. assign tasks to workers
5. require configurable gate approvals
6. route outputs through a review step
7. persist mission state locally

If that works, the rest becomes expansion instead of wishful thinking.

## What I Recommend We Build First

### Milestone 1
Protocol core models plus a tiny local mission runner.

Deliverables:
- Python package scaffold
- starship, chameleon, officer, captain, specialist, oxpecker models
- gate config model
- mission model
- stardate utility
- captain's log persistence
- JSON or SQLite persistence

### Milestone 2
OpenClaw integration.

Deliverables:
- session adapter
- subagent-backed specialist execution
- managed directive and lesson store
- simple approval workflow
- audit trail

### Milestone 3
Operator experience.

Deliverables:
- CLI commands
- dashboard report output
- optional GUI
- bootstrap installer and container packaging

## Risks and Tensions
- the protocol is broad enough to become a fork-shaped trap
- some ideas are conceptual metaphors, not yet concrete engineering requirements
- review chains can become expensive and slow if we literalize every Oxpecker and peer review role
- there is overlap with native OpenClaw features, so careless implementation will duplicate instead of extend

## Strong Recommendation
Treat the protocol as:
- an orchestration and governance layer over OpenClaw
- implemented incrementally
- proven with one mission engine before fleet and GUI work

That is the path least likely to explode beautifully in vacuum.
