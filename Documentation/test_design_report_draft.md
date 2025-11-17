# Cupid Code Test Design Report - First Draft
**Team 6 | Fall 2025**

---

## Executive Summary

This document outlines our testing strategy for the Cupid Code application. We've implemented **unit tests** for backend API endpoints, **integration tests** for component interactions, and **end-to-end Playwright tests** for critical user workflows.

**Testing Infrastructure**:
- Backend Unit Tests: ~50 test classes
- Backend Integration Tests: ~40 test classes (partially complete)
- Playwright E2E Tests: 3 test suites covering Login, Cupid, and Dater workflows
- **Estimated Code Coverage**: 60-70%

---

## 1. Testing Approach & Philosophy

Our testing strategy focuses on ensuring that every user interaction behaves as expected. We prioritize testing critical user paths (authentication, gig lifecycle, payments) over exhaustive edge case coverage due to time constraints.

We're following a traditional testing pyramid:
- **Unit tests** for individual API endpoints and helper functions
- **Integration tests** for database interactions and cross-component functionality
- **E2E tests** with Playwright for complete user workflows

---

## 2. What We're Testing

### Backend Unit & Integration Tests

**Framework**: Django's `APITestCase` with `unittest.mock`

We wrote unit tests for all API views (~1,938 lines) and helper functions (~862 lines), organized by user role:
- **User tests**: Authentication, registration, profile management
- **Dater tests**: AI chat, calendar, gig requests, payment cards
- **Cupid tests**: Gig acceptance/completion, payouts, feedback
- **Manager tests**: Analytics, user statistics, account moderation
- **General tests**: Geolocation, Yelp API, notifications

**Testing Pattern**: Each endpoint has at least one success case and one failure case. This gave us broad coverage quickly, though we haven't tested all edge cases.

### Challenges We Anticipated

**Most Challenging to Test**:

1. **AI Chat Integration**: The OpenAI API integration is tricky because it:
   - Requires API key authentication (costs money per call)
   - Returns non-deterministic responses
   - Involves fetching message history, building context, calling API, and storing results
   - **Our approach**: Mock `get_ai_response()` to avoid real API calls and return predictable test responses

