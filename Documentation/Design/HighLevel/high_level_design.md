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
Provide a concise high‑level technical design for the current Cupid Code platform so the team can complete an MVP (Minimum Viable Product) that delivers the Must requirements (MoSCoW) for 2025–2026. This document aligns inherited code (frontend Vue app + Django backend) with the updated requirements specification and guides subsequent detailed design, implementation, and risk mitigation.

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
Current schema (SQLite) implements merged role+profile patterns (Dater, Cupid) and an early Gig workflow. Several security‑sensitive financial storage models (PaymentCard, BankAccount) exist that must be deprecated before production. Goal: Stabilize current entities, schedule refactors (AI session separation, payment tokenization, assignment abstraction), and remove unsafe PCI data.

### 10.2 Entity Inventory: Implemented vs Planned
| Entity (Code Name) | Implemented? | Purpose (Current) | Planned Change / Future Name |
|--------------------|-------------|-------------------|------------------------------|
| User               | Yes         | Auth + role + phone_number | Add UUID PK (optional), audit fields |
| Dater (OneToOne User) | Yes      | Extended dater attributes & metrics | Rename to DaterProfile; trim large free‑text fields; encrypt selected PII |
| Cupid (OneToOne User) | Yes      | Cupid state & performance stats | Rename to CupidProfile; add availability & payout token (no raw banking) |
| Gig                | Yes         | Match Dater to Cupid + status | Extract GigAssignment (separate Cupid link + timestamps) |
| Quest              | Yes         | Requested items / context for a Gig | Fold into Gig (JSON) or keep normalized; evaluate |
| Message            | Yes         | Mixed user + AI chat entries (from_ai flag) | Split into AISession + AIMessage (session metadata, tokens) |
| Date               | Yes         | Scheduled date event (planning) | Keep; may relate to future couple/shared features |
| Feedback           | Yes         | Star rating + message for a Gig (owner→target) | Add XOR validation (only one target type later) |
| PaymentCard        | Yes (Unsafe) | Stores raw card PAN + CVV (PCI scope) | REMOVE: Replace with PaymentMethodToken (Stripe) |
| BankAccount        | Yes (Unsafe) | Stores raw routing/account numbers | REMOVE: External payout provider token only |
| Subscription       | No          | Future recurring access | Add after payment rails established |
| Transaction        | No          | Ledger / wallet accounting | Add with payments (Stripe webhooks) |
| Payment (Intent)   | No          | Track provider intent/status | Add before enabling real payments |
| Notification       | No          | Queue of outbound messages | Add (email/SMS + in‑app) |
| AuditLog           | No          | Immutable security/business events | Add (append‑only) |
| FeatureFlag        | No          | Runtime configuration | Add (simple key/value) |
| KeyRotationEvent   | No          | Track encryption key usage | Add with encryption rollout |

### 10.3 Current Entity Details (from /code/server/api/models.py)
(Fields summarized; omit Django implicit id unless primary key overridden.)

User  
- Fields: id (int PK), username, email, password, role (dater|cupid|manager), phone_number (unique, length=10).  
- Gaps: No created_at/updated_at audit timestamps; no soft delete; no MFA.

Dater  
- PK: user (OneToOne).  
- Key Fields: budget, communication_preference, multiple narrative TextFields (description, strengths, weaknesses, interests, past, nerd_type, relationship_goals), ai_degree, cupid_cash_balance, location, rating_sum/rating_count, is_suspended, profile_picture.  
- Observations: Many large free‑text fields (potential PII/behavioral); no structured enums; separate rating_sum/count used for aggregation.

Cupid  
- PK: user (OneToOne).  
- Fields: accepting_gigs, gigs_completed/failed, status (enum int), cupid_cash_balance, location, gig_range, rating_sum/count, is_suspended.  
- Issue: save() mutates self.user via username lookup (fragile) — prefer direct FK reference already present.

Message  
- Fields: owner (FK User), text, from_ai (bool).  
- Limitation: No session correlation, no token counts, no ordering index, no retention label.

