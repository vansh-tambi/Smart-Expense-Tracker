# Smart Expense Tracker with AI Insights

Full-stack expense tracker using Flask REST API, React (functional components + hooks), and MongoDB.

## ✨ Tech Stack

- **Backend**: Python Flask + PyMongo
- **Frontend**: React + Vite + Tailwind CSS
- **Database**: MongoDB
- **Validation**: Pydantic + MongoDB JSON Schema

## 📁 Folder Structure

```text
Smart Expense Tracker/
  backend/
    app.py                    # Flask app entry point
    requirements.txt          # Python dependencies
    .env.example             # Environment template
    conftest.py              # pytest fixtures and config
    
    models/
      db.py                  # MongoDB connection & schema setup
    
    routes/
      expense_routes.py      # HTTP endpoints only
    
    schemas/
      expense_schema.py      # Pydantic validation
    
    services/
      expense_service.py     # Business logic: CRUD & aggregation
      ai_service.py          # Rule-based insight generation
    
    utils/
      error_handlers.py      # Centralized error handling
      logger.py              # Logging configuration
    
    tests/
      test_schema_validation.py  # Pydantic validation tests
      test_expense_service.py    # Service layer tests
      test_ai_service.py         # AI insight tests
      test_api_endpoints.py      # Integration tests

  frontend/
    index.html               # HTML template
    package.json             # npm dependencies + Tailwind config
    vite.config.js           # Vite + Tailwind plugin
    .env.example            # Environment template
    
    src/
      main.jsx               # React entry point
      App.jsx                # Root app component
      index.css              # Global styles + Tailwind import
      
      api/
        expensesApi.js       # API client functions
      
      hooks/
        useExpenses.js       # Custom hook for expense state
        useInsights.js       # Custom hook for insights
      
      components/
        AddExpenseForm.jsx   # Form to add expense
        ExpenseItem.jsx      # Individual expense display
        ExpenseList.jsx      # List of all expenses
        CategorySummary.jsx  # Category totals
        InsightsPanel.jsx    # AI insights display
      
      pages/
        DashboardPage.jsx    # Main dashboard page
```

## 🏗️ Architecture & Design Principles

### Backend

| Layer | Responsibility |
|-------|-----------------|
| routes/ | HTTP request/response only, calls services |
| services/ | All business logic, no HTTP knowledge |
| schemas/ | Pydantic validation, sanitization |
| models/ | MongoDB connection, collection initialization |
| utils/ | Logging, error handling, utilities |

**Key Pattern**: No business logic in route handlers. All SQL-like operations in services.

### Frontend

| Component Type | Responsibility |
|---|---|
| pages/ | Full page views |
| components/ | Reusable UI components (buttons, forms, lists) |
| hooks/ | State management and API calls |
| api/ | axios/fetch wrapper for HTTP requests |

## 🔒 Validation & Data Integrity

### Pydantic Schema Validation (Backend)
- `amount` must be > 0 (rejects 0 and negatives)
- `category` required, restricted to predefined values
- `date` must be YYYY-MM-DD format (defaults to today)
- `note` optional, defaults to empty string

### MongoDB Collection Validator
- Enforces amount >= 0.01
- Requires category and date
- Validates date format at DB level

### Supported Categories
Food, Transport, Shopping, Entertainment, Health, Utilities, Education, Other

## 📊 Core Features

| Feature | Endpoint | Validation |
|---------|----------|-----------|
| **Add Expense** | POST /api/expenses/ | Pydantic → MongoDB |
| **List Expenses** | GET /api/expenses/ | Sorted by date desc |
| **Category Summary** | GET /api/expenses/summary | Aggregated totals |
| **AI Insights** | GET /api/expenses/insights | Rule-based analysis |
| **Delete Expense** | DELETE /api/expenses/<id> | ObjectId validation |
| **Health Check** | GET /api/health | Server status |

## 🤖 AI Insight Engine

Rule-based insights (no LLM calls):
- ⚠️ **Category warnings**: Alerts if any category exceeds spending threshold
- 📈 **Weekly high spend**: Warning if past 7 days > $200
- 🍽️ **Top category this week**: Shows highest category
- ✅ **Positive reinforcement**: Congratulates balanced spending

Category thresholds:
- Food: 35% of total
- Shopping: 30%
- Entertainment: 25%
- Transport: 20%
- Others: 40% (default)

