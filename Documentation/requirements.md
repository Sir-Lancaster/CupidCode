# Requirements Specification 

## Summary

### Problem Statement

Dating presents unique challenges for many individuals, especially those who identify as “nerds” or socially anxious. Preparing for and navigating a date often feels overwhelming, and many lack accessible support systems to guide them. Cupid Code was designed as a solution: an AI-assisted dating platform that provides personalized advice, real-time interventions, and on-demand Cupid gig workers to help “save” dates with items or services when things go wrong.

Our team inherited Cupid Code in a partially completed state. The previous team established the foundation of the application with core components like authentication, user roles, and a visual manager dashboard. However, much of the platform’s critical functionality — especially those tied to the money system and AI — remains incomplete or non-functional. Many must-have requirements identified in the original RSD were either partially implemented or left unfinished, which prevents the platform from operating as intended.

In summary, we were provided a project that demonstrates the conceptual framework of Cupid Code but falls short of delivering a usable MVP. Authentication works, roles are defined, and Cupids can sign up, but daters cannot fund their accounts, Cupids cannot withdraw earnings, and the AI fails to provide meaningful assistance. This leaves the system more of a prototype shell than a functional product.

### Solution Statement

The previous team established important foundations we can build on. Below is a concise accounting of the system as we received it, grouped by completion level.

#### Completed
- Authentication (username/password): working sign-in/sign-up.
- Cupid sign-up portal: gig workers can register.
- Microphone permission integration: device mic access is available in the app.
- Documentation/manuals present: user and manager manuals exist in the repository.
- Browser-based web app: site accessible on mobile and desktop browsers.

#### Partially Implemented
- Dater profiles: interests and goals present; communication preferences still to add.
- Manager dashboard: user interface exists; current stats appear placeholder and not wired to live data.
- Scheduling: daters can schedule dates; Cupid busy/peak-time logic not verified.
- Order and gig placement UI: gigs/orders can be created, but no real payment flow occurs yet.
- AI listening: microphone capture path exists; guidance and responses remain limited.

#### Incomplete
- Funds pipeline: daters cannot add funds; budgets can be set on gigs but do not deduct from a user balance.
- Cupid payments and payouts: Cupids may be shown a share (for example, 10 percent) but no actual transfer or deduction occurs; no withdraw/transfer flow exists.
- Subscriptions: monthly tiers ($10/$15) not implemented.
- Free tier: limited-budget intervention not implemented, as it depends on subscriptions and funds.
- AI interventions and automated purchases: no meaningful real-time coaching or purchase execution (flowers, food, tickets) yet.
- Notifications: real-time notifications (and email/SMS fallbacks) not present.
- Single Sign-On (SSO): Google, GitHub, and similar options not implemented.
- Ratings and feedback tied to gigs: not activated because money and gig completion are not flowing.
- Cupid availability toggle (on/off duty): not present.
- Revenue and analytics: revenue model cannot function without subscriptions and payouts; dashboard metrics are not tied to transactions.

## Requirements

### Functional Requirements

Key: **M** = Must, **S** = Should, **C** = Could, **W** = Won’t

- Integrate shared calendar sync for couples. **(S)**
- Suggest anniversary/birthday plans from saved preferences. **(S)**


### Nonfunctional Requirements

Key: **M** = Must, **S** = Should, **C** = Could, **W** = Won’t

1. **Performance**
  - Connect to the AI API for the listen and chat features. **(C)**
  - Record change history for shared features (who edited joint preferences or calendar sync) to provide an audit trail. **(C)**

2. **Security**
  - When auto filling the user information, the users' address is still encrypted rendering the information useless. We need to fix that. **(M)**
  - Ensure that card data is properly encrypted in the database. **(M)**
  - change the encryption of addresses on the calendar and gigs pages. **(M)**
  - Link cards to a payment processor to allow for seamless adding of cash to a users account. **(S)** 
  - Enforce role‑based data segregation for couples so spouse‑only artifacts (surprise gifts, private notes) remain hidden until revealed. **(C)**
  - Provide per‑partner privacy and consent controls for shared features (who can see/edit plans, gifts, and timeline). **(C)**
  
