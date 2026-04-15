# Project Walkthrough Script: Smart Expense Tracker

**Goal:** Deliver a sharp, structured, confident presentation of the Smart Expense Tracker within 10 minutes.

---

### 1. Hook (Problem + Why it Matters) [1 min]
*   "Welcome, everyone. We all know how easy it is to lose track of spending. Basic trackers exist, but they just show you graphs—they don’t tell you *what* those graphs mean.
*   "Today, I'm presenting the **Smart Expense Tracker**, an intelligent platform that not only logs your expenses safely but actually acts as a financial analyst, diagnosing your spending habits."

### 2. Live Demo (Fast, No Fumbling) [2 mins]
*   *(Action: Share screen, show dashboard)*
*   "Here’s the main dashboard. Notice how responsive it is. I'll add an expense right now—let's say $150 on "Dining". Watch how the UI instantly updates without any page reloads."
*   "But the magic is here in the 'Insights' tab. When I request insights, the AI analyzes my past week: it categorizes spending percentages, points out that I'm over budget on food, and provides actionable advice."

### 3. Architecture Explanation [1.5 mins]
*   "Under the hood, we are running a decoupled architecture. React handles the state cleanly on the client side. The backend is a Python Flask API connecting to a MongoDB cluster."
*   "I chose a decoupled approach specifically because it allows our frontend and backend teams to iterate on features completely independently, scaling components as they grow."

### 4. Code Structure & Separation of Concerns [2 mins]
*   *(Action: Briefly flash the backend structure on IDE)*
*   "I’d like to highlight the backend structure. Notice how we have completely isolated layers:"
    *   **Routes**: Strictly handle HTTP routing.
    *   **Schemas**: Pydantic locks down our payload validation.
    *   **Services**: Hold pure business logic.
    *   **Repositories**: Encapsulate all database interaction.
*   "By introducing this Repository pattern, our Services never write actual MongoDB syntax. If we ever migrate to PostgreSQL, our business logic won't change one bit."

### 5. AI Usage & Constraints [1.5 mins]
*   "The most complex part was integrating the AI Insights engine reliably. LLMs are notoriously unpredictable and can timeout."
*   "To solve this, I designed a **Hybrid AI Strategy**. The application attempts to invoke the LLM for natural insights first. However, if it hits a rate limit or hallucinates, a sophisticated rule-based engine kicks in immediately. This enforces a fallback layer guaranteeing that the user is *never* left waiting on a broken API call."

### 6. Architectural Tradeoffs [1 min]
*   "No architecture is perfect. To get this MVP running efficiently, I made some explicit tradeoffs:"
    1.  "**Flask over FastAPI:** I prioritized a mature, simple synchronous flow to iterate rapidly over sheer asynchronous speed."
    2.  "**NoSQL over SQL:** I wanted flexibility in categorization, but to offset the lack of SQL schemas, we heavily enforced Pydantic strict validations at the door."
    3.  "**In-Memory Rate Limiting:** Our LLM rate limits run in process memory, which is perfect for an MVP but would need Redis for distributed multi-worker deployments."

### 7. Future Improvements [1 min]
*   "Looking ahead, my next steps for scaling would involve:"
    *   "Extracting the LLM generation into asynchronous Celery tasks to prevent UI blocking."
    *   "Migrating to Redis for robust caching of summaries."
    *   "Expanding our test suites into E2E Cypress testing."
*   "Thank you. Let's take a look at the repo or field any questions you might have."
