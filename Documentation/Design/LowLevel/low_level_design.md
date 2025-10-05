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

### 7.1 Accessibility

Cupid Code’s interface is designed to ensure that every user—regardless of visual, motor, or cognitive differences—can comfortably interact with the app. Accessibility is a core part of the redesign 
and is integrated across all roles (Dater, Cupid, and Manager).

#### Color Scheme & Contrast

Cupid Code’s visual identity draws from a terminal-inspired palette that balances bold contrast with simplicity. The selected colors are:

- **Imperial Red:** <span style="color:#FB3640; font-weight:bold;">#FB3640</span>  
- **Polynesian Blue:** <span style="color:#1F487E; font-weight:bold;">#1F487E</span>  
- **Vivid Sky Blue:** <span style="color:#00CCFF; font-weight:bold;">#00CCFF</span>  
- **Pigment Green:** <span style="color:#09A129; font-weight:bold;">#09A129</span>  
- **Black (Background):** <span style="color:#000000; font-weight:bold;">#000000</span>

This color scheme was tested against the most common forms of color blindness—**Protanopia**, **Deuteranopia**, **Tritanopia**, and **Achromatopsia**—to ensure clear differentiation between 
interface elements.  

##### Accessibility Mode

To further improve usability, Cupid Code includes an **Accessibility Mode** toggle that adjusts colors and contrast for users with visual sensitivities.  

When enabled, Accessibility Mode makes the following changes:
- Background color changes from **<span style="color:#000000; font-weight:bold;">#000000</span>** (Black) → **<span style="color:#FFFFFF; background-color:#000000; font-weight:bold;">#FFFFFF</span>** (White)
- Text color changes from **<span style="color:#09A129; font-weight:bold;">#09A129</span>** (Pigment Green) → **<span style="color:#000000; font-weight:bold;">#000000</span>** (Black)
- All interactive buttons and icons retain their accent colors for brand recognition and clarity.

The **Accessibility Mode toggle** will be visible on every page through:
1. The **Top Navigation Bar** (icon toggle next to the hamburger menu).  
2. The **Profile Settings Page** (persistent user preference stored in their account).  

When toggled, the interface updates instantly without requiring a page reload, ensuring users can switch modes seamlessly. The chosen setting is saved in the user’s profile so that 
it remains active across future sessions.

### 7.2 Navigation Flow

Cupid Code uses a predictable, mobile-first navigation model that minimizes friction and guarantees that core tasks are within two taps from the Home screen for every role.

#### 7.2.1 Two-Click Rule
- From each role’s **Home** screen (Dater, Cupid, Manager), all primary tasks (AI help, Plan/Find Gigs, Payments, Profile, Notifications; and for Manager: Cupid Info, Dater Info) are reachable in **≤ 2 taps**.
- Success toasts and notifications provide **deep links** back to the relevant record (e.g., a specific gig, payment receipt, or rating modal) without breaking the two-click expectation when returning to Home.

#### 7.2.2 Constant Navigation Bars
- **Top Bar (all pages):** Centered logo; left **hamburger menu**; optional quick actions (Profile, Payment) when appropriate to the role.
- **Bottom Navigation (mobile-first):** Persistent 4–5 items max; active route is clearly indicated (icon + label + underline).  
  - **Dater:** Home, AI, Payment, Profile, Notifications  
  - **Cupid:** Home, Find Gigs, Completed, Profile, Notifications  
  - **Manager:** Home (Dashboard), Cupid Info, Dater Info, Notifications
- The **current page’s** nav item is visually disabled or marked active to avoid redundant taps.

#### 7.2.3 Hamburger (Role-Aware Shortcuts)
- Opens a left drawer with role-specific shortcuts and secondary actions (e.g., Accessibility Mode toggle, Logout).
  - **Dater:** Profile, Payment, Calendar, Accessibility Mode, Logout
  - **Cupid:** Profile, Find Gigs, Completed Gigs, Feedback, Accessibility Mode, Logout
  - **Manager:** Dashboard, Cupid Info, Dater Info, Accessibility Mode, Logout
