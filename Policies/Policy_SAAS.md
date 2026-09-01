Title: SaaS Licensing & Software Entitlement Policy
1. Purpose and Scope
This policy governs the automated allocation, tracking, and revocation of software licenses and SaaS entitlements.It ensures that seat-based products are distributed cost-effectively and strictly aligned with the role data provided in the verified HR onboarding JSON request.  
2. Role-Based Licensing MatrixDefault Entitlements: Essential software tools are distributed globally according to standard corporate profiles, such as allocating Microsoft 365 and Jira.  
Role-Specific Provisioning: Premium or specialized SaaS licenses are governed by the role_entitlement_rules database matrix.  
Deterministic Execution: A new hire designated as a "Data Analyst" must automatically be assigned licenses for PowerBI Pro and DataGrip. The LLM agent will extract this rule and queue the assign_license(emp_id, prod_id) tool to insert the assignment and deduct an available seat.  
Seat Availability Constraints: The tool execution engine must verify the total_seats available in the software_products table before allocation.  
3. Exceptions & HITL GatewayStock Deficits: If a required license has zero available seats, the system must pause execution, trigger a fallback alert to the SysAdmin, and log the transaction as failed.  
Approval-Gated Software: Any SaaS tool flagged as requires_approval in the database schema cannot be automatically provisioned.  
Manual Intervention: The orchestrator must route these specific requests to the Human-in-the-Loop (HITL) dashboard. The IT Admin must review the RAG policy citations and manually click "Approve" before the license is allocated.  
4. Offboarding & License ReclamationImmediate Revocation: Upon a triggered offboarding request, the automated execution engine must immediately utilize the revoke_license(emp_id, prod_id) tool.  
Seat Reclaiming: The system must free up the associated licenses by reclaiming them from the database and restoring the available seat count.  
Orphaned Account Prevention: The final compliance report cannot be generated until the inventory reflects zero active software assignments tied to the departing employee.  
