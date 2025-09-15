# Requirements Specification 

## Summary

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

## Overall MoSCoW

### Must

- (none)

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

### Could

- Enforce role‑based data segregation for couples so spouse‑only artifacts (surprise gifts, private notes) remain hidden until revealed.
  _From categories: Nonfunctional_
- Provide per‑partner privacy and consent controls for shared features (who can see/edit plans, gifts, and timeline).
  _From categories: Nonfunctional_
- Record change history for shared features (who edited joint preferences or calendar sync) to provide an audit trail.
  _From categories: Nonfunctional_
- Suggest family‑inclusive activities when desired.
  _From categories: User_

### Won't

- (none)

## Use Case Diagrams

