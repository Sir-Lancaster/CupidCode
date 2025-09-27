*Chat GPT was used in the creation of this document.*
# Cupid Code High-Level Design Document
Sprint Leader: Kayden Lancaster

Sprint Followers: Zac Cunningham, Greg Steele, Dallin Tew, Carter Johnson

## Contents
  - [Introduction](#1-introduction)
  - [Sysem Overview](#2-system-overview----kayden)
  - [Architecture](#3-architecture----carter)
  - [Major Components](#4-major-components----dallin)
  - [External Interfaces](#5-external-interfaces----dallin)
  - [User Interface Design](#6-user-interface-design----zac)
  - [Input and Output](#7-input-and-output----zac)
  - [Security](#8-security----carter)
  - [Risks and Mitigations](#9-risks-and-mitigation----greg)
  - [Data Design](#10-data-design----greg)
  - [Diagrams](#11-diagrams----all)
## 1. Introduction
**Purpose**  
Provide a concise high‑level technical design for the current Cupid Code platform so the team can complete an MVP that delivers the Must requirements (MoSCoW) for 2025–2026. This document aligns inherited code (frontend Vue app + Django backend) with the updated requirements specification and guides subsequent detailed design, implementation, and risk mitigation.

**Scope**  
Covers:  
- System context and current vs planned capabilities (AI assist, gigs, payments, notifications).  
- Architectural style (web client + Django REST backend) and core component boundaries.  
- Roles and data domains (Dater, Cupid, Manager/Admin, Couple/Shared).  
- High‑level data handling (profiles, gigs, feedback, authentication, future payments, AI session artifacts).  
- Integration points (future: Stripe, PayPal, weather, messaging, location).  
Excludes: low‑level class diagrams, detailed endpoint specs, test plans, deployment runbooks (to be documented separately). References: Requirements Specification (requirements.md) for authoritative functional, nonfunctional, business, and user requirements.

**Audience**  
- Engineering team members adding features (AI, payments, notifications).  
- Product/managerial stakeholders validating scope vs requirements.  
- Security/review stakeholders assessing data handling and role boundaries.  
- New contributors needing a structural overview before reading code.

**Goals Alignment (Selected Musts)**  
- Real‑time AI feedback (listen + chat).  
- Multi‑role web access (desktop + mobile browsers).  
- External notifications (email/SMS planned).  
- Secure data handling & age gating.  
- Future payment rails (Stripe/PayPal) for funding and Cupid payouts.  
- Maintain extensibility for couple features and auditability.

**Non‑Goals (Current Release)**  
- Native mobile apps.  
- Full subscription tiering or microtransactions (explicit Won’t).  
- Full multilingual & advanced analytics dashboards (later phases).  

## 2. System Overview -- Kayden
**System Description**  
Cupid Code is a role‑based web application that assists users (primarily socially anxious or inexperienced daters) with AI‑driven, context‑aware coaching and on‑demand human “Cupid” gig interventions. The platform delivers:  
- Dater experience: AI chat + (future) passive listening for live guidance; scheduling and gig request flows.  
- Cupid experience: Manage gigs, respond to interventions, (future) earnings and availability.  
- Manager/Admin: User oversight, future compliance/reporting, operational dashboards.  
- Couple extension (Should/Could): Shared calendar, joint preferences, gift/timeline concepts.  
Current stack:  
- Frontend: Vue 3 (Vite) SPA (router, components under src/, role‑specific views).  
- Backend: Django + Django REST style views (api app) with SQLite (to migrate to managed cloud DB).  
- Auth: Username/password (working), role persisted in backend models.  
- AI: Placeholder endpoints; microphone capture pipeline present; logic for real guidance still minimal.  
- Storage: Local DB for users, gigs, feedback scaffolding (see server/api/models.py).  
- Tests: Selenium UI scripts for login and role flows.  

**Legacy System Overview**  
Inherited (working or partial):  
- Authentication & role assignment.  
- Basic Vue SPA routing and layout.  
- Gig creation UI (no financial settlement).  
- Audio capture scaffolding + placeholders for AI responses.  
Partial / incomplete (to be delivered):  
- Funds pipeline (balances, deposits via Stripe/PayPal, payouts).  
- Real‑time notifications (web + external email/SMS).  
- AI reasoning + personalized memory (user preference persistence & adaptive coaching).  
- Cupid availability / scheduling logic validation.  
- Feedback loops (post‑gig rating, AI reflection).  
- Security hardening (encryption fixes, PII handling, audit trails).  

**Planned Enhancements (Near Term)**  
- Integrate payment providers (abstracted service layer).  
- AI session store referencing user profile + prior date context.  
- Notification subsystem (queued + provider adapters).  
- Role‑segregated data views and future couple privacy controls.  
- Deployment to Azure (containerized or managed app service).  

**Key Constraints / Assumptions**  
- Must remain web-first; performance acceptable for real‑time guidance within latency budgets (<1–2s AI round trip after backend integration).  
- Incremental migration from SQLite to Azure Postgres/MySQL once payment + audit features start (avoids migration pain later).  
- Privacy: Microphone streaming only opt‑in per session; no permanent raw audio retention (derived features only).  

**High-Level Data Domains**  
- Identity & Roles (User, DaterProfile, CupidProfile, Manager/Admin).  
- Scheduling & Gigs (gig requests, status, Cupid assignment, intervention notes).  
- AI Interaction (chat transcripts, advice events, memory embeddings—planned).  
- Financial (wallet, transactions, payouts—planned).  
- Feedback & Ratings (post‑gig + AI evaluation—planned).  
- Notifications (in-app + external dispatch queue—planned).  

**External / Future Integrations**  
- Payments: Stripe, PayPal (Must).  
- Weather API (Could) for contextual planning.  
- Location services (Could) for Cupid tracking.  
- Dating app API linking (Could).  
- Email/SMS provider (Twilio / SendGrid) for push-out notifications (Must for notifications objective).  

**Quality & NFR Priorities (Short Term)**  
- Security remediation (address encryption misuse, card storage via tokenization not raw DB).  
- Accessibility improvements (contrast, screen reader semantics in Vue components).  
- Reliability: Graceful degradation when AI or payment providers unavailable.  

**Architecture Diagram (Placeholder)**  
(Will depict: Browser SPA (Vue) → REST/JSON API (Django) → Data Layer (DB + future cache) → External Services (AI API, Stripe, PayPal, Email/SMS, Weather). Will be added in Section 11.)

**Success Criteria for This Phase**  
- End-to-end flow: Dater logs in → requests AI help → receives contextual response referencing stored preferences.  
- Cupid gig lifecycle visible (create → assign placeholder → mark complete).  
- Stubs for payment & notification services integrated behind clear service interfaces to enable parallel work streams.  


## 3. Architecture -- Carter
- **Chosen Architecture:** (e.g., client-server, microservices, monolith)
- **Design Rationale:** Why was this architecture chosen?

## 4. Major Components -- Dallin
For each component:
- **Name:**
- **Responsibilities:**
- **Technologies Used:**
- **Internal Interfaces:** How does it communicate with other components?

## 5. External Interfaces -- Dallin
- **Third-Party APIs/Services:** List and describe each (e.g., Stripe, PayPal, notification services).
- **Protocols/Data Formats:** (e.g., REST, WebSocket, JSON)

## 6. User Interface Design -- Zac
**UI/UX Principles**
- Cupid codes redesign aims to make users' experience frustration-free by simplifying the overall design.
- Part of the redesign includes making the UI a mobile-first responsive design.                              
- Navigation will adhere to the standard of 2 clicks to get anywhere from the home page.   
- Cupid code aims to be accessible to all, which is why the color palettes were selected with color blindness in mind.

**Rebranding and Color Schemes**
As part of the Rebranding for Cupid Code, our team has decided to lean into who our users are and focus the color scheme and logos around them.
Our main users, the daters, are comprised of tech enthusiasts; for this reason, we have decided to give the app a more techy vibe and style the app around the terminal. 
- The rebranding will feature a new logo designed to resemble intricate code elements.
- Buttons that have graphics will also follow the new rebranding and look like code.
- The color scheme we have selected is based on the look of a terminal.
        - Dark background
        - light green words
        - minimal other colors
- the colors we have selected in hex are (from right to left)
        - #FB3640
        - #1F487E
        - #00CCFF
        - #09A129
        - #000000
 **Insert Image Here** 

- This color scheme aligns with our tech-driven vibe, ensuring the users feel right at home.
- Accessibility is essential to our team, so we have compared our color scheme to the following color blindness types, and we have included an image of that comparison for each.

**Protanopia**

IMAGE GOES HERE

**Deuteranopia** 

IMAGE GOES HERE

**Tritanopia**

IMAGE GOES HERE 

**Achromatopsia**

IMAGE GOES HERE

**Protanomaly**

IMAGE GOES HERE

**Deuteranomaly** 

IMAGE GOES HERE

**Tritanomaly**

IMAGE GOES HERE

**Achromatomaly**

IMAGE GOES HERE

- Most Color Blindnesses are compatible with our color scheme.
- To ensure all can see and use our app efficiently, we will be adding an Accessibility mode.
- The Accessibility mode will make the following changes.
        - The black background (#000000) will change to a white background (#FFFFFF)
        - The Green Text (#09A129) will be changed to Black (#000000)

        IMAGE OF NEW COLOR PALETTE
- Accessibility mode will be easily accessible from the home screen.


- **Navigation Flow:**
- **Wireframes/Mockups:** (Insert or link to images)

## 7. Input and Output -- Zac
- **Types of Input:** (User actions, external data, etc.)
- **Types of Output:** (UI updates, notifications, reports)
- **Expected Volume:** (If relevant)

## 8. Security -- Carter
- **Security at Each Layer:** (OS, application, network, data)
- **Sensitive Data Handling:**
- **Compliance Considerations:** (e.g., GDPR)

## 9. Risks and Mitigation -- Greg
- **Key Risks:**
- **Mitigation Strategies:**

## 10. Data Design
### 10.1 Scope & Goals
Define the persistent data model that supports current MVP plus near‑term roadmap (AI coaching, gigs, notifications, payments groundwork) while enabling secure handling of PII (Personal Identifiable Information) and future analytics. Emphasis: clarity of entity boundaries, minimal PII, auditability, forward migration (SQLite→Postgres), and extensibility.

### 10.2 Core Entities Overview
| Entity | Purpose | Key Relationships |
|--------|---------|------------------|
| User | Auth identity + global role flags | 1–1 UserProfile; 0–1 DaterProfile; 0–1 CupidProfile |
| UserProfile | General profile & demographics | FK user |
| DaterProfile | Dater‑specific preferences/context | FK user |
| CupidProfile | Cupid availability, rating meta | FK user |
| Gig | Requested intervention / coaching task | FK requester (User); 0–1 GigAssignment |
| GigAssignment | Links a Gig to a Cupid + status workflow | FK gig; FK cupid (User) |
| AISession | Logical AI coaching session (chat or listen) | FK user; 1–M AIMessage |
| AIMessage | Individual exchange (user or AI) | FK ai_session |
| Notification | Outbound or in‑app notification record | FK user (recipient) |
| Payment | High‑level payment intent / order meta | FK user (payer); 1–M Transaction |
| Transaction | Ledger-style entry (charges, payouts) | FK payment (nullable for system credits) |
| Subscription | (Future) recurring access model | FK user |
| Feedback | Ratings/comments about Gig or AI session | FK user (author); optional FK gig / ai_session |
| AuditLog | Immutable security/business critical events | FK user (actor, optional) |
| FeatureFlag | Runtime controlled experiment/config | — |
| KeyRotationEvent | Tracks encryption key versions | — |

(Implementation can defer some entities until needed; still model them conceptually.)

### 10.3 Entity Details (Selected MVP Focus)
Provide deeper specs for those landing in MVP:

1. User  
  - Fields: id (UUID), username, email (unique), password_hash, roles (bitmask or enum list), is_active, created_at, last_login_at.  
  - Notes: email optional for early dev? Decide; password hashing: Argon2id (time & memory cost documented).  

2. UserProfile  
  - Fields: id, user_id (FK), display_name, date_of_birth (PII), timezone, pronouns, created_at, updated_at.  
  - Derived: age (computed, not stored).  
  - Privacy: date_of_birth encrypted (AES-256-GCM) at application layer.  

3. DaterProfile  
  - Fields: id, user_id, goals (text), comfort_level (enum), interests (JSON array), boundaries (text), ai_persona_prefs (JSON), updated_at.  

4. CupidProfile  
  - Fields: id, user_id, bio, experience_years, availability_calendar_ref, avg_rating_cache, payout_account_token (external provider token, never raw credentials).  

5. Gig  
  - Fields: id, requester_user_id, title, description, status (requested|matched|in_progress|completed|cancelled), scheduled_for (datetime), created_at, updated_at.  
  - Indexes: (requester_user_id, created_at), status.  

6. GigAssignment  
  - Fields: id, gig_id (unique), cupid_user_id, accepted_at, completed_at, cancelled_at, cancel_reason.  
  - Constraint: 1–1 with Gig; gig.status kept consistent via service layer.  

7. AISession  
  - Fields: id, user_id, mode (chat|listen), started_at, ended_at, context_snapshot (JSON), model_version, cost_tokens_estimate.  

8. AIMessage  
  - Fields: id, ai_session_id, role (user|assistant|system), content (text), tokens_in, tokens_out, created_at.  
  - Index: (ai_session_id, created_at).  

9. Notification  
  - Fields: id, user_id, channel (in_app|email|sms), template_key, payload (JSON), status (queued|sent|failed), sent_at, failure_reason.  

10. Payment  
  - Fields: id, user_id, provider (stripe|paypal|test), external_intent_id, amount_cents, currency, purpose (gig_fee|subscription|top_up|payout_reversal), status (initiated|succeeded|failed|refunded), created_at.  

11. Transaction  
  - Fields: id, payment_id (nullable), user_id (owner), direction (debit|credit), amount_cents, currency, balance_after_cents, type (fee|payout|charge|adjustment), created_at.  
  - Invariant: Sum of transactions per user reflects virtual wallet balance; enforce with service-level locking.  

12. Feedback  
  - Fields: id, user_id, gig_id?, ai_session_id?, rating (1–5), comment, created_at.  

13. AuditLog  
  - Fields: id, actor_user_id?, event_type, object_type, object_id, metadata (JSON), created_at, ip_hash.  
  - Immutability: No updates, only inserts; optionally partition by month.  

### 10.5 Sensitive Data & Protection Plan
| Field | Entity | Classification | Protection | Notes |
|-------|--------|---------------|-----------|-------|
| password_hash | User | Restricted | Argon2id | Cost factors documented |
| email | User | Confidential | Stored plaintext + unique idx; optional SHA256(salt) for analytics matching | Redact in logs |
| date_of_birth | UserProfile | PII | AES-256-GCM app-layer | Age gating derived |
| payout_account_token | CupidProfile | Confidential | Opaque token from payment provider | No raw banking data |
| ip_hash | AuditLog | Pseudonymized | SHA256(ip + rotating_salt) | Salt rotates yearly |
| access_token_hash | (AuthToken) | Restricted | HMAC-SHA256 | Raw token only client-side |
| refresh_token_hash | (AuthToken) | Restricted | HMAC-SHA256 | Rotation on use |
| boundaries / goals | DaterProfile | Sensitive (behavioral) | At-rest DB encryption (optional future) | Consider field-level encryption |
| content (AIMessage) | AIMessage | Potentially Sensitive | Retention-limited (≤90 days) | Anonymize older rows |
| external_intent_id | Payment | Confidential | Plain, indexed | Not PAN |

Encryption / Key Management:
- Keys: Stored in Azure Key Vault (KMS) referenced via env variable indirection.
- Key Versioning: key_version column or metadata stored in KeyRotationEvent.
- Rotation Cadence: Annual for data keys; immediate on incident.
- Logging: Exclude sensitive fields (structured logger denylist).

### 10.6 Data Flow (High-Level)
1. User registers → User + UserProfile rows persisted; AuditLog event.
2. Dater starts AI session → AISession row, subsequent AIMessage rows stream in.
3. Gig created → Gig row; on Cupid assignment create GigAssignment + Notification queue.
4. Payment initiated → Payment (initiated) + external provider intent; success webhooks finalize status, create Transaction(s).
5. Feedback submitted → Feedback row; may update CupidProfile.avg_rating_cache via async job.

(Sequence diagrams will visualize 2, 3, 4 in Section 11.)

### 10.7 Constraints & Integrity Rules
- GigAssignment.gig_id unique (one active assignment).
- Feedback must reference exactly one of (gig_id, ai_session_id), not both (CHECK constraint).
- Transaction.amount_cents > 0; direction + sign enforced in service layer.
- AuditLog immutable (no UPDATE/DELETE).
- Soft deletion (if introduced) uses deleted_at; queries exclude by default.

### 10.8 Indexing & Performance (Initial)
| Table | Index | Rationale |
|-------|-------|-----------|
| User | (username), (email) | Auth lookups |
| Gig | (status, scheduled_for) | Dashboard filtering |
| GigAssignment | (cupid_user_id, accepted_at) | Cupid workload |
| AIMessage | (ai_session_id, created_at) | Chronological retrieval |
| Notification | (status, channel) | Queue processing |
| Transaction | (user_id, created_at) | Balance & statements |
| AuditLog | (event_type, created_at DESC) | Filtering audits |

Review after real data to add composite or partial indexes (e.g., notifications where status=queued).

### 10.9 SQLite → Postgres Migration Strategy
Steps:
1. Freeze schema changes (migration branch).
2. Ensure all Django migrations deterministic & squashed if excessive.
3. Add migration health script (checks constraints, null anomalies).
4. Provision Postgres (dev/stage) with identical charset & timezone UTC.
5. Dry run: migrate schema → load anonymized fixture data.
6. Validate row counts, sample checksums (per table).
7. Switch app config for staging; run integration tests (auth, AI stubs, gig lifecycle).
8. Production cutover: maintenance window (if needed) → dump SQLite → transform (scripts) → load → run post‑load verification.
Rollback: point-in-time snapshot (before switch) + revert env config.

### 10.10 Retention & Deletion Policy (Draft)
| Entity | Retention | Action on Delete Request | Rationale |
|--------|-----------|--------------------------|-----------|
| UserProfile (PII) | Active + 30 days grace | Hard delete after grace if no legal hold | Privacy |
| DaterProfile | Active + 30 days | Hard delete | Minimal legacy value |
| CupidProfile | Active + 1 year after inactivity | Anonymize payout_account_token | Accounting audit |
| AISession / AIMessage | 90 days (content) | Anonymize earlier (remove free text, keep counts) | Reduce sensitive text footprint |
| Gig / GigAssignment | 1 year | Anonymize requester & cupid (replace with surrogate) after 1 year | Operational analytics |
| Payment / Transaction | 7 years | Retain; detach user by surrogate if account deleted | Financial compliance |
| Feedback | 1 year | Anonymize user_id | Trend analytics |
| AuditLog | 7 years | Retain (no PII beyond hashed IP) | Security & compliance |
| Notification | 30 days | Hard delete | Low value after sent |

Deletion Workflow:
1. User submits deletion → queue job.
2. Verify pending financial / compliance holds.
3. Execute anonymization + deletions transactionally (with retry).
4. Record AuditLog event (user_deleted).

### 10.11 Backup & Restore
- Engine: Postgres native base backup + WAL archiving.
- Frequency: Full daily @ 02:00 UTC; WAL continuous.
- Retention: 30 days full; WAL 7 days.
- Encryption: Storage-level + server-side KMS.
- RPO: ≤15 min. RTO: ≤60 min.
- Quarterly restore drill: script executes automated restore & checksum compare per critical table sample.

### 10.12 Data Quality & Observability
Checks:
- Pre-deploy migration validator (foreign key, null anomalies, enum values).
- Post-migration counts & random row hash sampling.
Metrics (exported via Prometheus):
- db_slow_query_p95
- ai_message_write_latency
- transaction_balance_mismatch (gauge should stay 0)
- notification_queue_depth
Alerts:
- Queue depth > 500 for 10m
- Slow query p95 > 400ms sustained 30m

### 10.13 Scaling Roadmap
Phase 1: Single Postgres instance (primary).  
Phase 2 Trigger: Read-heavy (AIMessage, AuditLog) > 70% read load → introduce read replica for reporting.  
Phase 3 Trigger: AIMessage volume > 50M rows → partition by month or move cold partitions to cheaper storage.  
Caching Targets (later): UserProfile (hot), FeatureFlags (global), Gig status board (per Cupid).  
Potential Future: Move Notification and AuditLog to append-only event store (e.g., separate logical DB).

### 10.14 Open Questions / Decisions Needed
| Topic | Question | Owner | Due |
|-------|----------|-------|-----|
| Email hashing | Hash email for analytics or rely on deterministic lowercasing? | Data Lead | TBD |
| Field-level encryption scope | Encrypt DaterProfile.behavioral fields now or defer? | Security | TBD |
| Token model | Sessions only vs add refresh token rotation? | Auth | TBD |
| Multi-tenancy | Any future white-label need? Impacts schema prefixing. | Product | TBD |

### 10.15 Deliverables To Add (Artifacts)
- er_diagram.png (C4-ish + ER overlay).
- data_dictionary.md (expanded fields, types, constraints).
- retention_matrix.md (table above formalized).
- migration_playbook.md (step list).
- encryption_key_policy.md (rotation, storage, incident response).

(Section 11 will reference the ER and key sequence diagrams.)

## 11. Diagrams -- All
- **Architecture Diagram**
- **Component Diagram**
- **Sequence Diagram(s)**
- **Use Case Diagram(s)**