Quest  
- Fields: budget, items_requested, pickup_location.  
- Single OneToOne on Gig; potentially mergeable.

Gig  
- Fields: dater (FK Dater), cupid (FK Cupid nullable), status (UNCLAIMED|CLAIMED|COMPLETE), date_time_of_request (auto), date_time_of_claim, date_time_of_completion, quest (OneToOne), dropped_count, accepted_count.  
- Missing: Explicit monetary, title/description, cancellation reason, normalized assignment audit.

Date  
- Fields: dater, date_time, location, description, status (planned|occurring|past|canceled), budget.  
- Not referenced elsewhere yet.

Feedback  
- Fields: owner (nullable, SET_NULL), target (User), gig, message, star_rating, date_time.  
- Missing: Constraints on rating range (validation), no uniqueness (duplicate ratings possible).

PaymentCard (To Remove)  
- Raw card_number, cvv, expiration stored as TextField. HIGH RISK.

BankAccount (To Remove)  
- Raw routing_number, account_number stored in cleartext. HIGH RISK.

### 10.4 Required Refactors & Tickets
| Priority | Action | Rationale |
|----------|--------|-----------|
| Critical | Remove PaymentCard & BankAccount before prod; migrate to external tokenization (Stripe) | Eliminate PCI scope & breach risk |
| High | Introduce AISession & AIMessage; migrate existing Message rows | Enables retention limits & analytics |
| High | Add created_at/updated_at (auto timestamps) to core entities | Auditing & troubleshooting |
| High | Replace Gig.cupid nullable with GigAssignment (Gig FK + Cupid FK + timestamps) | Normalizes lifecycle events |
| Medium | Consolidate / structure large Dater narrative fields (enum + JSON) | Queryability & privacy |
| Medium | Add soft delete or active flags (User, Dater, Cupid) | Regulatory deletes |
| Medium | Add Feedback constraints (rating 1–5, unique (owner,gig) ) | Data integrity |
| Medium | Add indexes (Gig.status, Message.owner + id) | Query performance |
| Low | Merge Quest into Gig JSON field or formalize separate use cases | Reduce joins |
| Low | Add AuditLog table | Security visibility |
| Low | Introduce FeatureFlag table | Safe gradual rollout |

### 10.5 Interim vs Target Model Mapping
| Conceptual (Original Doc) | Current Model | Gap / Plan |
|---------------------------|---------------|------------|
| UserProfile               | (Absent)      | Either add minimal profile table or keep fields in role models |
| DaterProfile              | Dater         | Rename + field review & encryption |
| CupidProfile              | Cupid         | Rename + availability expansion |
| GigAssignment             | (Inline cupid FK on Gig) | Create new table; move timestamps |
| AISession/AIMessage       | Message       | Split & migrate |
| Payment/Transaction       | (Absent)      | Add with Stripe integration |
| Notification              | (Absent)      | Add queue table + outbox pattern |
| AuditLog                  | (Absent)      | Add append-only table |

### 10.6 Sensitive Data & Protection 
| Field / Data | Location Now | Issue | Action |
|--------------|--------------|-------|--------|
| password (hashed) | User.password | OK (Django default PBKDF2) | Consider Argon2 config |
| phone_number | User.phone_number | PII (no format validation) | Add normalization + E.164 future |
| card_number / cvv / expiration | PaymentCard | Plaintext storage | DROP model; no raw card data |
| routing_number / account_number | BankAccount | Plaintext storage | DROP model; external payout token |
| location (text) | Dater/Cupid | Potential PII granularity | Define granularity or geocode tokenization |
| description / strengths / weaknesses / past / interests | Dater | Sensitive narrative | Consider classification + optional encryption |
| Message.text | Message | Sensitive conversation | Apply retention limit & later anonymization |
| rating_sum / rating_count | Dater/Cupid | Low sensitivity | OK |
| gig timestamps | Gig | OK | Ensure timezone UTC |

Planned Protection Additions:
- Application-layer field encryption (select narrative or location fields if stored long term).
- Tokenization for payouts (provider-managed).
- Retention jobs for Message (purge or anonymize after X days).