- The **Accessibility Mode toggle** is duplicated here for universal availability.

#### 7.2.4 Responsive Behavior (Screen Size Changes)
- **Mobile (default)**: Bottom nav is pinned; scrolling content lives beneath it; Top Bar remains fixed.
- **Tablet / Desktop**: Bottom nav moves to a **top secondary nav** (beneath the Top Bar) to leverage horizontal space; multi-column card grids are enabled where applicable.

### 7.3 Page Wireframes & Descriptions

# <span style="color:#FB3640; font-weight:800;">WARNING: PROTOTYPE SCREENS ONLY</span>

The images referenced in this section are **non-functional prototypes** created in **Figma** to illustrate layout, flow, and component placement. They are not connected to live data or services, and **buttons/inputs do not work**. Final implementation details (spacing, copy, and micro-interactions) may change during development.

#### 7.3.1 Common Screens (Create Account, Login, Notifications)

---

**IMAGE HERE**

**Page Name:** Cupid Create Account

**Purpose:**  
Enable a new Cupid to register an account using only the most essential information required to create their profile and begin using the app. Following customer feedback, the **Create Account** process was simplified to reduce initial friction — Cupids now provide only basic details (name, email, username, and password). After registration, the system automatically sends a **notification prompting the user to complete their full profile** at a later time, allowing faster onboarding.

**Elements on this page:**  
- **Inputs**
  - First Name (text)
  - Last Name (text)
  - Username (text; uniqueness check on submit)
  - Email (email keypad; format validation)
  - Password (masked; strength meter)
  - Confirm Password (masked; match validation)
- **Selectors / Toggles**
  - Role Selector: **Cupid** / Dater (preselected as **Cupid** on this screen)
- **Buttons**
  - **Create Account** (primary)
  - **Back to Login** (secondary text link)
- **Validation / Messaging**
  - Inline error messages below fields on blur and on submit
  - Toast on success (“Account created ”)

**Expected User Actions:**  
- Enter required fields →  tap **Create Account**.  
- On success: account record created; user is directed to **Cupid Home** 
- If validation fails: inline errors displayed with clear remediation (e.g., “Username already in use,” “Passwords don’t match,”).

**IMAGE HERE**

**Page Name:** Dater Create Account

**Purpose:**  
Allow a new Dater to register a basic account with minimal required information to begin exploring the app. Following the same simplification applied to the Cupid registration process, the **Dater Create Account** page now collects only core credentials (name, email, username, and password). After successful registration, the system automatically sends a **notification reminding the user to complete their full dating profile**, which includes details such as interests, relationship goals, and preferences. This staged onboarding ensures a faster initial signup experience while still enabling richer personalization later.

**Elements on this page:**  
- **Inputs**
  - First Name (text)
  - Last Name (text)
  - Username (text; uniqueness check on submit)
  - Email (email keypad; format validation)
  - Password (masked; strength meter)
  - Confirm Password (masked; match validation)
- **Selectors / Toggles**
  - Role Selector: **Dater** / Cupid (preselected as **Dater** on this screen)
- **Buttons**
  - **Create Account** (primary)
  - **Back to Login** (secondary text link)
- **Validation / Messaging**
  - Inline error messages displayed below fields on blur and submit
  - Toast on success (“Account created”)
  - Optional post-registration notification prompting completion of full profile

**Expected User Actions:**  
- Enter required fields → tap **Create Account**.  
- On success: account record is created, and the user is directed to the **Dater Home** screen.  
- If validation fails: inline errors are displayed with clear remediation (e.g., “Username already in use,” “Passwords don’t match,” “Invalid email format”).

**IMAGE HERE**

**Page Name:** Universal Login Page

