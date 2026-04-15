# Smart Expense Tracker

## 1. Project Overview
Smart Expense Tracker is a full-stack web application that helps users record daily expenses, view spending patterns, and receive AI-assisted financial insights. It is designed as a clean, practical system that balances development speed with strong validation and maintainable architecture.

## 2. Features
- Add, view, and delete expenses
- Category-based expense summary with totals
- AI insights endpoint for spending guidance
- Strong input validation at application and database layers
- Structured error handling and logging
- Test suite for schemas, services, AI logic, and API endpoints

## 3. Tech Stack
- Backend: Python, Flask, Flask-CORS, PyMongo, Pydantic
- Frontend: React, Vite, Axios, Tailwind CSS
- Database: MongoDB
- Testing: Pytest, Pytest-Cov, Mongomock

## 4. Architecture Explanation
The system follows a layered architecture for clarity and maintainability.

### Backend layers
- routes: HTTP interface only (request/response)
- services: Business logic and domain operations
- schemas: Input validation and normalization
- models: Database connection and collection setup
- utils: Logging and centralized error handling

### Frontend layers
- pages: Screen-level layout and composition
- components: Reusable UI building blocks
- hooks: State and data-fetch behavior
- api: Axios-based backend communication layer

This separation reduces coupling, keeps logic testable, and supports safe feature growth.

## 5. Folder Structure
```text
Smart Expense Tracker/
  backend/
    app.py
    requirements.txt
    conftest.py
    models/
    routes/
    schemas/
    services/
    utils/
    tests/
  frontend/
    package.json
    vite.config.js
    src/
      api/
      components/
      hooks/
      pages/
  docs/
    ai-guidelines.md
    walkthrough-script.md
```

## 6. Key Technical Decisions
- Service-layer backend to keep route handlers thin and logic reusable
- Pydantic plus MongoDB validator for defense-in-depth validation
- Axios API client for centralized request and error behavior
- React hooks for lightweight, readable state management
- Rule-based AI insights for deterministic and auditable output

## 7. AI Usage (How and Why)
AI is used as an assistant, not an autonomous decision-maker.

How:
- Generate and refine development artifacts (code drafts, documentation, test ideas)
- Produce spending insight suggestions from expense patterns

Why:
- Improve development speed and consistency
- Provide users with understandable recommendations

Governance:
- AI outputs are reviewed before use
- No direct execution without validation
- Input to AI tools is sanitized
- AI does not control core business logic
- Core architecture decisions remain human-owned

Detailed policy: see docs/ai-guidelines.md.

## 8. Tradeoffs and Limitations
- Rule-based insights are explainable but less adaptive than ML-driven models
- Current scope focuses on single-project workflow; user auth and multi-tenant separation are future work
- MongoDB flexibility is high, but relational constraints are less strict than SQL-first systems
- Frontend state approach is intentionally simple and may need expansion as feature count grows

## 9. Setup Instructions
### Prerequisites
- Python 3.9+
- Node.js 16+
- MongoDB (local or Atlas)

### Backend setup
1. Open terminal in backend folder.
2. Create and activate a virtual environment.
3. Install dependencies.
4. Configure environment variables.
5. Run the Flask server.

```powershell
cd "e:\WebDev\Projects\Smart Expense Tracker\backend"
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
python app.py
```

### Frontend setup
1. Open terminal in frontend folder.
2. Install dependencies.
3. Configure frontend environment variables if needed.
4. Start Vite development server.

```powershell
cd "e:\WebDev\Projects\Smart Expense Tracker\frontend"
npm install
Copy-Item .env.example .env
npm run dev
```

### Run tests
```powershell
cd "e:\WebDev\Projects\Smart Expense Tracker\backend"
pytest -v --cov=services --cov=schemas
```

## 10. Future Improvements
- Add authentication and user-level data isolation
- Add budget planning, monthly goals, and alerts
- Improve insights with trend forecasting and confidence indicators
- Add CI/CD quality gates and deployment profiles
- Expand observability with metrics, traces, and operational dashboards
