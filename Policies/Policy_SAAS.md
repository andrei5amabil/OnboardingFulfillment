# POL-SAAS-001: SaaS Licensing & Software Entitlement Policy

## Section 1: Purpose and Scope
1.1. This policy governs the automated allocation, tracking, and revocation of software licenses and SaaS entitlements.
1.2. It ensures seat-based products are distributed cost-effectively and strictly aligned with HR onboarding data.

## Section 2: Role-Based Licensing Matrix
2.1. Default Entitlements: Standard productivity tools (e.g., Microsoft 365, Jira) are provisioned globally across corporate profiles.
2.2. Role-Specific Provisioning: Specialized licenses are governed by the product_assignment_rules database table.
2.3. Seat Constraints: Available seats in software_products must be verified before proposing or executing license allocation.

## Section 3: Exceptions & HITL Gateway
3.1. Stock Deficits: If a required license has zero available seats, the system must halt auto-provisioning, flag a fallback alert, and route to the IT Admin.
3.2. Approval-Gated Software: Any SaaS tool with requires_approval=true in the database cannot be automatically provisioned and requires HITL sign-off.
3.3. Manual Intervention: The orchestrator must route approval-gated software to the HITL dashboard with relevant RAG policy citations.

## Section 4: Offboarding & License Reclamation
4.1. Immediate Revocation: Upon an offboarding trigger, the deterministic engine executes revoke_license(emp_id, prod_id).
4.2. Seat Reclamation: Reclaimed licenses are restored to the available seat count in software_products.
4.3. Orphaned Prevention: Final compliance clearance requires zero active software assignments tied to the departing employee.