**Purpose:**  
Provide a unified, simple login experience for all user roles — **Manager**, **Cupid**, and **Dater** — while maintaining the same consistent design language and accessibility standards. The shared login page minimizes redundancy and allows for a single authentication flow. After successful login, users are automatically redirected to their respective Home screen based on account role.

**Elements on this page:**  
- **Inputs**
  - Email (email keypad; format validation)
  - Password (masked; hidden characters with visibility toggle option in final build)
- **Buttons**
  - **Login** (primary; triggers authentication process)
- **Navigation Links**
  - **Create Account** tab (switches view to registration options for Cupid or Dater)
  - **Welcome** tab (optional introduction or marketing overview)
- **Informational Text**
  - Terms of Service and Privacy Policy disclaimer displayed beneath login button
  - Inline validation messaging if credentials are incorrect (e.g., “Invalid email or password”)
- **Branding**
  - Centered **Cupid Code** logo reinforcing consistent brand identity
  - Dark terminal-style background with bright accent colors matching the rebranding palette

**Expected User Actions:**  
- Enter registered **Email** and **Password** → tap **Login**.  
- On success: user is authenticated and redirected to the appropriate Home screen based on their role:  
  - Dater → **Dater Home**  
  - Cupid → **Cupid Home**  
  - Manager → **Manager Dashboard**  
- On failure: inline message appears beneath the password field prompting the user to retry or reset their password (future feature).  
- User may switch tabs at the top to **Create Account** if they don’t yet have an account, or to **Welcome** to learn more about the app.

**IMAGE HERE**

**Page Name:** Notifications Page (Dater View)

**Purpose:**  
Provide users with an organized list of updates and alerts related to their activity within Cupid Code. The **Notifications Page** helps users stay informed about completed gigs, new gig creations, profile updates, and reminders. This page maintains the same layout for all user roles (Dater, Cupid, Manager) but adapts the **bottom navigation bar** to match the role’s available features. Notifications ensure real-time awareness without requiring users to check multiple pages manually.

**Elements on this page:**  
- **Sections**
  - **Unopened:** Displays new or unread notifications at the top, visually emphasized with bright text and color contrast for quick recognition.  
  - **Opened:** Displays previously viewed notifications, shown in a slightly dimmed or muted color style to distinguish them from unread items.
- **Notification Cards**
  - Title (short summary of event, e.g., *“Profile Updated”*, *“Flower Gig Created”*, *“Movie Gig Completed”*)  
  - Date (timestamp of when the event occurred)  
  - Description (brief message about the update)  
  - **Read** button — marks the notification as opened and, when tapped, directs the user to the relevant page (e.g., profile, gig details, or rating page).  
  - Rounded corner design, consistent with terminal-style color palette (blue cards with green text).  
- **Navigation**
  - **Top Bar:** Centered Cupid Code logo with a hamburger menu on the left. The menu includes quick access to settings, accessibility mode toggle, and logout.  
  - **Bottom Navigation Bar (Role-Based):**
    - **Dater:** Home, AI, Payment, Profile, Notifications (active).  
    - **Cupid:** Home, Find Gigs, Completed Gigs, Profile, Notifications (active).  
    - **Manager:** Home (Dashboard), Cupid Info, Dater Info, Notifications (active).

**Expected User Actions:**  
- Scroll to browse unread and read notifications.  
- Tap the **Read** button to open the related page and automatically change the notification’s state to *opened*.  
- Once viewed, the notification visually transitions to the “Opened” section.  
- Use the **bottom navigation bar** to quickly access other app areas.  
- Access the **hamburger menu** to toggle accessibility mode or log out.  

#### 7.3.2 Dater Screens 

---

**IMAGE HERE**

**Page Name:** Dater Home Page

