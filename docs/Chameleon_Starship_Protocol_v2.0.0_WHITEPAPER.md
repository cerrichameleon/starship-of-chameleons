# Chameleon Starship Protocol

### An Object-Oriented AI Agent Orchestration System

**Version:** 2.0.0
**Status:** Draft
**Date:** March 17, 2026

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Core Architecture](#core-architecture)
3. [Class Definitions](#class-definitions)
4. [Interface Specifications](#interface-specifications)
5. [Memory System](#memory-system)
6. [Directive Injection Protocol](#directive-injection-protocol)
7. [Skill Library System](#skill-library-system)
8. [Traffic Light Approval Gates](#traffic-light-approval-gates)
9. [Oxpecker Assignment](#oxpecker-assignment)
10. [Peer Review Workflow](#peer-review-workflow)
11. [Version Control & Rollback](#version-control--rollback)
12. [Performance Dashboard](#performance-dashboard)
13. [Emergency Override System](#emergency-override-system)
14. [Mission Templates](#mission-templates)
15. [Cross-Room Collaboration](#cross-room-collaboration)
16. [Implementation Guidelines](#implementation-guidelines)
17. [Officer Class & Naval Rank System](#officer-class--naval-rank-system)
18. [Fleet Management](#fleet-management)
19. [Ship-to-Ship Communication](#ship-to-ship-communication)
20. [Metadata & Stardate System](#metadata--stardate-system)
21. [Captain's Log](#captains-log)
22. [Complete Feature List](#complete-feature-list)
23. [Uhura Security Pattern](#23-uhura-security-pattern)
24. [Chief Engineer & Resource Optimization System](#24-chief-engineer--resource-optimization-system)
25. [Starship Bootstrap & Deployment System](#25-starship-bootstrap--deployment-system)
26. [GUI Command Interface (Captain’s Console)](#26-gui-command-interface-captains-console)
27. [Containerization & Distribution Model](#27-containerization--distribution-model)
28. [Parallel Captain Communication Channel](#288-parallel-captain-communication-channel)

---

## 1. Executive Summary

The **Chameleon Starship Protocol** is a comprehensive orchestration framework for managing hierarchies of specialized AI agents, called **Chameleons**, to complete complex, multi-stage creative and technical projects.

Inspired by the adaptability of chameleons and the structured command of a starship bridge, the protocol defines:

- A universal base class (**Chameleon**) from which every agent inherits
- Two behavioral interfaces (**ISpecialist** and **IConductor**) that shape how agents operate
- A hierarchical command structure with Captains, Crew Captains, and Specialists
- A persistent memory system with working memory, lessons, directives, and immutable prime directives
- Quality assurance through **Oxpeckers**, dedicated review agents assigned to every entity
- **Traffic Light Gates** that give users granular control over automation levels
- A **Skill Library** for packaging and reusing validated expertise across agents

The system is designed to be human-in-the-loop by default, with all gates RED, progressively unlocking automation as trust is established. Every decision, output, and interaction is traceable, reversible, and governed by three immutable Prime Directives:

1. **Reduce Suffering**
2. **Increase Prosperity**
3. **Increase Understanding**

---

## 2. Core Architecture

### 2.1 Structural Overview

- One **Captain** per Starship
- Divisions containing Rooms
- Each Room led by a **Crew Captain**
- Rooms staffed by **Specialists**
- Every Chameleon supported by an **Oxpecker** review role
- Shared systems for Skill Library, Mission Engine, Version Control, Performance, Gate Management, and Directive Management

### 2.2 Design Principles

1. Inheritance over configuration
2. Composition via interfaces
3. Immutability at the core
4. Human-first automation
5. Observable state
6. Graceful degradation
7. Directive saturation

---

## 3. Class Definitions

### 3.1 Chameleon (Base Class)

Core properties:
- `chameleon_id`
- `name`
- `role_type`
- `reports_to`
- `prime_directives`
- `directives`
- `lessons`
- `working_memory`
- `status`
- `created_at`
- `version`

Core methods:
- `receive_directive()`
- `record_lesson()`
- `promote_lesson_to_directive()`
- `update_working_memory()`
- `get_execution_context()`
- `snapshot()`
- `restore()`

### 3.2 Captain

- Top-level orchestrator
- Receives missions from the user
- Decomposes missions into tasks
- Assigns to Crew Captains
- Manages gates
- Tracks performance
- Always asks gate configuration at mission start
- Has a dedicated advisory Oxpecker called **Number 1**

### 3.3 Crew Captain

- Room-level manager
- Receives tasks from Captain
- Assigns work to Specialists
- Manages peer review cycles
- Reports progress and issues
- Has a dedicated room Oxpecker

### 3.4 Specialist Roles

Example roles:
- Artist
- Writer
- Deepfacer
- Coder
- Reviewer

### 3.5 Oxpecker

- Review and QA role
- Every Chameleon gets a personal Oxpecker
- Every Room gets a room-level Oxpecker
- Captain gets **Number 1**
- Number 1 is advisory only and never blocks the Captain

---

## 4. Interface Specifications

### 4.1 ISpecialist

Behavior includes:
- `execute_task()`
- `submit_for_peer_review()`
- `conduct_peer_review()`
- `load_skill()`
- `get_quality_score()`

### 4.2 IConductor

Behavior includes:
- `decompose_mission()`
- `assign_task()`
- `route_output()`
- `check_gate()`
- `escalate()`
- `get_performance_report()`

---

## 5. Memory System

Four tiers:
1. Working Memory, ephemeral, last 10 interactions
2. Lessons, max 15 validated learnings
3. Directives, mutable role-specific operational rules
4. Prime Directives, immutable universal constraints

### 5.3 Lesson Lifecycle

Observation → Candidate Lesson → User Validation → Active Lesson, with paths to remain as lesson, be promoted to directive, or packaged into a skill.

---

## 6. Directive Injection Protocol

Every execution context is saturated with applicable directives, lessons, and guidelines.

Injection order:
1. Prime Directives
2. Role Directives
3. Task Directives
4. Active Lessons
5. Skill Directives
6. Working Memory Context

Conflict resolution:
- Prime Directives always win
- More specific overrides more general
- User-promoted directives override system defaults
- Most recent wins when specificity ties
- Unresolvable conflicts escalate to user

---

## 7. Skill Library System

Skills include:
- directives
- lessons
- compatible roles
- versioning metadata

Constraints:
- Max skills per Starship: 100
- Warning threshold: 90
- Auto-skill recommendation after 10+ approvals

---

## 8. Traffic Light Approval Gates

- **RED**: explicit approval required
- **YELLOW**: notify/check, auto-proceed after 1 hour timeout
- **GREEN**: full automation

Default: all gates RED.

---

## 9. Oxpecker Assignment

Rules:
- Every Specialist gets a personal Oxpecker
- Every Crew Captain gets a personal Oxpecker
- Every Room gets a room-level Oxpecker
- The Captain gets Number 1

Number 1 is advisory only.

---

## 10. Peer Review Workflow

Flow:
1. Specialist completes task
2. Personal Oxpecker reviews
3. Output enters room peer review queue
4. Other Specialists review
5. Feedback consolidated
6. Revisions if needed
7. Room Oxpecker performs final room review
8. Crew Captain routes to gate system

---

## 11. Version Control & Rollback

- Per-Chameleon snapshots
- Rollback restores mutable state
- Prime Directives remain unchanged
- Starship-level snapshots include all Chameleon states, skill library, gate configurations, mission progress, and performance history

---

## 12. Performance Dashboard

Metrics include:
- task completion rate
- approval rate
- revision count
- average task duration
- skill utilization
- gate distribution
- lesson creation rate
- escalation frequency

---

## 13. Emergency Override System

Commands:
- RESET
- ROLLBACK
- PAUSE
- RESUME
- DEBUG
- OVERRIDE_GATE
- KILL
- QUARANTINE

All require user authorization and full audit logging.

---

## 14. Mission Templates

Reusable workflow definitions for:
- task decomposition
- room configurations
- specialist assignments
- gate presets
- expected deliverables

Example mission type in the white paper: T-shirt design production.

---

## 15. Cross-Room Collaboration

Mechanisms:
- shared artifacts
- cross-room requests
- shared skills
- Captain-mediated coordination

Rules:
- approvals required across rooms/divisions
- interactions logged

---

## 16. Implementation Guidelines

Recommended startup pattern:
1. Initialize Starship
2. Set Prime Directives
3. Define mission
4. Ask gate preferences
5. Decompose mission
6. Execute through specialists and review
7. Iterate and build lessons/skills

Anti-patterns include:
- setting all gates to GREEN too early
- ignoring lesson curation
- overloading one room
- bypassing peer review for speed
- ignoring Number 1 recommendations

---

## 17. Officer Class & Naval Rank System

Introduces an **Officer** base class extending `Chameleon`.

Naval ranks from Ensign through Fleet Admiral.

Capabilities:
- rank validation
- promotion/demotion
- rank comparison
- ship command validation
- chain-of-command enforcement

Captain now extends Officer.

---

## 18. Fleet Management

Adds a **Fleet** system with:
- Starship registry
- fleet creation
- ship add/remove
- flagship designation
- fleet status reporting
- chain of command enumeration
- fleet-wide directives from Admirals

---

## 19. Ship-to-Ship Communication

Structured messaging types:
- HAIL
- REPORT
- DIRECTIVE
- DISTRESS
- BROADCAST
- PERSONAL
- ENCRYPTED

Includes CommunicationChannel, ShipToShipCommunicator, and FleetCommunicator abstractions.

---

## 20. Metadata & Stardate System

Stardate format:
- `YYYY.DDD.HHMM`

Used for:
- task metadata
- messages
- Captain’s Log entries
- fleet directives

---

## 21. Captain's Log

Structured journal with entry types:
- GENERAL
- MISSION
- PERSONNEL
- NAVIGATION
- COMMUNICATION
- INCIDENT
- PERSONAL

Stored as JSON under `logs/`.

---

## 22. Complete Feature List

The white paper includes a broad feature inventory spanning:
- core system structure
- memory and knowledge
- quality assurance
- automation control
- skill management
- reliability
- observability
- safety
- workflow reuse
- officer/rank system
- fleet management
- communication
- metadata/stardates
- Captain’s Log
- Uhura pattern

---

## 23. Uhura Security Pattern

Principle:
> Captain commands, Uhura communicates.

Security boundary:
- Captain does not directly open external channels or send messages
- Uhura validates, sanitizes, and logs communications
- Captain’s Log remains local/sandboxed

Purpose:
- prevent prompt-injected exfiltration
- create audit trails
- separate command authority from communication authority

---

## 24. Chief Engineer & Resource Optimization System

Purpose:
- adaptive model routing
- cost control
- provider management

Core rule:
- use the weakest model that can reliably complete the task
- escalate only when necessary

Modes:
- Frugal
- Balanced
- High Accuracy
- Night Shift
- Critical Mission

---

## 25. Starship Bootstrap & Deployment System

Purpose:
- one-click deployment of a fully operational Starship

Capabilities:
- auto-install OpenClaw
- configure agents/workspace
- secure API/OAuth setup
- launch GUI
- containerized runtime

---

## 26. GUI Command Interface (Captain’s Console)

Operator UI with panels for:
- Mission Control
- Engineering
- Security
- Crew Management
- Performance Dashboard

Goal: plain-English, low-friction controls.

---

## 27. Containerization & Distribution Model

Each Starship runs in a Docker container with:
- OpenClaw runtime
- agents
- GUI
- auth
- logs

Benefits:
- portability
- one-click deployment
- isolation
- safety

---

## 28.8 Parallel Captain Communication Channel

Principle:
- the Captain remains continuously accessible to the user during mission execution
- communication should run separately from mission execution so work is not interrupted unless explicitly commanded

Components:
- Captain Channel Service
- Mission Engine
- Control Bus
- Uhura Interface Layer

Design philosophy:
- the Captain remains on the bridge at all times
- communication observes and guides; it does not halt the machinery unless commanded

---

*This file is a local project copy captured from the user-provided white paper so the protocol spec remains available in the repository workspace.*