## 🧪 Testing

### Run All Tests
```powershell
cd backend
pytest -v --cov=services --cov=schemas
```

### Test Coverage
- **test_schema_validation.py**: 40+ tests for Pydantic validation
- **test_expense_service.py**: 20+ tests for CRUD logic
- **test_ai_service.py**: 15+ tests for insight generation
- **test_api_endpoints.py**: 20+ tests for HTTP endpoints

## 🚀 Setup Instructions

### Prerequisites
- Python 3.9+
- Node.js 16+
- MongoDB 4.0+
- npm or yarn

### Backend Setup

#### 1. Navigate to backend folder
```powershell
cd "e:\WebDev\Projects\Smart Expense Tracker\backend"
```

#### 2. Create Python virtual environment
```powershell
python -m venv venv
```

#### 3. Activate virtual environment
```powershell
# Windows PowerShell
.\venv\Scripts\Activate.ps1

# Or Command Prompt
.\venv\Scripts\activate.bat
```

#### 4. Install dependencies
```powershell
pip install -r requirements.txt
```

#### 5. Configure MongoDB connection
```powershell
# Copy .env template
Copy-Item .env.example .env

# Edit .env with your MongoDB URI
# For local MongoDB:
# MONGO_URI=mongodb://localhost:27017
# DB_NAME=smart_expense_tracker
```

#### 6. Ensure MongoDB is running
```powershell
# If using MongoDB Community on Windows, ensure mongod is running
# Or use MongoDB Atlas: mongodb+srv://username:password@cluster.mongodb.net/...
```

#### 7. Run backend (development)
```powershell
python app.py
# Server runs on http://localhost:5000
```

#### 8. Run tests
```powershell
pytest -v
# Or with coverage report
pytest -v --cov=services --cov=schemas --cov-report=html
```

### Frontend Setup

#### 1. Navigate to frontend folder
```powershell
cd "e:\WebDev\Projects\Smart Expense Tracker\frontend"
```

#### 2. Install dependencies
```powershell
npm install
```

#### 3. Configure API endpoint (optional)
```powershell
# Copy .env template
Copy-Item .env.example .env

# Edit .env if backend is on different port
# VITE_API_URL=http://localhost:5000
```

#### 4. Start development server
```powershell
npm run dev
# Server runs on http://localhost:5173
# Vite auto-proxies /api requests to http://localhost:5000
```

#### 5. Build for production
```powershell
npm run build
# Output in dist/ folder
```

## 📡 API Reference

### Add Expense
```bash
POST /api/expenses/

Request:
{
  "amount": 25.50,
  "category": "Food",
  "date": "2024-04-15",
  "note": "Lunch at office"
}

Response (201):
{
  "success": true,
  "data": {
    "id": "507f1f77bcf86cd799439011",
    "amount": 25.50,
    "category": "Food",
    "date": "2024-04-15",
    "note": "Lunch at office",
    "created_at": "2024-04-15T12:34:56.789Z"
  }
}
```

### List All Expenses
```bash
GET /api/expenses/

Response (200):
{
  "success": true,
  "data": [
    {...expense 1},
    {...expense 2}
  ],
  "count": 2
}
```

### Category Summary
```bash
GET /api/expenses/summary

Response (200):
{
  "success": true,
  "data": [
    {
      "category": "Food",
      "total": 100.50,
      "count": 5
    },
    {
      "category": "Transport",
      "total": 75.00,
      "count": 3
    }
  ]
}
```

### Get Insights
```bash
GET /api/expenses/insights

Response (200):
{
  "success": true,
  "insights": [
    "⚠️ You're spending 40% of your budget on Food ($500.00). Consider cutting back.",
    "📈 You've spent $350.00 in the last 7 days — that's above your weekly target of $200.",
    "🍽️ Your top spending category this week is Food ($250.00)."
  ]
}
```

### Delete Expense
```bash
DELETE /api/expenses/507f1f77bcf86cd799439011

Response (200):
{
  "success": true,
  "data": {...deleted expense}
}

Response (404):
{
  "error": "Expense not found"
}
```

### Health Check
```bash
GET /api/health

Response (200):
{
  "status": "ok"
}
```

## 🔌 Error Responses

