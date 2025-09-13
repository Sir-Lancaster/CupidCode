 
# CS3450 Team 2


## Requirements Doc 

**Jan 27 2024**

**Sprint Leader: Daniel Barfuss**

**Sprint Followers: Nate Stott, Emma Wright, Eric DeBloois, Nate McKenzie, Brighton Ellis, Brandon Herrin**

**Problem Statement**

Dating  poses challenges due to the high stakes of forming a romantic relationship  with someone unfamiliar. There are many social pitfalls to fall into, and often, people find that there is little outside help available. This difficulty is especially pronounced for computer scientists and "nerd" types, who already have a reputation for struggling with interpersonal relationships. There  is a need for a solution that addresses these common dating hurdles by providing tailored support for individuals in this demographic, enhancing their ability to form meaningful connections.

**Solution Statement**

Preparing for a date can be intimidating, and it can be tough to know what to say or how to act. Cupid Code is a revolutionary dating assistance platform that utilizes artificial intelligence to help individuals through that process. Cupid Code supplies the user with an artificial intelligence (AI) partner that the user can ask questions and get tips for the date. It can even listen in on the conversation and provide immediate assistance when it senses trouble. If a planned activity falls through, then the AI can pay for an item or service and call for a “Cupid”, a hired assistant, to deliver it right to you during the date. 


## Functional Requirements:

1. **User Authentication:**
    * Daters, Cupids, and Managers must be able to authenticate using an email, and password.
2. **User Roles and Interfaces:**
    * Daters will have access to features like scheduling dates, adding funds, setting budget limits, talking with the AI, and giving and receiving feedback.
    * Cupids will be able to view available requests, accept requests, complete/drop requests, and transfer earned money. As well as give and receive feedback.
    * Managers will have the authority to monitor user activities, access real-time data, and remove Daters and Cupids for policy violations.
3. **AI Integration:**
    * The AI will be able to listen during dates, provide real-time advice to Daters, and summon Cupids for emergency date-saving assistance.
    * The dater will be able to chat with the AI to get advice before, during, and after their date.
4. **Budget Management:**
    * Daters will be able to set budget limits for each date, and the Cupid must operate within those limits.
    * Daters will also be able set a default budget for all future dates.
6. **Scheduling:**
    * Daters will have the ability to schedule dates, and will be able to manage their dating calendar.
7. **Payment System:**
    * Daters will be able to transfer funds to Cupid Code for use in emergency date-saving assistance.
    * Cupids will be able to view the amount of money they have earned, and transfer it to their bank account.


## Non-Functional Requirements:

1. **Security:**
    * The platform must create and adhere to rigorous security standards that ensure the confidentiality and integrity of user data. Such as encrypting data at rest and in transit, and only allow Daters, Cupids and Managers with a valid login to get into the system.
    * User data will only be available to those who are authorized to view it.
2. **Scalability:**
    * The system will be scalable to accommodate a growing user base.
3. **Availability:**
    * The platform will be reliable, with minimal downtime or disruptions with five 9’s of durability.
4. **Performance:**
    * The platform will have low latency communication between Daters, Cupids, and the AI.
5. **Usability:**
    * The user interfaces for Daters, Cupids, and Managers will be intuitive and user-friendly.
6. **Compatibility:**
    * The application will be compatible with various devices and browsers. 
    * The application will utilize responsive design to ensure good experiences on desktop and mobile.
7. **Compliance:**
    * The system will comply with any relevant regulations and legal requirements. ACM codes of ethics are applied to keep confidentiallity of Daters and Cupids.
8. **Documentation:**
    * Comprehensive and clear documentation will be available for Daters, Cupids, and Managers via user manuals for each individual user type.


## Business Requirements:

1. **Mission Statement:**
    * Cupid Code envisions a future where the challenges of dating are met with technological innovation and compassionate human assistance, creating a supportive ecosystem for individuals seeking genuine connections.
2. **Revenue Model:**
    * Cupid Code will charge a monthly subscription of the Daters.
    * Cupid Code will monetize its services by charging a small percentage of the funds allocated by Daters for each date. This revenue will contribute to sustaining and growing the platform.
3. **User Acquisition and Retention:**
    * Implement features and incentives to encourage user loyalty and retention.
4. **Technology Infrastructure:**
    * Invest in a robust and scalable technology infrastructure to support the growing user base and ensure a seamless user experience.
5. **Quality of Service:**
    * Prioritize the delivery of high-quality service to Daters and Cupids, ensuring that the AI provides dating advice and Cupids offer assistance during dates.
    * Quality of service will be determined by allowing Cuipds and Daters to rate each other. Managers may take action on these reviews as necessary.
