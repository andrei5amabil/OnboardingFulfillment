Title: Access Exception & Privilege Escalation Policy
1. Purpose and Scope
This policy governs the protocol for any user access request that deviates from the predefined departmental and role-based baseline.It ensures that non-standard requests are securely triaged, explicitly justified, and manually approved without causing the 24-48 hour operational delays seen in traditional asynchronous ticket management.  
2. Baseline Deviations (Diffs)
Role Mismatch: An exception is automatically triggered if an incoming HR payload requests a license, hardware asset, or network enclave that is not explicitly mapped to the user's role in the product_assignment_rules table.  
Agent Triage: The LLM orchestration agent must not automatically execute provisioning for out-of-band requests. Instead, it must isolate these requests into an exception block within the generated JSON plan.  
3. Privileged Access Management (PAM)High-Risk Systems: Requests for administrative rights, root-level database access, or global SaaS admin consoles (e.g., 365 Admin Center) are classified as Privilege Escalations. 
 Mandatory Justification: Any HR payload containing a request for Privileged Access must include a notes string containing the business justification. If omitted, the request is automatically rejected by the orchestration engine.  
4. Human-in-the-Loop (HITL) Gateway
Diff Inspection: All flagged exceptions and privilege escalations must be routed to the Human-in-the-Loop (HITL) gateway dashboard.  IT Admin Authorization: The IT Admin must inspect the generated plan, review the RAG-cited policy clauses, and evaluate the specific differences (diffs) between the standard role entitlements and the requested exceptions. 
 Explicit Action: The execution engine remains locked until the IT Admin explicitly clicks the Approve or Reject action on the dashboard.  
5. Audit and Compliance
Escalation Logging: If an exception is approved via the HITL dashboard, the specific approval action, the admin's identity, and the business justification must be permanently written to the audit log to satisfy compliance audits.  