All errors follow this format:
```json
{
  "error": "Error message",
  "details": [
    {
      "field": "amount",
      "message": "ensure this value is greater than 0"
    }
  ]
}
```

### HTTP Status Codes
- `200 OK`: Successful GET/DELETE
- `201 Created`: Successful POST
- `400 Bad Request`: Validation error
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

## 📝 Environment Variables

### Backend (.env)
```
FLASK_PORT=5000
MONGO_URI=mongodb://localhost:27017
DB_NAME=smart_expense_tracker
FLASK_ENV=development
```

### Frontend (.env)
```
VITE_API_URL=http://localhost:5000
```

## 🛠️ Troubleshooting

### MongoDB Connection Error
```
Error: connect ECONNREFUSED 127.0.0.1:27017
```
**Solution**: Start MongoDB or update MONGO_URI in .env

### Port Already in Use
```
Error: Address already in use :::5000
```
**Solution**: Change FLASK_PORT in .env or kill process on port 5000

### CORS Error in Frontend
```
Access to XMLHttpRequest at blocked by CORS policy
```
**Solution**: Ensure Flask-CORS is active and backend .env specifies correct URL

### Test Failures
```
ModuleNotFoundError: No module named mongomock
```
**Solution**: Install test dependencies: `pip install -r requirements.txt`

## 📚 Project Files Overview

### Key Backend Files

**app.py** - Flask application factory
- Creates app instance
- Registers blueprints
- Registers error handlers

**models/db.py** - MongoDB initialization
- Lazy-loads MongoDB connection
- Creates expenses collection with JSON Schema validator
- Creates indexes on date and category

**routes/expense_routes.py** - HTTP endpoints
- POST /api/expenses/ - calls expense_service.create_expense()
- GET /api/expenses/ - calls expense_service.get_all_expenses()
- GET /api/expenses/summary - calls expense_service.get_category_summary()
- GET /api/expenses/insights - calls ai_service.generate_insights()
- DELETE /api/expenses/<id> - calls expense_service.delete_expense()

**services/expense_service.py** - Business logic
- create_expense() - Validates, inserts, serializes
- get_all_expenses() - Retrieves all, sorted desc
- get_category_summary() - Aggregation pipeline
- delete_expense() - Removes document

**services/ai_service.py** - AI insights
- generate_insights() - Analyzes spending, generates text insights
- Checks category percentages against thresholds
- Detects high weekly spending
- Finds top category this week

**schemas/expense_schema.py** - Validation
- ExpenseCreateSchema - Validates input data
- ExpenseResponseSchema - Serializes output

### Key Frontend Files

**api/expensesApi.js** - HTTP client
- Wraps axios/fetch for backend calls
- Handles errors, transforms responses

**hooks/useExpenses.js** - State management
- useState for expenses list
- useEffect to fetch expenses
- Functions to add/delete/refresh

**hooks/useInsights.js** - Insights state
- useState for insights
- useEffect to fetch insights
- Refresh on expense changes

**components/AddExpenseForm.jsx** - Form
- Input fields: amount, category, date, note
- Validation before submit
- Calls useExpenses.addExpense()

**components/ExpenseList.jsx** - List view
- Maps expenses from useExpenses
- Renders ExpenseItem for each
- Delete button on each item

**components/CategorySummary.jsx** - Summary table
- Displays category totals
- Fetches from /api/expenses/summary
- Shows percentage breakdown

**components/InsightsPanel.jsx** - Insights display
- Uses useInsights hook
- Renders insight messages
- Refreshes on expense changes

**pages/DashboardPage.jsx** - Main page
- Combines all components
- Manages state flow
- Handles empty states

## 🚀 Quick Start

```powershell
# Terminal 1: Backend
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
# Edit .env
python app.py

# Terminal 2: Frontend
cd frontend
npm install
npm run dev
```

Then open http://localhost:5173 in your browser.

## 📄 License

MIT

## ✅ Checklist

- ✅ Backend validation with Pydantic
- ✅ MongoDB collection schema validation
- ✅ Service layer (no logic in routes)
- ✅ AI insight generation
- ✅ Comprehensive test suite (95+ tests)
- ✅ Logging and error handling
- ✅ React components + hooks
- ✅ Tailwind CSS styling
- ✅ API documentation
- ✅ Setup instructions

---

Built with ❤️ for expense tracking with AI insights
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
