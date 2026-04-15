# 🚀 Smart Expense Tracker - Complete Setup Guide

## 📋 Quick Checklist

- [ ] Prerequisites installed (Python 3.9+, Node.js 16+, MongoDB)
- [ ] Backend dependencies installed
- [ ] Frontend dependencies installed
- [ ] MongoDB running
- [ ] Environment files created (.env files)
- [ ] Backend tests passing
- [ ] Frontend dev server running
- [ ] API endpoints working
- [ ] Ready for deployment

---

## 🛠️ Prerequisites

### Windows PowerShell 7+ (Recommended)
```powershell
# Check PowerShell version
$PSVersionTable.PSVersion

# Update if needed (run as Administrator)
winget install Microsoft.PowerShell
```

### Python 3.9+
```powershell
# Check version
python --version

# Download from: https://www.python.org/downloads/
```

### Node.js 16+
```powershell
# Check version
node --version
npm --version

# Download from: https://nodejs.org/
```

### MongoDB 4.0+
```powershell
# Option 1: Local MongoDB Community Edition
# Download: https://www.mongodb.com/try/download/community

# Option 2: MongoDB Atlas (Cloud)
# Sign up: https://www.mongodb.com/cloud/atlas

# After installation, verify it's running:
mongosh --version  # MongoDB Shell
```

---

## 📖 Step-by-Step Setup

### Phase 1: Backend Setup (30 minutes)

#### 1.1 Open Backend Terminal
```powershell
cd "e:\WebDev\Projects\Smart Expense Tracker\backend"
```

#### 1.2 Create Python Virtual Environment
```powershell
python -m venv venv
```

#### 1.3 Activate Virtual Environment
```powershell
# Windows PowerShell
. .\venv\Scripts\Activate.ps1

# Windows CMD (if PowerShell fails)
.\venv\Scripts\activate.bat
```

**Expected output**: `(venv)` prefix in terminal

#### 1.4 Install Dependencies
```powershell
pip install -r requirements.txt
```

**Expected packages**:
- flask, flask-cors
- pymongo, pydantic
- pytest, mongomock, pytest-cov

#### 1.5 Configure MongoDB Connection
```powershell
# Copy template
Copy-Item .env.example .env

# Edit .env (use PowerShell ISE or your editor)
code .env

# For local MongoDB:
# MONGO_URI=mongodb://localhost:27017
# DB_NAME=smart_expense_tracker

# For MongoDB Atlas:
# MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
# DB_NAME=smart_expense_tracker
```

#### 1.6 Start MongoDB (if local)
```powershell
# In a new terminal, if MongoDB Community is installed:
mongod

# Or use MongoDB Shell to connect:
mongosh
```

#### 1.7 Run Backend Tests
```powershell
# Run all tests
pytest -v

# Run specific test file
pytest tests/test_schema_validation.py -v

# Run with coverage report
pytest --cov=services --cov=schemas
```

**Expected**: 33+ tests passing

#### 1.8 Start Backend Server
```powershell
# Terminal should still be in backend/ with (venv) active
python app.py

# Expected output:
# Running on http://127.0.0.1:5000
# Press CTRL+C to quit
```

**Keep this terminal running!**

---

### Phase 2: Frontend Setup (20 minutes)

#### 2.1 Open New Terminal for Frontend
```powershell
# DO NOT close the backend terminal!
# Open a NEW terminal/tab

cd "e:\WebDev\Projects\Smart Expense Tracker\frontend"
```

#### 2.2 Install Dependencies
```powershell
npm install

# This will:
# - Download ~25MB to node_modules
# - Install React, Vite, Tailwind CSS
# - Takes 3-5 minutes

# Check if it completed successfully:
ls node_modules | measure
# Should show many folders
```

#### 2.3 Verify Tailwind CSS Installation
```powershell
npm list tailwindcss @tailwindcss/vite

# Expected: Both packages listed with versions
```

#### 2.4 Configure API Endpoint (Optional)
```powershell
# Copy template (if .env doesn't exist yet)
if (!(Test-Path .env)) {
    Copy-Item .env.example .env
}

# Edit if backend is on different port
# By default, Vite proxy routes /api to localhost:5000
```

