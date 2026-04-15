# 💰 Smart Expense Tracker with AI Insights

A full-stack expense tracker built with **Python Flask**, **React**, and **MongoDB** — featuring rule-based AI spending insights, schema validation, and a premium dark glassmorphism UI.

---

## 📁 Project Structure

```
Smart Expense Tracker/
├── backend/
│   ├── app.py                    # Flask app factory
│   ├── .env                      # Environment variables
│   ├── requirements.txt
│   ├── models/
│   │   └── db.py                 # MongoDB connection
│   ├── schemas/
│   │   └── expense_schema.py     # Pydantic validation
│   ├── services/
│   │   ├── expense_service.py    # Business logic
│   │   └── ai_service.py        # AI insight generator
│   ├── routes/
│   │   └── expense_routes.py    # Blueprint (thin controllers)
│   └── utils/
│       ├── logger.py
│       └── error_handlers.py
│
└── frontend/
    └── src/
        ├── api/
        │   └── expensesApi.js
        ├── hooks/
        │   ├── useExpenses.js
        │   └── useInsights.js
        ├── components/
        │   ├── AddExpenseForm.jsx
        │   ├── ExpenseList.jsx
        │   ├── ExpenseItem.jsx
        │   ├── CategorySummary.jsx
        │   └── InsightsPanel.jsx
        ├── pages/
        │   └── DashboardPage.jsx
        ├── App.jsx
        ├── main.jsx
        └── index.css
```

---

## 🚀 Setup & Running

### Prerequisites

- Python 3.9+  
- Node.js 18+  
- MongoDB running locally on port 27017

---

### Backend

```bash
cd backend

# Create & activate virtual environment
python -m venv venv
.\venv\Scripts\activate        # Windows
# source venv/bin/activate     # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Configure environment (edit if needed)
# MONGO_URI=mongodb://localhost:27017
# DB_NAME=smart_expense_tracker

# Start the server
python app.py
```

The API will be available at **http://localhost:5000**

---

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The UI will be available at **http://localhost:5173**

---

## 📡 API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/expenses/` | Add a new expense |
| `GET` | `/api/expenses/` | List all expenses |
| `DELETE` | `/api/expenses/:id` | Delete an expense |
| `GET` | `/api/expenses/summary` | Category-wise totals |
| `GET` | `/api/expenses/insights` | AI spending insights |

### Example: Add Expense

```bash
curl -X POST http://localhost:5000/api/expenses/ \
  -H "Content-Type: application/json" \
  -d '{"amount": 25.50, "category": "Food", "note": "Lunch"}'
```

### Valid Categories

`Food` · `Transport` · `Shopping` · `Entertainment` · `Health` · `Utilities` · `Education` · `Other`

---

## 🤖 AI Insights

Insights are rule-based and generated in `services/ai_service.py`. They include:

- ⚠️ Category over-spend alerts (e.g. >35% of budget on Food)
- 📈 Weekly high-spend warnings (>$200 in 7 days)
- 🍽️ Top spending category of the week
- ✅ Positive reinforcement when spending is balanced

> **To integrate a real LLM** (e.g. Gemini/GPT), replace the logic inside `generate_insights()` in `ai_service.py` with an API call — the function signature and return type (`List[str]`) stay the same.

---

## 🛡️ Validation Rules

- `amount` — must be **> 0** (enforced by Pydantic)
- `category` — **required**, must be one of the valid categories
- `date` — optional, defaults to today's date (ISO format)

---

## 🔧 Environment Variables (`backend/.env`)

| Variable | Default | Description |
|----------|---------|-------------|
| `MONGO_URI` | `mongodb://localhost:27017` | MongoDB connection string |
| `DB_NAME` | `smart_expense_tracker` | Database name |
| `FLASK_PORT` | `5000` | Backend port |
| `FLASK_ENV` | `development` | Flask environment |
