Title: Corporate Network & Virtual Private Network (VPN) Access Policy
1. Purpose and Scope
1.1. This policy defines the rules for provisioning, managing, and terminating access to the corporate internal network and secure departmental enclaves.
1.2. It applies to all employee identity payloads processed by the automated onboarding engine.  
2. Network Segmentation & Departmental Access
2.1. Default Access (Tier 1): All standard employees receive default access to public-facing corporate SaaS applications (e.g., Microsoft 365, Jira). This tier does not require a VPN connection.
2.2. Secure Enclave Access (Tier 2): Departments handling sensitive, proprietary, or regulated data are isolated in secure network enclaves.
2.3. Mandatory Finance & HR VPN: Any employee onboarded into the "Finance" or "Human Resources" departments must be automatically provisioned with a secure Client-to-Site VPN profile mapped to their respective enclave. Omission of this profile constitutes a Day-1 blocker and a security policy violation.
2.4. Developer Environments: Employees with "Engineering" or "Developer" roles must be provisioned with VPN access to staging and production Kubernetes clusters, strictly governed by the entitlements in the role_entitlement_rules database.  
3. Remote Work & Provisioning Requirements
3.1. Location-Based Routing: Employees designated with a work_location of "remote" must be issued a split-tunnel VPN profile to ensure optimal routing for cloud-based SaaS tools.
3.2. Authentication Enforcement: All VPN authentications must be secured via the Multi-Factor Authentication (MFA) protocols established in POL-IAM-001. VPN profiles cannot be activated using a Temporary Access Pass (TAP).
3.3. Device Trust: VPN connections are exclusively permitted from company-owned hardware provisioned and recorded in the IT Asset Records. 
4. Exception Handling
4.1. Cross-Departmental Access: If an employee requires VPN access to an enclave outside their designated department (e.g., a Data Analyst requiring access to the Engineering database), the Orchestration Agent must flag the request_id.
4.2. HITL Escalation: Cross-departmental network requests must be routed to the Human-in-the-Loop (HITL) gateway. The IT Admin must explicitly approve the network bridging in the dashboard before the deterministic tool engine can execute provision_account().  
5. Offboarding & Session Termination
5.1. Immediate VPN Revocation: Upon the execution of an offboarding request, the automated execution engine must immediately invalidate all active VPN sessions and cryptographic tokens associated with the departing employee.
5.2. Network Audit: The system must verify Zero Residual Access to all secure enclaves before generating the final Compliance Report.  
