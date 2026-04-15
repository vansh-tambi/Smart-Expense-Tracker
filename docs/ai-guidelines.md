# AI Usage Guidelines

## Purpose
This document defines how AI tools may be used in the Smart Expense Tracker project. The goal is to improve developer productivity while preserving code quality, security, correctness, and maintainability.

## Scope
These guidelines apply to all contributors who use AI-assisted tools for:
- Code generation
- Refactoring suggestions
- Documentation drafting
- Testing assistance
- Analysis and troubleshooting support

## Rules for AI Usage
1. AI-generated code must be reviewed before use.
2. No direct execution of AI outputs without validation.
3. All inputs to AI must be sanitized.
4. AI should only assist, not control business logic.
5. Avoid over-reliance on AI for core system design.

## Review and Validation Requirements
Before accepting any AI-generated output:
- Perform human code review for correctness, readability, and maintainability.
- Validate behavior through local testing (unit, integration, or manual checks as applicable).
- Confirm compliance with project standards, security requirements, and architecture decisions.
- Verify dependencies and API usage introduced by AI suggestions.
- Reject or revise outputs that are unclear, unsafe, or inconsistent with project goals.

## Input Sanitization Requirements
When providing prompts or data to AI tools:
- Do not include secrets (API keys, passwords, tokens, private credentials).
- Remove or anonymize personally identifiable information (PII).
- Avoid sharing production-only configuration or sensitive infrastructure details.
- Minimize context to only what is needed for the task.

## Role Boundaries
AI must be treated as a support tool, not an authority:
- AI can suggest code patterns, implementation options, and refactors.
- AI cannot make final architectural decisions.
- Final business logic decisions and trade-offs must remain with the engineering team.

## Example Prompts
Use prompts that are specific, bounded, and reviewable.

### Backend examples
- "Generate a Flask route handler for creating an expense with schema validation and clear error responses."
- "Suggest unit tests for expense summary calculations, including edge cases for zero and negative values."
- "Refactor this service function for readability without changing behavior."

### Frontend examples
- "Create a React component for rendering an expense list with loading and error states."
- "Suggest improvements to form validation for amount, category, and date fields."
- "Write a custom hook pattern for fetching and refreshing insights data."

## Limitations of AI Outputs
AI-generated outputs have known limitations:
- May produce syntactically valid but logically incorrect code.
- May omit edge cases, constraints, or project-specific assumptions.
- May provide outdated patterns or incompatible library usage.
- May generate inconsistent naming, architecture drift, or unnecessary complexity.
- May produce confident but unverifiable explanations.

## Risks and Mitigations

### Risk: Incorrect insights
AI may infer wrong conclusions from incomplete or ambiguous context.
- Mitigation: Cross-check with source code, tests, and domain requirements.

### Risk: Hallucinations
AI may invent APIs, functions, libraries, or behaviors that do not exist.
- Mitigation: Verify all references against official docs and project codebase.

### Risk: Unsafe execution
Executing unreviewed AI output can introduce bugs, security flaws, or data loss.
- Mitigation: Require review, testing, and staged validation before merge.

## Governance
- These guidelines should be reviewed periodically as tooling and project needs evolve.
- Pull requests that include AI-assisted changes should document review and validation performed.

## Quick Checklist
Before merging AI-assisted changes, confirm:
- [ ] Output reviewed by a human contributor
- [ ] Logic validated through testing
- [ ] Inputs and context were sanitized
- [ ] No AI-generated decision bypassed business logic ownership
- [ ] Proposed design aligns with project architecture