3. **Usability**
  - Add error messages when invalid input options are provided. **(M)**
  - Clarify instructions for running software to reduce confusion. **(M)**
  - Include software dependency information and installation instructions in the documentation. **(S)**
  - Improve contrast for readability. **(M)**
  - Ensure compatability with screen readers. **(M)**
  - Comply with general accessibility practives **(S)**

4. **Rebranding**
  - Re-generate the images for the app **(M)**
  - Dynamically allocate space depending on the screen size of the user. **(S)**
  - Change the color schemes **(C)**
  - Improve consistency in the app. for example the navigation menu is nested in a hamburger menu when a user is logged in, but not when you are not logged in. **(C)**
  - Change the layout of the pages, center the buttons, change the shapes to be more inline with the theme of the application. **(C)**


### Business Requirements

Key: **M** = Must, **S** = Should, **C** = Could, **W** = Won’t

- Support married users as an adjacent audience (without changing core goals). **(S)**
- Support subscription billing (tiers for singles/married users). **(S)**

### User Requirements

Key: **M** = Must, **S** = Should, **C** = Could, **W** = Won’t

1. **General End-users**
  - Interact with a sleek, contemporary user interface. **(M)**
  - Adjust account settings using a variety of managerial tools. **(M)**
  - Link more than one payment method to finance services. **(M)**
  - Utilize an organized task management system. **(M)**
  - Switch easily between application roles. **(S)**
  - Opt to use a mobile application for portability and ease. **(C)**

2. **Dating End-users**
  - Receive push alerts to receive real-time assistance. **(M)**
  - Engage in meaningful dialogue with an AI chatbot. **(M)**
  - Allow AI chatbot to listen during dates. **(M)**
  - Swipe on potential matches by linking an external dating service. **(S)**
  - Work with a fully integrated match-finder that offers all standard dating app support (i.e. messaging). **(C)**

3. **Cupid End-users**
  - Have several gig management tools to organize gigs. **(M)**
  - Update a connected dater's software in real time. **(M)**
  - Access a variety of third-party services to assist dater. **(M)**
  - Ability to message the dater with updates, pointers, etc. **(S)**
  - Navigate using a Google Maps API or similar. **(C)**

4. **Married/Coupled End-users**
  - Provide a relationship timeline of past date nights and milestones. **(S)**
  - Provide shared calendar sync for couples. **(S)**
  - Suggest gifts based on spouse preferences and past data. **(S)**
  - Support joint profile preferences for couples. **(S)**
  - Suggest family‑inclusive activities when desired. **(C)**

## User Stories 

### User 

- As a user, I want the app to dynamically adjust its layout to my screen size so that I can comfortably use it on any device.
- As a user, I want the AI chat and listening features to connect quickly and reliably to the backend API so that my conversations feel seamless.
- As a user, I want my payment information to be securely encrypted during transactions so that I feel safe making purchases.
- As a user, I want error messages to appear when I enter invalid data in forms so that I know what went wrong and how to fix it.
- As a user, I want the app to validate monetary amounts and confirm large transactions before processing so that I don’t make costly mistakes.
- As a user, I want the interface to have high contrast and support screen readers so that it’s accessible to users with visual impairments.
- As a user, I want clear documentation that includes required software versions and setup instructions so that I can install and run the app without confusion.
- As a user, I want my address to remain encrypted only where necessary so that my privacy is protected without interfering with features like calendar and gigs.
- As a user, I want the app to reflect a fresh brand identity with updated colors, images, and layout so that it feels modern and engaging.
- As a user, I want customizable navigation elements instead of generic hamburger menus so that I can tailor the interface to my preferences.
- As a user, I want to interact with a stylish, modern-looking user interface so I can easily and confidently use Cupid Code.
- As a user, I want to have multiple account management tools so I can properly atune my account settings ad hoc.
- As a user, I want to have the option to connect multiple payment options so I can seamlessly finance Cupid Code's services.
- As a user, I want to have a structured task management system so I can straightforwardly tend to my responsibilities.

### Dater