#### 2.5 Start Development Server
```powershell
npm run dev

# Expected output:
# VITE v5.x.x ready in XXX ms
# ➜  Local:   http://localhost:5173/
# ➜  press h + enter to show help
```

**Keep this terminal running!**

---

### Phase 3: Test the Application (10 minutes)

#### 3.1 Open Browser
```
http://localhost:5173
```

You should see:
- ✅ Dark theme UI
- ✅ Add Expense Form
- ✅ Expense List (empty initially)
- ✅ Category Summary
- ✅ AI Insights Panel

#### 3.2 Test Adding an Expense
1. Fill in form:
   - Amount: `25.50`
   - Category: `Food`
   - Date: (auto-fills today)
   - Note: `Lunch`
2. Click "Add Expense"
3. Expected: Expense appears in list

#### 3.3 Test Category Summary
1. Add multiple expenses different categories
2. View Category Summary section
3. Expected: Totals and counts display

#### 3.4 Test AI Insights
1. Add several expenses
2. View Insights Panel
3. Expected: Insights like "You're spending too much on Food"

#### 3.5 Test Delete
1. Hover over expense item
2. Click Delete button
3. Expected: Expense removed

---

## 🧪 Verification Checklist

### Backend Health Checks

```powershell
# Terminal 1 (Backend should still be running)

# Check health endpoint
curl http://localhost:5000/api/health

# Expected response: {"status": "ok"}

# Add test expense via curl
curl -X POST http://localhost:5000/api/expenses/ `
  -H "Content-Type: application/json" `
  -d '{
    "amount": 50,
    "category": "Transport",
    "date": "2024-04-15"
  }'

# List expenses
curl http://localhost:5000/api/expenses/

# Get summary
curl http://localhost:5000/api/expenses/summary

# Get insights
curl http://localhost:5000/api/expenses/insights
```

### Frontend Health Checks

```powershell
# Terminal 2 (Frontend dev server)

# Check that it's running with no errors
# Look for "ready in XXX ms" message

# In browser DevTools (F12):
# 1. Network tab: Check all requests are 200/201
# 2. Console: Should have no errors (warnings OK)
# 3. Application tab: Check localStorage/cookies
```

---

## 📁 Project Structure Review

```
Smart Expense Tracker/
├── backend/
│   ├── app.py                      ← Main app entry
│   ├── requirements.txt             ← Python dependencies
│   ├── .env                         ← MongoDB config (create from .env.example)
│   ├── .env.example                ← Template
│   ├── conftest.py                 ← pytest configuration
│   ├── models/db.py                ← MongoDB setup
│   ├── routes/expense_routes.py    ← HTTP endpoints
│   ├── services/
│   │   ├── expense_service.py      ← Business logic
│   │   └── ai_service.py           ← AI insights
│   ├── schemas/expense_schema.py   ← Validation
│   ├── utils/
│   │   ├── error_handlers.py
│   │   └── logger.py
│   └── tests/                      ← Test suite (74 tests)
│
├── frontend/
│   ├── package.json                ← npm dependencies
│   ├── vite.config.js              ← Vite + Tailwind config
│   ├── .env.example                ← Template
│   ├── index.html                  ← HTML entry point
│   └── src/
│       ├── main.jsx                ← React entry
│       ├── App.jsx                 ← Root component
│       ├── index.css               ← Global styles + Tailwind
│       ├── api/expensesApi.js      ← HTTP client
│       ├── hooks/
│       │   ├── useExpenses.js
│       │   └── useInsights.js
│       ├── components/
│       │   ├── AddExpenseForm.jsx
│       │   ├── ExpenseList.jsx
│       │   ├── CategorySummary.jsx
│       │   ├── InsightsPanel.jsx
│       │   └── ExpenseItem.jsx
│       └── pages/
│           └── DashboardPage.jsx
│
├── README.md                       ← Main documentation
├── BACKEND_SUMMARY.md              ← Backend details
└── FRONTEND_SUMMARY.md             ← Frontend details
```

---

## 🐛 Troubleshooting

### Backend Issues

#### Error: `ModuleNotFoundError: No module named 'flask'`
```powershell
# Solution: Missing dependencies
pip install -r requirements.txt
```

