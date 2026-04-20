# Protocol Direction

## Core Product Direction
The Chameleon Starship Protocol should sit on top of OpenClaw as an orchestration and governance layer.

OpenClaw provides the execution substrate:
- sessions
- subagents
- tools
- memory
- messaging
- approvals
- multi-agent capabilities

The protocol provides the structure:
- Captain as the sole primary user-facing interface
- internal hierarchy of specialists and support roles
- mission decomposition and routing
- approval and review policy
- persistent mission organization
- operator clarity

## Key Interaction Rule
The user primarily communicates with the Captain.
The Captain orchestrates everyone else.
This is a major product simplification and should stay central.

## Cost Control Rule
Oxpeckers must be used minimally and strategically.

They are quality control, not permanent shadow workers.
If Oxpeckers review every step of every task, costs will become unacceptable.

### Oxpecker Usage Policy
Use Oxpeckers for:
- final review on important deliverables
- high-risk outputs
- milestone checkpoints
- spot checks when quality drifts
- post-failure diagnosis

Avoid Oxpeckers for:
- every intermediate draft
- every routine task
- every low-risk iteration
- trivial internal coordination

## Chief Engineer Requirement
Do not forget the Engineer.

The protocol needs a Chief Engineer role responsible for:
- model selection
- provider routing
- cost optimization
- deciding when stronger models are actually needed
- keeping execution affordable

Core rule:
Use the weakest model that can reliably do the job.
Escalate only when necessary.

## Product Goal Horizon
Near-term: simple sample missions that prove the orchestration model works.
Mid-term: prototype missions with OpenClaw integration.
Long-term: support an ambitious mission such as building an Android video game.

## Recommended Sample Missions
Before attempting the Android game mission, prove the protocol on smaller jobs:

1. document mission
   - create a small design brief and route it through captain to specialist to final review

2. coding mission
   - make a tiny utility script with one coder specialist and one final review gate

3. content mission
   - generate a short landing page draft with minimal review and one approval checkpoint

4. multi-step build mission
   - plan, implement, and summarize a tiny feature with task decomposition and completion report

## Architecture Priorities Now
1. OpenClaw adapter layer
2. Captain-only user communication path
3. Chief Engineer cost-routing logic
4. minimal-use Oxpecker review policy
5. sample missions
6. later, Android game prototype mission
