# Technical Trade-offs & Limitations

In the development of the **Smart Expense Tracker**, several architectural tradeoffs were made prioritizing rapid development, simplicity, and ease of deployment without over-engineering initial capabilities.

## Architecture Decisions

### Why Flask over FastAPI?
While FastAPI is definitively faster and features built-in asynchronous support and Pydantic integrations, **Flask** was selected due to its maturity, widespread support, and simplicity regarding setup. For an MVP expense tracker, the primary bottleneck isn't framework speed but rather database and AI I/O wait times. Flask provides a straightforward synchronous flow that minimizes setup friction while easily matching expected scale throughputs.

### Why MongoDB over a Relational DB (PostgreSQL)?
A document-based database like MongoDB was chosen over SQL for its flexibility entirely. Managing user profiles, custom expense categorization lists, or embedding multiple tags is natively cleaner in BSON structures compared to handling multiple junction tables in a relational model. However, we offset the primary risk of NoSQL (data inconsistencies) by enforcing extremely strict **Pydantic Validation** before writes, effectively simulating a relational schema but without the migration complexities.

## Risks & Limitations

### 1. Data Inconsistency and Relational Integrity
- **Limitation**: While MongoDB allows high flexibility, the lack of strict foreign key constraints means cross-collection relationships (e.g., Users -> Expenses -> Custom Categories) need application-side checks.
- **Improvement**: Integrating an ODM like MongoEngine or enforcing database-level JSON schema validators strictly could provide guarantees at the lowest storage layer if the schema solidifies extensively.

### 2. AI Hallucination & Consistency
- **Limitation**: LLMs are non-deterministic. The AI could return incorrectly formatted responses (failing to return the expected `{"insights": []}` schema) or generate completely irrelevant financial advice out of context.
- **Mitigation**: A hybrid fallback mechanism isolates these risks. If the AI hallucinates bad shapes or timeouts, the engine intercepts and routes to deterministic, rule-based algorithmic thresholds ensuring a mathematically accurate safety net.
- **Improvement**: Integrating structured LLM parsing tools like Instructor or LangChain to forcibly prompt specific output schemas explicitly.

### 3. Scaling Issues (Synchronous Bottleneck)
- **Limitation**: The Flask API is strictly synchronous execution. Heavy operations (such as waiting multiple seconds for the external LLM to respond) effectively block the worker thread, vastly restricting RPS (Requests Per Second) under heavy concurrent user loads.
- **Improvement**: Migrating complex workloads (like generating AI summaries) into asynchronous task queues (e.g., Celery + Redis). Alternatively, adopting an asynchronous deployment strategy using FastAPI/ASGI would handle I/O bound wait times drastically better under pressure.

### 4. Basic Rate Limiting
- **Limitation**: The AI rate-limiting logic is currently performed using an in-memory floating point timestamp. This works perfectly locally but falls apart in multi-worker environments (e.g., Gunicorn) where each worker process holds its own isolated memory state.
- **Improvement**: Adopt Redis for centralized rate limiting and data caching to guarantee atomicity of counts across all deployed pods.
