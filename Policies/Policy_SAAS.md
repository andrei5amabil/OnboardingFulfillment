# POL-SAAS: SaaS Licensing & Software Entitlement Standard

## 1. Purpose & Scope
This policy regulates the automated assignment, verification, and reclamation of software subscriptions, licenses, and seat entitlements.

## 2. Entitlement Evaluation
- **[POL-SAAS-201] Relational Baseline:** User licenses must strictly adhere to the mapped entitlements in `product_assignment_rules`. The AI orchestrator is strictly prohibited from granting unmapped licenses without human approval.
- **[POL-SAAS-202] Pre-Allocation Stock Check:** The deterministic execution engine must verify `total_seats` availability in the software catalog prior to invoking assignment tools.
- **[POL-SAAS-203] Seat Exhaustion Guardrail:** If an assigned product has zero available seats remaining, the orchestrator must flag a deficit error, suspend license execution, and alert the IT administrator.

## 3. Approval Gates & Exceptions
- **[POL-SAAS-301] Gated Products:** Software flagged with `requires_approval: true` must be routed directly to the Human-in-the-Loop (HITL) gateway. The deterministic runner must not execute assignment until approval is submitted.
- **[POL-SAAS-302] Out-of-Band Entitlements:** Any software requested outside the standard role-based matrix triggers an access exception that requires documented business justification and IT administrator sign-off.

## 4. License Revocation
- **[POL-SAAS-401] Rapid Reclamation:** Upon employee offboarding, the system must execute license revocation tools to release all provisioned seats back to the shared pool.
- **[POL-SAAS-402] Orphaned Seat Audit:** The workflow must verify that the employee holds zero active software assignments before generating the final compliance report.