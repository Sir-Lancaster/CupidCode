*Chat GPT was used in the creation of this document.*
# Cupid Code High-Level Design Document
Sprint Leader: Kayden Lancaster

Sprint Followers: Zac Cunningham, Greg Steele, Dallin Tew, Carter Johnson

## Contents
  - [Introduction](#1-introduction)
  - [System Overview](#2-system-overview)
  - [Architecture](#3-architecture)
  - [Major Components](#4-major-components)
  - [External Interfaces](#5-external-interfaces)
  - [User Interface Design](#6-user-interface-design)
  - [Input and Output](#7-input-and-output)
  - [Security](#8-security)
  - [Risks and Mitigations](#9-risks-and-mitigation)
  - [Data Design](#10-data-design)

## 1. Introduction
**Purpose**  
Provide a concise high‑level technical design for the current Cupid Code platform so the team can complete an MVP (Minimum Viable Product) that delivers the Must requirements (MoSCoW) for 2025–2026. This document aligns inherited code (frontend Vue app + Django backend) with the updated requirements specification and guides subsequent detailed design, implementation, and risk mitigation.

**Scope**  
Covers:  
- System context and current vs planned capabilities (AI assist, Gigs, payments, notifications).  
- Architectural style (web client + Django REST backend) and core component boundaries.  
- Roles and data domains (Dater, Cupid, Manager/Admin).  
- High‑level data handling (profiles, Gigs, feedback, authentication, future payments, AI session artifacts).  
- Integration points (future: PayPal, messaging, location, OpenAI).  
Excludes: low‑level class diagrams, detailed endpoint specs, test plans, deployment runbooks (to be documented separately). References: Requirements Specification (requirements.md) for authoritative functional, nonfunctional, business, and user requirements.

**Audience**  
- Engineering team members adding features (AI, payments, notifications).  
- Product/managerial stakeholders validating scope vs requirements.  
- Security/review stakeholders assessing data handling and role boundaries.  
- New contributors needing a structural overview before reading code.

**Goals Alignment (Selected Musts)**  
- Real‑time AI feedback (listen + chat).  
- Multi‑role web access (desktop + mobile browsers).  
- Notifications (email/Push planned).  
- Secure data handling.  
- Future payment rails (PayPal) for funding and Cupid payouts.  

## 2. System Overview
**System Description**  
Cupid Code is a role‑based web application that assists users (primarily socially anxious or inexperienced Daters) with AI‑driven, context‑aware coaching and on‑demand human “Cupid” Gig interventions. The platform delivers:  
- Dater experience: AI chat + (future) passive listening for live guidance; scheduling and Gig request flows.  
- Cupid experience: Manage Gigs, respond to interventions, earnings and availability.  
- Manager/Admin: User oversight, future compliance/reporting, operational dashboards.  
Current stack:  
- Frontend: Vue 3 (Vite) SPA (router, components under src/, role‑specific views).  
- Backend: Django REST style views (api app) with SQLite (to migrate to managed cloud DB).  
- Auth: Username/password (working), role persisted in backend models.  
- AI: Placeholder endpoints; microphone capture pipeline present; logic for real guidance still minimal.  
- Storage: Local DB for users, Gigs, feedback scaffolding (see server/api/models.py).  
- Tests: Playwright UI scripts for login, Gig creation, Payments, and role flows.  

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
- Feedback loops (post‑gig rating, AI reflection).  
- Security hardening (encryption fixes, PII handling, audit trails).  

**Planned Enhancements (Near Term)**  
- Integrate payment providers (abstracted service layer).  
- AI session store referencing user profile + prior Date context.  
- Notification subsystem (queued + provider adapters).  
- Role‑segregated data views and future couple privacy controls.  
- Deployment to Azure (containerized or managed app service).  

**Key Constraints / Assumptions**  
- Must remain mobile-first; performance acceptable for real‑time guidance within latency budgets (<1–2sec AI round trip after backend integration).  
- Incremental migration from SQLite to Azure Postgres/MySQL once payment + audit features start (avoids migration pain later).  
- Privacy: Microphone streaming only opt‑in per session; no permanent raw audio retention (derived features only).  

**High-Level Data Domains**  
- Identity & Roles (User, DaterProfile, CupidProfile, Manager/Admin).  
- Scheduling & Gigs (Gig requests, status, Cupid assignment, intervention notes).  
- AI Interaction (chat transcripts, advice events, memory embeddings).  
- Financial (Paypal checkout payment flow).  
- Feedback & Ratings (post‑gig + AI evaluation—planned).  
- Notifications (in-app + external dispatch queue—planned).  

**External / Future Integrations**  
- Payments: PayPal (Must).  
- Location services (Could) for Cupid tracking.  
- Dating app API linking (Could).  
- Email/SMS provider (Twilio / SendGrid) for push-out notifications (Must for notifications objective).  

**Quality & NFR Priorities (Short Term)**  
- Security remediation (address encryption misuse, card storage via tokenization not raw DB).  
- Accessibility improvements (contrast, screen reader semantics in Vue components).  
- Reliability: Graceful degradation when AI or payment providers unavailable.  

**Architecture Diagram (Placeholder)**  
(Will depict: Browser SPA (Vue) → REST/JSON API (Django) → Data Layer (DB + future cache) → External Services (AI API, PayPal, Email/SMS). Will be added in Section 11.)

**Success Criteria for This Phase**  
- End-to-end flow: Dater logs in → requests AI help → receives contextual response referencing stored preferences.  
- Cupid Gig lifecycle visible (create → assign placeholder → mark complete).  
- Stubs for payment & notification services integrated behind clear service interfaces to enable parallel work streams.  


## 3. Architecture
### Architecture Style
Cupid Code is designed using a **client–server monolithic architecture** centered on **Django**. While the backend currently functions as a monolith for simplicity and rapid development, it is organized into **modular services** (authentication, scheduling, payments, AI integration, notifications). This modular design provides a clear **pathway to evolve into a service-oriented or microservices architecture** in the future if scalability demands increase.  

This style was chosen because:
- It is well-suited to the **team size** and **tight project deadlines**.  
- It allows for **simpler deployment** and maintenance compared to a microservices setup.  
- It leverages the **existing Django codebase** and ecosystem, minimizing onboarding time for developers.  
- It balances the need for quick iteration with long-term maintainability and potential scaling.

### Deployment View
Cupid Code will be deployed in **three environments**: local development, staging/testing, and production. Each environment mirrors the core setup to ensure smooth promotion of code between stages.  

- **Frontend (Vue.js):**  
  Compiled into static assets and served via **Azure App Service** or a **CDN** for fast delivery (Not Implemented).  
- **Backend (Django):**  
  Runs in an **Azure App Service container** with autoscaling enabled for higher loads (Not Implemented). Handles API requests, business logic, and orchestration of external services.  
- **Database (PostgreSQL):**  
  Deployed as a **managed Azure Database for PostgreSQL** instance (Not Implemented). Configured with automatic backups, encryption at rest, and role-based access controls.  
- **Secrets Management:**  
  Sensitive keys (API keys, DB credentials) stored in **Azure Key Vault**, never hardcoded (Not Implemented).  
- **Networking & DNS:**  
  Deployed behind **Azure Application Gateway** with HTTPS termination (Not Implemented). DNS configured via a custom domain with TLS certificates auto-renewed by **Azure Certificate Manager** (Not Implemented).  

This setup ensures **fast iteration for developers**, **secure production hosting**, and **cloud-native scalability**.

### Major Components & Interactions
Cupid Code follows a **three-tier separation of concerns** with clear boundaries between presentation, logic, and storage:

1. **Frontend (Presentation Layer)**  
   - Vue.js single-page application (SPA).  
   - Role-based portals for Daters, Cupids, and Admins.  
   - Communicates with backend solely via HTTPS API calls.  

2. **Backend (Application Layer)**  
   - Django monolith structured into modular apps (auth, scheduling, payments, notifications, AI).  
  - Celery + Redis handle background jobs like reminders, notifications, and AI feedback (Not Implemented).  
  - Integrates with third-party services: PayPal (payments) (Implemented), Stripe (Not Implemented), AI APIs (Not Implemented), email/SMS providers via SendGrid/Twilio (Partially Implemented).  

3. **Database (Data Layer)**  
   - PostgreSQL stores user accounts, schedules, orders, and logs.  
   - Payment methods are never stored directly; only tokens from Stripe/PayPal are persisted.  
   - Strict schema with foreign keys to preserve consistency.  

### Design Rationale
- **Maintainability:** Monolith reduces deployment complexity while modularization ensures clean code boundaries.  
- **Scalability:** Although currently monolithic, service boundaries allow migration to microservices as traffic grows.  
- **Security:** Data separation, managed services, and secure key handling reduce attack surface.  
- **Extensibility:** Easy to add subscription tiers, new AI integrations, or enhanced scheduling features.  
- **Cloud-Native:** Uses Azure-managed services for scalability, security, and monitoring out of the box.  

### Component Diagram
The following diagram illustrates Cupid Code’s architecture and external integrations:

```mermaid
graph TD
    A["User Browser (Vue.js SPA)"] -->|HTTPS API Calls| B["Django Backend (Monolithic Core)"]
    B --> C["PostgreSQL Database (Managed Azure Instance)"]
    B --> D["Celery + Redis (Background Tasks)"]
    B --> E["Payment Gateway (Stripe/PayPal)"]
    B --> F["AI Services (Chat/Coaching APIs)"]
    B --> G["Notification Services (Email/SMS Providers)"]
    H["Azure Key Vault (Secrets Storage)"] --> B
    I["Azure App Service (Hosting Backend)"] --> B
    J["CDN / Static Hosting (Serving Vue Assets)"] --> A
    K["Azure DNS + TLS (Custom Domain + HTTPS)"] --> A
```

## 4. Major Components

#### **Gig Request**
![Sequence-Diagram](./images/Sequence_Diagram.jpg)

### Frontend (Vue 3 + Vite)

- **Responsibilities**  
The frontend is responsible for rendering the user interface and ensuring a smooth, responsive experience across devices. It manages client-side routing, maintains global application state (e.g., authentication, session data, preferences), and enforces accessibility standards such as ARIA roles and keyboard navigation. It communicates with the backend via APIs and, where necessary, establishes WebSocket connections for real-time features like chat or live notifications.  

- **Technologies/Versions**  
Vue 3.4.20 (Composition API) provides a modular approach to building reactive components, while Vite 7.2.2 handles efficient bundling and hot-module reloading for development. Vue Router 4.3.0 manages client-side navigation using hash-based routing. Real-time features are handled through polling mechanisms rather than WebSocket connections.  

- **Internal Interfaces**  
Common abstractions include a `makeRequest` utility module for standardized HTTP requests, `auth.js` utilities to track authentication state, role-specific Vue component directories (DaterVues, CupidVues, ManagerVues), and reusable UI components (Banner, NavBar, Popup, Heart) to enforce consistency across the application.  



### Backend API (Django + DRF)

- **Responsibilities**  
The backend exposes a RESTful API that supports all client-facing features. It manages authentication and enforces role-based access for different user types (Dater, Cupid, Manager). It implements business logic such as matchmaking, chat storage, and media uploads. It also handles background jobs such as notification dispatch, analytics aggregation, and payment confirmation through asynchronous workers.  

- **Technologies/Versions**  
Django 5.0.2+ provides a secure and scalable foundation, with REST API endpoints created using `@api_view` decorators and Django's built-in serialization. Django REST Framework 3.14.0+ is included but used selectively for specific functionality. 

- **Internal Interfaces**  
The backend is structured around Django models for data persistence, `serializers.py` for data validation and formatting, `helpers.py` for utility functions, and dedicated service modules like `paypal_service.py` for external integrations. Background job processing is planned but not yet implemented.  



### Database (SQLite → Postgres)

- **Responsibilities**  
The database persists all critical application data, including users, profiles, matches, chat messages, financial transactions, and notification logs. It provides transactional integrity, supports relational queries, and ensures long-term data durability.  

- **Technologies/Versions**  
SQLite is currently used for both development and the current deployment for its simplicity and lightweight setup.

- **Internal Interfaces**  
Django models serve as the primary abstraction for interacting with the database, with models defined for User, Dater, Cupid, Gig, Quest, Message, and Feedback entities. Repository/service layers may be introduced to separate business logic from persistence logic.  



### AI Service

- **Responsibilities**  
The AI service supports advanced features such as natural language chat responses, moderation of inappropriate content, and optional voice transcription. It can also rank or filter suggestions based on user context, providing a more personalized experience.  

- **Technologies/Versions**  
Integration with OpenAI API (version 2.6.1+) is configured for text-based AI features. Speech-to-text capabilities using websocket is implemented.

- **Internal Interfaces**  
AI functionality is integrated into existing API endpoints rather than separate services. The frontend includes audio capture capabilities with websocket, and the backend includes OpenAI client setup for processing chat requests when fully implemented.  



### Payments (Stripe / PayPal)

- **Responsibilities**  
This component manages the full lifecycle of user payments, including subscriptions, one-time transactions, and credits. It ensures that transactions are recorded securely, validates payment status' via webhook callbacks, and generates receipts or invoices for users.  

- **Technologies/Versions**  
PayPal Smart Buttons (@paypal/paypal-js version 9.0.1) are implemented for payment processing, providing PCI-compliant hosted flows. 

- **Internal Interfaces**  
The `paypal_service.py` module handles PayPal OAuth token management and payout processing. PayPal payment events are processed through the existing gig workflow, with payout functionality implemented for Cupid earnings. Receipt generation and subscription logic are planned for future implementation.  



### Notifications (Email / SMS / Push)

- **Responsibilities**  
Notifications provide timely communication to users outside the app, such as payment confirmations and gig confirmations. Channels include email and push notifications.  

- **Technologies/Versions**  
SendGrid (version 6.11.0+) is configured for email delivery. Twilio and sendgrid is used for this.

- **Internal Interfaces**  
In-app notifications are handled through the Vue frontend with polling mechanisms. The backend includes notification models and API endpoints. External notification providers will be integrated through dedicated service modules when implemented.  



### Auth / Identity

- **Responsibilities**  
This component handles all user identity management. It supports user registration, login, session or token issuance, password recovery, and optional two-factor authentication. It also enforces rules like age verification to ensure compliance with platform requirements.  

- **Technologies/Versions**  
Django’s authentication system is extended with JWT (e.g., SimpleJWT) for API token management. OAuth integrations (Google, Apple) may be added for social logins.  

- **Internal Interfaces**  
The system includes a token generator for access/refresh tokens, session middleware for web clients, and validation services for age-gating and security checks.  



### Admin / Manager Dashboard

- **Responsibilities**  
The dashboard provides administrators and managers with tools to oversee platform activity. Features include analytics views for monitoring engagement, moderation panels for handling reports or flagged content, and user management capabilities.  

- **Technologies/Versions**  
Django Admin provides an out-of-the-box management interface. Alternatively, a custom Vue-based admin panel can be built for a richer user experience.  

- **Internal Interfaces**  
Modules include metrics aggregation services for analytics, and privilege enforcement mechanisms to ensure only authorized managers can access sensitive data.  


**Backend Components UML** 

![Components Diagram](images/componentsDiagram.png)




## 5. External Interfaces 
### Third-Party APIs / Services

1. **AI Bot**  
    - **Description:** The AI logic is dependent on and provided by Prof. Falor. It powers the “intelligence” behind AI chat and listening features.  
    - **Used in:** All interactions involving a Cupid, including conversational chat, AI-assisted suggestions, and real-time responses.  
    - **Notes:** The AI bot acts as the core decision-making engine; API reliability and latency are critical for responsive interaction.

2. **Geolocation API**  
    - **Description:** Provides device location data, either via GPS, IP address, or browser geolocation.  
    - **Used in:** Matching users based on proximity and finding nearby Gigs or events.  
    - **Notes:** Requires explicit user permission; must handle location errors or denials gracefully.

3. **Pyttsx3**  
    - **Description:** Python text-to-speech library for converting text into spoken audio.  
    - **Used in:** Accessibility features (for visually impaired users) and optionally for AI voice output during Gigs.  
    - **Notes:** Runs locally and does not require internet access; can be used as a fallback if external TTS services fail.

4. **Twilio API**  
    - **Description:** Cloud communication platform providing SMS, email, and voice messaging services.  
    - **Used in:** Sending notifications, verification codes, and alerts to users.  
    - **Notes:** Includes retry and fallback mechanisms; provider quotas should be monitored to avoid delivery failures.

5. **Yelp Fusion API (via `yelpapi`)**  
    - **Description:** Access to business data, reviews, events, and ratings through the Yelp platform.  
    - **Used in:** Finding Gigs, events, and venues for users based on location and preferences.  
    - **Notes:** Must handle API rate limits and cache results to improve performance and reduce API calls.

6. **Azure REST API**  
    - **Description:** Cloud-based services for hosting, storage, and connecting multiple devices.  
    - **Used in:** Supporting backend infrastructure, real-time device communication, and scalable storage for media or data.  
    - **Notes:** Provides high availability and scalability; secure authentication and endpoint validation are required.


## 6. User Interface Design

### UI/UX Principles

- Cupid codes redesign aims to make users' experience frustration-free by simplifying the overall design.
- Part of the redesign includes making the UI a mobile-first responsive design.                              
- Navigation will adhere to the standard of 2 clicks to get anywhere from the home page.   
- Cupid code aims to be accessible to all, which is why the color palettes were selected with color blindness in mind.

### Rebranding and Color Schemes

As part of the Rebranding for Cupid Code, our team has decided to lean into who our users are and focus the color scheme and logos around them.
Our main users, the Daters, are comprised of tech enthusiasts; for this reason, we have decided to give the app a more techy vibe and style the app around the terminal. 

- The rebranding will feature a new logo designed to resemble intricate code elements.
- Below is an example of what the new logo could look like.

![Logo](images/Logodesign.jpg)

- Buttons that have graphics will also follow the new rebranding and look like code.
- The color scheme we have selected is based on the look of a terminal.
  - Dark background
  - light green words
  - minimal other colors
- The colors we have selected in hex are (from right to left)
  - #FB3640
  - #1F487E
  - #00CCFF
  - #09A129   
  - #000000

![color scheme](images/Default.png)

### Accessibility

- This color scheme aligns with our tech-driven vibe, ensuring the users feel right at home.
- Accessibility is essential to our team, so we have compared our color scheme to the following color blindness types, and we have included an image of that comparison for each.

**Protanopia**

![Protanopia](images/Protanopia.png)

**Deuteranopia** 

![Deuteranopia](images/Deuteranopia.png)

**Tritanopia**

![Tritanopia](images/Tritanopia.png)

**Achromatopsia**

![Achromatopsia](images/Achromatopsia.png)

**Protanomaly**

![Protanomaly](images/Protanomaly.png)

**Deuteranomaly** 

![Deuteranomaly](images/Deuteranomaly.png)

**Tritanomaly**

![Tritanomaly](images/Tritanomaly.png)

**Achromatomaly**

![Achromatomaly](images/Achromatomaly.png)

- Most Color Blindnesses are compatible with our color scheme.
- To ensure all can see and use our app efficiently, we will be adding an Accessibility mode.
- The Accessibility mode will make the following changes.
  - The black background (#000000) will change to a white background (#FFFFFF)
  - The Green Text (#09A129) will be changed to Black (#000000)
- Accessibility mode will be easily accessible from the home screen.
- Below is the color Palette for the accessibility mode.
  
![Accessible.png](images/Accessible.png)

### Navigation Flow

As stated before, we aim to make the user's experience as simple as possible; therefore, we strive to follow the following navigation plan.
Our home page is designed after the layout of the Canvas Mobile app.

- All pages are accessible with just two clicks from the home page.
- Pages:
  
1. **Sign up page**

  - This page will be simple in design
  - A new user will use a toggle to determine whether they are signing up as a cupid or a Dater
  - If they are signing up as a cupid then they will have a  smaller sign up page as not as much information is needed from them
  - If they are signing up as a Dater then a long sign up page will be present as more details information is needed
  - Examples of Dater sign up info 
    - Nerd type 
    - Relationship goals 
    - Intrests 
    - Past dating history 
    - Dating strengths 
  - Both sign up pages will have a create account page
  
2. **Login page**
    
  - Simple normal looking login page
  - Will be the same page for all users (Daters, Cupids, Managers)
  - Button to sign in with at bottom

**Dater**
  
1. **Home Page**

  - Top nav bar (This is on Every page)
    - Logo center 
    - Hamburger button
      - Accessible mode toggle 
      - Link to profile page
      - Link to payment page
      - Logout link
  - Main content card style 
    - Card to link to AI page 
    - Card to link to Plan a Date/ create a Gig page 
    - Card to link to Rate Cupids/Order Status page 
    - Card to link to Calendar 
    - Upcoming Dates Preview
      - 1-3 cards showing upcoming Dates/events 
    - On smaller screen sizes there will be a bottom nav bar with buttons to take you to the different pages
      - On larger screens this nav bar will be at the top underneath the logo
      - Bottom nav bar (This is on every page)
        - link to Home page (disabled when on home page) 
        - Link to AI page 
        - Link to Payment page 
        - Link to Profile page 
        - Link to Notifications Page 

2. **AI Page**

  - Top nav bar (discussed previously)
  - AI chat tab  
    - Chat history ( only available for current chat)
    - User will be able to ask AI questions and recieve responses in real time
    - AI voice button ( changes UI to AI listening tab) 
    - AI listening tab
    - User will be able to start and stop AI recording 
    - user should be able to see an AI response after stoping the recording
    - AI chat button ( changes UI to AI chat tab)
  - Bottom nav bar (discussed previously)  
  
3. **Plan a Date/create Gig page**
    
  - Top nav bar 
  - User will be able to manually plan a Date/ create a Gig
  - Will need to input the What, When, Where, How($$), to create a valid Date/Gig
  - Button to add Gig/create Date 
  - Bottom nav bar 
  
4. **Rate Cupid/ Order Status page**
    
  - Top nav bar  
  - Unclaimed section 
    - Cards for all unclaimed Gigs 
  - Claimed section 
    - Cards for all claimed Gigs 
  - Completed Gigs section 
    - Cards for all completed Gigs 
      - Completed Gigs cards will have a button to rate cupid 
  - Rate cupid popup 
    - Will have a way to describe interaction with cupid 
    - Will have a way to rate the cupid using hearts 
    - Send button 
    - Cancel button 
    - Bottom nav bar
  
5. **Calender page**
 
  - Top nav bar 
  - Upcoming Dates section
    - Cards of upcoming Dates ordered from closest to farthest
      - Date details will include  
        - When
        - Where 
        - What 
        - Budget 
  - Past Dates section 
    - Cards of past Dates ordered from closest to farthest
    - All card details are the same as the upcoming Dates cards
  - Bottom nav bar
  
6. **Payment page**
 
  - Top nav bar 
  - Current account balance 
  - User will be able to select from saved cards 
  - User will be able to input amount they wish to add to account 
  - Deposit button
  - Add card section
  - User will be able to add and save a new card to their account
    - Save button 
  - Bottom nav bar 
  
7. **Profile Page**
  - Top nav bar 
  - User's information will be split up into sections which can be edited
  - Section topics will include the following
    - Personal Information section  
    - User information section 
    - Details about you section
  - Save button
  - Update pasword section 
    - Dater will need to enter old password once, and new password twice.
    - Update password button
  - Bottom nav bar 
  
8. **Notifications page**

  - Top nav bar 
  - Unopened notifications section
  - A user will see there unread notifications at the top in order from newest to oldest
  - Opened notifications
  - A user will see a list of opened notifications in order from newest to oldest

**Cupid**
 
1. **Home page**

  - Because a cupid has less needs, we are able to give them multiple ways to get anywhere they need from the home page
  - Top nav bar 
    - Hamburger side bar 
      - Link to profile page 
      - Link to find Gigs page 
      - Link to completed Gigs page 
      - Link to feeback page 
      - Logout button
  - Main section will have cards that link to all of the same pages
  - Availble Gigs section
    - Here users should be able to see 2-3 availble Gigs in card form to make accepting Gigs faster and easier
  - On smaller screen sizes there will be a bottom nav bar with buttons to take you to the different pages
  - This nav bar will appear on every page
    - On larger screens this nav bar will be at the top underneath the logo
    - Nav bar buttons will link to the following pages
      - Home (if on home disabled) 
      - Find Gigs page 
      - Completed Gigs page 
      - Feedback page 
      - Profile page
      - Notification page 
  
2. **Find Gigs Page**
    
  - Top nav bar
  - Active Gig section 
    - Here a cupid wil be able to see the Gigs they have accepted 
    - Active Gigs should appear in card format with relevant information
    - Each active Gig should have a completed button and a reject button
  - Available Gigs section
    - Here a cupid will be able to see the Gigs they can accept
    - Each available Gig will be shown in card fomat with relevant information
    - Accept buttons should be on each card 
  - Bottom nav bar
  
3. **Completed Gigs page**
    
  - This page allows the cupid to reflect on their completed Gigs
  - All completed Gigs will be in card form with relevant information to the Gig
  - Each card will have a Rate Dater button which create pop up to rate Dater
  - Rate Dater pop up 
    - A cupid will be able to describe interaction with Dater
    - There will be a rating system like 1-5 stars 
    - send and cancel buttons 
  - Bottom nav bar
  
4. **Feedback page**
  
  - Top nav bar 
  - This page will have an overall star ratings at the top
  - all feedback/ ratings from Daters will be shown in card format
  - Each feedback card will show relevant information
  - Bottom nav bar 
  
5. **Profile Page**
    
  - Top nav bar 
  - Profile picture 
  - Cupids will be able to find their account balance, and how many successful Gigs vs the amount of Gigs they have accepted
  - Cupids personal information will be able to be edited 
  - Save button 
  - Bottom Nav bar 
  
6. **Notifications page**
    
  - Top nav bar
  - Unopened notifications section
  - A user will see there unread notifications at the top in order from newest to oldest
  - Opened notifications
  - A user will see a list of opened notifications in order from newest to oldest

**Manager**
  
1. **Home page**

  - Banner at top showing logo and Logout button 
  - 2 cards that link to both Cupids info page, and Daters info page
  - Will have graph to show revenue over time
  - Will have a general stats section which will hold information like: 
    - Total Dater 
    - Total cupids 
    - Active cupids 
    - Active Daters 
  - Gigs stats section will hold information like: 
    - Total Gigs 
    - Gigs per day 
    - Gigs completed 
    - Gigs dropped 
  - Will be a convert to PDF button to take stats and graph and produce a downloadable PDF of that information
  - On smaller screen sizes there will be a bottom nav bar with buttons to take you to the different pages
  - This nav bar will appear on every page
    - On larger screens this nav bar will be at the top underneath the logo
    - Nav bar buttons will link to the following pages
      - Home ( will be disabled when on home page) 
      - Cupids info 
      - Daters info 
  
2. **Cupids info page**

  - Manager will be able to see all cupids in card form 
  - Each cupid card will have relevant information like: 
    - Rating 
    - Name 
    - Completed Gigs 
    - A button to suspend the cupid 
  - Bottom nav bar 
  
3. **Daters info page**

  - Manager will be able to see all Daters in card form 
  - Each Dater card will have relevant information like:   
    - Rating 
    - Name 
    - A button to suspend the Dater
  - Bottom nav bar

### UI Diagrams

**Cupid Sign Up**

![sign up Cupid](images/createCupid.jpg)

**Dater Sign Up** 

![sign up Dater](images/createDater.jpg)

**Login Page** 

![Login](images/login.jpg)

**Dater Home Page**

![Dater Home](images/daterHome.jpg)

**AI Chat Tab**

![AI chat](images/AIchat.jpg)

**AI Voice Tab**

![AI Voice](images/AIListen.jpg)

**Plan Date Page**

![plan date](images/planDate.jpg)

**Rate Cupid/ Order Progress Page** 

![rate cupid](images/rateCupid.jpg)

**Calendar Page** 

![calendar](images/calendar.jpg)

**Payment Page**

![payment](images/Payment.jpg)

**Dater Profile Page** 

![Dater profile](images/daterProfile.jpg)

**Dater & Cupid Notifications Page**

![notifications](images/Notification.jpg)

**Cupid Home Page** 

Note: Although all of the Cupid diagrams do not show the notification button on the bottom nav bar, it will be there.

![Cupid home](images/cupidHome.jpg)

**Find Gigs Page** 

![find Gigs](images/findGigs.jpg)

**Completed Gigs Page** 

![completed Gigs](images/completedGigs.jpg)

**Feedback Page** 

![feedback](images/feedback.jpg)

**Cupid Profile Page**

![Cupid profile](images/cupidProfile.jpg)

**Manager Home Page** 

![Manager home](images/managerHome.jpg)

**Cupid Info Page** 

![Cupid info](images/cupidInfo.jpg)

**Dater Info Page**

![Dater info](images/daterInfo.jpg)


## 7. Input and Output
Although most of this was mentioned previously, we have condensed all the the inputs and outputs into single lists.


### Inputs

- User Profile Information 
  - Name 
  - Email 
  - Password 
  - Preferences 
    - Budget
    - Range 
    - Activity types 
- Authentication 
  - Username 
  - Password 
- AI interactions 
  - Chat prompts 
  - Questions 
  - Commands 
- Calendar date creation
  - Edit date 
- Payment card details 
- Ratings
- Navigation Actions 
  - Button Presses 
  - Taps 
  - Menu selections  

### Outputs 
 
- AI responses 
- Push notifications 
- Date Plans 
- Calendar Views 
  - upcoming date notifications 
- Payment Confirmations
- Profile Updates 
- Order & Cupid status updates 
- Accessibility toggle

### Expected Volume
To anticipate load and scalability needs, we project the following average volumes at launch:

- Daily Acitive Users: 100, scaling to 1,000 in later phases. 
- Notifications: 1-3 per user per day (AI updates, date reminders, jobs status)
- AI requests: 1-3 per user per session (questions, planning, feedback) 
- Payment: 1 transaction per active user per week 
- Calendar Events: 2-3 new or updated events per user per month

## 8. Security
### Overview — Defense in Depth
Cupid Code adopts a **defense-in-depth** approach: multiple independent controls are applied across the stack (client, server, data, and infrastructure).  Security is treated as a property of the entire system (architecture, code, build pipeline, and operations) rather than a single checkbox.  Controls are layered so that failure of one layer does not immediately expose sensitive data or critical functions.

---

### Threat Model — Summary & Key Mitigations
This section summarizes the highest-priority threats for Cupid Code and concrete mitigations.  The focus reflects your app’s features (real-time AI listening, payments, gig-worker access, shared couple data).

#### High-level threats
- **Unauthorized access / authN / authZ bypass**  
  *Mitigations:* strong password hashing (Argon2 preferred; PBKDF2 as fallback), email/phone verification, MFA for sensitive roles, short-lived access tokens + refresh tokens, OAuth2/OpenID Connect for external SSO, RBAC with least-privilege enforcement, require step-up auth for destructive operations (refunds, bans, data exports). Log and alert suspicious login patterns (IP/geolocation anomalies, impossible travel).

- **Injection (SQL, command, template)**  
  *Mitigations:* use Django ORM and parameterized queries only; avoid raw SQL. Validate and sanitize all inputs server-side. Static analysis and dependency scanning to catch vulnerable libraries. Apply a deny-by-default input validation policy for endpoints that accept free text.

- **Cross-Site Scripting (XSS)**  
  *Mitigations:* rely on Vue template auto-escaping; enforce CSP headers, sanitize any user HTML before rendering (if rich text is allowed), use HttpOnly cookies for session tokens when appropriate, and encode untrusted data placed into attributes or script contexts.

- **Cross-Site Request Forgery (CSRF)**  
  *Mitigations:* enable Django CSRF middleware for all form/API interactions that use cookies; require CSRF tokens on state-changing endpoints. For token-based API auth (Bearer/JWT), prefer header-based auth instead of cookies to avoid CSRF vectors.

- **Secret leakage (keys, tokens)**  
  *Mitigations:* never commit secrets to source control. Store secrets in Azure Key Vault (or equivalent KMS) and access them via managed identities. Enforce automated secret scanning for PRs and CI. Apply least-privilege to service accounts and rotate keys regularly.

- **Sensitive data exposure (PII, addresses, payment info)**  
  *Mitigations:* do not store raw payment card data — use Stripe/PayPal tokenization; encrypt PII at rest (field-level/envelope encryption for addresses); minimize retention; anonymize or redact logs; implement strict access controls and audit trails for PII access.

- **Denial of Service (DoS)**  
  *Mitigations:* rate limiting at API gateway, use Azure DDoS protection, autoscaling rules for legitimate traffic spikes, and circuit breakers for heavy third-party calls (AI, payment providers).

- **Privilege escalation / insider misuse**  
  *Mitigations:* RBAC, least privilege, separation of duties, require 2FA for admin actions, restrict DB and Key Vault access to ephemeral credentials and approved service principals, and log all privileged actions for review.

---

### Layered Controls (by layer)
#### Frontend (Vue)
- Enforce HTTPS everywhere (HSTS).  
- CSP headers; subresource integrity for critical third-party scripts (Not Implemented).  
- Input validation on UI (but do not rely on it — always validate server side).  
- Use secure storage patterns: avoid persistent storage of sensitive tokens in localStorage; prefer short-lived tokens in memory, or HttpOnly cookies with proper SameSite settings for session cookies (Not Implemented).  
- Obfuscate (never "securely hide") sensitive UI elements for couples (e.g., “surprise” flags) until consent reveals them.

#### Backend (Django)
- Use Django’s security middleware: CSRF, X-Frame-Options, XSS protections.  
- Centralized auth using Django + OAuth2/OIDC for SSO options (Google, GitHub) with verified email (Not Implemented).  
- Granular RBAC enforcement at both view and object level (row-level checks where necessary) (Not Implemented).  
- Use parameterized queries exclusively; restrict any raw SQL to reviewed, tested code.  
- All background workers run with limited permissions; service accounts scoped to required resources.

#### Data Layer (Postgres, blob storage)
- Encryption at rest (DB-managed or Azure-managed AES-256) (Not Implemented).  
- Encrypted backups and snapshots (Not Implemented).  
- Field-level encryption for PII such as addresses; use envelope encryption keys stored in Key Vault (Not Implemented).  
- Tokenize payment instruments: store only processor tokens (Stripe PaymentMethod IDs) and transaction metadata (Not Implemented).  

#### Infrastructure / Cloud
- Secrets in Azure Key Vault; access with managed identities and RBAC (Not Implemented).  
- TLS 1.3 across all endpoints; strict cipher suites (Not Implemented).  
- Azure-native logging and monitoring (integrate with SIEM / Azure Sentinel) (Not Implemented).  
- Network-level controls: private subnets for DB, limited inbound rules, and API gateway rate limiting (Not Implemented).  

---

### Data Protection: specifics & best practices
- **At-rest encryption:** enforce Azure-managed encryption (AES-256) for Postgres, Blob storage, and backups. Use database-level Transparent Data Encryption (TDE) where supported.  
- **In-transit encryption:** require TLS 1.2+ (prefer TLS 1.3) for all communications (client↔API, API↔DB, API↔third-party). Certificate management handled by Azure Certificates/Key Vault or Let’s Encrypt via automation.  
- **Secrets & Key Rotation:** store all secrets/keys in Azure Key Vault. Enforce automated rotation policies for keys and credentials (e.g., 90-day rotation or as required by policy). Use short-lived service tokens where possible. Monitor Key Vault access logs.  
- **Addresses & Calendar data:** treat addresses as sensitive PII. Use field-level encryption (envelope encryption) for these fields; decrypt only in server memory and only when needed by a business flow (e.g., displaying to the user or sharing with an assigned Cupid, with user consent). For couple-shared data, honor per-partner consent flags before decryption.  
- **Payment/Card handling:** do not store PANs or CVV. Use Stripe Elements / Payment Intents to collect card data directly and receive a token/PaymentMethod id that can be used server-side. Keep PCI scope minimal by delegating card capture and storage to the payment processor. Log only non-sensitive transaction metadata.  
- **Token scopes and lifetime:** use OAuth2 scopes for granular API tokens (e.g., `read:profile`, `write:gigs`, `admin:billing`). Keep access tokens short-lived (minutes to hours) and use refresh tokens with rotation and revocation. Implement token revocation lists and immediate session invalidation after password changes or account deletion.
 (Not Implemented for: At-rest encryption, Secrets & Key Rotation via Key Vault, Field-level encryption for addresses, Stripe tokenization, OAuth2 scopes/short-lived tokens.)

---

### Role-Based Access Control (RBAC) — model & enforcement
Define clear roles and least-privilege permissions. Enforce both coarse-grained (API-level) and fine-grained (resource/object-level) rules.

#### Roles & typical permissions
- **Dater (end-user)**  
  - Create/update own profile and preferences.  
  - Initiate payments (via Stripe/PayPal token flow), schedule dates, enable/disable in-date listening.  
  - View own transaction history, AI interaction logs (anonymized), and delete own account.

- **Cupid (gig worker)**  
  - View assigned gigs/orders and non-sensitive contextual info needed to fulfill tasks (approximate address, time window) — only after user's explicit consent where required.  
  - Update gig status, send messages to assigned dater, request reimbursements.  
  - No access to user's full financial history or private couple notes unless explicitly authorized.

- **Manager / Admin**  
  - System telemetry, safety/moderation tools (flagging, bans), dispute resolution (refunds), and compliance reporting.  
  - Sensitive actions (e.g., refunds, account takeovers, data exports) require two-person approval or step-up authentication.  
  - Admin accesses are logged, time-limited sessions with enforced MFA.

#### Enforcement patterns
- Use object-level permissions (Django Guardian-style or similar) for resources that must be shared selectively (couple timelines, surprise gifts).  
- All privileged endpoints require an `admin` scope and step-up MFA.  
- Periodic automated audits of role assignments; revoke stale privileges.  
- Implement consent flags for couples: features like “hide surprise gift” are enforced in the authorization layer — decryption and display logic check consent before revealing.
 (Not Implemented for: object-level permissions, admin scopes with step-up MFA, automated audits of role assignments, consent flags enforcement.)

---

### Compliance & Governance
- **Age gating:** require DOB at registration and validate via email/phone verification. Deny or lock accounts under 18. Keep dob validation logs for audit.  
- **Data subject rights:** support export (machine-readable format) and permanent deletion of user data. Provide an admin workflow to comply with verified deletion requests and a method to redact backups per policy.  
- **Audit logs:** immutable, tamper-evident logs of authentication events, role changes, payment events, admin actions, and data accesses. Centralize logs in a SIEM and retain according to regulatory requirements (e.g., 1 year for routine logs, longer for financial events). Log access must itself be audited.  
- **PII minimization:** collect only required attributes. Where possible, store derived or hashed values instead of raw PII (e.g., hashed addresses for deduplication). Anonymize AI logs used for model improvement; retain raw transcripts only when explicitly approved by the user.  
- **Payments / PCI:** remain out of PCI-scope by relying on Stripe/PayPal for card storage and processing. Ensure server interactions with payment APIs follow recommended best practices (server-side verification of webhooks, idempotency keys).  
- **Legal & privacy policy:** publish a clear privacy policy describing data use, retention, and sharing. Provide opt-outs for marketing and telemetry. Maintain a data processing addendum if working with processors in GDPR jurisdictions.  
- **Testing & audits:** plan regular security scans (SAST/DAST), quarterly dependency vulnerability scans, and at least annual penetration testing. Consider a bug-bounty or coordinated vulnerability disclosure program as the product grows.
 (Not Implemented for: age gating verification, data export/deletion tooling, immutable audit logs/SIEM integration, Stripe/PayPal PCI out-of-scope setup, formal privacy policy, SAST/DAST and vulnerability scanning.)

---

### Operational Security Practices & Incident Response
- **Secure SDLC:** require code reviews, SAST in CI, dependency vulnerability checks (dependabot/renovate), and secret scanning for pull requests.  
- **CI/CD:** separate pipelines and credentials for dev/staging/prod. Use ephemeral deploy tokens and require approvals for production deploys.  
- **Access management:** enforce MFA for all developer and admin accounts; use role-based access to Azure resources; periodic access reviews.  
- **Monitoring & alerting:** integrate application logs and Azure activity logs into a SIEM (Azure Sentinel recommended). Create runbooks for critical alerts.  
- **Incident response:** maintain an incident response playbook (containment, forensics, user notification timelines), contacts for legal/regulatory obligations, and pre-defined communication templates for breach notifications. Test the IR playbook with tabletop exercises.
 (Not Implemented for: SAST/secret scanning in CI, environment-separated pipelines with approvals, MFA for developers/admins, SIEM integration/runbooks, incident response playbook.)

## 9. Risks and Mitigation

### Explanation of Risk Mitigation Table
The table below summarizes the key risks identified for the AI-assisted dating help app, across critical categories such as Technology, Security, Data, and Schedule. Each risk is described with its causal factors, potential impact, and likelihood of occurrence. To support proactive management, specific preventative mitigations are outlined that aim to reduce the chance or severity of each risk. Contingency or fallback plans describe actions to be taken if a risk materializes despite these safeguards.

Triggers and early warning indicators provide measurable signals or thresholds that help detect when a risk is emerging or escalating, enabling rapid response. The residual risk denotes the remaining exposure after applying mitigations, while the status tracks the current risk handling state (e.g., Open, Monitoring).

This structured approach ensures clarity, accountability, and readiness to handle uncertainties, helping safeguard the project’s success and user trust in our app.

#### Risk Table Key
- **L (Low):** Rare/Minor (unlikely or easily handled)
- **M (Medium):** Possible/Moderate (would disrupt but manageable)
- **H (High):** Likely/Critical (seriously affects project or business)
- **Status:** Open = active/unresolved; Monitoring = being tracked; Closed = fully mitigated/resolved
- **Exposure:** Combines likelihood and impact for overall risk attention
- **Trigger/Indicator:** Metric or event that flags a risk may materialize


| ID  | Category         | Risk Statement                                                  | Likelihood | Impact | Exposure | Preventative Mitigation                | Contingency / Fallback             | Trigger/Indicator                   | Status    |
|-----|------------------|-----------------------------------------------------------------|------------|--------|----------|-----------------|----------------------------------------|-------------------------------------|-------------------------------------|
| R1  | Payments/Webhooks| Webhook failures/job overlaps → Revenue loss, user impact       | Medium     | High   | High      | Sandbox-first, idempotency keys        | Circuit breaker, manual audit, retry| Failure rate >2%/day                | Monitoring |
| R2  | AI Latency/Cost  | AI slow/costly → Bad experience, unscalable costs               | Medium     | Medium | Medium   | Observability, rate limiting           | Disable costly features, fallback   | Latency p95 >1.2s for 3 days         | Monitoring |
| R3  | Notification     | Non-delivery → Missed connections, retention drop               | Low        | High   | Medium   | Retry logic, multiple providers        | Alert users, manual notification    | Notification failures >1%/day        | Monitoring |
| R4  | Auth/SSO         | SSO/auth errors → Users locked out, increased support            | Low        | High   | Low      | Feature flags, error logging           | Switch to local login, escalate     | Auth error spikes >100/hr            | Monitoring |
| R5  | Data Migration   | Migration loss → Data integrity compromised, app downtime        | Low        | High   | Medium         | Sandbox/backup, rollback plan          | Restore backup, freeze changes      | Audit fails, missing records         | Monitoring |
| R6  | Schedule         | ML/data delays → Missed launch/revenue                          | Medium     | Medium | Medium   |  Milestone review, cadence checks       | Shift resources, move deadlines     | Milestone slip, unresolved blockers  | Monitoring |
| R7  | Security  | Bank info unencrypted → Data breach → Legal, financial, and reputation damage | Medium        | High      | High        | Implement AES-256 encryption, limit access, audit regularly | Immediate full encryption, user & regulator notification | Audit reveals unencrypted bank info, or breach occurs | Open     |

## 10. Data Design
### 10.1 Scope & Goals
Current schema (SQLite) implements merged role+profile patterns (Dater, Cupid) and an early Gig workflow. Several security‑sensitive financial storage models (PaymentCard, BankAccount) exist that must be deprecated before production. Goal: Stabilize current entities, schedule refactors (AI session separation, payment tokenization, assignment abstraction), and remove unsafe PCI data.

### 10.2 Entity Inventory: Implemented vs Planned
| Entity (Code Name) | Implemented? | Purpose (Current) | Planned Change / Future Name |
|--------------------|-------------|-------------------|------------------------------|
| User               | Yes         | Auth + role + phone_number | Add UUID PK (optional), audit fields |
| Dater (OneToOne User) | Yes      | Extended Dater attributes & metrics | Rename to DaterProfile; trim large free‑text fields; encrypt selected PII |
| Cupid (OneToOne User) | Yes      | Cupid state & performance stats | Rename to CupidProfile; add availability & payout token (no raw banking) |
| Gig                | Yes         | Match Dater to Cupid + status | Extract GigAssignment (separate Cupid link + timestamps) |
| Quest              | Yes         | Requested items / context for a Gig | Fold into Gig (JSON) or keep normalized; evaluate |
| Message            | Yes         | Mixed user + AI chat entries (from_ai flag) | Split into AISession + AIMessage (session metadata, tokens) |
| Date               | Yes         | Scheduled date event (planning) | Keep; may relate to future couple/shared features |
| Feedback           | Yes         | Star rating + message for a Gig (owner→target) | Add XOR validation (only one target type later) |
| PaymentCard        | Yes (Unsafe) | Stores raw card PAN + CVV (PCI scope) | REMOVE: Replace with PayPal SDK |
| BankAccount        | Yes (Unsafe) | Stores raw routing/account numbers | REMOVE: External payout provider token only |
| Subscription       | No          | Future recurring access | Add after payment rails established |
| Transaction        | No          | Ledger / wallet accounting | Add with payments (PayPal webhooks) |
| Payment (Intent)   | No          | Track provider intent/status | Add before enabling real payments |
| Notification       | No          | Queue of outbound messages | Add (email/SMS + in‑app) |
| AuditLog           | No          | Immutable security/business events | Add (append‑only) |
| FeatureFlag        | No          | Runtime configuration | Add (simple key/value) |
| KeyRotationEvent   | No          | Track encryption key usage | Add with encryption rollout |

### 10.3 Current Entity Details (from /code/server/api/models.py)
![DatabaseERD](./images/cupidERD.png)

(Fields summarized; omit Django implicit id unless primary key overridden.)

User  
- Fields: id (int PK), username, email, password, role (Dater|cupid|manager), phone_number (unique, length=10).  
- Gaps: No created_at/updated_at audit timestamps; no soft delete; no MFA.

Dater  
- PK: user (OneToOne).  
- Key Fields: budget, communication_preference, multiple narrative TextFields (description, strengths, weaknesses, interests, past, nerd_type, relationship_goals), ai_degree, location, rating_sum/rating_count, is_suspended, profile_picture.  
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
- Fields: Dater (FK Dater), cupid (FK Cupid nullable), status (UNCLAIMED|CLAIMED|COMPLETE), date_time_of_request (auto), date_time_of_claim, date_time_of_completion, Quest (OneToOne), dropped_count, accepted_count.  
- Missing: Explicit monetary, title/description, cancellation reason, normalized assignment audit.

Date  
- Fields: Dater, date_time, location, description, status (planned|occurring|past|canceled), budget.  

Feedback  
- Fields: owner (nullable, SET_NULL), target (User), Gig, message, star_rating, date_time.  
- Missing: Constraints on rating range (validation), no uniqueness (duplicate ratings possible).

PaymentCard (To Remove)  
- Raw card_number, cvv, expiration stored as TextField. HIGH RISK.

BankAccount (To Remove)  
- Raw routing_number, account_number stored in cleartext. HIGH RISK.

### 10.4 Required Refactors & Tickets
| Priority | Action | Rationale |
|----------|--------|-----------|
| Critical | Remove PaymentCard & BankAccount before prod; migrate to external tokenization (PayPal) | Eliminate PCI scope & breach risk |
| High | Introduce AISession & AIMessage; migrate existing Message rows | Enables retention limits & analytics |
| High | Add created_at/updated_at (auto timestamps) to core entities | Auditing & troubleshooting |
| High | Replace gig.cupid nullable with gigAssignment (Gig FK + Cupid FK + timestamps) | Normalizes lifecycle events |
| Medium | Consolidate / structure large Dater narrative fields (enum + JSON) | Queryability & privacy |
| Medium | Add soft delete or active flags (User, Dater, Cupid) | Regulatory deletes |
| Medium | Add Feedback constraints (rating 1–5, unique (owner,Gig) ) | Data integrity |
| Medium | Add indexes (gig.status, Message.owner + id) | Query performance |
| Low | Add AuditLog table | Security visibility |
| Low | Introduce FeatureFlag table | Safe gradual rollout |

### 10.5 Interim vs Target Model Mapping
| Conceptual (Original Doc) | Current Model | Gap / Plan |
|---------------------------|---------------|------------|
| UserProfile               | (Absent)      | Either add minimal profile table or keep fields in role models |
| DaterProfile              | Dater         | Rename + field review & encryption |
| CupidProfile              | Cupid         | Rename + availability expansion |
| gigAssignment             | (Inline cupid FK on Gig) | Create new table; move timestamps |
| AISession/AIMessage       | Message       | Split & migrate |
| Payment/Transaction       | (Absent)      | Add with PayPal integration |
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
| Gig timestamps | Gig | OK | Ensure timezone UTC |

Planned Protection Additions:
- Application-layer field encryption (select narrative or location fields if stored long term).
- Tokenization for payouts (provider-managed).
- Retention jobs for Message (purge or anonymize after X days).

### 10.7 Data Flows (Tagging Current vs Planned)
1. Dater requests Gig (Implemented) → Gig row (status=UNCLAIMED).  
2. Cupid claims Gig (Implemented) → status=CLAIMED; future: create gigAssignment row.  
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
- UNIQUE (owner, Gig) on Feedback.
- UNIQUE (gigAssignment.gig_id) when introduced.
- NOT NULL defaults for gig.status (already via choices).
- DB index additions (see 10.9).

### 10.9 Index & Performance Plan
Immediate (add migrations):
- Gig: index_together (status, date_time_of_request).
- Message: (owner_id, id) for chronological user queries.
- Feedback: (gig_id).
Post-Refactor:
- AIMessage: (session_id, created_at).
- gigAssignment: (cupid_id, created_at).
- Partial indexes (Postgres) for active Gigs once migrated.

### 10.10 Migration / Refactor Strategy
Phase A (Pre-security hardening):
- Create migrations to add timestamps (auto_now_add / auto_now) where missing.
- Add indexes above.

Phase B (Security Remediation):
- Create new PaymentMethodToken model (provider, user FK, last4, brand, exp_month/year, provider_token).  
- Migrate (export + securely delete) then DROP PaymentCard & BankAccount tables.  
- Commit architecture doc update referencing PayPal checkout.

Phase C (AI Session Separation):
- Add AISession + AIMessage tables.
- Backfill: For each unique (owner) contiguous Message block create session.

Phase D (Gig Assignment):
- Create gigAssignment; migrate existing cupid/time fields.
- Remove cupid FK from Gig (or keep nullable for fast access, but ensure consistency).

### 10.11 Retention & Deletion
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