2. **Gig Lifecycle State Management**: Testing inactive → active → completed transitions requires:
   - Careful database state setup
   - Ensuring only valid state transitions occur (can't complete an inactive gig)
   - Verifying payment transfers trigger correctly
   - **Our approach**: Mock database queries and use fixtures with known gig states

3. **Geolocation Services**: IP-based location lookup involves:
   - GeoIP2 database that may be missing or outdated
   - Localhost addresses needing special handling
   - External Nominatim API for address geocoding
   - **Our approach**: Mock location lookups with fixed coordinates

4. **Payment Processing**: PayPal integration can't be fully tested without sandbox:
   - External API calls to PayPal
   - Asynchronous webhook callbacks
   - Real money transactions
   - **Our approach**: Mock PayPal SDK, test balance updates independently

5. **Manager Analytics**: Statistics calculations involve complex aggregations:
   - Drop rates, completion rates require counting across multiple tables
   - Active session tracking needs Django session management
   - Edge cases like division by zero when no gigs exist
   - **Our approach**: Mock querysets with known counts for predictable calculations

---

## 3. Playwright End-to-End Tests

### What We're Testing

**Framework**: Playwright with Python (supports Chromium, Firefox, WebKit)

We have 3 E2E test suites that validate complete user workflows:
- **`test_login.py`**: Authentication for all three user roles (Dater, Cupid, Manager)
- **`test_cupid.py`**: Gig claiming, completion, dropping, and payment verification
- **`test_dater.py`**: Full navigation testing across all Dater pages

**Infrastructure**: Tests use a fresh database backup that's restored after each run to ensure repeatable results.

### Key Test Scenarios

**Login Tests** - Verify authentication and role-based routing:
- Login as Dater → redirects to `/dater/home`, profile shows correct data
- Login as Cupid → redirects to `/cupid/home`, balance displays correctly
- Login as Manager → redirects to `/manager/home`
- Logout works for all roles

**Cupid Workflow Tests** - Complete gig lifecycle:
- Claim gigs: Click "Accept" on inactive gigs → move to active state
- Drop gigs: Click "Drop" on active gig → returns to inactive
- Complete gigs: Click "Complete" → gig disappears, balance increases
- View feedback: Navigate to feedback page → see star ratings and comments

**Dater Navigation Tests** - Ensure all pages load correctly:
- Navigate between all 8 Dater pages (Home, AI Chat, AI Listen, Balance, Calendar, Feedback, Gigs, Profile)
- Verify page titles display correctly
- Test 112 navigation paths total (every page to every other page and back)

---

## 4. Code Coverage

### Estimated Coverage

**Backend**: **60-70%**
- 50 unit test classes covering all API views (~1,938 lines)
- 40 integration test classes (partially complete)
- Each endpoint has at least 1 success and 1 failure test
- Some helper functions lack full coverage (Twilio SMS, SendGrid email mocked but not integration tested)

**Frontend**: **40-50%**
- 38 Vue components total
- 3 Playwright test suites covering:
  - ✅ Authentication & logout
  - ✅ Profile viewing
  - ✅ Gig lifecycle (claim, complete, drop)
  - ✅ Payment updates
  - ✅ Navigation (all Dater pages, all Cupid pages)
- ❌ No Vue component unit tests
- ❌ Many component interactions not tested

**What's Not Covered**:
- Audio transcription (AI Listen feature)
- PayPal webhook handling (only mocked)
- Yelp API edge cases (no results, timeouts)
- Manager analytics edge cases (division by zero)
- Mobile-specific touch interactions



---

## 5. Problems Uncovered by Testing

### Bugs Found and Fixed

**Unit Testing Discoveries**:
1. **Gig State Transitions**: Gigs could be completed without being claimed first → Added state validation
2. **Balance Calculation**: Cupid balance not updating correctly → Fixed with atomic database transactions
3. **Location Parsing**: Commas in location strings broke proximity calculations → Strip commas in helper function
4. **Feedback Validation**: Negative star ratings were accepted → Added 1-5 range validation

**Playwright Testing Discoveries**:
1. **Navigation Loops**: Clicking "Home" while on home page caused errors → Added route guards
2. **CSRF Token Issues**: Forms failing on second submission → Refresh token on component mount
3. **Double-Click Bugs**: Buttons clickable multiple times during API calls → Disable buttons during loading
4. **Profile Test Offset**: Input assertions failing because CSRF token is first input element → Adjusted test to skip index 0

### What We're Still Worried About

**Backend Concerns**:
- **AI Chat**: No user-friendly error message when OpenAI API fails (just 500 error)
- **Manager Analytics**: Edge cases with zero gigs might cause division errors
- **Yelp API**: Daily rate limits could break date suggestions in production
- **Payment Webhooks**: If PayPal webhook fails, Cupid doesn't get paid (no reconciliation system)

**Frontend Concerns**:
- **State Management**: Component state might leak between pages during navigation
- **Loading States**: Some async operations don't show loading indicators
- **Mobile**: Touch gestures and small screen layouts not thoroughly tested
- **Error Handling**: Many API failures just show console errors, not user-friendly messages

---

## 6. System-Level Tests for Final Presentation

### End-to-End Demo: Complete Gig Lifecycle

**Scenario**: Demonstrate a Dater requesting help, Cupid completing the task, feedback exchange, and payment

**Steps to Reproduce**:

**1. Dater Creates Gig** (Manual - AI features are hard to automate)
- Login at `http://localhost:8000` as Dater: `bob@cupidcode.com`
- Navigate to "AI Listen"
- Click "Start Recording" → Speak: *"I need flowers and chocolates for my date tonight"* → Click "Stop"
- **Expected**: Gig appears in "Gigs" page showing "Items: Flowers, Chocolates"
- **Screenshot**: Gig card with items listed

**2. Cupid Claims Gig**
- Logout and login as Cupid: `really@me.com`
- Navigate to "Gigs Available"
- Click "Accept Gig" on the flowers/chocolates gig
- **Expected**: Gig moves to "Active Gigs" section
- **Screenshot**: Active gig showing "Complete" and "Drop" buttons

**3. Cupid Completes Gig**
- Go to "Active Gigs" → Click "Complete Gig"
- Navigate to Profile
- **Expected**: Balance increased (e.g., $12 → $15), success count incremented
- **Screenshot**: Profile showing updated balance

**4. Dater Leaves Feedback**
- Logout and login as Dater
- Navigate to "Feedback" → Select the completed gig
- Rate 5 stars, comment: *"Great job!"* → Submit
- **Expected**: Confirmation message displayed
- **Screenshot**: Feedback submitted confirmation

**5. Cupid Views Feedback**
- Logout and login as Cupid
- Navigate to "Feedback"
- **Expected**: See new feedback entry with 5 stars and "Great job!" comment
- **Screenshot**: Feedback display

**6. Manager Views Analytics**
- Logout and login as Manager: `manager@cupidcode.com`
- View dashboard
- **Expected**: Gig completion stats updated, active sessions displayed
- **Screenshot**: Manager dashboard metrics

**Time**: ~5-7 minutes | **Success**: All transitions work, payments update, no console errors

### Authentication & Role-Based Access

**Test Unauthorized Access**:
1. Navigate to `http://localhost:8000/dater/home` without logging in → **Expected**: Redirect to login
2. Login as Dater, try to access `/cupid/gigs` → **Expected**: 403 Forbidden or redirect
3. Login as Cupid, try to access `/manager/analytics` → **Expected**: 403 Forbidden

**Screenshot**: Error pages showing access denied

### AI Chat Testing

**Test Conversational Flow**:
1. Login as Dater → Navigate to "AI Chat"
2. Send message: *"I'm nervous about my first date"*
3. **Expected**: AI responds within 3-5 seconds with dating advice
4. Send follow-up: *"What should I wear?"*
5. **Expected**: AI references previous context about nervousness

**Screenshot**: Chat conversation showing context-aware responses

### Cross-Browser Testing (Automated with Playwright)

Run tests across browsers:
```bash
pytest --browser chromium  # Default
pytest --browser firefox
pytest --browser webkit    # Safari engine
pytest --device="iPhone 13"  # Mobile test
```

**Expected**: All tests pass in all browsers, no layout issues
**Screenshot**: Test results showing passes in Chromium, Firefox, WebKit

---

## 8. Running Tests - Step-by-Step Instructions

### 8.1 Backend Unit/Integration Tests

**Prerequisites**:
- Python 3.8+
- Django installed
- All dependencies from `requirements.txt`

**Setup**:
```bash
cd Code/
poetry install  # Install dependencies
cd server/
```

**Run All API Tests**:
```bash
python manage.py test api.tests
```

**Run Specific Test Module**:
```bash
# Unit tests only
python manage.py test api.tests.unit_tests.cupid_tests

# Integration tests only
python manage.py test api.tests.integration_tests.user_tests
```

**Run Single Test Class**:
```bash
python manage.py test api.tests.unit_tests.dater_tests.TestSendChatMessage
```

**Expected Output**:
```
..................................................
----------------------------------------------------------------------
Ran 50 tests in 2.341s

OK
```

**Screenshot**: Terminal showing test results with all tests passing

### 8.2 Playwright End-to-End Tests

**Prerequisites**:
- Python 3.8+
- Playwright installed (`pip install playwright`)
- Playwright browsers installed (`playwright install`)
- Django dev server running on `http://localhost:8000`
- Fresh database backup at `Code/server/db_backup.sqlite3`

**Setup**:
```bash
# Install Playwright and browsers
pip install playwright pytest-playwright
playwright install

# Terminal 1: Start Django server
cd Code/server/
python manage.py runserver

# Terminal 2: Run tests
cd Code/playwright/
```

**Create Database Backup**:
```bash
cd Code/server/
python manage.py migrate  # Create fresh database
cp db.sqlite3 db_backup.sqlite3  # Backup for tests
```

**Run All Playwright Tests**:
```bash
pytest
```

**Run Individual Test Suite**:
```bash
pytest test_login.py    # Authentication tests
pytest test_cupid.py    # Cupid workflow tests
pytest test_dater.py    # Dater navigation tests
```

**Run with Specific Browser**:
```bash
pytest --browser chromium  # Default
pytest --browser firefox
pytest --browser webkit    # Safari engine
```

**Run in Headed Mode** (see browser GUI):
```bash
pytest --headed
```

**Run with Device Emulation**:
```bash
pytest --device="iPhone 13"
pytest --device="Galaxy S9+"
```

**Generate Test Report with Screenshots/Videos**:
```bash
pytest --screenshot=on --video=on
```

**Expected Output**:
```
======================== test session starts =========================
platform linux -- Python 3.11.0, pytest-7.4.0, pluggy-1.3.0
rootdir: /home/carteroj/school_projects/CS-3450/cupid_code_team_6_2025/Code/playwright
plugins: playwright-0.4.3
collected 8 items

test_login.py::test_dater_login PASSED                          [ 12%]
test_login.py::test_cupid_login PASSED                          [ 25%]
test_login.py::test_manager_login PASSED                        [ 37%]
test_cupid.py::test_gigs PASSED                                 [ 50%]
test_cupid.py::test_gigs_completion PASSED                      [ 62%]
test_cupid.py::test_feedback PASSED                             [ 75%]
test_cupid.py::test_navigation PASSED                           [ 87%]
test_dater.py::test_navigation PASSED                           [100%]

======================== 8 passed in 45.23s ==========================
```

**Screenshots**: 
- Browser window showing test execution
- Terminal output with test results

**Common Issues**:

1. **"Element not found" errors**
   - Cause: Django server not running or wrong URL
   - Fix: Ensure `python manage.py runserver` is active on port 8000

2. **"Unexpected data" errors**
---

## 7. How to Run Our Tests

### Backend Tests

```bash
cd Code/server/
python manage.py test api.tests  # Run all unit and integration tests
```

---

## 8. Conclusion

We've built a solid testing foundation covering critical user workflows and backend endpoints. Our **60-70% code coverage** gives us confidence in core features like authentication, gig lifecycle, and payments. 

**What's working well**:
- Backend unit tests catch API bugs early
- Playwright tests validate complete user flows
- Automated tests prevent regressions

**What needs improvement**:
- Vue component unit tests (not implemented)
- Edge case coverage (only 1 success + 1 failure per endpoint)
- Error message UX (many errors just show console logs)
- Integration tests incomplete

**For the final presentation**, we'll demonstrate the complete gig lifecycle (Dater creates gig → Cupid completes → feedback exchange) and show cross-browser compatibility. We're prepared to discuss known limitations around AI error handling, payment webhooks, and mobile testing.

---

**Document Status**: First Draft
**Last Updated**: November 17, 2025
**Team 6**: Daniel, Nate S., Nate M., Brighton, Emma, Carter