**Purpose:**  
Serve as the **central hub** for Dater users, allowing quick access to all major app functions while presenting upcoming event information in a clear, visually structured layout. The Dater Home Page embodies Cupid Code’s **two-click navigation rule**, ensuring users can reach any feature—AI chat, date planning, rating cupids, or calendar—in two taps or fewer. It also provides an at-a-glance view of **upcoming events**, reinforcing the app’s focus on organization and simplicity.

**Elements on this page:**  
- **Top Bar**
  - Cupid Code logo centered at the top.  
  - Hamburger menu on the left for quick access.
- **Main Sections**
  - **Pages Section**
    - Four large interactive cards representing key actions:
      - **AI:** Opens the AI Chat/Voice Assistant page for help and suggestions.
      - **Rate Cupid:** Opens the page for rating past Cupid interactions or reviewing completed gigs.
      - **Plan Date:** Opens the date creation or gig request page.
      - **Calendar:** Opens the calendar view to see all scheduled and past events.
  - **Upcoming Events Section**
    - Displays 1–3 upcoming date cards (e.g., *Movies*, *Dinner*, *Walk in the Park*).  
    - Each card includes event title and date, formatted for quick readability.  
- **Navigation**
  - **Bottom Navigation Bar:** Persistent and role-specific (Dater View).  
    - **Home:** Active (disabled while on this page).  
    - **AI:** Opens AI Chat/Voice Assistant page.  
    - **Payment:** Opens Payment page for managing funds.  
    - **Profile:** Opens Dater Profile page for editing details.  
    - **Notifications:** Opens Notifications page (shared across roles).

**Expected User Actions:**  
- Tap one of the **Page cards** (AI, Rate Cupid, Plan Date, or Calendar) to navigate directly to the corresponding feature.  
- Scroll down to view **Upcoming Events**; tap an event card for more details or follow-up actions (e.g., rating, editing).  
- Use the **Bottom Nav Bar** or **Hamburger Menu** for quick navigation to other app sections.  
- The Dater can return to this Home Page from any other screen in **two taps or fewer**, maintaining the user experience standard defined in the High-Level Design.

**IMAGE HERE**

**Page Name:** Dater AI Chat Page

**Purpose:**  
Provide Dater users with an interactive space to receive real-time AI assistance for dating-related questions, conversation advice, and activity planning. The **AI Chat Page** serves as Cupid Code’s intelligent companion feature, offering both **text-based** and **voice-enabled** interaction modes. This page maintains a friendly, conversational layout while preserving the app’s terminal-inspired aesthetic and brand color palette.

**Elements on this page:**  
- **Top Bar**
  - Centered **Cupid Code** logo with the title **AI Chat** directly below.  
  - **Hamburger menu** on the left with quick access to settings, Accessibility Mode, and Logout options.
- **Chat Interface**
  - Alternating message bubbles:
    - **User Messages:** Displayed in **blue** with right alignment.
    - **AI Responses:** Displayed in **green** with left alignment and AI avatar.  
  - Timestamps displayed below or between message clusters for context.  
  - Smooth auto-scroll behavior to keep the latest messages in view.
- **Input Area**
  - Text input field with placeholder text *“message…….”*  
  - Send button (blue arrow icon) to submit typed messages.  
  - Optional **microphone icon** to activate voice input for AI listening mode.
- **Conversation Features**
  - Chat history persists for the current session.  
  - AI responses appear dynamically after short simulated typing delay.  
  - Message formatting supports line breaks and varied tone for natural dialogue.  
  - If a network or AI error occurs, a temporary toast displays an error message (e.g., *“Could not connect to AI. Try again.”*).

- **Navigation**
  - **Bottom Navigation Bar (Dater View):**
    - **Home:** Returns to Dater Home Page.  
    - **AI:** Active (disabled while on this page).  
    - **Payment:** Opens Payment Page.  
    - **Profile:** Opens Dater Profile Page.  
    - **Notifications:** Opens Notifications Page.

