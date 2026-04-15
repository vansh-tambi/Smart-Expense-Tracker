# Smart Expense Tracker Architecture

## High-Level Architecture
The Smart Expense Tracker is built using a modern, decoupled client-server architecture, cleanly separating the React frontend from the Python Flask backend. The backend strictly follows a layered architecture to guarantee a clear separation of concerns, ensuring high maintainability and ease of testing.

```text
+---------------------+        HTTP / JSON         +-------------------------+
|                     |  <--------------------->   |                         |
|   React Frontend    |                            |   Flask API API         |
|   (Client Layer)    |        Responses           |   (Server Layer)        |
|                     |                            |                         |
+---------------------+                            +-------------------------+
          |                                                    |
          |       +------------------------------------+       |
          v       |                                    |       v
+-----------------+----+                      +-------------------------+
|                      |                      |    AI Insights Engine   |
|   Browser Storage /  |                      |    (Hybrid: LLM + Rule) |
|   State Management   |                      +-------------------------+
+----------------------+                               |
                                                       v
                                              +-------------------------+
                                              |       MongoDB           |
                                              |    (NoSQL Database)     |
                                              +-------------------------+
```

## Data and Control Flow

### Backend Flow (Request Lifecycle)
1.  **Request Handling / Middleware**: Incoming HTTP requests hit Flask. Middleware injects a unique tracking `Request-ID` and logs the API usage.
2.  **Routes / Controllers (`routes/`)**: Handlers map to RESTful URL endpoints (`/api/expenses/`). They unmarshal the JSON strings to dictionaries.
3.  **Data Validation (`schemas/`)**: Strict Pydantic models validate constraints (e.g., amount > 0, dates not in the future, categorized correctly). Invalid data is caught instantly and a standardized error is returned.
4.  **Service Layer (`services/`)**: Business logic is executed. This layer encapsulates logic orchestrating the AI service or complex data structuring, completely isolated from DB syntax.
5.  **Repository Layer (`repositories/`)**: Abstracted data access executes operations securely against MongoDB (e.g., insertions, aggregations).
6.  **Response Handling**: Data is returned through standardized JSON envelopes mapping to UI expectations, bundled with the `Request-ID` and execution duration metrics.

### Frontend Flow
1.  **User Input (UI)**: The user submits a form (e.g., adding a new expense).
2.  **State Layer**: The React component handles form controls and signals the API utility hook.
3.  **API Transport**: Javascript `fetch` sends an asynchronous HTTP request matching the backend's strict Pydantic requirements.
4.  **State Update**: Upon successful 201 response, the local state (e.g., context or reducer) is updated transparently, skipping a redundant network page-reload.
5.  **Re-render**: Components reacting to the expenses state reflect the changes smoothly.

### Hybrid AI Integration Flow
1.  When `/api/expenses/insights` is hit, the application gathers aggregated category totals.
2.  **Primary Action (LLM Generation)**: The AI service tries to invoke an LLM (wrapped in a try block) via the API key.
3.  **Rate Limiting Check**: Simple programmatic debouncing prevents excessive LLM API costs.
4.  **Fallback Mechanism**: If the LLM call times out, hits a rate limit, or crashes, the system deterministically executes rule-based generation (analyzing percentages vs threshold heuristics) guaranteeing users are *always* presented with insights.

## Key Design Decisions

*   **Repository Layer**: Completely isolates MongoDB PyMongo queries. Why? It promotes separation of concerns; moving to PostgreSQL in the future wouldn’t affect our Service layer. It guarantees clean, isolated testability via dependency injection mocks.
*   **Pydantic for Data Validation (instead of Marshmallow / Mongo Validators)**: Provides strict, declarative schemas tightly mirroring data classes. It executes validations locally before hitting the database, preserving bandwidth and preventing schema corruption.
*   **Global Error Handling**: Standardizes error structures across the API so the frontend receives predictable layouts resulting in robust UX without silent crashes.
*   **Request-ID Tracing**: Guarantees simple and rapid debugging paths by making backend logs fully relatable to exact frontend responses.