### 10.7 Data Flows (Tagging Current vs Planned)
1. Dater requests Gig (Implemented) → Gig row (status=UNCLAIMED).  
2. Cupid claims Gig (Implemented) → status=CLAIMED; future: create GigAssignment row.  
3. AI Chat (Partial) → Message rows (from_ai bool) — future: create AISession then AIMessage rows.  
4. Feedback submitted (Implemented) → Feedback row (no validation on duplicates).  
5. Payments & Notifications (Planned) → No current persistence (remove earlier implication).  

### 10.8 Constraints & Integrity (Current vs Needed)
Current Enforced:
- OneToOne (User ↔ Dater / Cupid).
- Foreign keys cascade (Gig→Dater/Cupid, Feedback→Gig/User).
- Unique phone_number.

Needed / Planned:
- CHECK rating 1–5 (Feedback).
- UNIQUE (owner, gig) on Feedback.
- UNIQUE (GigAssignment.gig_id) when introduced.
- NOT NULL defaults for Gig.status (already via choices).
- DB index additions (see 10.9).

### 10.9 Index & Performance Plan
Immediate (add migrations):
- Gig: index_together (status, date_time_of_request).
- Message: (owner_id, id) for chronological user queries.
- Feedback: (gig_id).
Post-Refactor:
- AIMessage: (session_id, created_at).
- GigAssignment: (cupid_id, created_at).
- Partial indexes (Postgres) for active gigs once migrated.

### 10.10 Migration / Refactor Strategy
Phase A (Pre-security hardening):
- Create migrations to add timestamps (auto_now_add / auto_now) where missing.
- Add indexes above.

Phase B (Security Remediation):
- Create new PaymentMethodToken model (provider, user FK, last4, brand, exp_month/year, provider_token).  
- Migrate (export + securely delete) then DROP PaymentCard & BankAccount tables.  
- Commit architecture doc update referencing Stripe vaulting.

Phase C (AI Session Separation):
- Add AISession + AIMessage tables.
- Backfill: For each unique (owner) contiguous Message block create session.

Phase D (Gig Assignment):
- Create GigAssignment; migrate existing cupid/time fields.
- Remove cupid FK from Gig (or keep nullable for fast access, but ensure consistency).

### 10.11 Retention & Deletion (Adjusted)
| Data | Interim Policy | Target Policy |
|------|----------------|---------------|
| Message.text | Stored indefinitely | 90 day retention / anonymize older |
| PaymentCard/BankAccount | Remove ASAP | Not stored (provider tokens only) |
| Dater narrative fields | Indefinite | Review & redact after 1 year inactivity |
| Gig lifecycle timestamps | Indefinite | Keep (low sensitivity) |
| Feedback | Indefinite | 1 year (anonymize author if user deleted) |

### 10.12 Backup & Restore
Current: Local SQLite (manual copy only).  
Target (pre-payments): Migrate to managed Postgres + daily logical backup + WAL. (Original backup plan retained but not yet applicable.)

### 10.13 Open Decisions
| Topic | Question | Status |
|-------|----------|--------|
| Drop raw financial tables timeline | Before first external test user? | Decide date |
| Introduce UUID PKs | Worth migration or keep int? | Evaluate |
| Encrypt narrative fields | Scope vs performance | Assess after MVP |
| Merge Quest into Gig | Simplify vs future reuse | Pending |
| Session model necessity now | Defer until AI metrics needed? | Decide Sprint N |

### 10.14 Artifacts To Produce
- schema_snapshot.md (generated via inspectdb) — baseline.
- migration_plan_refactor.md (Phases A–D tasks).
- draft_models_future.py (proposed AISession, AIMessage, GigAssignment).
- risk_note_financial_data.md (documents removal of PaymentCard/BankAccount).

(Original conceptual entities retained above only where they map to planned refactors.)

## 11. Diagrams -- All
- **Architecture Diagram**
- **Component Diagram**
- **Sequence Diagram(s)**
- **Use Case Diagram(s)**


