*Artificial Intelligence (GitHub Copilot, ChatGPT) was used in the creation of this document*
# Low-Level Design

Sprint Leader: Kayden Lancaster
Team: Zac Cunningham, Greg Steele, Dallin Tew, Carter Johnson

### Contents
- [Introduction](#1-introduction)
- [System Architecture](#2-system-architecture-detailed-view)
- [Subsystem & Class Design](#3-subsystems--class-design)
- [Database Design](#4-database-design)
- [Performance Considerations](#5-performance-considerations)
- [Security Design](#6-security-design)
- [User Interface & Experience](#7-user-interface--experience)
- [Technology Stack](#8-technology-stack)
- [Deployment Plan](#9-deployment-plan)
- [Testing & Monitoring](#10-testing--monitoring)

## 1. Introduction

### Purpose
This Low‑Level Design (LLD) turns the Cupid Code high‑level vision into implementable specifications for an MVP that satisfies 2025–2026 Must requirements. It defines concrete data models and migrations, REST APIs and error contracts, service boundaries, background jobs, and security controls so engineers can build, test, and deploy with consistency.

### Scope
Covers:
- Frontend (Vue 3 + Vite SPA, router, components) and API client contracts.
- Backend (Django + DRF) endpoints, serializers, services, and signals.
- Data layer (SQLite dev → Azure PostgreSQL prod), schemas, indexes, migrations.
- Async jobs (Celery + Redis) for notifications, AI tasks, and long‑running work.
- Integrations (Stripe/PayPal tokenized payments, email/SMS providers).
- Config/ops (env config, secrets, observability, deployment assumptions on Azure).

Out of scope: microservices decomposition, native mobile apps, full analytics dashboards.

### Audience
- Engineers implementing features and infrastructure.
- Test engineers writing unit/integration/E2E tests.
- Tech leads and security reviewers validating decisions and controls.

### Assumptions and Constraints
- No raw card/bank data stored; payment methods use processor tokens (Stripe/PayPal).
- PII minimized; sensitive fields encrypted at rest; logs redacted.
- API versioning under /api/v1; additive changes favored.
- All timestamps UTC, ISO‑8601 over the wire.
- RBAC enforced at view and object level.
- Performance targets met via pagination, indexing, and async offloading.
- Cloud secrets via Azure Key Vault; CI/CD separates dev/staging/prod.

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

### 4.1 Current State
The current state uses SQLite for the database containers and Django models populate them. 

**Our current implemented entities are:**
- User
- Dater
- Cupid
- Gig
- Quest
- Message
- Date
- Feedback
- PaymentCard (will be depreciated)
- BankAccount (will be de preciated)

**What we need for an MVP (2025):**
- Timestamps on moddles
- Flattened gig Assignments
- Messages lack session content
- unsafe financial storage. Needs to be switched to Stripe third party.

### 4.2 Target Model (MVP)
**Keep/rename**
- User: 
  - built-in auth
  - role 
  - phone_number
  - add created_at
  - updated_at
  - consider soft_delete flag
- DaterProfile (rename Dater):
  - budget
  - communication_preference
  - location
  - rating_sum/count
  - profile_picture
  - review large narrative fields
- CupidProfile (rename Cupid): 
  - accepting_gigs
  - status
  - gig_range
  - rating_sum/count
  - add availability windows later
- Gig: 
  - dater_id
  - status
  - budget
  - time window
  - location
  - details JSON
  - counters
  - remove inline cupid FK after assignment split
- Date:
    - dater_id
    - date_time
    - location
    - description
    - status
    - budget
- Feedback: 
  - owner_id (nullable)
  - target_user_id
  - gig_id
  - message
  - stars (1–5)
  - created_at
  - unique (owner_id, gig_id)

**Add**
- GigAssignment:
  - gig_id (unique)
  - cupid_id
  - claimed_at
  - completed_at
  - canceled_at
  - cancellation_reason
- AISession: 
  - owner_id
  - started_at
  - ended_at
  - context JSON
  - retention_label
- AIMessage: 
  - session_id
  - role (user|ai|system)
  - text, tokens_in/out
  - created_at
  - index (session_id, created_at)
- PaymentMethodToken:
  - user_id
  - provider (stripe|paypal)
  - provider_token
  - brand
  - last4
  - exp_month
  - exp_year
  - unique (user_id, provider, provider_token)
- PaymentIntent: 
  - user_id
  - provider
  - intent_id
  - amount
  - currency
  - status
  - created_at
  - updated_at
  - metadata JSON
- Transaction: 
  - user_id
  - amount
  - currency
  - type (debit|credit)
  - source (payment|payout|adjustment)
  - external_id
  - created_at
- Notification: 
  - user_id
  - channel (email|sms|inapp)
  - template_key
  - payload JSON
  - status
  - created_at
  - sent_at
  - error
- AuditLog:
  - actor_user_id
  - action
  - object_type
  - object_id
  - metadata JSON
  - created_at (append-only)

**Remove**
- PaymentCard, BankAccount (unsafe; replace with Stripe)

### 4.3 Normalization & Constraints
- 3NF across core tables; relationships via FKs; avoid M2M for MVP
- Constraints:
  - Feedback: CHECK stars IN [1..5], UNIQUE (owner_id, gig_id)
  - GigAssignment: UNIQUE (gig_id), FKs to Gig and CupidProfile
  - AIMessage: FK to AISession, ON DELETE CASCADE
  - Notification/AuditLog: append-only (status updates allowed on Notification)
- Global rules: all timestamps UTC; prefer hard deletes with cascades unless policy requires soft delete

### 4.4 Sensitive Data Handling
- No PAN/CVV or bank numbers in DB; use Stripe/PayPal tokens (PaymentMethodToken)
- Encryption at rest (Azure Postgres) + optional field-level encryption for addresses and selected narratives
- Redact PII from logs; store only non-sensitive payment metadata
- Access control: decrypt sensitive fields only in authorized flows (e.g., assigned Cupid with consent)

### 4.5 Index & Query Plan
- User: UNIQUE (username), UNIQUE (phone_number)
- Gig: (status, date_time_of_request), (dater_id, status)
- GigAssignment: (cupid_id, claimed_at)
- AISession: (owner_id, started_at)
- AIMessage: (session_id, created_at)
- Feedback: (gig_id); UNIQUE (owner_id, gig_id)
- Notification: (status, created_at), (user_id, created_at)
- PaymentIntent/Transaction: (user_id, created_at), (external_id)

### 4.6 Migration Plan (SQLite → Azure Postgres)
- Step 1: 
  - Add migrations for new tables (GigAssignment, AISession, AIMessage, PaymentMethodToken, PaymentIntent, Transaction, Notification, AuditLog)
  - created_at/updated_at
- Step 2: 
  - Backfill data under feature flags:
    - GigAssignment from Gig.cupid + timestamps.
    - AISession/AIMessage by grouping Message rows per owner chronologically
- Step 3: 
  - Remove PaymentCard/BankAccount code paths
  - integrate Stripe/PayPal
  - export and securely purge
  - DROP tables
- Step 4: 
  - Provision Azure Postgres
  - set server/.env DATABASE_URL
  - run Django migrations against Postgres
- Step 5: 
  - Validate with smoke/E2E tests
  - compare record counts and invariants
  - promote cutover
- Rollback: 
  - restore Postgres snapshot
  - revert feature flags

### 4.7 ER Diagram (to be updated)
- Core: 
  - User 1–1 DaterProfile/CupidProfile
  - DaterProfile 1–* Gig
  - Gig 1–1 GigAssignment
  - Gig 1–* Feedback
  - User 1–* AISession 1–* AIMessage
  - User 1–* Notification
  - User 1–* Transaction
  - append-only AuditLog

### 4.8 Open Questions
- Merge Quest into Gig.details JSON or keep normalized?
- Field-level encryption scope: addresses only or selected narratives as well?
- Keep nullable Gig.cupid for denormalized reads after introducing GigAssignment?

### 4.9 Model Pseudocode (Github Copilot using ChatGPT 5)

Note: Pseudocode shaped like Python/Django models for clarity. Names map 1:1 to Section 4.2.

```python
# PSEUDOCODE — NEW TABLES

class GigAssignment:
    # FKs
    gig_id: FK -> Gig (unique)            # one assignment per gig
    cupid_id: FK -> CupidProfile

    # Lifecycle
    claimed_at: datetime?                 # set once on claim
    completed_at: datetime?               # set on completion
    canceled_at: datetime?                # set on cancel
    cancellation_reason: str?             # enum-like: USER_CANCELED|CUPID_NO_SHOW|OTHER

    # Derived status
    def status(self) -> str:
        if self.completed_at: return "COMPLETED"
        if self.canceled_at: return "CANCELED"
        if self.claimed_at: return "CLAIMED"
        return "UNCLAIMED"

    # Commands (validate invariants; idempotent)
    def claim(self, now):
        assert self.claimed_at is None and self.completed_at is None and self.canceled_at is None
        self.claimed_at = now

    def complete(self, now):
        assert self.claimed_at is not None and self.completed_at is None and self.canceled_at is None
        self.completed_at = now

    def cancel(self, now, reason):
        assert self.completed_at is None and self.canceled_at is None
        self.canceled_at = now
        self.cancellation_reason = reason

    class Meta:
        unique_together = [(gig_id,)]
        index_together = [(cupid_id, claimed_at)]
```

```python
class AISession:
    owner_id: FK -> User
    started_at: datetime = now()
    ended_at: datetime?
    context: JSON                         # e.g., profile snapshot, gig/date refs
    retention_label: str = "SHORT"        # SHORT|STANDARD|LONG (policy-driven)

    def end(self, now):
        if not self.ended_at:
            self.ended_at = now

    class Meta:
        index_together = [(owner_id, started_at)]
```

```python
class AIMessage:
    session_id: FK -> AISession (on delete cascade)
    role: str                             # "user" | "ai" | "system"
    text: str
    tokens_in: int = 0
    tokens_out: int = 0
    created_at: datetime = now()

    class Meta:
        index_together = [(session_id, created_at)]
```

```python
class PaymentMethodToken:
    user_id: FK -> User
    provider: str                         # "stripe" | "paypal"
    provider_token: str                   # e.g., pm_xxx or vaulted ID
    brand: str?                           # visa/mastercard
    last4: str?                           # masked digits
    exp_month: int?
    exp_year: int?

    class Meta:
        unique_together = [(user_id, provider, provider_token)]
        index_together = [(user_id, provider)]
```

```python
class PaymentIntent:
    user_id: FK -> User
    provider: str                         # "stripe" | "paypal"
    intent_id: str                        # provider reference
    amount: int                           # minor units (cents)
    currency: str = "USD"
    status: str = "REQUIRES_ACTION"       # REQUIRES_ACTION|PROCESSING|SUCCEEDED|FAILED|CANCELED
    metadata: JSON = {}

    created_at: datetime = now()
    updated_at: datetime = now()

    def mark_succeeded(self, now):
        self.status = "SUCCEEDED"; self.updated_at = now

    def mark_failed(self, now, err=None):
        self.status = "FAILED"; self.updated_at = now
        self.metadata["error"] = err

    class Meta:
        unique_together = [(provider, intent_id)]
        index_together = [(user_id, created_at)]
```

```python
class Transaction:
    user_id: FK -> User
    amount: int                           # positive integer in minor units
    currency: str = "USD"
    type: str                             # "debit" | "credit"
    source: str                           # "payment" | "payout" | "adjustment"
    external_id: str?                     # e.g., provider charge/payout id
    created_at: datetime = now()

    def validate_sign(self):
        # Convention: debit reduces balance; credit increases
        assert self.amount > 0

    class Meta:
        index_together = [(user_id, created_at)]
        unique_together = [(source, external_id)]  # when present
```

```python
class Notification:
    user_id: FK -> User
    channel: str                          # "email" | "sms" | "inapp"
    template_key: str                     # e.g., "gig_claimed", "payment_succeeded"
    payload: JSON                         # rendered variables
    status: str = "QUEUED"                # QUEUED|SENT|FAILED
    created_at: datetime = now()
    sent_at: datetime?
    error: str?

    def mark_sent(self, now):
        self.status = "SENT"; self.sent_at = now

    def mark_failed(self, now, err):
        self.status = "FAILED"; self.sent_at = now; self.error = err

    class Meta:
        index_together = [(status, created_at), (user_id, created_at)]
```

```python
class AuditLog:
    actor_user_id: FK -> User?            # null for system
    action: str                           # e.g., "USER.SUSPEND", "PAYMENT.REFUND"
    object_type: str                      # "User" | "Gig" | "PaymentIntent" ...
    object_id: str                        # string for portability
    metadata: JSON                        # context snapshot
    created_at: datetime = now()

    def save(self):
        # Append-only: disallow updates/deletes by policy
        super().save()

    class Meta:
        index_together = [(object_type, object_id), (created_at,)]
```

```python
# PSEUDOCODE — EXISTING TABLE UPDATES (SELECTED)

class User (extend):
    created_at: datetime = now()
    updated_at: datetime = now()
    # optional: soft_deleted: bool = False
    # Index: UNIQUE(phone_number)

class DaterProfile (rename from Dater):
    # fields unchanged; add timestamps
    created_at: datetime = now()
    updated_at: datetime = now()

class CupidProfile (rename from Cupid):
    created_at: datetime = now()
    updated_at: datetime = now()

class Feedback (update):
    owner_id: FK -> User (nullable)       # who left the feedback
    target_user_id: FK -> User
    gig_id: FK -> Gig
    message: str
    stars: int                            # 1..5
    created_at: datetime = now()

    def clean(self):
        assert 1 <= self.stars <= 5

    class Meta:
        unique_together = [(owner_id, gig_id)]
        index_together = [(gig_id,)]
```

```python
# PSEUDOCODE — SERVICE/WORKER SKETCHES

def backfill_gig_assignments():
    # For each Gig with cupid set: create GigAssignment row with claimed/completed times
    for gig in select Gig where gig.cupid_id is not null:
        create_if_absent(GigAssignment, gig_id=gig.id, cupid_id=gig.cupid_id,
                         claimed_at=gig.date_time_of_claim,
                         completed_at=gig.date_time_of_completion)

def migrate_messages_to_ai_sessions():
    # Group Messages by owner into chronological sessions
    for owner_id in distinct(Message.owner_id):
        msgs = fetch_messages(owner_id).order_by("id")
        session = None
        for m in msgs:
            if session is None or should_start_new_session(session, m):
                session = AISession(owner_id=owner_id, started_at=m.created_at, context={})
                session.save()
            AIMessage(session_id=session.id, role=("ai" if m.from_ai else "user"),
                      text=m.text, created_at=m.created_at).save()
```

Implementation notes:
- All timestamps UTC; DB defaults enforce UTC.
- Monetary values stored in minor units (int).
- No PAN/CVV/bank numbers in DB; only provider tokens.
- Prefer hard deletes except where audit/compliance requires retention.

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