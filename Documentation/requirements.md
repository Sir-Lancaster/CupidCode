# Requirements Specification 

## Summary

## Requirements

### Functional Requirements

Key: **M** = Must, **S** = Should, **C** = Could, **W** = Won’t

- Notifications and suggestions outside of the app through email, text, etc. **(M)**
- Automatic real time feedback from agentic AI **(M)** 
- Webpage accessible on computer and phone **(M)**
- Database access for AI to remember things about the user **(M)**
- Connection to Stripe and PayPal payment processing APIs **(M)**
- Date planning interface **(S)**
- Date planning capability for AI **(S)**
- Date plan editing capability for user **(S)**
- Integrate shared calendar sync for couples. **(S)**
- Suggest anniversary/birthday plans from saved preferences. **(S)**
- Integrate a weather API so the agentic AI can plan appropriate activities and give relevant suggestions **(C)**
- AI capability to give feedback after a date **(C)**
- AI capability to set goals for the user based on their date history **(C)**
- AI capability to make predictions about the user to create a more complete profile and make more accurate suggestions **(C)**
- Integrate dating app APIs (e.g. Tinder) to find dates for the user **(C)**
- Integrate location services for real-time updates on the location of Cupids **(C)**
- Microtransactions **(W)**

### Nonfunctional Requirements

Key: **M** = Must, **S** = Should, **C** = Could, **W** = Won’t

- Enforce role‑based data segregation for couples so spouse‑only artifacts (surprise gifts, private notes) remain hidden until revealed. **(C)**
- Provide per‑partner privacy and consent controls for shared features (who can see/edit plans, gifts, and timeline). **(C)**
- Record change history for shared features (who edited joint preferences or calendar sync) to provide an audit trail. **(C)**

### Business Requirements

Key: **M** = Must, **S** = Should, **C** = Could, **W** = Won’t

- Support married users as an adjacent audience (without changing core goals). **(S)**
- Support subscription billing (tiers for singles/married users). **(S)**

### User Requirements

Key: **M** = Must, **S** = Should, **C** = Could, **W** = Won’t

- Provide a relationship timeline of past date nights and milestones. **(S)**
- Provide shared calendar sync for couples. **(S)**
- Suggest gifts based on spouse preferences and past data. **(S)**
- Support joint profile preferences for couples. **(S)**
- Suggest family‑inclusive activities when desired. **(C)**

## User Stories (Married-Only) — Grouped by Persona

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

- (none)

### Manager

- (none)

### Business/Company

- As a Company, I want to support married-couple experiences so that we grow our audience without changing the product’s core goals.
- As a Company, I want a couples-tier subscription option so that households can access shared features at fair pricing.

## Overall MoSCoW (Consolidated — Married-Only, Deduped)

### Must

- Notifications and suggestions outside of the app through email, text, etc.
  _From categories: Functional_
- Automatic real time feedback from agentic AI
  _From categories: Functional_
- Webpage accessible on computer and phone
  _From categories: Functional_
- Database access for AI to remember things about the user
  _From categories: Functional_
- Connection to Stripe and PayPal payment processing APIs
  _From categories: Functional_

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
- Date planning interface.
  _From categories: Functional_
- Date planning capability for AI.
  _From categories: Functional_
- Date plan editing capability for user.
  _From categories: Functional_

### Could

- Enforce role‑based data segregation for couples so spouse‑only artifacts (surprise gifts, private notes) remain hidden until revealed.
  _From categories: Nonfunctional_
- Provide per‑partner privacy and consent controls for shared features (who can see/edit plans, gifts, and timeline).
  _From categories: Nonfunctional_
- Record change history for shared features (who edited joint preferences or calendar sync) to provide an audit trail.
  _From categories: Nonfunctional_
- Suggest family‑inclusive activities when desired.
  _From categories: User_
- Integrate a weather API so the agentic AI can plan appropriate activities and give relevant suggestions
  _From categories: Functional_
- AI capability to give feedback after a date
  _From categories: Functional_
- AI capability to set goals for the user based on their date history
  _From categories: Functional_
- AI capability to make predictions about the user to create a more complete profile and make more accurate suggestions
  _From categories: Functional_
- Integrate dating app APIs (e.g. Tinder) to find dates for the user
  _From categories: Functional_
- Integrate location services for real-time updates on the location of Cupids
  _From categories: Functional_

### Won't

- Microtransactions
  _From categories: Functional_

## Use Case Diagrams
