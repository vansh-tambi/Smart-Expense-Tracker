# Smart Expense Tracker with AI Insights

Full-stack expense tracker using Flask REST API, React (functional components + hooks), and MongoDB.

## Folder Structure

```text
Smart Expense Tracker/
  backend/
    app.py
    requirements.txt
    .env.example
    models/
      __init__.py
      db.py
    routes/
      __init__.py
      expense_routes.py
    schemas/
      __init__.py
      expense_schema.py
    services/
      __init__.py
      expense_service.py
      ai_service.py
    utils/
      __init__.py
      error_handlers.py
      logger.py

  frontend/
    index.html
    package.json
    vite.config.js
    .env.example
    src/
      main.jsx
      App.jsx
      index.css
      api/
        expensesApi.js
      hooks/
        useExpenses.js
        useInsights.js
      components/
        AddExpenseForm.jsx
        ExpenseItem.jsx
        ExpenseList.jsx
        CategorySummary.jsx
        InsightsPanel.jsx
      pages/
        DashboardPage.jsx
```

## Backend Design

- routes: HTTP layer only (request/response)
- services: business logic and AI insight logic
- models: MongoDB connection and collection setup
- schemas: request validation with Pydantic
- utils: error handlers and logging

No business logic is placed in route handlers.

## Core Features

- Add expense (amount, category, date, note)
- Get all expenses
- Category-wise summary
- AI-based spending insights

## Validation and Database Rules

- Pydantic validation enforces:
  - amount > 0
  - category required and restricted to supported values
  - date format YYYY-MM-DD
- MongoDB collection validator on expenses enforces:
  - amount minimum 0.01
  - category required
  - date required

## API Endpoints

- POST /api/expenses/
- GET /api/expenses/
- GET /api/expenses/summary
- GET /api/expenses/insights
- DELETE /api/expenses/<expense_id>
- GET /api/health

## Setup Instructions

### 1. Start MongoDB

Ensure MongoDB is running locally at mongodb://localhost:27017 (or use your own URI).

### 2. Backend Setup (Flask)

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
python app.py
```

Backend runs on http://localhost:5000.

### 3. Frontend Setup (React)

```powershell
cd frontend
npm install
Copy-Item .env.example .env
npm run dev
```

Frontend runs on http://localhost:5173.

Vite is configured to proxy /api to the Flask backend.

## Example Request

```bash
curl -X POST http://localhost:5000/api/expenses/ \
  -H "Content-Type: application/json" \
  -d '{"amount":45.5,"category":"Food","date":"2026-04-15","note":"Lunch"}'
```

## AI Insight Behavior

The AI service currently uses a rule-based engine to generate insights, including alerts such as:

- You are spending too much on food this week.
- Weekly spending is above threshold.
- Top category for the week.

To switch to LLM-based insights later, replace logic in backend/services/ai_service.py while keeping the same service interface.
