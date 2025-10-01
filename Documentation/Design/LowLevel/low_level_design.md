# Low-Level Design

Sprint Leader: Kayden Lancaster
Team: Zac Cunningham, Greg Steele, Dallin Tew, Carter Johnson

## 1. Introduction

Purpose of the LLD (blueprint for implementation).

Scope (aligns with HLD; no divergence unless justified).

Document conventions (UML, naming, diagrams).

## 2. System Architecture (Detailed View)

Finalized architecture diagram (with updated detail: services, components, APIs).

Alternatives considered (e.g., monolith vs microservices, database options).

Rationale for final design.

## 3. Subsystems & Class Design

For each subsystem: Auth/Identity, Gig Scheduling, Messaging/AI, Payments, Notifications, Admin/Manager Dashboard, UI (Frontend Vue)

For each:

Responsibilities (specific role in system).

Class Breakdown (detailed class list, adhering to SRP).

UML Class Diagrams (fields, methods, relationships).

Design Choices & Alternatives (inheritance vs composition, why chosen).

Edge Cases considered.

## 4. Database Design

Schema definition (tables, columns, types, constraints).

Normalization (3NF justification).

ER Diagram (updated with refactors).

Sensitive Data Handling (encrypted fields, tokens for payments, retention rules).

Refactor Plan (from current SQLite → Azure Postgres).

## 5. Performance Considerations

Potential bottlenecks (AI latency, payments, notifications, DB joins).

Mitigation strategies (caching, indexing, async jobs, autoscaling).

Scaling plan (load increases: DB vertical/horizontal scaling, queueing).

## 6. Security Design

Threat model (specific to Cupid Code).

Mitigations (auth hardening, encryption at rest/in transit, RBAC, tokenization).

Alternatives considered (e.g., JWT vs session cookies).

Justification of final approach.

## 7. User Interface & Experience

Wireframes/prototypes (for all roles: Dater, Cupid, Manager/Admin).

Accessibility support (color blindness mode, keyboard navigation).

Usability considerations (2-click navigation, mobile-first design).

User flows for key actions (sign up, gig request, payment, feedback).

## 8. Technology Stack

Languages, frameworks, libraries (Vue, Django, DRF, Celery, Redis, Stripe SDK).

Justification of choices (community support, scalability, team skillset).

Alternatives considered (React vs Vue, Flask vs Django, etc.).

## 9. Deployment Plan

Environments (Dev, Staging, Prod).

Deployment pipeline (CI/CD, Azure App Services, containers).

Secrets management (Azure Key Vault).

Monitoring/logging strategy.

## 10. Testing & Monitoring

Unit test strategy (per subsystem).

Integration and E2E testing (Selenium, API tests).

Automated test coverage goals.

Monitoring (Azure Sentinel, alerting, log aggregation).

## 11. Appendices

UML diagrams (class, sequence, ER).

Wireframes and user flow diagrams.