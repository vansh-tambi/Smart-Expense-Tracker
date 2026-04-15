# 10-Minute Walkthrough Script

## 1) Problem Statement (1 minute)
Hello everyone. This project is a Smart Expense Tracker built to solve a common problem: people track expenses, but they often miss patterns in their spending.

Our goal is simple:
- Let users quickly add and manage expenses.
- Show category-level spending summaries.
- Provide practical AI-assisted insights so users can make better spending decisions.

## 2) Demo Flow (2 minutes)
Here is the demo flow I will show:
- Start on the dashboard.
- Add a few expenses across categories like Food, Transport, and Shopping.
- Show how the expense list updates immediately.
- Delete one expense to demonstrate clean state updates.
- Open the category summary to highlight totals and percentages.
- Refresh AI insights and show guidance generated from current data.

What this demonstrates is a full loop: input, storage, aggregation, and insight generation.

## 3) Backend Architecture (1.5 minutes)
The backend uses Flask with a layered architecture:
- routes: Handles HTTP request and response only.
- services: Contains business logic like CRUD, summary calculations, and insight generation.
- schemas: Uses Pydantic for strict input validation.
- models: Manages MongoDB connection and schema validator setup.
- utils: Handles centralized logging and error formatting.

This separation keeps the system easier to test, easier to maintain, and safer to extend.

## 4) Frontend Structure (1.5 minutes)
The frontend uses React with Vite and reusable component design:
- pages: Main dashboard screen.
- components: Expense form, list, summary card, and insights panel.
- hooks: Custom hooks for expense state and insight fetching.
- api: Axios-based API client for backend communication.

This structure keeps UI logic modular and avoids coupling data fetching directly into visual components.

## 5) AI Usage and Constraints (1 minute)
AI in this project is assistive, not authoritative.

How it is used:
- To generate spending insights from stored expense data.
- To support developer productivity during implementation.

Constraints:
- AI-generated code is reviewed before use.
- No direct execution of AI output without validation.
- Inputs are sanitized before being provided to AI tooling.
- AI does not own business-critical decision logic.

## 6) Key Technical Decisions (1 minute)
Key decisions include:
- Flask + service-layer pattern for clear backend boundaries.
- MongoDB for flexible document-based expense records.
- Pydantic + database validation for defense in depth.
- React hooks for lightweight state management.
- Axios client with centralized error handling.

Each decision focused on clarity, reliability, and fast iteration.

## 7) Tradeoffs (1 minute)
Important tradeoffs:
- MongoDB flexibility vs strict relational constraints.
- Faster delivery with simple architecture vs advanced enterprise patterns.
- Rule-based insights are predictable, but less adaptive than full ML models.
- Minimal frontend state tooling keeps complexity low, but may require scaling later.

These tradeoffs were intentional for a focused, maintainable MVP.

## 8) Future Improvements (1 minute)
Next improvements would be:
- Authentication and user-specific data isolation.
- Budget goals with alerts and monthly trend analysis.
- More advanced AI insights with explainability and confidence scoring.
- Better observability: metrics, tracing, and structured audit logs.
- Deployment hardening with CI/CD and environment-specific configs.

That is the complete walkthrough of the Smart Expense Tracker: clear architecture, practical features, and responsible AI usage.