6. **Financial Management:**
    * Establish sound financial management practices to handle revenue collection, financial reporting, and fund disbursement to Cupids.
7. **Compliance and Legal Considerations:**
    * Adhere to relevant legal and regulatory requirements in the dating and gig economy industries.
    * Implement privacy policies and data protection measures to safeguard user information.
8. **Innovation and Adaptability:**
    * Foster a culture of innovation within the organization to stay ahead of industry trends and continuously improve the platform.
    * Be adaptable to changes in user preferences and technological advancements.
9. **Brand Image and Marketing:**
    * Develop and maintain a positive brand image through effective marketing strategies that highlight the unique features and benefits of Cupid Code.
    * Implement branding initiatives to create brand recognition and trust among Daters and Cupids.
10. **Partnerships and Collaborations:**
    * Explore partnerships with other businesses, venues, or dating-related services to enhance the overall user experience and expand service offerings.
11. **Customer Support and Conflict Resolution:**
    * Establish a responsive customer support system to address user concerns and conflicts promptly.
    * Implement mechanisms for conflict resolution between Daters, Cupids, and the organization.
12. **Social Responsibility:**
    * Consider and contribute to social responsibility initiatives that align with the values of Cupid Code, fostering a positive impact on the community.


## User Requirements: 


1. **User Registration & Profile Creation:**

    * All users can create an account on the Cupid Code app.
    * All Daters and Cupids can create an account on the Cupid Code app.
    * The registration process will be user-friendly and require basic information (email, password, full name, etc.).
    * Daters will be able to create a detailed profile with information about their interests, preferences, and past dating experiences.

2. **Cupid Service:**

    * The dater will hire a "Cupid" to purchase and deliver items during a date.
    * Cupids can be available on-demand, and Daters can specify the items they need.

3. **AI Chat for Dating Advice:**

    * The app will feature an AI-powered chat where Daters can seek dating advice.
    * The AI chat can provide relevant and helpful advice based on Dater queries.

4. **Manager Panel:**

    * Managers will have the ability to see a cupid's stats.
    * Managers will have the ability to take appropriate actions based on cupid stats.

5. **Privacy and Security:**

    * The app will prioritize user privacy, ensuring that personal information is secure.

6. **Feedback and Ratings:**

    * Daters will be able to provide feedback and ratings Cupids' services.
    * Cupids will be able to provide feedback and ratings Daters' services.
    * Cupids and Daters will be able to see feedback written about them.

7. **User Support:**

    * The app will have a user support system to assist users with any issues they encounter.
    * Support channels will include chat, email, or an online help center.

8. **User Preferences:**

    * Daters will be able to customize their preferences for AI advice and Cupid services.
    * These preferences will only be used once the corresponding systems are implemented.

8. **Calendar:** 

    * Daters can set up when dates are, using an in-app calendar.

9. **Emergency Advice during Dates:**

    * The app will have a feature to enable the AI to listen in on dates when activated by the Dater.
    * Emergency advice will be provided in real-time during dates to assist Daters in navigating challenging situations.

10. **Notifications:**

    * Daters will have the option to receive notifications before, during, and after scheduled dates.
    * Notifications may include reminders, suggestions, and post-date feedback.
    * A panel for managers to access and review complaints and feedback related to Cupids.
    * Dater advice for both the AI advice and 

11. **User Support:**

    * The app will have a user support system to assist users with any issues they encounter.
    * Support channels will include chat, email, or an online help center.




## Requirement Priority 


#### Must-haves (M):



* Browser (web page that looks well on the phone)/App for Cupid Code.
* Username/Password for user authentication.
* Daters can ask for tips using AI API (cheap/free).
* Profile for the Dater with details like type of nerd, relationship goals, and communication preferences.
* AI can be prompted to provide intervention or tips(listening in is a could-have)
* Budget allocation for Cupids to save dates (company and Cupids receive a cut).
* Save chat history feature in the chat box. If history cannot be saved, direct the user to a new chat.
* Profile for Cupids similar to DoorDash or Grubhub style (able to state availability).
* Cupids can be rated/fired by Daters.
* Cupids can be on duty/off duty based on availability.
* Portal for Cupids to sign up.
* Manager dashboard.
    * Purpose: for tracking revenue, subscription numbers, and other analytics. Functionality may be in future release (see “Could-haves”)


#### Should-haves (S):



* Simulate usage of the budget for class reveal with fake money (e.g., hacking in, etc.).
* Schedule date in the app or assume Cupid is busy (charge for peak time).
* Single Sign-On (SSO) options (Github, LinkedIn, Google, Facebook) as an alternative login method.
* Mic on device permission to hear conversations.
* $10/$15 a month subscription for Cupids.
* Free tier with a limited budget for initial interventions (e.g., $15 free intervention).
* AI uses Dater profile details with prompt.
* Notifications within the app for real-time updates and communication.
* Orders can be placed through the Cupid app.
* Manager analytics for profit, subscriptions, and money spent on interventions + cut Cupids receive.

