# POL-EXC: Access Exception & Privilege Escalation Policy

## 1. Purpose & Scope
This policy governs protocols for user access requests that deviate from predefined departmental and role baselines, preventing unvetted permissions and uncoordinated delays[cite: 6].

## 2. Baseline Deviations & Diff Detection
- **[POL-EXC-201] Relational Mismatch Flagging:** Any entitlement request not explicitly mapped in `product_assignment_rules` or IT asset tables triggers an automated exception[cite: 6].
- **[POL-EXC-202] Execution Isolation:** The orchestration agent must never auto-execute unmapped entitlements[cite: 6]. Out-of-band requests must be isolated into an exception block within the generated plan[cite: 6].

## 3. Privileged Access Management (PAM)
- **[POL-EXC-301] High-Risk Classification:** Requests for administrative rights, root-level database access, or global SaaS admin consoles are classified as Privilege Escalations[cite: 6].
- **[POL-EXC-302] Mandatory Business Justification:** Payloads requesting privileged access must include a non-empty business justification string[cite: 6]. Omitting this justification causes immediate automated rejection[cite: 6].

## 4. Human-in-the-Loop (HITL) Gateway
- **[POL-EXC-401] Mandatory IT Review:** All flagged exceptions and privilege escalations must route to the HITL dashboard for diff inspection and policy citation review[cite: 6].
- **[POL-EXC-402] Explicit Admin Authorization:** Deterministic execution remains locked until an IT Admin explicitly approves or rejects the exception in the dashboard[cite: 6].

## 5. Audit & Compliance
- **[POL-EXC-501] Escalation Logging:** Approved exceptions must permanently record the admin identity, timestamp, and submitted business justification to the compliance audit log[cite: 6].