**Expected User Actions:**  
- Type a question or statement into the message bar → tap the **Send** icon.  
- Read AI’s response, which may include humor, conversation advice, or dating suggestions.  
- Use the **Hamburger Menu** to adjust Accessibility Mode or logout if desired.  
- Return to the Home Page or other sections using the **Bottom Navigation Bar**.  
- Press the **Microphone Icon** to enable voice chat and receive AI feedback via text.

**IMAGE HERE**

**Page Name:** Dater AI Voice Page (AI Listen Mode)

**Purpose:**  
Allow Dater users to interact with the AI through **voice-based input and response**, offering real-time conversational assistance without typing. The **AI Listen Page** is designed for users who prefer hands-free interaction or need faster in-the-moment feedback—such as during a date scenario. This page complements the AI Chat page and maintains the same terminal-inspired interface style and accessibility standards.

**Elements on this page:**  
- **Top Bar**
  - Centered **Cupid Code** logo with “AI Listen” title below it.  
  - **Hamburger menu** for quick access to all pages, accessibility mode, and logging out
- **Voice Interface**
  - Large animated microphone icon at the center to indicate listening state.  
  - **Play button** to begin voice recording.  
  - **Stop button** to end recording and trigger the AI’s response.  
  - Visual feedback (e.g., glow or pulse) when the microphone is active.
- **AI Response Area**
  - AI responses displayed in **green message bubbles**, similar to the chat view.  
  - Each message contains conversational guidance or quick tips based on the user's spoken input.  
  - Messages auto-stack vertically with smooth scroll behavior.  
  - Example responses include humor and adaptive advice (e.g., *“Abort the beet-string-theory monologue…”*).
- **Accessibility & Feedback**
  - AI messages use clear, concise language for readability.  
  - Optional voice output (future enhancement) to read AI responses aloud.  
  - Toast notifications appear for connection errors or permission denials (e.g., *“Microphone access required”*).
- **Navigation**
  - **Bottom Navigation Bar (Dater View):**
    - **Home:** Returns to Dater Home Page.  
    - **AI:** Active (disabled while on this page).  
    - **Payment:** Opens Payment Page.  
    - **Profile:** Opens Dater Profile Page.  
    - **Notifications:** Opens Notifications Page.

**Expected User Actions:**  
- Tap the **Play** button to begin recording their voice query.  
- Speak naturally while the microphone is active.  
- Tap the **Stop** button to send the recorded query to the AI.  
- View the AI’s **text-based response** immediately below, offering live advice or suggestions.  
- Use the **Hamburger Menu** to toggle Accessibility Mode or log out.  
- Navigate to other pages using the **Bottom Navigation Bar** once finished with the AI session.

**IMAGE HERE**

**Page Name:** Dater Plan Date / Create Gig Page

**Purpose:**  
Allow Dater users to create new **date events** or **gigs** quickly by specifying the basic details of the planned outing. This page provides a clean, minimal layout that prioritizes usability and speed, ensuring that users can create an event in seconds while adhering to the app’s **two-click navigation rule**. The page was streamlined based on customer feedback to include only the four key inputs: **When, What, Where, and Budget**.

**Elements on this page:**  
- **Top Bar**
  - Centered **Cupid Code** logo with page title **“Plan Date / Create Gig”** below it.  
  - **Hamburger menu** on the left providing quick access to all pages,, Accessibility Mode, and Logout.  
- **Input Fields**
  - **When:** Date input field (MM/DD/YY format) for selecting the event date.  
  - **What:** Text input describing the activity (e.g., *Flowers*, *Dinner*, *Concert*).  
  - **Where:** Text input for the event location (e.g., *Old Main*, *Megaplex*, *Park*).  
  - **Budget:** Currency input field with dollar sign indicator for specifying the cost or spending limit.  
- **Buttons**
  - **Create:** Primary action button that submits the form and generates a new gig record.  
- **Validation / Messaging**
  - Inline validation ensures all fields are filled before submission.  
  - Error messages displayed under invalid fields (e.g., *“Please enter a valid date”*, *“Budget must be greater than $0.00”*).  
  - Success toast appears after creation (e.g., *“Gig created successfully!”*).