- As a dater, I want to recieve push notifications so I can get real time support on my dates.
- As a dater, I want to have meaningful conversation with an AI chatbot so I can fall back on a dynamic and nuanced support system.
- As a dater, I want my AI chatbot to optionally listen on my date so I can immersively make smart dating decisions.

### Married User / Couple

- As a Married User, I want to sync both our calendars so that date plans don’t conflict.
- As a Married User, I want recurring date-night reminders so that we maintain a regular routine.
- As a Married User, I want special-occasion plans (anniversaries/birthdays) so that I don’t miss important dates.
- As a Married User, I want a shared relationship timeline of past date nights and milestones so that we can reflect and plan better.
- As a Married User, I want joint preferences (budget, cuisines, activities) so that suggestions fit both of us.
- As a Married User, I want family-friendly suggestions so that we can include kids when desired.
- As a Married User, I want gift suggestions for my spouse so that I can plan thoughtful surprises.
- As a Married User, I want per-partner privacy and consent controls so that I can choose what my spouse can see.
- As a Surprise Planner, I want private gift planning (hidden until reveal) so that my spouse doesn’t see surprises early.
- As a Couple, I want an audit trail of changes to our shared settings so that we can resolve who changed what quickly.

### Cupid

* As a cupid, I want to have multiple gig management solutions so I can systemically govern my gigs.
* As a cupid, I want to directly connect to a dater's Cupid Code experience and reactively update their software.
* As a cupid, I want to have multiple third-party services available to me so I can effectively serve my dater.

### Manager

- (none)

### Business/Company

- As a Company, I want to support married-couple experiences so that we grow our audience without changing the product’s core goals.
- As a Company, I want a couples-tier subscription option so that households can access shared features at fair pricing.

## Overall MoSCoW

### Must

- General users can interact with a sleek, contemporary user interface.
  _From categories: User_
- General users can adjust account settings using a variety of managerial tools.
  _From categories: User_
- General users can link more than one payment method to finance services.
  _From categories: User_
- General users can utilize an organized task management system.
  _From categories: User_
- Daters can receive push alerts to receive real-time assistance.
  _From categories: User_
- Daters can engage in meaningful dialogue with an AI chatbot.
  _From categories: User_
- Daters can allow AI chatbot to listen during dates.
  _From categories: User_
- Cupids can have several gig management tools to organize gigs.
  _From categories: User_
- Cupids can update a connected dater's software in real time.
  _From categories: User_
- Cupids can access a variety of third-party services to assist dater.
  _From categories: User_

### Should

- Integrate shared calendar sync for couples.
  _From categories: Functional, User_
- Provide a relationship timeline of past date nights and milestones.
  _From categories: User_
- Suggest anniversary/birthday plans from saved preferences.
  _From categories: Functional_
- Suggest gifts based on spouse preferences and past data.
  _From categories: User_
- Support joint profile preferences for couples.
  _From categories: User_
- Support married users as an adjacent audience (without changing core goals).
  _From categories: Business_
- Support subscription billing (tiers for singles/married users).
  _From categories: Business_
- General users can switch easily between application roles.
  _From categories: User_
- Swipe on potential matches by linking an external dating service.
  _From categories: User_
- Ability to message the dater with updates, pointers, etc.
  _From categories: User_

### Could

- Enforce role‑based data segregation for couples so spouse‑only artifacts (surprise gifts, private notes) remain hidden until revealed.
  _From categories: Nonfunctional_
- Provide per‑partner privacy and consent controls for shared features (who can see/edit plans, gifts, and timeline).
  _From categories: Nonfunctional_
- Record change history for shared features (who edited joint preferences or calendar sync) to provide an audit trail.
  _From categories: Nonfunctional_
- Suggest family‑inclusive activities when desired.
  _From categories: User_
- General users can opt to use a mobile application for portability and ease.
  _From categories: User_
- Daters can work with a fully integrated match-finder that offers all standard dating app support (i.e. messaging).
  _From categories: User_
- Cupids can navigate using a Google Maps API or similar.
  _From categories: User_

### Won't

- (To be updated as development progresses)

## Use Case Diagrams

