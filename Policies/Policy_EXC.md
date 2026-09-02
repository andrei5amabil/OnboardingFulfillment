# POL-EXC-001: Access Exception & Privilege Escalation Policy

## Section 1: Purpose and Scope
1.1. This policy governs the protocol for any user access request that deviates from the predefined departmental and role-based baseline.
1.2. It ensures non-standard requests are securely triaged, justified, and manually approved without operational delay.

## Section 2: Baseline Deviations (Diffs)
2.1. Role Mismatch: An exception is triggered if an incoming HR payload requests a license, hardware asset, or network enclave not mapped in product_assignment_rules.
2.2. Agent Triage: The LLM agent must isolate out-of-band requests into a dedicated exception proposal block and require human approval.

## Section 3: Privileged Access Management (PAM)
3.1. High-Risk Systems: Requests for administrative rights, root-level database access, or global SaaS admin consoles are classified as Privilege Escalations.
3.2. Mandatory Justification: Any HR payload requesting Privileged Access must include a justification in the notes field. If missing, the request is marked as rejected.

## Section 4: Human-in-the-Loop (HITL) Gateway
4.1. Diff Inspection: All flagged exceptions and privilege escalations must route to the HITL gateway dashboard.
4.2. Admin Authorization: The IT Admin must review the RAG-cited policy clauses and diffs before approving.
4.3. Execution Lock: Deterministic tools remain locked until the IT Admin explicitly clicks Approve or Reject.

## Section 5: Audit and Compliance
5.1. Escalation Logging: Approved exceptions must permanently record the admin ID, timestamp, and justification in the audit log.
