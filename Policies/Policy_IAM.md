Title: Enterprise Identity & Access Management (IAM) Standard
1. Purpose and Scope
1.1. This policy dictates the mandatory lifecycle management (creation, maintenance, and revocation) of all human and non-human digital identities across the corporate network.
1.2. It applies to all full-time employees, contractors, and automated service accounts managed through the automated onboarding and offboarding orchestration system.  
2. Role-Based Access Control (RBAC) & Least Privilege
2.1. Principle of Least Privilege (PoLP): All user accounts are provisioned with the absolute minimum access required to perform their baseline job function.
2.2. Deterministic Entitlements: Software seats and licenses (e.g., Microsoft 365, JetBrains, PowerBI) must strictly adhere to the mapped entitlements found in the role_entitlement_rules database.
2.3. Out-of-Band Requests: Any request for software or access not predefined in the employee's role matrix requires explicit, documented Human-in-the-Loop (HITL) approval from both the Department Manager and the IT Systems Administrator. The LLM Orchestrator must flag these requests as requires_approval: true.  
3. Onboarding & Authentication Standards
3.1. Identity Creation: A unique Corporate Email and Enterprise ID (ENT-ID) must be provisioned for all verified onboarding payloads originating from HR. Shared accounts are strictly prohibited.
3.2. Temporary Access Pass (TAP): To eliminate the insecure transmission of plain-text passwords, the provisioning system must generate a time-bound, single-use Temporary Access Pass (TAP) token.
3.3. TAP Delivery: The TAP activation link must be sent to the employee's verified personal email and expires 24 hours after the employee's official start_date.
3.4. Multi-Factor Authentication (MFA): MFA enrollment is mandatory. The TAP login forces the user into the MFA registration flow upon their first successful authentication.  
4. Offboarding & Access Revocation
4.1. Immediate Deactivation: Upon the HR-approved termination_date, all corporate access, active sessions, and authentication tokens must be disabled simultaneously across all connected applications.
4.2. Zero Residual Access: The automated offboarding engine must verify that no orphaned accounts or active software licenses remain attached to the departed employee's ENT-ID.
4.3. Asset & Data Transfer: Before the destruction of the identity vault, ownership of active files, GitHub repositories, and open IT tasks must be transferred to the designated manager or a specified colleague (e.g., transfer_ownership_to).  
5. Audit and State Persistence
5.1. Transaction Logging: Every provisioning and de-provisioning action executed by the deterministic tool engine must be persistently recorded.
5.2. Compliance Reporting: A finalized state report must be generated and written to the audit_logs table upon the completion of any onboarding or offboarding workflow to satisfy ISO 27001 auditing requirements.  