#### Error: `Address already in use :::5000`
```powershell
# Solution: Port 5000 is occupied
# Option 1: Kill process on port 5000
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Option 2: Change port in .env
FLASK_PORT=5001
```

#### Error: `connect ECONNREFUSED 127.0.0.1:27017`
```powershell
# Solution: MongoDB not running
# Local: Start MongoDB
mongod

# Cloud: Check MONGO_URI in .env has correct credentials
```

#### Error: `Special options not supported` (mongomock)
```powershell
# Information: This appears during tests with mongomock
# This is expected - mongomock doesn't support all MongoDB options
# Tests still pass, this is just a warning
```

### Frontend Issues

#### Error: `npm ERR! code ERESOLVE`
```powershell
# Solution: npm dependency conflict
npm install --legacy-peer-deps
```

#### Error: CORS error in console
```powershell
# Solution: Backend not running or wrong URL
# Check: 
# 1. Backend running on :5000
# 2. Frontend vite.config.js proxy correct
# 3. Flask-CORS installed
```

#### Error: Tailwind classes not applying
```powershell
# Solution 1: Reinstall dependencies
rm -r node_modules
npm install

# Solution 2: Rebuild Vite
npm run dev

# Solution 3: Check index.css has @import "tailwindcss"
code src/index.css
```

#### Error: Module not found error
```powershell
# Solution: Clear cache and reinstall
rm -r node_modules .vite
npm install
```

---

## 📊 What to Expect

### Terminal 1 (Backend)
```
╭───────────────────────────────╮
│ WARNING: This is a development │
│ server. Do not use it in a     │
│ production deployment. Use a   │
│ production WSGI server instead│
╰───────────────────────────────╯
 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit
 * Restarting with stat reloader
```

### Terminal 2 (Frontend)
```
  VITE v5.x.x dev server running at:

  ➜  Local:   http://localhost:5173/
  ➜  press h + enter to show help

  ➜  Local: http://localhost:5173/
```

### Browser (http://localhost:5173)
- Dark theme expense tracker interface
- Form to add expenses
- List of expenses (initially empty)
- Category summary chart
- AI insights panel

---

## 🚀 Next Steps

### Development
1. Keep both terminals running
2. Edit code and see changes auto-refresh
3. Run tests with `pytest` in backend terminal

### Testing
1. Add multiple expenses
2. Test each category
3. Verify summary calculations
4. Check AI insights trigger correctly

### Production Deployment
1. Build frontend: `npm run build`
2. Deploy backend to server (Heroku, AWS, etc.)
3. Deploy frontend dist/ to CDN or static server
4. Update MongoDB to Atlas (if not already)
5. Set environment variables on server
6. Add domain to CORS origins

---

## 📞 Support

### Common Questions

**Q: Can I commit .env to git?**
A: No! Add to .gitignore. Use .env.example only.

**Q: Can I run both on different machines?**
A: Yes! Update frontend API_URL to backend server address.

**Q: Do I need MongoDB installed locally?**
A: No! Use MongoDB Atlas (cloud). Just update MONGO_URI.

**Q: What's the default admin user?**
A: There isn't one in this version. Add authentication layer if needed.

**Q: Can I customize categories?**
A: Yes! Edit VALID_CATEGORIES in schemas/expense_schema.py and rebuild.

---

## ✅ Success Criteria

You'll know everything is working when:

1. ✅ Backend terminal shows `Running on http://127.0.0.1:5000`
2. ✅ Frontend terminal shows `Local: http://localhost:5173/`
3. ✅ Browser loads dark theme UI without errors
4. ✅ Can add expense and see it in list
5. ✅ Category summary updates
6. ✅ AI insights appear after adding expenses
7. ✅ Console has no errors (F12)
8. ✅ Can delete expenses

---

**🎉 Congratulations! Smart Expense Tracker is ready!**

For more details, see:
- [README.md](README.md) - Full documentation
- [BACKEND_SUMMARY.md](BACKEND_SUMMARY.md) - Backend implementation details
- [FRONTEND_SUMMARY.md](FRONTEND_SUMMARY.md) - Frontend implementation details