- **Navigation**
  - **Bottom Navigation Bar (Dater View):**
    - **Home:** Returns to Dater Home Page.  
    - **AI:** Opens AI Chat/Voice Assistant page.  
    - **Payment:** Opens Payment Page.  
    - **Profile:** Opens Dater Profile Page.  
    - **Notifications:** Opens Notifications Page.

**Expected User Actions:**  
- Fill out each field (**When, What, Where, Budget**).  
- Tap **Create** to submit the gig.  
- On success: the new gig is added to the Dater’s list under the **Unclaimed Gigs** section and becomes visible to Cupids.  
- On failure (missing or invalid fields): inline errors prompt the user to correct information.  
- After successful creation, the user may return to **Home** or view notifications confirming gig creation.

**IMAGE HERE**

**Page Name:** Dater Rate Cupid / Gig Status Page

**Purpose:**  
Enable Dater users to **track the status of their gigs** (dates) and provide feedback once a Cupid completes a task. This page organizes all gigs into three clear categories — **Unclaimed**, **Claimed**, and **Completed** — making it simple for users to understand the progress of each event at a glance. Once a gig is marked as completed, users can submit a **rating** for the Cupid involved, contributing to service quality and user accountability.

**Elements on this page:**  
- **Top Bar**
  - Centered **Cupid Code** logo 
  - **Hamburger menu** on the left providing quick access to all pagest, Accessibility Mode, and Logout.

- **Main Sections**
  - **Unclaimed Gigs:**  
    - Displays gigs that have been created but not yet accepted by any Cupid.  
    - Each gig card includes details:  
      - **What:** Activity (e.g., *Flowers*, *Movies*)  
      - **When:** Date of event  
      - **Where:** Location  
      - **Budget:** Specified amount  
    - Cards are informational only (no action buttons).  

  - **Claimed Gigs:**  
    - Displays gigs currently accepted by a Cupid.  
    - Cards show the same details as above and are marked with a *Claimed* status.  
    - Used primarily for tracking — no user input required.  

  - **Completed Gigs:**  
    - Displays gigs that have been completed by Cupids.  
    - Each card includes a **Rate** button, allowing the user to rate their Cupid’s performance.  
    - Clicking **Rate** opens a **popup modal** (see below) for submitting a review.

- **Rating Popup Modal (when Rate is tapped)**
  - Text area for optional comments (user feedback).  
  - Five-heart rating scale (1–5 hearts).  
  - **Submit** button to finalize rating.  
  - **Cancel** button to close the modal without submitting.  
  - Confirmation toast appears on success: *“Thank you for rating your Cupid!”*

- **Navigation**
  - **Bottom Navigation Bar (Dater View):**
    - **Home:** Returns to Dater Home Page.  
    - **AI:** Opens AI Chat or AI Listen Page.  
    - **Payment:** Opens Payment Page.  
    - **Profile:** Opens Dater Profile Page.  
    - **Notifications:** Opens Notifications Page.

**Expected User Actions:**  
- Review **Unclaimed**, **Claimed**, and **Completed** gigs in their respective sections.  
- Tap the **Rate** button under any completed gig to open the rating modal.  
- Select 1–5 hearts and optionally add a short comment, then tap **Submit** to send the rating.  
- After rating submission, the modal closes, and the gig card updates to reflect that the Cupid has been rated.  
- Navigate freely using the **Bottom Navigation Bar** or **Hamburger Menu** to access other features.  

**IMAGE HERE**

**Page Name:** Dater Calendar Page

**Purpose:**  
Provide Dater users with an organized overview of both **upcoming** and **past** dates in a clean, card-based layout. The Calendar Page helps users visually manage their schedule without requiring a traditional calendar grid, aligning with Cupid Code’s minimal and mobile-friendly design philosophy. It allows users to quickly review when and where events are happening, as well as revisit completed dates for rating or reference.

