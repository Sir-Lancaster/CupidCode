# Requirements Specification 

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

### User Stories
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