#### Could-haves (C):



* Preferred for AI to hit Cupid panic button rather than the Dater.
* Dater can select when AI listens in on conversations.
* Automated interventions (e.g., handling situations like sold-out concerts).
* Listening to conversations by AI and responding for tips.


#### Won’t-haves (W):



* Log failed logins and ban repeat offenders
    * This would increase security against bots and brute forcing.
    * This is not a major concern at this time, as we are focusing on creating a minimum viable product first.
* Expenses tracking for individual Cupids 
    *  Cupids will receive a flat-rate return for completing gigs instead.
* Chat between Daters and Cupids
    * While this feature would be nice to have, it was deemed unowrthy of our time and effort at this time.
    * Cupids and Daters already have access to enough information to complete the requested tasks without direct communication.


## User Stories 


### **As a Dater, I want to…**


1. Easily register on the Cupid app so that I can start using the AI-assisted dating features.


2. Create a detailed profile with my interests and preferences so that the AI can provide me with more personalized dating advice.


3. Ask the AI for dating advice so that I can make informed decisions and improve my dating experience.


4. Receive timely notifications before and after my dates so that I can stay organized and receive valuable suggestions.


5. Have the option to activate the AI to listen in on my dates for emergency advice so that I can navigate challenging situations more effectively.


6. Set a budget for the AI to “buy and deliver” items during my date so that it doesn't crash and burn and the Cupid doesn't spend too much money.


7. Have the ability to provide feedback and ratings for the App services so that I can contribute to the improvement of the overall service quality.


8. Have privacy and security features in place so that protection of my personal information is ensured.


9. Be able to customize my preferences for AI advice and services so that I can tailor the experience to my specific needs and preferences.


10. Have access to a Dater support system so that I can get assistance with any issues or concerns I may have while using the Cupid app.


11. Prioritize my privacy and allow me to control the level of AI involvement in my dates so that I can feel comfortable using the service.


### **As a Cupid, I want to…**


1. Receive notifications for available jobs in my area so that I can offer my assistance and earn money.


2. Accept and complete jobs on the Cupid Code app in a straightforward and simple process so that I can efficiently provide quality service.


3. Receive feedback and ratings from Daters after completing a job so that I can improve my service and build a positive reputation.


4. Have access to a support system so that any issues or concerns that may arise may be addressed while fulfilling jobs for Daters.


5. Prioritize Daters’ privacy and protect sensitive information to ensure a secure and trustworthy service.


6. Access my job history and earnings on the Cupid Code app so that I can track my performance and income.


7. Be informed about any updates or changes in the Cupid Code app's policies or features so that I can stay informed and compliant.


8. Have the ability to set my availability and preferences for the types of jobs I am willing to take on so that I can manage my workload effectively.


9. Be recognized and rewarded for providing exceptional service through incentives or recognition programs on the Cupid Code app so that I can justify continuing to be a Cupid.


10. Be able to rate and give feedback on daters I delivered to so that the app is not being used maliciously by fake daters.


### **As a manager, I want to…**


1. Have quick access to a panel to review complaints and feedback related to Cupids so that I can address issues promptly and improve service quality.


2. Receive notifications for high-priority or urgent complaints so that I can prioritize and resolve critical issues efficiently.


3. View Daters feedback and ratings for both AI advice and Cupids' services so that I can identify areas for improvement.


4. Have the ability to take appropriate actions based on user feedback, such as providing additional training to Cupids or implementing system improvements, so that I can improve the service.


5. Ensure the Cupid Code app has a secure and confidential system for handling user complaints and feedback so that I can ensure privacy and compliance.


6. Track and analyze trends in user feedback so that I can identify patterns and make informed decisions for overall service enhancements.


7. Receive regular reports on Cupids' performance, including job completion rates, Dater satisfaction scores, and any notable achievements so that I can make sure to handle Cupids who may be causing issues.


8. Have access to tools that allow effective communication with Cupids and Daters so that I can facilitate conflict resolution or gather additional information.


9. Be notified about any changes or updates in the Cupid Code app's policies or features that may impact the management of Dater feedback and service quality so that I can handle the impact.


10. Support a seamless workflow for handling complaints so that I can ensure that the resolution process is efficient and user-friendly.


11. Have the flexibility to customize the feedback and complaint management system so that I can align features with the evolving needs of the Cupid Code app.




## Use Case Diagram

![UML diagram](images/UML_diagram.png "image_tooltip")