**Elements on this page:**  
- **Top Bar**
  - Centered **Cupid Code** logo  
  - **Hamburger menu** on the left for quick access to Profile, Payment, Accessibility Mode, and Logout.
- **Main Sections**
  - **Upcoming Dates Section**
    - Displays all future scheduled dates sorted chronologically.  
    - Each card includes:
      - **What:** Activity name (e.g., *Flowers*, *Movies*)  
      - **When:** Event date (MM/DD/YY format)  
      - **Where:** Event location  
      - **Budget:** Planned cost of the event  
    - Cards are interactive; tapping one opens more detailed date information or the related gig status page.
  - **Past Dates Section**
    - Displays completed dates (events before today’s date).  
    - Each card mirrors the same structure as Upcoming Dates.  
    - Cards may include a subtle dim effect to indicate completion.  
    - Tapping a past date card redirects the user to the **Rate Cupid / Completed Gig** page, where they can provide feedback if not yet rated.

- **Visual Design**
  - Distinct section headers: **“Upcoming Dates”** and **“Past Dates”** displayed in bright green for visual separation.  
  - Rounded blue cards with green text maintain consistency with the terminal-inspired rebranding style.  
  - Uniform spacing between cards for easy scrolling and readability.

- **Navigation**
  - **Bottom Navigation Bar (Dater View):**
    - **Home:** Returns to Dater Home Page.  
    - **AI:** Opens AI Chat or AI Listen Page.  
    - **Payment:** Opens Payment Page.  
    - **Profile:** Opens Dater Profile Page.  
    - **Notifications:** Opens Notifications Page.

**Expected User Actions:**  
- Scroll through **Upcoming Dates** to review upcoming events.  
- Tap any **Upcoming Date Card** to view or edit event details (future enhancement).  
- Scroll down to **Past Dates** to review previous events.  
- Tap a **Past Date Card** to open the **Rate Cupid / Gig Status Page** and provide a rating if applicable.  
- Use the **Bottom Navigation Bar** or **Hamburger Menu** to navigate to other features or toggle Accessibility Mode.  

**IMAGE HERE**

**Page Name:** Dater Payment Page

**Purpose:**  
Allow Dater users to **manage their account balance** and **stored payment methods** for funding date-related activities. This page combines balance visibility, fund addition, and card management into one simple interface. It follows the rebranding’s minimal and terminal-inspired look while emphasizing clarity and secure data handling.

**Elements on this page:**  
- **Top Bar**
  - Centered **Cupid Code** logo
  - **Hamburger menu** on the left for quick access to all pages, Accessibility Mode, and Logout.  

- **Main Sections**
  - **Current Account Balance:**  
    - Large, bold green text displaying the user’s available balance (e.g., *$200.00*).  
    - Updates dynamically after successful fund additions.  
  - **Add Funds Section:**  
    - **Saved Cards Dropdown:** Lets the user select a previously saved payment method.  
    - **Amount Input Field:** Accepts currency values (formatted to two decimals).  
    - **Add Amount Button:** Submits the transaction to add funds to the user’s account.  
  - **Add Card Section:**  
    - **Name on Card:** Text input for the cardholder’s full name.  
    - **Expiration Date:** Two separate fields for month (MM) and year (YYYY).  
    - **CVV:** Short numeric input (3–4 digits) for card security code, masked for privacy.  
    - **Add Card Button:** Saves new card information to the user’s account using secure encryption and tokenization.  

- **Validation / Messaging**
  - Inline error handling for missing or invalid data (e.g., *“Please enter a valid card number”*, *“Amount cannot be $0.00”*).  
  - Toast messages for success or failure (e.g., *“Funds added successfully”*, *“Payment failed, please try again”*).  
  - Input formatting enforces numeric-only entry for amount, expiration date, and CVV fields.  

