# POL-NET: Corporate Network & Virtual Private Network (VPN) Standard

## 1. Purpose & Scope
This policy governs automated provisioning, network isolation, and session revocation across corporate networks and departmental enclaves[cite: 9].

## 2. Network Segmentation & Enclave Access
- **[POL-NET-201] Default Tier-1 SaaS:** Standard cloud tools require no dedicated VPN connection[cite: 9].
- **[POL-NET-202] Restricted Enclave Entitlement:** VPN profiles granting access to isolated departmental enclaves or database infrastructure are provisioned strictly via database entitlement rules[cite: 9].
- **[POL-NET-203] Zero Day-1 Blockers:** Any mandatory VPN entitlement defined in the database must be provisioned prior to the start date to prevent operational blocking[cite: 9].

## 3. Work Location & Tunnel Configuration
- **[POL-NET-301] Split-Tunneling for Remote Work:** Requests with `work_location: remote` require a split-tunnel VPN profile to optimize cloud SaaS routing[cite: 9].
- **[POL-NET-302] Device Trust & Authentication:** VPN connections require verified MFA and are restricted to company-managed hardware recorded in the asset database[cite: 9]. VPN access cannot be established via a TAP token[cite: 9].

## 4. Cross-Enclave Exception Routing
- **[POL-NET-401] Cross-Departmental Routing Check:** Requests for network bridges outside standard departmental enclaves trigger an automated exception flag[cite: 9].
- **[POL-NET-402] HITL Network Approval:** Bridged enclave access must be reviewed and authorized by an IT Admin via the HITL gateway before profile generation[cite: 9].

## 5. Offboarding & Session Revocation
- **[POL-NET-501] Cryptographic Invalidation:** Offboarding triggers immediate invalidation of all active VPN sessions, certificates, and cryptographic tokens[cite: 9].
- **[POL-NET-502] Zero Residual Network Access:** Automated verification must confirm zero persistent network routes before offboarding can be finalized[cite: 9].