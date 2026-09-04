# POL-IAM: Enterprise Identity & Access Management Standard

## 1. Purpose & Scope
This standard establishes mandatory lifecycle rules for creating, maintaining, and revoking digital identities across all corporate infrastructure[cite: 8].

## 2. Identity Creation & Authentication
- **[POL-IAM-201] Enterprise Identifier Minting:** Every verified onboarding request must generate a unique Corporate Email and Enterprise ID (ENT-ID)[cite: 8]. Shared accounts are strictly prohibited[cite: 8].
- **[POL-IAM-202] Temporary Access Pass (TAP):** To eliminate plain-text password transmission, the system must generate a single-use, time-bound TAP activation token expiring 24 hours after the official start date[cite: 8].
- **[POL-IAM-203] Mandatory MFA Enrollment:** Initial authentication via TAP must enforce immediate Multi-Factor Authentication (MFA) registration before granting access to internal resources[cite: 8].

## 3. Access Governance & Principle of Least Privilege
- **[POL-IAM-301] Least Privilege Baseline:** User access is restricted to the minimum required baseline strictly resolved through the database entitlement matrix[cite: 8].
- **[POL-IAM-302] Out-of-Band Access Approval:** Unmapped identity entitlements require explicit approval from the Department Manager and IT Admin before assignment execution[cite: 8].

## 4. Identity Revocation & Offboarding
- **[POL-IAM-401] Immediate Deactivation:** All corporate access, active sessions, and authentication tokens must be simultaneously terminated upon the approved termination date[cite: 8].
- **[POL-IAM-402] Ownership Handover:** Ownership of repositories, files, and active workflow tasks must be transferred to the designated replacement (`transfer_ownership_to`) before identity deactivation[cite: 8].

## 5. State Persistence & Compliance
- **[POL-IAM-501] Audit State Recording:** Every provisioning and de-provisioning event executed by deterministic tools must be persistently recorded in `audit_logs`[cite: 8].