- **Navigation**
  - **Bottom Navigation Bar (Dater View):**
    - **Home:** Returns to Dater Home Page.  
    - **AI:** Opens AI Chat or AI Listen Page.  
    - **Payment:** Active (disabled while on this page).  
    - **Profile:** Opens Dater Profile Page.  
    - **Notifications:** Opens Notifications Page.

**Expected User Actions:**  
- Select a **saved card** and enter an **amount** to add to their account → tap **Add Amount**.  
- View updated **Account Balance** after confirmation.  
- Enter **new card information** and tap **Add Card** to securely save payment details for future use.  
- Navigate to other app sections using the **Bottom Navigation Bar** or access **Accessibility Mode** via the Hamburger Menu.  

**IMAGE HERE**

**Page Name:** Dater Profile Page

**Purpose:**  
Allow Dater users to **view, edit, and update their personal and dating-related information** in one place. The profile page is designed for clarity and flexibility, ensuring users can manage their details without leaving the app. Although the page appears long in prototype form, the final version will feature **scrollable content**.

**Elements on this page:**  
- **Top Bar**
  - Centered **Cupid Code** logo  
  - **Hamburger menu** on the left providing quick access to Payment, Accessibility Mode, and Logout.  

- **Main Sections**
  - **Profile Header**
    - Displays profile picture (uploadable or editable via file selector).  
    - Shows user’s name and role (e.g., *Dater Profile*).  

  - **Personal Information Section**
    - **First Name** (text input)  
    - **Last Name** (text input)  
    - **Username** (text input; read-only if tied to login credentials)  
    - **Email** (email field; read-only or editable depending on verification)  
    - **Phone Number** (numeric input)  
    - **Address** (text input for local matching or deliveries)  
    - **Profile Picture Upload** (image picker button + file label display)  

  - **About & Preferences Section**
    - **Physical Description:** Multi-line text area describing physical traits (e.g., height, build, hair, eyes, attire).  
    - **Nerd Type:** text field describing personality category (e.g., *Analytical Agricultural Physicist*).  
    - **Relationship Goals:**  
      - Long-term and short-term goals, editable text area (e.g., “Seeking: a statistically significant romantic connection”).  
    - **Interests:** Multi-line text area for hobbies and interests.  
    - **Past Dating History:** short text input summarizing relationship experience.  
    - **Dating Strengths:** Text field highlighting personal strengths in relationships.  
    - **Dating Weaknesses:** Text field or list noting self-identified challenges or humorous traits.

  - **Save & Update Section**
    - **Update/Save Changes Button:** Submits modifications to user data.  
    - Confirmation toast appears (“Profile updated successfully”).  

  - **Update Password Section**
    - **Old Password:** Masked input field for current password.  
    - **New Password:** Masked input with strength indicator.  
    - **Repeat Password:** Confirms match before submission.  
    - **Update Password Button:** Submits new password for authentication update.  
    - Success/failure toast displayed depending on validation.

- **Validation / Messaging**
  - Inline validation for empty required fields or invalid formats (e.g., email, phone).  
  - Error messages appear beneath affected fields.  
  - Success message confirms when updates are saved.  
  - Password update section includes check for matching and minimum strength.  

- **Navigation**
  - **Bottom Navigation Bar (Dater View):**
    - **Home:** Returns to Dater Home Page.  
    - **AI:** Opens AI Chat or AI Listen Page.  
    - **Payment:** Opens Payment Page.  
    - **Profile:** Active (disabled while on this page).  
    - **Notifications:** Opens Notifications Page.  

**Expected User Actions:**  
- Scroll through sections to review or edit personal information.  
- Tap **Update/Save Changes** to commit modifications.  
- Use **Profile Picture Upload** to change the avatar image.  
- Access the **Update Password Section** to reset credentials securely.  
- Navigate to other app areas via the **Bottom Navigation Bar** or **Hamburger Menu**.  



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
