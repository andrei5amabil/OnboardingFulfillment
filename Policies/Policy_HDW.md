# POL-HDW: Enterprise IT Asset & Hardware Provisioning Standard

## 1. Purpose & Core Principles
This policy defines the governance and fulfillment lifecycle for physical IT equipment across onboarding and offboarding workflows.

## 2. Hardware Allocation Protocol
- **[POL-HDW-201] Deterministic Resolution:** All physical equipment allocations must be determined strictly by the database entitlement matrix. The orchestration engine must never infer or assign hardware models outside verified database records.
- **[POL-HDW-202] Inventory & Seat Verification:** Before provisioning an asset, the system must cross-reference available quantities in the IT Asset Records.
- **[POL-HDW-203] Stock Depletion Fallback:** If a required hardware asset has zero available stock, the automated workflow must immediately halt the hardware task, dispatch a critical notification to the SysAdmin, and mark the workflow execution as failed.

## 3. Work Location Logistics
- **[POL-HDW-301] Remote Delivery:** Requests with `work_location: remote` require automatic generation of an equipment dispatch ticket and courier delivery to the verified home address.
- **[POL-HDW-302] On-Site Dispatch:** Requests with `work_location: on-site` or `work_location: hybrid` must route hardware setup tasks to the local campus IT Helpdesk prior to the employee's start date.

## 4. Offboarding Reclamation
- **[POL-HDW-401] Hardware Recovery:** Initiating an offboarding workflow automatically generates return instructions and pre-paid shipping waybills for all assigned serial numbers.
- **[POL-HDW-402] Inventory Reconciliation:** Offboarding compliance cannot be signed off until returned assets are marked as sanitized and returned to inventory in the database.